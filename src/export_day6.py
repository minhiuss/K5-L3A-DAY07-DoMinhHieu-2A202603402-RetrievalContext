import json
import os
from pathlib import Path
import psycopg
from dotenv import load_dotenv

DAY06 = Path("..") / "K5-L3A-Day06-DoMinhHieu-2A202603402-DataIngestionEngineering"
OUT = Path("starter/data/day6")

load_dotenv()
url = os.getenv("DATABASE_URL")
if not url:
    raise SystemExit("Thiếu DATABASE_URL trong .env")

with psycopg.connect(url) as conn:
    rows = conn.execute(
        """SELECT chunk_id, document_id, source, page, section, platform, text
           FROM chunks WHERE strategy = %s ORDER BY chunk_id""",
        ("B",),
    ).fetchall()

chunks = []
for chunk_id, document_id, source, page, section, platform, text in rows:
    chunks.append({
        "chunk_id": chunk_id,
        "document_id": document_id,
        "source": source,
        "page": page,
        "text": text,
        "metadata": {"section": section, "platform": platform},
    })

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "chunks.json").write_text(
    json.dumps(chunks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

data = json.loads((DAY06 / "benchmark" / "questions.json").read_text(encoding="utf-8"))
questions = data["questions"]
(OUT / "questions.json").write_text(
    json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"chunks: {len(chunks)} (kỳ vọng 212) · questions: {len(questions)} (kỳ vọng 20) → {OUT}")
