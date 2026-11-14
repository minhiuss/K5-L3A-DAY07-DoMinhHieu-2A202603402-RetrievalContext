import json
from pathlib import Path

data = json.loads(Path("benchmark/questions_all.json").read_text(encoding="utf-8"))
cases = []
for q in data["questions"]:
    answerable = q.get("answerable", True)
    cases.append({"id": q["id"], "split": q["split"], "question": q["question"],
                  "filter": q.get("filter"), "answerable": answerable,
                  "expected_behavior": "search_and_answer" if answerable else "search_and_abstain"})
Path("benchmark/cases.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for split in ("dev", "test"):
    rows = [c for c in cases if c["split"] == split]
    print(split, len(rows), "câu,", sum(not c["answerable"] for c in rows), "thiếu bằng chứng")
