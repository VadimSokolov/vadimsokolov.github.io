"""Graph Transformer Lab: export the four trained models, the graphs and layouts to graph-transformer-data.js.

Needs Nick Polson's Week 8 code next to this script or in CODE_DIR:
  graph_transformer_medici.py, ambani_graph_transformer.py, results.json (training log of the deck's run),
and weights4.pt, the state dicts of all four models trained by graph_transformer_medici.train_all
(seed 41916, 3,000 steps); saving them takes one line after train_all in that script.

Run:  python graph-transformer-lab.py CODE_DIR weights4.pt [int8|f32]
Weights are stored as int8 with one scale per output row (largest change in any prediction about 0.005).
The Laplacian eigenvectors use a sign convention the browser copies: largest absolute entry positive.
"""
import sys, json, math, base64, random
CODE, WFILE = sys.argv[1], sys.argv[2]
sys.path.insert(0, CODE)
import numpy as np, torch, networkx as nx
from scipy.stats import spearmanr
import graph_transformer_medici as g
import ambani_graph_transformer as amb

QUANT = sys.argv[3] if len(sys.argv) > 3 else "int8"

def lap_pe_fixed(G, nodes):
    """Same as g.laplacian_pe, with a sign convention the browser can copy:
    each eigenvector is flipped so that its largest absolute entry is positive."""
    n = len(nodes)
    A = nx.to_numpy_array(G, nodelist=nodes); d = A.sum(1)
    dinv = np.where(d > 0, 1.0 / np.sqrt(np.maximum(d, 1e-12)), 0.0)
    L = np.eye(n) - dinv[:, None] * A * dinv[None, :]
    _, vec = np.linalg.eigh(L)
    for j in range(vec.shape[1]):
        i = np.argmax(np.abs(vec[:, j]))
        if vec[i, j] < 0: vec[:, j] *= -1
    pe = np.zeros((g.N_MAX, g.K_PE), dtype=np.float32); k = min(g.K_PE, n - 1)
    pe[:n, :k] = vec[:, 1:k + 1]
    return pe
g.laplacian_pe = lap_pe_fixed

W = torch.load(WFILE)
models = {}
for m in g.MODES:
    models[m] = g.GraphTransformer(m); models[m].load_state_dict(W[m]); models[m].eval()

def q(t):
    a = t.detach().numpy().astype(np.float32)
    if QUANT == "f32" or a.size < 64:
        return {"s": list(a.shape), "f": base64.b64encode(a.astype("<f4").tobytes()).decode()}
    a2 = a.reshape(a.shape[0], -1) if a.ndim > 1 else a.reshape(1, -1)
    sc = np.abs(a2).max(1) / 127.0; sc[sc == 0] = 1
    qi = np.clip(np.round(a2 / sc[:, None]), -127, 127).astype(np.int8)
    return {"s": list(a.shape), "q": base64.b64encode(qi.tobytes()).decode(), "c": [float(f"{x:.6g}") for x in sc]}

def deq(e):
    if "f" in e: return np.frombuffer(base64.b64decode(e["f"]), dtype="<f4").reshape(e["s"])
    qi = np.frombuffer(base64.b64decode(e["q"]), dtype=np.int8).reshape(len(e["c"]), -1).astype(np.float32)
    return (qi * np.array(e["c"], dtype=np.float32)[:, None]).reshape(e["s"])

out_models = {m: {k: q(v) for k, v in W[m].items()} for m in g.MODES}
# models with the exported (possibly quantized) weights, to measure the quantization error
qm = {}
for m in g.MODES:
    qm[m] = g.GraphTransformer(m)
    qm[m].load_state_dict({k: torch.from_numpy(deq(e).copy()) for k, e in out_models[m].items()}); qm[m].eval()

# graphs
names = sorted(nx.florentine_families_graph().nodes())
def layer(edges):
    H = nx.Graph(); H.add_nodes_from(names); H.add_edges_from(edges); return H
marriage = layer(nx.florentine_families_graph().edges())
business = layer(g.BUSINESS)
both = layer(list(marriage.edges()) + g.BUSINESS)
houses = amb.build(amb.HOUSES)
control = amb.build(amb.CONTROL, amb.PERSON + amb.BUSINESS + amb.INLAW)
succ = control.copy(); succ.remove_node("Mukesh")

def norm_pos(pos):
    xs = np.array([p[0] for p in pos.values()]); ys = np.array([p[1] for p in pos.values()])
    return {k: [round(float((p[0] - xs.min()) / (xs.max() - xs.min())), 4), round(float((p[1] - ys.min()) / (ys.max() - ys.min())), 4)] for k, p in pos.items()}
pos_f = norm_pos(nx.kamada_kawai_layout(marriage))
pos_h = norm_pos(nx.kamada_kawai_layout(houses))
pos_c = norm_pos(amb.CONTROL_POS)

def ref(G, mods):
    b = g.batch_of([G]); n = G.number_of_nodes()
    with torch.no_grad():
        return {m: [round(float(x), 5) for x in g.run(mods[m], b)[0][0, :n].numpy()] for m in g.MODES}, [round(float(x), 5) for x in b[4][0, :n].numpy()]

refs, qerr = {}, 0
for key, G in [("marriage", marriage), ("business", business), ("both", both), ("houses", houses), ("control", control), ("succession", succ)]:
    p, t = ref(G, models); pq, _ = ref(G, qm)
    refs[key] = {"nodes": list(G.nodes()), "true": t, "pred": pq, "pred_full": p}
    for m in g.MODES:
        qerr = max(qerr, float(np.max(np.abs(np.array(p[m]) - np.array(pq[m])))))
        print(f"{key:10s} {m:6s} rmse {np.sqrt(np.mean((np.array(p[m]) - np.array(t)) ** 2)):.3f} rho {spearmanr(p[m], t).statistic:.2f} top {[list(G.nodes())[i] for i in np.argsort(-np.array(p[m]))[:3]]}")
print("max quantization error in predictions", qerr)

# held-out validation with the fixed-sign PE (to report)
vr = random.Random(g.SEED + 1)
val = g.batch_of([g.random_graph(vr) for _ in range(500)])
vres = {}
with torch.no_grad():
    for m in g.MODES:
        vp = g.run(models[m], val)[0]
        vres[m] = {"rmse": math.sqrt(g.masked_mse(vp, val[4], val[3]).item()), "spearman": g.rank_corr(vp, val[4], val[3])}
print("val", vres)
logs = json.load(open(CODE + "/results.json"))["val_mse_log"]
data = {
  "cfg": {"D": g.D_MODEL, "H": g.N_HEAD, "L": g.N_LAYER, "MAX_DEG": g.MAX_DEG, "MAX_SPD": g.MAX_SPD, "K_PE": g.K_PE, "seed": g.SEED, "steps": g.STEPS, "batch": g.BATCH},
  "models": out_models,
  "val": vres,
  "logs": {m: [[s, round(math.sqrt(v), 5)] for s, v in logs[m]] for m in g.MODES},
  "florence": {"names": names, "marriage": [list(e) for e in marriage.edges()], "business": [list(e) for e in g.BUSINESS], "wealth": g.WEALTH, "priorates": g.PRIORATES, "pos": pos_f},
  "houses": {"names": list(houses.nodes()), "edges": [list(e) for e in amb.HOUSES], "pos": pos_h},
  "control": {"names": list(control.nodes()), "edges": [list(e) for e in amb.CONTROL], "person": amb.PERSON, "business": amb.BUSINESS, "inlaw": amb.INLAW, "pos": pos_c},
  "ref": refs,
}
s = "window.GT = " + json.dumps(data, separators=(",", ":")) + ";\n"
open("graph-transformer-data.js", "w").write(s)
print("bytes", len(s))
