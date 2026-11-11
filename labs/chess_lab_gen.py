"""Generate chess positions from engine games with random openings and label them with Stockfish.
Usage: python chess_lab_gen.py WORKER_ID N_POSITIONS OUT_DIR"""
import sys, random, csv
import chess, chess.engine
wid, target, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(1000 + wid)
eng = chess.engine.SimpleEngine.popen_uci("stockfish")
eng.configure({"Threads": 1, "Hash": 16})
n = 0
with open(f"{out}/pos_{wid}.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    while n < target:
        b = chess.Board()
        for _ in range(rng.randint(2, 10)):
            mv = list(b.legal_moves)
            if not mv: break
            b.push(rng.choice(mv))
        ply = 0
        while not b.is_game_over(claim_draw=True) and ply < 200 and n < target:
            if rng.random() < 0.5:
                info = eng.analyse(b, chess.engine.Limit(depth=9))
                sc = info["score"].pov(b.turn).score(mate_score=3000)
                best = info["pv"][0].uci() if info.get("pv") else ""
                w.writerow([b.fen(), sc, best]); n += 1
            if rng.random() < 0.15:
                b.push(rng.choice(list(b.legal_moves)))
            else:
                b.push(eng.play(b, chess.engine.Limit(depth=rng.choice([1, 2, 3, 4]))).move)
            ply += 1
        if n % 5000 < 60: print(wid, n, flush=True)
eng.quit()
print("done", wid, n, flush=True)
