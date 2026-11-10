"""Graph Transformer Lab: export the trained models of the five seeds, the graphs, layouts and the
paper's robustness summary for the browser.

Run from anywhere:  python graph-transformer-lab.py CODE_DIR [OUT_DIR]
CODE_DIR holds the paper's code: graph_transformer_medici.py, ambani_graph_transformer.py,
weights_seed*.pt (from train_seeds.py), robust_results.json (from evaluate_all.py) and results.json.

Writes graph-transformer-data.js (graphs, layouts, the first seed's weights, training curves and
the five-seed summary) and graph-transformer-seed-<seed>.js for each further seed.
Weights are int8 with one scale per output row; the largest change in any prediction is about 0.005.
The Laplacian eigenvectors use a sign convention the browser copies: largest absolute entry positive.
"""
import sys, json, glob, re, base64
CODE = sys.argv[1]; OUT = sys.argv[2] if len(sys.argv) > 2 else "."
sys.path.insert(0, CODE)
import numpy as np, torch, networkx as nx
import graph_transformer_medici as g
import ambani_graph_transformer as amb

def lap_pe_fixed(G, nodes):
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

def q(t):
    a = t.detach().numpy().astype(np.float32)
    if a.size < 64:
        return {"s": list(a.shape), "f": base64.b64encode(a.astype("<f4").tobytes()).decode()}
    a2 = a.reshape(a.shape[0], -1) if a.ndim > 1 else a.reshape(1, -1)
    sc = np.abs(a2).max(1) / 127.0; sc[sc == 0] = 1
    qi = np.clip(np.round(a2 / sc[:, None]), -127, 127).astype(np.int8)
    return {"s": list(a.shape), "q": base64.b64encode(qi.tobytes()).decode(), "c": [float(f"{x:.6g}") for x in sc]}

def deq(e):
    if "f" in e: return np.frombuffer(base64.b64decode(e["f"]), dtype="<f4").reshape(e["s"])
    qi = np.frombuffer(base64.b64decode(e["q"]), dtype=np.int8).reshape(len(e["c"]), -1).astype(np.float32)
    return (qi * np.array(e["c"], dtype=np.float32)[:, None]).reshape(e["s"])

names = sorted(nx.florentine_families_graph().nodes())
def layer(edges):
    H = nx.Graph(); H.add_nodes_from(names); H.add_edges_from(edges); return H
marriage = layer(nx.florentine_families_graph().edges()); business = layer(g.BUSINESS); both = layer(list(marriage.edges()) + g.BUSINESS)
houses = amb.build(amb.HOUSES); control = amb.build(amb.CONTROL, amb.PERSON + amb.BUSINESS + amb.INLAW)
succ = control.copy(); succ.remove_node("Mukesh")
GRAPHS = [("marriage", marriage), ("business", business), ("both", both), ("houses", houses), ("control", control), ("succession", succ)]

def norm_pos(pos):
    xs = np.array([p[0] for p in pos.values()]); ys = np.array([p[1] for p in pos.values()])
    return {k: [round(float((p[0] - xs.min()) / (xs.max() - xs.min())), 4), round(float((p[1] - ys.min()) / (ys.max() - ys.min())), 4)] for k, p in pos.items()}

files = sorted(glob.glob(CODE + "/weights_seed*.pt")); seeds = [int(re.search(r"seed(\d+)", f).group(1)) for f in files]
refs, qerr = {}, 0.0
for f, sd in zip(files, seeds):
    W = torch.load(f)["weights"]
    out_models = {m: {k: q(v) for k, v in W[m].items()} for m in g.MODES}
    qm = {}
    for m in g.MODES:
        qm[m] = g.GraphTransformer(m); qm[m].load_state_dict({k: torch.from_numpy(deq(e).copy()) for k, e in out_models[m].items()}); qm[m].eval()
        full = g.GraphTransformer(m); full.load_state_dict(W[m]); full.eval()
        for key, G in GRAPHS:
            b = g.batch_of([G]); n = G.number_of_nodes()
            with torch.no_grad():
                pq = g.run(qm[m], b)[0][0, :n].numpy(); pf = g.run(full, b)[0][0, :n].numpy()
            qerr = max(qerr, float(np.abs(pq - pf).max()))
            refs.setdefault(str(sd), {}).setdefault(key, {"nodes": list(G.nodes())})[m] = [round(float(x), 5) for x in pq]
    if sd == seeds[0]:
        base_models = out_models
    else:
        open(f"{OUT}/graph-transformer-seed-{sd}.js", "w").write(f"(window.GT_SEEDS = window.GT_SEEDS || {{}})[{sd}] = " + json.dumps(out_models, separators=(",", ":")) + ";\n")
    print("seed", sd, "exported", flush=True)
print("max quantization error in predictions", qerr)

rob = json.load(open(CODE + "/robust_results.json"))
summ = {k: {m: {"rmse": [float(np.mean([r["rmse"] for r in v])), float(np.std([r["rmse"] for r in v]))], "spearman": [float(np.mean([r["spearman"] for r in v])), float(np.std([r["spearman"] for r in v]))]} for m, v in rob["sets"][k].items()} for k in rob["sets"]}
logs = json.load(open(CODE + "/results.json"))["val_mse_log"]
data = {
  "cfg": {"D": g.D_MODEL, "H": g.N_HEAD, "L": g.N_LAYER, "MAX_DEG": g.MAX_DEG, "MAX_SPD": g.MAX_SPD, "K_PE": g.K_PE},
  "seeds": seeds, "models": base_models, "summary": summ, "degree_baseline": rob["degree_baseline"],
  "logs": {m: [[s, round(float(np.sqrt(v)), 5)] for s, v in logs[m]] for m in g.MODES},
  "florence": {"names": names, "marriage": [list(e) for e in marriage.edges()], "business": [list(e) for e in g.BUSINESS], "wealth": g.WEALTH, "priorates": g.PRIORATES, "pos": norm_pos(nx.kamada_kawai_layout(marriage))},
  "houses": {"names": list(houses.nodes()), "edges": [list(e) for e in amb.HOUSES], "pos": norm_pos(nx.kamada_kawai_layout(houses))},
  "control": {"names": list(control.nodes()), "edges": [list(e) for e in amb.CONTROL], "person": amb.PERSON, "business": amb.BUSINESS, "inlaw": amb.INLAW, "pos": norm_pos(amb.CONTROL_POS)},
}
s = "window.GT = " + json.dumps(data, separators=(",", ":")) + ";\n"
open(f"{OUT}/graph-transformer-data.js", "w").write(s)
json.dump(refs, open(f"{OUT}/gt-refs.json", "w"))
print("base bytes", len(s))
