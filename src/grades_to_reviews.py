import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "report" / "grading_test.md").read_text(encoding="utf-8")
blocks = re.split(r"^### ", text, flags=re.M)[1:]
reviews: dict[str, list] = {}
for b in blocks:
    name, qid = re.match(r"(\w+) · (q\d+)", b).groups()
    line = re.search(r"\*\*Chấm:\*\*(.*)", b).group(1)
    ticks = re.findall(r"`([^`]*)`", line)
    reason = line.split("lý do:", 1)[1].strip()
    if "abstain" in line:
        r = {"query_id": qid, "abstention_correct": ticks[0].upper() == "D", "citation_support": []}
    else:
        cites = [] if "không có" in ticks[2] else [t.upper() == "D" for t in ticks[2].split()]
        r = {"query_id": qid, "context_grade": int(ticks[0]), "answer_grade": int(ticks[1]), "citation_support": cites}
    r["reason"] = reason
    reviews.setdefault(name, []).append(r)
for name, rows in reviews.items():
    out = ROOT / "starter" / "results" / f"agent-test-{name}" / "reviews.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(name, len(rows), "reviews →", out.relative_to(ROOT))
