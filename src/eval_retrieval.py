import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "starter"))
from baseline import hit, pack_context
from retrievers import DenseRetriever, HybridRetriever, LexicalRetriever

QUESTIONS = ROOT / "starter" / "data" / "converted" / "questions.json"

CONFIGS = {
    "M1-dense":       ("dense", 3, 800, "Baseline: Day06 config C (chunk B + platform filter) via pgvector."),
    "M2-tfidf":       ("tfidf", 3, 800, "Lexical: exact menu/button words may beat embeddings."),
    "M3-hybrid":      ("hybrid", 3, 800, "RRF dense+tfidf: each fixes the other's misses."),
    "I1-hybrid-b2400": ("hybrid", 3, 2400, "Budget 800 fits ~1 chunk B (up to ~800 chars) → evidence at rank 2-3 is cut; 2400 keeps all 3."),
    "I2-hybrid-k5":   ("hybrid", 5, 4000, "More candidates (top-5) + budget for them catch evidence ranked 4-5."),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=("dev", "test"), required=True)
    ap.add_argument("--configs", nargs="*", default=list(CONFIGS))
    args = ap.parse_args()
    questions = [q for q in json.loads(QUESTIONS.read_text(encoding="utf-8")) if q["split"] == args.split]
    dense, lexical = DenseRetriever(), LexicalRetriever()
    retrievers = {"dense": dense, "tfidf": lexical, "hybrid": HybridRetriever(dense, lexical)}
    out_dir = ROOT / "starter" / "results" / f"retrieval-{args.split}"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {}
    for name in args.configs:
        method, top_k, budget, hypothesis = CONFIGS[name]
        traces = []
        for q in questions:
            start = time.perf_counter()
            results = retrievers[method].search(q["question"], filters=q.get("filter"), top_k=max(top_k, 3))
            ms = (time.perf_counter() - start) * 1000
            context, ids = pack_context(results[:top_k], budget=budget)
            marked = [{"id": c["id"], "page": c["page"], "score": c["score"], "hit": hit(c, q["gold"])} for c in results]
            traces.append({"query_id": q["id"], "question": q["question"], "filter": q.get("filter"),
                           "results": marked, "context_ids": ids, "context_chars": len(context), "ms": ms,
                           "hit1": bool(marked and marked[0]["hit"]),
                           "hit3": any(c["hit"] for c in marked[:3]),
                           "context_hit": any(c["hit"] and c["id"] in ids for c in marked)})
        n = len(traces)
        s = {"method": method, "top_k": top_k, "budget_chars": budget, "hypothesis": hypothesis, "N": n,
             "hit1": sum(t["hit1"] for t in traces), "hit3": sum(t["hit3"] for t in traces),
             "context_hit": sum(t["context_hit"] for t in traces),
             "avg_context_chars": round(statistics.mean(t["context_chars"] for t in traces)),
             "median_ms": round(statistics.median(t["ms"] for t in traces), 1), "cost_usd": 0,
             "misses_hit3": [t["query_id"] for t in traces if not t["hit3"]],
             "misses_context": [t["query_id"] for t in traces if not t["context_hit"]]}
        summary[name] = s
        (out_dir / f"{name}.traces.json").write_text(json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{name:16} Hit@1 {s['hit1']}/{n}  Hit@3 {s['hit3']}/{n}  Context {s['context_hit']}/{n}  "
              f"ctx {s['avg_context_chars']} chars  {s['median_ms']} ms  miss@3 {s['misses_hit3']}")
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
