"""GBC versus ABC on a d dimensional Gaussian location model (Part IV of gbc-lab.html).

Adapted from gbc_vs_abc.py (Polson, 41916 Bayes, AI and Deep Learning slides). Same model, seed,
budget and networks; instead of figures it writes gbc-abc-data.js with the results table and the
theta_1 draws of ABC and GBC for the first four test data sets at each d.

Model:  theta ~ N(0, I_d),  y_1..y_n | theta ~ N(theta, I_d),  summary s = ybar.
Exact posterior: theta_j | s ~ N(n s_j / (n+1), 1/(n+1)), independent over j.

Both methods use the SAME reference table of N simulated (theta, s) pairs.
ABC:  rejection, keep the k nearest simulations to s_obs (acceptance rate k/N).
GBC:  quantile neural network theta_j = H_j(s, tau), trained with the pinball
      (check) loss on all N pairs; posterior draws are H(s_obs, tau), tau ~ U(0,1).
Pure NumPy, no deep learning library needed.
"""
import numpy as np, time, json
from scipy.stats import norm

rng = np.random.default_rng(41916)
n_obs, N, k_abc, M_test = 20, 100_000, 1_000, 100
dims = [1, 2, 5, 10]


def simulate(N, d):
    theta = rng.standard_normal((N, d))
    s = theta + rng.standard_normal((N, d)) / np.sqrt(n_obs)   # ybar is sufficient
    return theta, s


# ---------------- quantile network in NumPy ----------------
K_EMB = 6  # cosine embedding of each tau


def features(s, tau):
    j = np.arange(1, K_EMB + 1)
    emb = np.cos(np.pi * tau[:, :, None] * j).reshape(len(s), -1)
    return np.hstack([s, emb])


class QNet:
    def __init__(self, p_in, p_out, h=128):
        self.W = [rng.standard_normal((p_in, h)) * np.sqrt(2 / p_in),
                  rng.standard_normal((h, h)) * np.sqrt(2 / h),
                  rng.standard_normal((h, p_out)) * np.sqrt(1 / h)]
        self.b = [np.zeros(h), np.zeros(h), np.zeros(p_out)]
        self.m = [np.zeros_like(w) for w in self.W + self.b]
        self.v = [np.zeros_like(w) for w in self.W + self.b]
        self.t = 0

    def forward(self, x):
        z1 = x @ self.W[0] + self.b[0]; a1 = np.maximum(z1, 0)
        z2 = a1 @ self.W[1] + self.b[1]; a2 = np.maximum(z2, 0)
        out = a2 @ self.W[2] + self.b[2]
        return out, (x, z1, a1, z2, a2)

    def step(self, x, theta, tau, lr):
        out, (x, z1, a1, z2, a2) = self.forward(x)
        u = theta - out
        g = -(tau - (u < 0)) / len(x)                    # d pinball / d out
        gW2 = a2.T @ g; gb2 = g.sum(0)
        d2 = (g @ self.W[2].T) * (z2 > 0)
        gW1 = a1.T @ d2; gb1 = d2.sum(0)
        d1 = (d2 @ self.W[1].T) * (z1 > 0)
        gW0 = x.T @ d1; gb0 = d1.sum(0)
        grads = [gW0, gW1, gW2, gb0, gb1, gb2]
        params = self.W + self.b
        self.t += 1
        for i, (p, gr) in enumerate(zip(params, grads)):   # Adam
            self.m[i] = 0.9 * self.m[i] + 0.1 * gr
            self.v[i] = 0.999 * self.v[i] + 0.001 * gr ** 2
            mh = self.m[i] / (1 - 0.9 ** self.t); vh = self.v[i] / (1 - 0.999 ** self.t)
            p -= lr * mh / (np.sqrt(vh) + 1e-8)
        return np.mean(np.maximum(tau * u, (tau - 1) * u))


def train_gbc(theta, s, steps=6000, batch=512):
    d = theta.shape[1]
    net = QNet(d + d * K_EMB, d)
    for it in range(steps):
        idx = rng.integers(0, len(s), batch)
        tau = rng.uniform(size=(batch, d))
        lr = 2e-3 * (0.5 ** (it / 2000))
        net.step(features(s[idx], tau), theta[idx], tau, lr)
    return net


def gbc_draws(net, s_obs, m=1000):
    d = len(s_obs)
    tau = rng.uniform(size=(m, d))
    out, _ = net.forward(features(np.tile(s_obs, (m, 1)), tau))
    return out


def w1_to_normal(x, mu, sd):
    """Wasserstein 1 distance between sample x and N(mu, sd^2)."""
    x = np.sort(x); q = (np.arange(len(x)) + 0.5) / len(x)
    return np.mean(np.abs(x - (mu + sd * norm.ppf(q))))


results, ex = {}, {}
post_sd = 1 / np.sqrt(n_obs + 1)
for d in dims:
    theta, s = simulate(N, d)
    t0 = time.time(); net = train_gbc(theta, s); t_train = time.time() - t0
    th_test, s_test = simulate(M_test, d)
    rec = {m: dict(w1=[], sdr=[], cov=[]) for m in ("ABC", "GBC")}
    t_abc = t_gbc = 0.0
    for i in range(M_test):
        so = s_test[i]; mu = n_obs * so / (n_obs + 1)
        t0 = time.time()
        dist = np.linalg.norm(s - so, axis=1)
        abc = theta[np.argpartition(dist, k_abc)[:k_abc]]
        t_abc += time.time() - t0
        t0 = time.time(); gbc = gbc_draws(net, so); t_gbc += time.time() - t0
        for name, draws in (("ABC", abc), ("GBC", gbc)):
            lo, hi = np.quantile(draws, [0.05, 0.95], axis=0)
            rec[name]["w1"].append(np.mean([w1_to_normal(draws[:, j], mu[j], post_sd) for j in range(d)]) / post_sd)
            rec[name]["sdr"].append(np.mean(draws.std(0)) / post_sd)
            rec[name]["cov"].append(np.mean((th_test[i] >= lo) & (th_test[i] <= hi)))
        if i < 4:
            ex.setdefault(d, []).append(dict(abc=np.round(abc[:, 0], 3).tolist(), gbc=np.round(gbc[:, 0], 3).tolist(), mu=round(float(mu[0]), 4), theta=round(float(th_test[i, 0]), 4), eps=round(float(np.sort(dist)[k_abc - 1]), 4)))
    results[d] = {m: {k2: float(np.mean(v)) for k2, v in rec[m].items()} for m in rec}
    results[d]["train_sec"] = t_train
    results[d]["abc_sec_per_dataset"] = t_abc / M_test
    results[d]["gbc_sec_per_dataset"] = t_gbc / M_test
    print(d, json.dumps(results[d]))

out = dict(n=n_obs, N=N, k=k_abc, M=M_test, post_sd=post_sd, results={str(d): results[d] for d in dims}, examples={str(d): ex[d] for d in dims})
with open("gbc-abc-data.js", "w") as f:
    f.write("// Generated by gbc-abc-lab.py; do not edit by hand.\nwindow.GBC_ABC = " + json.dumps(out, separators=(",", ":")) + ";\n")
