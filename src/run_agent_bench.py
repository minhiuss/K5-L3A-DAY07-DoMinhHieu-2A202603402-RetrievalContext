import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "starter"))
from agentic import run_agent
from controller import LLMController
from retrievers import build


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=("dev", "test"), required=True)
    ap.add_argument("--method", choices=("dense", "tfidf", "hybrid"), default="hybrid")
    ap.add_argument("--top-k", type=int, default=3)
    ap.add_argument("--budget", type=int, default=2400)
    ap.add_argument("--max-searches", type=int, default=3)
    ap.add_argument("--name", default=None, help="results folder suffix; default = method")
    ap.add_argument("--first-query-original", action="store_true", help="I3: lượt 1 tìm bằng câu hỏi gốc")
    ap.add_argument("--partial-ok", action="store_true", help="I3: giữ câu trả lời một phần có citation")
    ap.add_argument("--ids", nargs="*", help="only run these query ids")
    args = ap.parse_args()

    cases = [c for c in json.loads((ROOT / "benchmark" / "cases.json").read_text(encoding="utf-8"))
             if c["split"] == args.split and (not args.ids or c["id"] in args.ids)]
    retriever = build(args.method)
    controller = LLMController(first_query_original=args.first_query_original, partial_ok=args.partial_ok)
    config = {"method": args.method, "top_k": args.top_k, "budget_chars": args.budget,
              "max_searches": args.max_searches, "model": controller.model,
              "first_query_original": args.first_query_original, "partial_ok": args.partial_ok}
    traces = []
    for c in cases:
        controller.reset()
        start = time.perf_counter()
        try:
            r = run_agent(c["question"], controller, retriever, filters=c.get("filter"),
                          max_searches=args.max_searches, top_k=args.top_k, budget=args.budget)
            status, error = r["status"], None
        except Exception as exc:
            r, status, error = {"answer": None, "citations": [], "events": []}, "error", f"{type(exc).__name__}: {exc}"
        t = {"query_id": c["id"], "split": c["split"], "answerable": c["answerable"], "question": c["question"],
             "filter": c.get("filter"), "status": status, "answer": r["answer"], "citations": r["citations"],
             "events": r["events"], "model_raw": controller.raw, "llm_calls": controller.calls,
             "searches": sum(e.get("event") == "search" for e in r["events"]),
             "tokens_in": controller.tokens_in, "tokens_out": controller.tokens_out,
             "cost_usd": round(controller.cost_usd(), 6), "seconds": round(time.perf_counter() - start, 2),
             "error": error, "config": config}
        traces.append(t)
        print(f"{c['id']:4} {status:8} searches={t['searches']} cites={t['citations']}  {(r['answer'] or error or '')[:90]}")

    out = ROOT / "starter" / "results" / f"agent-{args.split}-{args.name or args.method}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "traces.json").write_text(json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    template = [{"query_id": t["query_id"], "answer_grade": None if t["answerable"] else None,
                 "citation_support": [None] * len(t["citations"]),
                 **({} if t["answerable"] else {"abstention_correct": None}), "note": ""}
                for t in traces if t["status"] != "error"]
    (out / "reviews_template.json").write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ok = [t for t in traces if t["status"] != "error"]
    print(f"→ {out}  |  {len(ok)}/{len(traces)} ran  |  cost ${sum(t['cost_usd'] for t in traces):.4f}  |  "
          f"answered {sum(t['status'] == 'answered' for t in ok)}, abstain {sum(t['status'] == 'abstain' for t in ok)}")


if __name__ == "__main__":
    main()
