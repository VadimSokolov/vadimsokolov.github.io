"""Who can pick stocks? Offline run for Part V of gbc-lab.html.

After Polson's slides "Who Can Actually Pick Stocks?" (Booth 41916, Bayes, AI and Deep Learning), which
follow Fisher and Jensen (2022). The slides came without code, so this is an independent reproduction.

Model: alphahat_i | alpha_i ~ N(alpha_i, s_i^2), alpha_i | G ~ G, G ~ DP(theta, G0), with
G0 = N(0, 3^2), theta ~ Gamma(2, 1), s_i ~ U(1, 2) known, n = 1000 funds per panel.
Target: Y = pi(c), the fraction of the panel's funds whose true alpha exceeds c, at nine thresholds.

1. Exact route: a collapsed (conjugate) Gibbs sampler for the hierarchy, with the Escobar-West update
   for theta. Run on one panel built like the slides' example (24% at -3, 75.4% at 0, 0.6% at +3).
2. Generative map: Y = F(X, Z), X = 34 summaries of the panel, Z ~ N(0, I_6). F is a ReLU network whose
   10 softmax outputs are the masses between thresholds, so the curve is monotone and in [0, 1].
   Trained by the energy score on panels simulated from the prior. Nothing evaluates a likelihood.
3. Calibration: coverage of the map's 90% bands over 200 fresh panels from the prior.

Writes gbc-funds-data.js (results and the trained network, which the page evaluates live).
Usage: python gbc-funds-lab.py [--sims 200000] [--steps 30000] [--out gbc-funds-data.js]
"""
import argparse
import json
import math
import time

import numpy as np
import torch
import torch.nn as nn
from numba import njit

N_FUNDS, TAU0, TRUNC = 1000, 3.0, 100
CS = np.array([-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3], dtype=float)
LEV = np.array([.01, .025, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .975, .99])
NZ, H = 6, 128


def prior_panels(rng, B, n=N_FUNDS):
    """B panels from the prior: returns alphahat (B, n), s (B, n), alpha (B, n)."""
    theta = rng.gamma(2.0, 1.0, size=B)
    V = rng.beta(1.0, theta[:, None], size=(B, TRUNC))
    V[:, -1] = 1.0
    w = V * np.concatenate([np.ones((B, 1)), np.cumprod(1 - V[:, :-1], axis=1)], axis=1)
    mu = TAU0 * rng.standard_normal((B, TRUNC))
    cw = np.cumsum(w, axis=1)
    u = rng.uniform(size=(B, n)) * cw[:, -1:]
    k = np.empty((B, n), dtype=np.int64)
    for b in range(B):
        k[b] = np.minimum(np.searchsorted(cw[b], u[b]), TRUNC - 1)
    alpha = np.take_along_axis(mu, k, axis=1)
    s = rng.uniform(1.0, 2.0, size=(B, n))
    return alpha + s * rng.standard_normal((B, n)), s, alpha


def summaries(ah, s):
    """34 summaries: 15 quantiles of t = alphahat / s, 15 of alphahat, mean, sd, P(t > 2), P(t < -2)."""
    t = ah / s
    return np.hstack([np.quantile(t, LEV, axis=1).T, np.quantile(ah, LEV, axis=1).T, ah.mean(1, keepdims=True),
                      ah.std(1, ddof=1, keepdims=True), (t > 2).mean(1, keepdims=True), (t < -2).mean(1, keepdims=True)])


def tail(alpha):
    return (alpha[..., None] > CS).mean(-2)


class Map(nn.Module):
    def __init__(self, p):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(p + NZ, H), nn.ReLU(), nn.Linear(H, H), nn.ReLU(), nn.Linear(H, len(CS) + 1))

    def forward(self, x, z):
        p = torch.softmax(self.net(torch.cat([x, z], -1)), -1)        # masses of the 10 bins between thresholds
        return torch.flip(torch.cumsum(torch.flip(p, [-1]), -1), [-1])[..., 1:]   # pi(c_j) = mass above c_j


def energy(F, y):
    """F: (B, m, 9) draws, y: (B, 9). Energy score averaged over the batch, on the arcsine square root
    scale, which spreads out fractions near 0 and 1 so that the far tail counts in the loss."""
    F, y = torch.asin(torch.sqrt(F.clamp(1e-6, 1 - 1e-6))), torch.asin(torch.sqrt(y.clamp(1e-6, 1 - 1e-6)))
    t1 = (F - y[:, None]).norm(dim=-1).mean(1)
    m = F.shape[1]
    t2 = torch.cdist(F, F).sum((1, 2)) / (m * (m - 1))
    return (t1 - 0.5 * t2).mean()


@njit(cache=True)
def gibbs(ah, s, sweeps, burn, seed, cs, tau2):
    np.random.seed(seed)
    n = len(ah)
    z = np.zeros(n, np.int64)
    cnt = np.zeros(n + 1, np.int64); sp = np.zeros(n + 1); sw = np.zeros(n + 1)
    K = 1
    for i in range(n):
        cnt[0] += 1; sp[0] += 1 / s[i] ** 2; sw[0] += ah[i] / s[i] ** 2
    theta = 1.0
    nkeep = sweeps - burn
    Y = np.zeros((nkeep, len(cs))); Ks = np.zeros(nkeep, np.int64); th = np.zeros(nkeep)
    grid = np.linspace(-6, 6, 121); Gm = np.zeros(120)
    g0 = np.zeros(120)
    for b in range(120):
        lo, hi = grid[b] / math.sqrt(tau2), grid[b + 1] / math.sqrt(tau2)
        g0[b] = 0.5 * (math.erf(hi / math.sqrt(2)) - math.erf(lo / math.sqrt(2)))
    pr = np.zeros(n + 1)
    for it in range(sweeps):
        for i in range(n):
            k = z[i]; pi_, wi = 1 / s[i] ** 2, ah[i] / s[i] ** 2
            cnt[k] -= 1; sp[k] -= pi_; sw[k] -= wi
            if cnt[k] == 0:
                K -= 1
                if k != K:
                    cnt[k] = cnt[K]; sp[k] = sp[K]; sw[k] = sw[K]
                    for j in range(n):
                        if z[j] == K:
                            z[j] = k
                cnt[K] = 0; sp[K] = 0.0; sw[K] = 0.0
            tot = 0.0
            for c in range(K):
                P = 1 / tau2 + sp[c]; m = sw[c] / P; v = 1 / P + s[i] ** 2
                pr[c] = cnt[c] * math.exp(-0.5 * (ah[i] - m) ** 2 / v) / math.sqrt(v); tot += pr[c]
            v = tau2 + s[i] ** 2
            pr[K] = theta * math.exp(-0.5 * ah[i] ** 2 / v) / math.sqrt(v); tot += pr[K]
            u = np.random.random() * tot; c = 0
            while c < K and u > pr[c]:
                u -= pr[c]; c += 1
            if c == K:
                K += 1
            z[i] = c; cnt[c] += 1; sp[c] += pi_; sw[c] += wi
        # Escobar and West (1995) update of theta under a Gamma(2, 1) prior
        eta = np.random.beta(theta + 1, n)
        a, bb = 2.0, 1.0 - math.log(eta)
        odds = (a + K - 1) / (n * bb)
        theta = np.random.gamma(a + K if np.random.random() < odds / (1 + odds) else a + K - 1, 1 / bb)
        if it >= burn:
            r = it - burn
            mus = np.zeros(K); g = np.zeros(K + 1)
            for c in range(K):
                P = 1 / tau2 + sp[c]
                mus[c] = sw[c] / P + np.random.standard_normal() / math.sqrt(P)
                g[c] = np.random.gamma(cnt[c], 1.0)
            g[K] = np.random.gamma(theta, 1.0)
            gs = g.sum()
            for j in range(len(cs)):
                acc = 0
                for c in range(K):
                    if mus[c] > cs[j]:
                        acc += cnt[c]
                Y[r, j] = acc / n
            for c in range(K):
                bi = int((mus[c] + 6) / 0.1)
                if 0 <= bi < 120:
                    Gm[bi] += g[c] / gs
            for bi in range(120):
                Gm[bi] += g[K] / gs * g0[bi]
            Ks[r] = K; th[r] = theta
    return Y, Ks, th, Gm / nkeep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sims", type=int, default=200_000)
    ap.add_argument("--steps", type=int, default=30_000)
    ap.add_argument("--sweeps", type=int, default=3000)
    ap.add_argument("--out", default="gbc-funds-data.js")
    a = ap.parse_args()
    rng = np.random.default_rng(41916)
    torch.manual_seed(41916)

    # The example panel: 240 funds at -3, 754 at 0, 6 at +3 per cent a year
    alpha0 = np.repeat([-3.0, 0.0, 3.0], [240, 754, 6]); rng.shuffle(alpha0)
    s0 = rng.uniform(1, 2, N_FUNDS); ah0 = alpha0 + s0 * rng.standard_normal(N_FUNDS)
    y0 = tail(alpha0)
    naive0 = (ah0[:, None] > CS).mean(0)
    print("truth", y0.round(3), "\nnaive", naive0.round(3))

    # 1. Gibbs
    gibbs(ah0[:50], s0[:50], 3, 1, 0, CS, TAU0 ** 2)        # compile
    t0 = time.time(); Yg, Ks, th, Gm = gibbs(ah0, s0, a.sweeps, 500, 1, CS, TAU0 ** 2); t_gibbs = time.time() - t0
    print(f"Gibbs {a.sweeps} sweeps in {t_gibbs:.1f}s; mean {Yg.mean(0).round(3)}; K {Ks.mean():.1f}; theta {th.mean():.2f}")

    # 2. Simulate the training set and fit the map
    t0 = time.time(); X, Y = [], []
    for _ in range(a.sims // 2000):
        ah, s, al = prior_panels(rng, 2000); X.append(summaries(ah, s)); Y.append(tail(al))
    X, Y = np.vstack(X), np.vstack(Y); t_sim = time.time() - t0
    xm, xs = X.mean(0), X.std(0) + 1e-6
    Xt = torch.tensor((X - xm) / xs, dtype=torch.float32); Yt = torch.tensor(Y, dtype=torch.float32)
    nval = 5000; F = Map(X.shape[1]); opt = torch.optim.Adam(F.parameters(), 1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, a.steps)
    m, B = 8, 512
    t0 = time.time()
    for it in range(a.steps):
        idx = torch.randint(nval, len(Xt), (B,))
        x = Xt[idx][:, None].expand(B, m, -1)
        loss = energy(F(x, torch.randn(B, m, NZ)), Yt[idx])
        opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        if it % 2000 == 0 or it == a.steps - 1:
            with torch.no_grad():
                xv = Xt[:nval][:, None].expand(nval, m, -1)
                val = energy(F(xv, torch.randn(nval, m, NZ)), Yt[:nval]).item()
            print(f"step {it} train {loss.item():.4f} val {val:.4f}")
    t_train = time.time() - t0

    def draws(ah, s, k=4000):
        x = torch.tensor((summaries(ah[None], s[None]) - xm) / xs, dtype=torch.float32).expand(k, -1)
        with torch.no_grad():
            return F(x, torch.randn(k, NZ)).numpy()
    t0 = time.time(); Ym = draws(ah0, s0); t_map = time.time() - t0
    print("map mean", Ym.mean(0).round(3), f"{1000 * t_map:.1f} ms")

    # 3. Coverage over 200 fresh panels
    ah, s, al = prior_panels(rng, 200); yt = tail(al); cov = np.zeros(len(CS)); width = np.zeros(len(CS))
    t0 = time.time()
    for b in range(200):
        d = draws(ah[b], s[b], 2000); lo, hi = np.quantile(d, [.05, .95], axis=0)
        cov += (yt[b] >= lo - 1e-4) & (yt[b] <= hi + 1e-4); width += hi - lo
    t_cov = time.time() - t0
    cov /= 200; width /= 200
    print("coverage", cov.round(3), f"200 panels in {t_cov:.2f}s")

    q = lambda D: {"mean": D.mean(0).round(4).tolist(), "q05": np.quantile(D, .05, axis=0).round(4).tolist(), "q95": np.quantile(D, .95, axis=0).round(4).tolist()}
    sub = lambda v, k: np.round(v[np.random.default_rng(0).choice(len(v), min(k, len(v)), replace=False)], 4).tolist()
    W = [p.detach().numpy() for p in F.parameters()]
    sig = lambda A: np.vectorize(lambda v: float(f"{v:.5g}"))(A).tolist()
    out = dict(cs=CS.tolist(), lev=LEV.tolist(), n=N_FUNDS, tau0=TAU0, nz=NZ,
               panel=dict(ah=ah0.round(3).tolist(), s=s0.round(3).tolist(), alpha=alpha0.tolist(), truth=y0.tolist(), naive=naive0.round(4).tolist()),
               gibbs=dict(**q(Yg), y2=sub(Yg[:, 7], 1500), K=np.bincount(Ks).tolist(), theta=float(th.mean()), G=Gm.round(5).tolist(), sec=t_gibbs, sweeps=a.sweeps, burn=500),
               map=dict(**q(Ym), y2=sub(Ym[:, 7], 1500), ms=1000 * t_map),
               cov=cov.round(3).tolist(), width=width.round(4).tolist(), cov_sec=t_cov,
               train=dict(sims=len(X), steps=a.steps, sec=t_train, sim_sec=t_sim),
               net=dict(xm=sig(xm), xs=sig(xs), W=[sig(w) for w in W]))
    with open(a.out, "w") as f:
        f.write("// Generated by gbc-funds-lab.py; do not edit by hand.\nwindow.GBC_FUNDS = " + json.dumps(out, separators=(",", ":")) + ";\n")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
