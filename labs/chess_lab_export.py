"""Export the ten-layer chess network for the browser: int8 weights with one scale per row.
The first layer is stored transposed (one row per input feature), since a board switches on only 20 to 36 of the 772 inputs.
Usage: python chess_lab_export.py NET_PT DEPTH WIDTH RESULTS_JSON OUT_JS"""
import sys, json, base64
import numpy as np, torch
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chess_lab_train import Net
PT, DEPTH, WIDTH, RES, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
RESID = len(sys.argv) > 6 and sys.argv[6] == "res"
sd = torch.load(PT, map_location="cpu")
def q(a):
    a = np.asarray(a, np.float32)
    if a.ndim == 1: return {"f": base64.b64encode(a.astype("<f4").tobytes()).decode()}
    sc = np.abs(a).max(1) / 127.0; sc[sc == 0] = 1
    qi = np.clip(np.round(a / sc[:, None]), -127, 127).astype(np.int8)
    return {"q": base64.b64encode(qi.tobytes()).decode(), "c": [float(f"{x:.6g}") for x in sc]}
layers = []
for i in range(DEPTH):
    W = sd[f"trunk.{i}.weight"].numpy(); b = sd[f"trunk.{i}.bias"].numpy()
    layers.append({"W": q(W.T if i == 0 else W), "b": q(b), "nin": W.shape[1], "nout": W.shape[0], "cols": i == 0, "res": bool(RESID and W.shape[0] == W.shape[1])})
data = {"layers": layers, "v": {"W": q(sd["v.weight"].numpy()[0]), "b": q(sd["v.bias"].numpy())}, "p": {"W": q(sd["p.weight"].numpy()), "b": q(sd["p.bias"].numpy())}, "results": json.load(open(RES)) if RES != "-" else None}
s = "window.CHESSNET = " + json.dumps(data, separators=(",", ":")) + ";\n"
open(OUT, "w").write(s); print("bytes", len(s))
