# Day 7 — Agentic RAG

**Bài cá nhân · Python 3.11+ · tiếp nối Day 6**

Dùng embedding và vector store từ Day 6 để xây một agent biết tìm bằng chứng, trả lời có nguồn và nhận biết khi không đủ thông tin. Bạn tự chọn kiến trúc, số tool và cách tổ chức retrieval.

> **Tùy chọn:** [Gợi ý dùng AI để lập trình](AGENT_SETUP.md) giúp bạn làm lab; phần này không bắt buộc và không tính điểm.

## Bài cần làm

![Agent tìm tài liệu trong kho Day 6 và trả lời có nguồn](assets/retrieval-pipeline.svg)

1. Kết nối dữ liệu, embedding và vector store Day 6.
2. Xây agent dùng model thật và ít nhất một khả năng truy xuất dữ liệu. Agent có thể dùng nhiều tool và nhiều lượt gọi.
3. Thử **ít nhất 3 phương pháp retrieval khác nhau**, trong đó có dense retrieval dùng vector store Day 6. Tự chọn các phương pháp còn lại; xem [gợi ý](GUIDE.md#2-thử-các-phương-pháp-retrieval).
4. Thử nhiều cấu hình, benchmark, phân tích lỗi và chọn cấu hình tốt trên **dev**; sau đó đánh giá trên **test**.

Benchmark tối thiểu có **24 câu**: dev gồm 15 câu có đáp án và 2 câu thiếu bằng chứng; test gồm 5 câu có đáp án và 2 câu thiếu bằng chứng. Xem [benchmark](BENCHMARK.md) và [rubric](RUBRIC.md).

## Thử thách nâng cao · +15 điểm

Index một tài liệu thực tế từ **100 trang** có bảng, ảnh và biểu đồ; xây agent truy xuất và trả lời các câu hỏi về nội dung đó. Hoàn thành [thử thách nâng cao](ADVANCED.md) và đạt **ít nhất 90% benchmark test** để nhận 15 điểm bonus. Phần cơ bản tối đa 85 điểm; toàn bài tối đa 100 điểm.

## Bắt đầu

1. Đọc [hướng dẫn](GUIDE.md), [rubric](RUBRIC.md) và [quy tắc](RULES.md).
2. Tạo repo cá nhân theo [cách nộp bài](SUBMISSION.md), chuẩn bị đầu ra Day 6 và model hỗ trợ tool calling.
3. Dùng hoặc thay thế [starter](starter/README.md); bạn cần kết nối model và vector store thật.
4. Chạy `python -m unittest discover -s tests -v`. Test mock chỉ kiểm tra code, không phải benchmark agent thật.

![Các bước thử nghiệm trên dev và đánh giá trên test](assets/experiment-loop.svg)

Nộp code, cách chạy, cấu hình, benchmark, trace và [báo cáo](report/individual/MSSV_HoTen.md). Thời gian ở [checkpoints](CHECKPOINTS.md) là gợi ý, có thể điều chỉnh theo lớp và phạm vi thử nghiệm.

---

## Bài làm — Đỗ Minh Hiếu (2A202603402)

Báo cáo: [report/individual/2A202603402_DoMinhHieu.md](report/individual/2A202603402_DoMinhHieu.md) · Phiếu chấm tay test: [report/grading_test.md](report/grading_test.md)

**Cấu hình chốt (I1):** hybrid RRF (pgvector dense + TF-IDF), top-k 3, context budget 2400 ký tự, tối đa 3 lượt tìm, DeepSeek `deepseek-chat`.

### Cần có
- Python 3.11+, Docker Desktop đang chạy, database pgvector của Day06 (`docker compose -p day6_student_starter start`, cổng 15433, bảng `chunks`, strategy `B`).
- `.env` ở gốc repo (không commit): `DATABASE_URL=postgresql://...@127.0.0.1:15433/day6_lab` và `DEEPSEEK_API_KEY=...`.
- Repo Day06 nằm cạnh repo này (để `src/export_day6.py` đọc `benchmark/questions.json`).

### Chạy (PowerShell, từ gốc repo)
```powershell
python -m venv C:\venvs\day07; C:\venvs\day07\Scripts\Activate.ps1
python -m pip install -r requirements.txt               # phiên bản đã dùng
$env:PYTHONUTF8 = "1"                                   # Windows: đọc/ghi UTF-8
python -m unittest discover -s tests -v                 # test mock của đề
python src/export_day6.py                               # 212 chunk B + 20 câu Day06 → starter/data/day6/
python starter/convert_day6.py --chunks starter/data/day6/chunks.json --questions starter/data/day6/questions.json --output starter/data/converted
python src/make_cases.py                                # benchmark/cases.json (24 câu, không gold)
python src/eval_retrieval.py --split dev                # 5 cấu hình retrieval trên dev
python src/run_agent_bench.py --split dev --method dense --budget 800 --name M1
python src/run_agent_bench.py --split dev --method hybrid --budget 2400 --name I1
python src/run_agent_bench.py --split dev --method hybrid --budget 2400 --first-query-original --partial-ok --name I3
# sau khi chốt I1:
python src/eval_retrieval.py --split test --configs M1-dense I1-hybrid-b2400
python src/run_agent_bench.py --split test --method dense --budget 800 --name M1
python src/run_agent_bench.py --split test --method hybrid --budget 2400 --name I1
python src/grades_to_reviews.py                         # report/grading_test.md → reviews.json
python starter/agent_metrics.py --cases benchmark/cases.json --traces starter/results/agent-test-I1/traces.json --reviews starter/results/agent-test-I1/reviews.json --split test --output starter/results/agent-test-I1/summary.json
```

### File
| File | Việc |
|---|---|
| `src/export_day6.py` | Đọc bảng pgvector Day06 + câu hỏi Day06 → JSON |
| `src/make_cases.py` | `benchmark/questions_all.json` (có gold) → `benchmark/cases.json` (không gold, cho agent) |
| `src/retrievers.py` | `DenseRetriever` (pgvector), `LexicalRetriever` (TF-IDF), `HybridRetriever` (RRF) |
| `src/eval_retrieval.py` | Hit@1, Evidence Hit@3, Context Evidence Rate theo cấu hình |
| `src/controller.py` | `LLMController.decide`: DeepSeek + tool `search` |
| `src/run_agent_bench.py` | Chạy `run_agent` trên từng câu, ghi trace + mẫu chấm |
| `src/grades_to_reviews.py` | Nhãn tay → `reviews.json` cho `agent_metrics.py` |

Kết quả nằm ở `starter/results/` (bị `.gitignore` chặn mặc định, đã thêm bằng `git add -f`). Dữ liệu sách: OpenStax, CC BY-NC-SA 4.0; `starter/data/` không push (tái tạo bằng lệnh trên).
