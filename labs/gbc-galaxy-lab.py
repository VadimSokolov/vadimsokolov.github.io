"""GBC on the galaxy velocities: the computation behind gbc-galaxy-lab.html.

Fits a K = 10 normal mixture to the 82 velocities of MASS::galaxies (Roeder 1990) by
generative Bayesian computation and by a Gibbs sampler under the same prior, and writes
gbc-galaxy-data.js for the lab page.

Model, in thousands of km/s:
    w ~ Dirichlet(e0, ..., e0), e0 = 0.3      (overfitted mixture: empty slots allowed)
    mu_k ~ N(21, 8^2),  sigma_k^2 ~ InvGamma(2, 2),  y_i ~ sum_k w_k N(mu_k, sigma_k^2)
Components are sorted by mean in every simulated draw, so slot k is "the k-th lowest
mean" and labels never enter as parameters.

Architecture (the slide's): U ~ N(0, I_1024) (the frozen random projection R of a wider U
is replaced by its limit, RU ~ N(0, I)), concatenated with S = 32 sample quantiles of the
82 velocities, three dense ReLU layers of width 1024, output 3K = 30 numbers
(w_k, mu_k, log sigma_k). Two losses are compared:
    pinball: coordinate j uses tau_j = Phi(U_j), loss sum_j rho_{tau_j}(theta_j - G_j)
    energy : the energy score E||G(U,S) - theta|| - 1/2 E||G(U,S) - G(U',S)||

A third fit, energy_local, trains the same network on the n = 10^5 data sets closest to the
observed summary out of --local prior simulations (2 x 10^7 by default). Restricting the
training pairs on x leaves p(theta | x) unchanged for x in the kept region, so this is still the
exact target posterior, learned where it matters.

Usage: python gbc-galaxy-lab.py [--steps 12000] [--n 100000] [--local 20000000] [--reuse]
"""
import argparse
import json
import math
import os
import time

import numpy as np
import torch
import torch.nn as nn

GALAXIES = [9172, 9350, 9483, 9558, 9775, 10227, 10406, 16084, 16170, 18419, 18552, 18600, 18927, 19052, 19070, 19330, 19343, 19349, 19440, 19473, 19529, 19541, 19547, 19663, 19846, 19856, 19863, 19914, 19918, 19973, 19989, 20166, 20175, 20179, 20196, 20215, 20221, 20415, 20629, 20795, 20821, 20846, 20875, 20986, 21137, 21492, 21701, 21814, 21921, 21960, 22185, 22209, 22242, 22249, 22314, 22374, 22495, 22746, 22747, 22888, 22914, 23206, 23241, 23263, 23484, 23538, 23542, 23666, 23706, 23711, 24129, 24285, 24289, 24366, 24717, 24990, 25633, 26690, 26995, 32065, 32789, 34279]
Y = np.array(GALAXIES) / 1000.0
N_OBS, K, E0 = len(Y), 10, 0.3
MU0, MU_SD, IG_A, IG_B = 21.0, 8.0, 2.0, 2.0
N_Q, U_DIM, WIDTH = 32, 1024, 1024
QLEV = (np.arange(N_Q) + 0.5) / N_Q
GRID = np.round(np.arange(5.0, 40.01, 0.25), 2)


def prior_draw(rng, n):
    w = rng.dirichlet(np.full(K, E0), size=n)
    mu = rng.normal(MU0, MU_SD, size=(n, K))
    s2 = IG_B / rng.gamma(IG_A, 1.0, size=(n, K))
    order = np.argsort(mu, axis=1)
    take = lambda a: np.take_along_axis(a, order, axis=1)
    return take(w), take(mu), np.sqrt(take(s2))


def simulate(rng, w, mu, sd):
    n = w.shape[0]
    cw = np.cumsum(w, axis=1)
    z = (rng.random((n, N_OBS, 1)) > cw[:, None, :]).sum(-1).clip(max=K - 1)
    return np.take_along_axis(mu, z, 1) + np.take_along_axis(sd, z, 1) * rng.standard_normal((n, N_OBS))


def summary(y):
    return np.quantile(y, QLEV, axis=-1, method="linear").T if y.ndim > 1 else np.quantile(y, QLEV, method="linear")


class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(U_DIM + N_Q, WIDTH), nn.ReLU(), nn.Linear(WIDTH, WIDTH), nn.ReLU(), nn.Linear(WIDTH, WIDTH), nn.ReLU(), nn.Linear(WIDTH, 3 * K))

    def forward(self, u, s):
        return self.net(torch.cat([u, s], dim=1))


def pinball(pred, theta, u):
    tau = torch.special.ndtr(u[:, : 3 * K])
    r = theta - pred
    return torch.maximum(tau * r, (tau - 1) * r).sum(1).mean()


def energy(g1, g2, theta):
    return ((g1 - theta).norm(dim=1) + (g2 - theta).norm(dim=1)).mean() / 2 - 0.5 * (g1 - g2).norm(dim=1).mean()


def train(kind, S, T, steps, dev, seed):
    torch.manual_seed(seed)
    g = Generator().to(dev)
    opt = torch.optim.Adam(g.parameters(), lr=3e-4)
    sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    n, bs, hist, t0 = S.shape[0], 1024, [], time.time()
    for it in range(steps):
        idx = torch.randint(0, n, (bs,), device=dev)
        s, th = S[idx], T[idx]
        u = torch.randn(bs, U_DIM, device=dev)
        if kind == "pinball":
            loss = pinball(g(u, s), th, u)
        else:
            loss = energy(g(u, s), g(torch.randn(bs, U_DIM, device=dev), s), th)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sch.step()
        if it % 100 == 0:
            hist.append(round(loss.item(), 4))
        if it % 2000 == 0:
            print(f"  {kind} step {it} loss {loss.item():.4f} ({time.time() - t0:.0f}s)", flush=True)
    return g, hist, time.time() - t0


def to_params(raw, tm, ts):
    th = raw * ts + tm
    w_raw = th[:, :K]
    w = np.clip(w_raw, 0, None)
    w = w / w.sum(1, keepdims=True).clip(min=1e-12)
    mu, sd = th[:, K : 2 * K], np.exp(th[:, 2 * K :])
    return w_raw, w, mu, sd


def dens(w, mu, sd):
    z = (GRID[None, None, :] - mu[:, :, None]) / sd[:, :, None]
    return (w[:, :, None] * np.exp(-0.5 * z**2) / (sd[:, :, None] * math.sqrt(2 * math.pi))).sum(1)


def occupied(rng, w, mu, sd):
    lp = np.log(np.clip(w, 1e-300, None))[:, None, :] - np.log(sd)[:, None, :] - 0.5 * ((Y[None, :, None] - mu[:, None, :]) / sd[:, None, :]) ** 2
    p = np.exp(lp - lp.max(-1, keepdims=True))
    p /= p.sum(-1, keepdims=True)
    z = (rng.random(p.shape[:2] + (1,)) > np.cumsum(p, -1)).sum(-1).clip(max=K - 1)
    occ = np.array([len(np.unique(r)) for r in z])
    return np.bincount(occ, minlength=K + 1)[1:] / len(occ)


def gibbs(rng, iters=30000, burn=5000, thin=5):
    w = np.full(K, 1.0 / K)
    mu = np.quantile(Y, (np.arange(K) + 0.5) / K)
    s2 = np.ones(K)
    out = []
    for it in range(iters):
        lp = np.log(w) - 0.5 * np.log(s2) - 0.5 * (Y[:, None] - mu) ** 2 / s2
        p = np.exp(lp - lp.max(1, keepdims=True))
        p /= p.sum(1, keepdims=True)
        z = (rng.random((N_OBS, 1)) > np.cumsum(p, 1)).sum(1).clip(max=K - 1)
        nk = np.bincount(z, minlength=K)
        w = rng.dirichlet(E0 + nk)
        for k in range(K):
            yk = Y[z == k]
            prec = 1 / MU_SD**2 + nk[k] / s2[k]
            mu[k] = rng.normal((MU0 / MU_SD**2 + yk.sum() / s2[k]) / prec, 1 / math.sqrt(prec))
            s2[k] = (IG_B + 0.5 * ((yk - mu[k]) ** 2).sum()) / rng.gamma(IG_A + nk[k] / 2)
        if it >= burn and it % thin == 0:
            o = np.argsort(mu)
            out.append((w[o].copy(), mu[o].copy(), np.sqrt(s2[o]), len(np.unique(z))))
    W = np.array([o[0] for o in out]); M = np.array([o[1] for o in out]); SD = np.array([o[2] for o in out])
    occ = np.bincount([o[3] for o in out], minlength=K + 1)[1:] / len(out)
    return W, M, SD, occ


def band(d):
    return {"mean": np.round(d.mean(0), 5).tolist(), "lo": np.round(np.quantile(d, 0.05, 0), 5).tolist(), "hi": np.round(np.quantile(d, 0.95, 0), 5).tolist()}


def atoms(rng, w, mu, n=500):
    i = rng.choice(len(w), size=min(n, len(w)), replace=False)
    a = np.stack([mu[i].ravel(), w[i].ravel()], 1)
    a = a[a[:, 1] > 0.005]
    return np.round(a, 3).tolist()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100_000)
    ap.add_argument("--steps", type=int, default=12_000)
    ap.add_argument("--draws", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="gbc-galaxy-data.js")
    ap.add_argument("--local", type=int, default=20_000_000, help="prior simulations screened for the localized training set")
    ap.add_argument("--reuse", action="store_true", help="keep results already in --out and fit only the missing ones")
    a = ap.parse_args()
    dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    rng = np.random.default_rng(a.seed)

    t0 = time.time()
    w, mu, sd = prior_draw(rng, a.n)
    S = summary(simulate(rng, w, mu, sd))
    T = np.concatenate([w, mu, np.log(sd)], 1)
    print(f"simulated {a.n} data sets in {time.time() - t0:.1f}s; device {dev}")
    # prior on the number of occupied components among 82 simulated points
    cw = np.cumsum(w[:20000], 1)
    zz = (rng.random((20000, N_OBS, 1)) > cw[:, None, :]).sum(-1).clip(max=K - 1)
    prior_occ = np.bincount([len(np.unique(r)) for r in zz], minlength=K + 1)[1:] / 20000

    old = {}
    if a.reuse and os.path.exists(a.out):
        txt = open(a.out).read()
        old = json.loads(txt[txt.index("{") : txt.rindex("}") + 1])["res"]

    def fit(kind, loss, S, T, extra):
        if kind in old:
            print(f"{kind}: reusing the saved result")
            return old[kind]
        sm, ss, tm, ts = S.mean(0), S.std(0), T.mean(0), T.std(0)
        St = torch.tensor((S - sm) / ss, dtype=torch.float32, device=dev)
        Tt = torch.tensor((T - tm) / ts, dtype=torch.float32, device=dev)
        s_obs = torch.tensor(((summary(Y) - sm) / ss)[None, :], dtype=torch.float32, device=dev)
        g, hist, secs = train(loss, St, Tt, a.steps, dev, a.seed)
        with torch.no_grad():
            raw = g(torch.randn(a.draws, U_DIM, device=dev), s_obs.expand(a.draws, -1)).cpu().numpy()
        w_raw, wp, mp, sp = to_params(raw, tm, ts)
        r = {"band": band(dens(wp, mp, sp)), "occ": np.round(occupied(rng, wp, mp, sp), 4).tolist(), "atoms": atoms(rng, wp, mp), "wsum": np.round(w_raw.sum(1), 3)[:2000].tolist(), "loss": hist, "seconds": round(secs + extra)}
        print(f"{kind}: {secs:.0f}s, sum of raw weights mean {w_raw.sum(1).mean():.3f} sd {w_raw.sum(1).std():.3f}, occupied {np.round(r['occ'], 3)}")
        return r

    res = {"energy": fit("energy", "energy", S, T, 0), "pinball": fit("pinball", "pinball", S, T, 0)}

    # Localized training set: keep the n simulated data sets whose summary is closest to the
    # observed one. Restricting pairs on x leaves p(theta | x) unchanged for x in that region.
    loc = {}
    if "energy_local" not in old:
        t0, s_obs_raw, keepS, keepT, keepD = time.time(), summary(Y), [], [], []
        chunk = 200_000
        for c in range(a.local // chunk):
            w2, mu2, sd2 = prior_draw(rng, chunk)
            S2 = summary(simulate(rng, w2, mu2, sd2))
            d2 = np.sqrt(((S2 - s_obs_raw) ** 2).mean(1))
            cut = np.partition(np.concatenate(keepD + [d2]), a.n - 1)[a.n - 1] if sum(len(k) for k in keepD) + len(d2) > a.n else np.inf
            i = d2 <= cut
            keepS.append(S2[i]); keepT.append(np.concatenate([w2, mu2, np.log(sd2)], 1)[i]); keepD.append(d2[i])
            if len(keepD) > 1:  # trim to the current n closest
                Dc = np.concatenate(keepD); o = np.argsort(Dc)[: a.n]
                keepS, keepT, keepD = [np.concatenate(keepS)[o]], [np.concatenate(keepT)[o]], [Dc[o]]
        SL, TL, DL = keepS[0], keepT[0], keepD[0]
        loc = {"n_prior": a.local, "kept": len(DL), "max_dist": round(float(DL.max()), 4), "median_dist": round(float(np.median(DL)), 4), "sim_seconds": round(time.time() - t0)}
        print(f"localized: kept {len(DL)} of {a.local} prior simulations, RMS distance <= {DL.max():.3f} ({time.time() - t0:.0f}s)")
        res["energy_local"] = fit("energy_local", "energy", SL, TL, time.time() - t0)
        res["energy_local"]["local"] = loc
    else:
        res["energy_local"] = old["energy_local"]

    if "gibbs" in old:
        res["gibbs"] = old["gibbs"]
    else:
        t0 = time.time()
        W, M, SD, occ = gibbs(rng)
        res["gibbs"] = {"band": band(dens(W, M, SD)), "occ": np.round(occ, 4).tolist(), "atoms": atoms(rng, W, M), "wsum": [1.0], "seconds": round(time.time() - t0)}
        print(f"gibbs: {len(W)} draws in {time.time() - t0:.0f}s, occupied {np.round(occ, 3)}")

    data = {"y": Y.tolist(), "grid": GRID.tolist(), "qlev": QLEV.tolist(), "sobs": np.round(summary(Y), 4).tolist(), "prior_occ": np.round(prior_occ, 4).tolist(),
            "config": {"n_sim": a.n, "n_local": a.local, "steps": a.steps, "draws": a.draws, "K": K, "e0": E0, "u_dim": U_DIM, "width": WIDTH, "n_q": N_Q, "device": dev, "seed": a.seed}, "res": res}
    with open(a.out, "w") as f:
        f.write("// Generated by gbc-galaxy-lab.py; do not edit by hand.\nwindow.GBC_GALAXY = " + json.dumps(data, separators=(",", ":")) + ";\n")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
