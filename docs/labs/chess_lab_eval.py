"""Matches for the ten-layer network: policy only, value one ply, and PUCT search, against simple opponents.
Usage: python chess_lab_eval.py NET_PT DEPTH WIDTH GAMES OUT_JSON"""
import sys, json, math, random
import numpy as np, torch, chess, chess.engine
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chess_lab_train import Net, PL
PT, DEPTH, WIDTH, GAMES, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
net = Net(DEPTH, WIDTH, "_res" in PT); net.load_state_dict(torch.load(PT, map_location="cpu")); net.eval(); torch.set_num_threads(1)
def feats(b):
    w = b.turn == chess.WHITE; x = np.zeros(772, np.float32)
    for sq, pc in b.piece_map().items():
        x[(PL[pc.symbol().upper()] + (0 if pc.color == b.turn else 6)) * 64 + (sq if w else sq ^ 56)] = 1
    x[768:] = [b.has_kingside_castling_rights(b.turn), b.has_queenside_castling_rights(b.turn), b.has_kingside_castling_rights(not b.turn), b.has_queenside_castling_rights(not b.turn)]
    return x
def ev(b):
    with torch.no_grad():
        v, p = net(torch.from_numpy(feats(b))[None])
    w = b.turn == chess.WHITE; ms = list(b.legal_moves)
    lg = np.array([p[0, (m.from_square if w else m.from_square ^ 56) * 64 + (m.to_square if w else m.to_square ^ 56)].item() for m in ms])
    pr = np.exp(lg - lg.max()); pr /= pr.sum()
    return 1 / (1 + math.exp(-v.item())), ms, pr
def term(b):
    if b.is_checkmate(): return -1.0
    if b.is_game_over(claim_draw=True): return 0.0
    return None
def mcts(b, n):
    class N_: pass
    def mk(bd):
        nd = N_(); nd.b = bd; t = term(bd)
        if t is not None: nd.term = True; nd.tv = t; return nd
        nd.term = False; v, ms, pr = ev(bd); nd.v = 2 * v - 1; nd.ms = ms; nd.P = pr; nd.N = np.zeros(len(ms)); nd.W = np.zeros(len(ms)); nd.ch = [None] * len(ms); return nd
    R = mk(b.copy())
    for _ in range(n):
        node, path = R, []
        while not node.term:
            tot = node.N.sum(); q = np.where(node.N > 0, node.W / np.maximum(node.N, 1), 0)
            i = int(np.argmax(q + 1.5 * node.P * math.sqrt(tot + 1) / (1 + node.N))); path.append((node, i))
            if node.ch[i] is None:
                bb = node.b.copy(); bb.push(node.ms[i]); node.ch[i] = mk(bb); node = node.ch[i]; break
            node = node.ch[i]
        v = node.tv if node.term else node.v
        for nd, i in reversed(path): v = -v; nd.N[i] += 1; nd.W[i] += v
    return R.ms[int(np.argmax(R.N))]
def pick(b, how):
    if how == "pol": _, ms, pr = ev(b); return ms[int(np.argmax(pr))]
    if how == "val":
        best, bv = None, -9
        for m in b.legal_moves:
            b.push(m); t = term(b); v = (1.0 if t == -1 else 0.5) if t is not None else 1 - ev(b)[0]; b.pop()
            if v > bv: bv, best = v, m
        return best
    return mcts(b, int(how[4:]))
eng = chess.engine.SimpleEngine.popen_uci("stockfish"); eng.configure({"Threads": 1, "Skill Level": 0})
judge = chess.engine.SimpleEngine.popen_uci("stockfish"); judge.configure({"Threads": 1})
VAL = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
def opp_move(b, opp, rng):
    ms = list(b.legal_moves)
    if opp == "random": return rng.choice(ms)
    if opp == "greedy":
        caps = [m for m in ms if b.is_capture(m)]
        if caps: return max(caps, key=lambda m: (VAL[b.piece_type_at(m.to_square)] if b.piece_type_at(m.to_square) else 1, rng.random()))
        return rng.choice(ms)
    d = int(opp.split("_d")[1]); return eng.play(b, chess.engine.Limit(depth=d)).move
def game(how, opp, net_white, rng):
    b = chess.Board()
    for _ in range(2): b.push(rng.choice(list(b.legal_moves)))
    for ply in range(200):
        if b.is_game_over(claim_draw=True): break
        b.push(pick(b, how) if (b.turn == chess.WHITE) == net_white else opp_move(b, opp, rng))
    if b.is_game_over(claim_draw=True):
        r = b.result(claim_draw=True); s = 0.5 if r == "1/2-1/2" else (1.0 if (r == "1-0") == net_white else 0.0)
    else:
        sc = judge.analyse(b, chess.engine.Limit(depth=12))["score"].pov(chess.WHITE if net_white else chess.BLACK).score(mate_score=3000)
        s = 1.0 if sc > 200 else 0.0 if sc < -200 else 0.5
    return s
PAIRS = [("pol", "random"), ("pol", "greedy"), ("pol", "stockfish_d1"), ("val", "stockfish_d1"), ("mcts100", "stockfish_d1"), ("mcts400", "stockfish_d1"), ("mcts400", "stockfish_d4")]
if len(sys.argv) > 6 and sys.argv[6]: PAIRS = [tuple(p.split(":")) for p in sys.argv[6].split(",")]
res = []
for how, opp in PAIRS:
    rng = random.Random(7); sc = [game(how, opp, g % 2 == 0, rng) for g in range(GAMES)]
    r = {"how": how, "opp": opp, "w": sc.count(1.0), "d": sc.count(0.5), "l": sc.count(0.0)}; res.append(r); print(r, flush=True)
json.dump(res, open(OUT, "w"))
eng.quit(); judge.quit()
