"""Ten-layer ReLU policy-value network for chess, trained on Stockfish-labelled positions.
Features from the side to move's view (board mirrored when black is to move):
  12 planes x 64 squares (own P N B R Q K, then the opponent's) + 4 castling bits = 772.
Value target: p = 1 / (1 + 10^(-cp/400)), the engine score as a win probability.
Policy target: the engine's best move as from*64 + to, in the same mirrored coordinates.
Usage: python chess_lab_train.py DATA_DIR OUT_DIR DEPTH WIDTH EPOCHS"""
import sys, glob, csv, math, json, time
import numpy as np, torch, torch.nn as nn
import chess
torch.manual_seed(0); np.random.seed(0)
PL = {'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5}

def feats(fen):
    b = chess.Board(fen); w = b.turn == chess.WHITE; x = np.zeros(772, np.float32)
    for sq, pc in b.piece_map().items():
        s = sq if w else sq ^ 56; own = pc.color == b.turn
        x[(PL[pc.symbol().upper()] + (0 if own else 6)) * 64 + s] = 1
    cr = [b.has_kingside_castling_rights(b.turn), b.has_queenside_castling_rights(b.turn), b.has_kingside_castling_rights(not b.turn), b.has_queenside_castling_rights(not b.turn)]
    x[768:] = cr
    return x, w

def load(DATA):
    cache = DATA + "/cache.npz"
    try:
        z = np.load(cache); return z["X"], z["V"], z["P"]
    except Exception: pass
    X, V, P = [], [], []
    for f in sorted(glob.glob(DATA + "/pos_*.csv")):
        for fen, cp, best in csv.reader(open(f)):
            if not best: continue
            x, w = feats(fen); m = chess.Move.from_uci(best)
            fr, to = (m.from_square, m.to_square) if w else (m.from_square ^ 56, m.to_square ^ 56)
            X.append(x); V.append(1 / (1 + 10 ** (-int(cp) / 400))); P.append(fr * 64 + to)
    X, V, P = np.array(X, np.uint8), np.array(V, np.float32), np.array(P, np.int64)
    np.savez_compressed(cache, X=X, V=V, P=P); return X, V, P

class Net(nn.Module):
    """depth linear layers, each followed by a ReLU. With res=True, a layer whose input and output widths agree
    adds its input back (h <- h + ReLU(W h + b)), as in residual networks."""
    def __init__(s, depth, width, res=False):
        super().__init__()
        dims = [772] + [width] * (depth - 1) + [128]
        s.trunk = nn.ModuleList([nn.Linear(dims[i], dims[i + 1]) for i in range(depth)])
        s.res = [res and dims[i] == dims[i + 1] for i in range(depth)]
        for L in s.trunk: nn.init.kaiming_normal_(L.weight, nonlinearity="relu"); nn.init.zeros_(L.bias)
        s.v = nn.Linear(128, 1); s.p = nn.Linear(128, 4096)
    def forward(s, x):
        for L, r in zip(s.trunk, s.res):
            h = torch.relu(L(x)); x = x + h if r else h
        return s.v(x).squeeze(-1), s.p(x)

if __name__ == "__main__":
    DATA, OUT, DEPTH, WIDTH, EPOCHS = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    RES = len(sys.argv) > 6 and sys.argv[6] == "res"; TAG = f"d{DEPTH}_w{WIDTH}" + ("_res" if RES else "")
    t0 = time.time(); X, V, P = load(DATA); n = len(V); print("positions", n, "loaded in", round(time.time() - t0), "s", flush=True)
    idx = np.random.permutation(n); nte = 20000; te, tr = idx[:nte], idx[nte:]
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    net = Net(DEPTH, WIDTH, RES).to(dev); opt = torch.optim.AdamW(net.parameters(), lr=1e-3, weight_decay=1e-5)
    steps = EPOCHS * (len(tr) // 512); sch = torch.optim.lr_scheduler.OneCycleLR(opt, 2e-3, total_steps=steps)
    Xt, Vt, Pt = torch.tensor(X[te], dtype=torch.float32, device=dev), torch.tensor(V[te], device=dev), torch.tensor(P[te], device=dev)
    def evaluate():
        net.eval()
        with torch.no_grad():
            v, p = net(Xt); vb = nn.functional.binary_cross_entropy_with_logits(v, Vt).item(); vm = (torch.sigmoid(v) - Vt).pow(2).mean().sqrt().item()
            acc = (p.argmax(-1) == Pt).float().mean().item()
        net.train(); return vb, vm, acc
    log = []
    for ep in range(EPOCHS):
        perm = np.random.permutation(tr)
        for i in range(0, len(perm) - 511, 512):
            bi = perm[i:i + 512]
            xb = torch.tensor(X[bi], dtype=torch.float32, device=dev); vb = torch.tensor(V[bi], device=dev); pb = torch.tensor(P[bi], device=dev)
            v, p = net(xb)
            loss = nn.functional.binary_cross_entropy_with_logits(v, vb) + 0.5 * nn.functional.cross_entropy(p, pb)
            opt.zero_grad(); loss.backward(); opt.step(); sch.step()
        r = evaluate(); log.append([ep + 1, *r]); print(f"epoch {ep+1} value BCE {r[0]:.4f} value RMSE {r[1]:.4f} policy top-1 {r[2]:.3f}  {time.time()-t0:.0f}s", flush=True)
    params = sum(q.numel() for q in net.parameters())
    torch.save(net.state_dict(), f"{OUT}/net_{TAG}.pt")
    json.dump({"depth": DEPTH, "width": WIDTH, "res": RES, "params": params, "log": log, "test_idx_seed": 0}, open(f"{OUT}/net_{TAG}.json", "w"))
    print("params", params)
