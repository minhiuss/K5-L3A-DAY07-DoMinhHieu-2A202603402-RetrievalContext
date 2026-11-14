# Phiếu chấm tay — test (M1 baseline, I1 đã chốt)

Đọc từng câu, điền vào các ô `__`. Thang điểm (BENCHMARK.md):
- **context** (chỉ câu có đáp án): 0 = context không có evidence · 1 = có nhưng thiếu điều kiện/nguồn · 2 = đủ evidence và nguồn.
- **answer** (chỉ câu có đáp án): 0 = sai / thiếu evidence / từ chối · 1 = đúng một phần · 2 = đúng và đủ.
- **citations**: mỗi citation ghi `Đ` (nguồn thật sự hỗ trợ câu trả lời) hoặc `S`, theo thứ tự.
- **abstain** (chỉ câu thiếu bằng chứng): `Đ` nếu agent thật sự từ chối, không bịa; `S` nếu không.
- **lý do**: 1 câu ngắn, bắt buộc.

Gợi ý nhanh: so câu trả lời với *Đáp án chuẩn*, rồi đọc đoạn trích của từng citation xem có nói đúng điều đó không.

## M1  (dense, top_k 3, budget 800)

### M1 · q16 — có đáp án
- **Câu hỏi:** In Google Docs, how do you turn on the mode that records each collaborator's edits?
- **Đáp án chuẩn:** Open the Editing drop-down menu at the top right of the window and choose Suggesting.
- **Evidence chuẩn (trang 203):** "To turn on Suggesting mode, go to the top right of the Docs window and look for the drop-down menu that says Editing."
- **Lượt tìm:** `Google Docs suggest edits mode track changes`; `enable Suggesting mode Google Docs toolbar`; `how to switch to Suggesting mode Google Docs Editing button` → context: B:204:3.8:0, B:203:3.8:0
- **Agent:** `abstain` — Không đủ bằng chứng để trả lời.
- **Chấm:** context `0` · answer `0` · citations `(không có)` · lý do: agent trich dung vi tri page nhung sai chunk va khong tra loi

### M1 · q17 — có đáp án
- **Câu hỏi:** If I make a copy of an older version of a Doc, do its comments and history come with it?
- **Đáp án chuẩn:** No. The copy is a new Doc without the version history, and comments and suggestions are not copied.
- **Evidence chuẩn (trang 212):** "When a copy is made of any version of a document, it is saved as a new Doc, without the version history attached to it. The comments and suggestions are also not copied."
- **Lượt tìm:** `make a copy of a document comments and version history` → context: B:212:3.9:1
- **Agent:** `answered` — No — when a copy is made of any version of a document, it is saved as a new Doc without the version history attached, and the comments and suggestions are also not copied [B:212:3.9:1].
  - `[B:212:3.9:1]` (trang 212): "Having copies of the same file, but as different versions, is an option if you want to download these versions to your business's computer desktop or hard drive, instead of keeping them online. Having a different version can also be useful if you want to send this version to a client or any third party. When a copy is made of any version of a document, it is saved as a new Doc, without the version history attached to it. The comments and suggestions are also not copied.…"
- **Chấm:** context `2` · answer `2` · citations `D` · lý do: agent tim chinh xac vi tri page va trich dan dung paragraph chua thong tin

### M1 · q18 — có đáp án
- **Câu hỏi:** With desktop Word, how many earlier versions of a file can I open, and what is required?
- **Đáp án chuẩn:** The last 25 versions, but only if the file is stored on OneDrive (and you are signed in to your Microsoft account).
- **Evidence chuẩn (trang 215):** "You will be able to access the last 25 versions of your file on OneDrive (that is, if your file is stored on OneDrive)"
- **Lượt tìm:** `Word open earlier versions of a file version history` → context: B:215:3.9:0
- **Agent:** `answered` — You can access the last 25 versions of your file, provided you sign in to your Microsoft account and the file is stored on OneDrive [B:215:3.9:0].
  - `[B:215:3.9:0]` (trang 215): "Figure 3.73 The version history in Microsoft Word desktop is activated if the document is located in OneDrive. (Used with permission from Microsoft) If you have a desktop version of Word, you have to sign in to your Microsoft account. You will be able to access the last 25 versions of your file on OneDrive (that is, if your file is stored on OneDrive), as you can see in Figure 3.74. 3.9 • Versions and Version History 205…"
- **Chấm:** context `2` · answer `2` · citations `D` · lý do: agent tim chinh xac vi tri page va trich dan dung paragraph chua thong tin


### M1 · q19 — có đáp án
- **Câu hỏi:** Why can wider line spacing help when several people are reviewing a draft?
- **Đáp án chuẩn:** Double-spacing gives better visibility of the edits and makes revisions in progress easier to see.
- **Evidence chuẩn (trang 163):** "This allows for better visibility for the changes or edits, and makes it easier to see the revisions in progress."
- **Lượt tìm:** `wider line spacing multiple reviewers draft comments`; `line spacing room for handwritten comments reviewers`; `line spacing reviewers edit draft easier to read` → context: B:164:3.3:0, B:205:3.8:0, B:190:3.7:0
- **Agent:** `abstain` — Không đủ bằng chứng để trả lời.
- **Chấm:** context `0` · answer `0` · citations `(không có)` · lý do: agent khong tim dung chunk, khong tra loi 

### M1 · q20 — có đáp án
- **Câu hỏi:** In Microsoft Word, where do you go to adjust the margins of a page?
- **Đáp án chuẩn:** The Layout tab, then the Margins icon.
- **Evidence chuẩn (trang 155):** "To adjust the margins of a page, go to the Layout tab."
- **Lượt tìm:** `Word adjust page margins Layout tab Margins` → context: B:153:3.2:3
- **Agent:** `answered` — The Layout tab contains the Page Setup command group, where you can adjust margins (along with paper size and orientation) [B:153:3.2:3].
  - `[B:153:3.2:3]` (trang 153): "The Layout tab contains commands and tools for adjusting the overall page setup of your document, located within the Page Setup command group. Page setup typically includes adjusting the paper size, margins, and orientation, as well as adding features like section breaks and columns. There are accepted standards for 3.2 • Formatting Document Layout in Microsoft Word 143…"
- **Chấm:** context `1` · answer `1` · citations `D` · lý do: context chuan nam o trang 155 va describe closest answer cho cau hoi. agent tra loi dung mot phan

### M1 · q21 — THIẾU BẰNG CHỨNG
- **Câu hỏi:** Can a user export only the images embedded in a document?
- **Vì sao thiếu:** Searched extracted text of PDF p.148-218 for 'export', 'extract', 'save image': 0 hits. Images are only inserted/formatted, never exported. Written by the student.
- **Lượt tìm:** `export only images embedded in document` → context: B:167:3.3:3, B:153:3.1:0
- **Agent:** `abstain` — Không đủ bằng chứng để trả lời.
- **Chấm:** abstain `D` · citations `(không có)` · lý do: pdf khong chua phan nao noi ve extract only images -> agent khong tra loi la dung

### M1 · q22 — THIẾU BẰNG CHỨNG
- **Câu hỏi:** Can I keep editing a Google Doc while offline, without internet?
- **Vì sao thiếu:** Book only says Docs autosaves 'as long as you are connected to the internet' (p.207); 'offline' has 0 hits. Near-topic trap: answer would be a guess.
- **Lượt tìm:** `Google Docs offline editing`; `Google Docs offline mode enable edit without internet` → context: B:198:3.8:0
- **Agent:** `abstain` — Không đủ bằng chứng để trả lời.
- **Chấm:** abstain `D` · citations `(không có)` · lý do: pdf khong co muc ve offline, agent tu choi, khong doan

## I1  (hybrid, top_k 3, budget 2400)

### I1 · q16 — có đáp án
- **Câu hỏi:** In Google Docs, how do you turn on the mode that records each collaborator's edits?
- **Đáp án chuẩn:** Open the Editing drop-down menu at the top right of the window and choose Suggesting.
- **Evidence chuẩn (trang 203):** "To turn on Suggesting mode, go to the top right of the Docs window and look for the drop-down menu that says Editing."
- **Lượt tìm:** `Google Docs suggestion mode track edits` → context: B:204:3.8:0, B:203:3.8:1, B:203:3.8:2
- **Agent:** `answered` — Go to the top right of the Docs window, click the drop-down menu that says Editing, and select Suggesting [B:203:3.8:1]. In this mode, added text is bracketed, deleted text gets a strikethrough, and each change has a comment box with a check or cross to accept or reject [B:203:3.8:1].
  - `[B:203:3.8:1]` (trang 203): "When you share the market trends report with your colleagues for their input, you need to make sure that everyone's individual edits are captured in a clear way, similar to Track Changes in Word. The way to do this is through Suggesting mode, as the chapter on Essentials of Software Applications for Business introduced. To turn on Suggesting mode, go to the top right of the Docs window and look for the drop-down menu that says Editing. As you click on it, select Suggesting, as Figure 3.62 shows.…"
- **Chấm:** context `2` · answer `2` · citations `D` · lý do: agent trich dung va tra loi dung

### I1 · q17 — có đáp án
- **Câu hỏi:** If I make a copy of an older version of a Doc, do its comments and history come with it?
- **Đáp án chuẩn:** No. The copy is a new Doc without the version history, and comments and suggestions are not copied.
- **Evidence chuẩn (trang 212):** "When a copy is made of any version of a document, it is saved as a new Doc, without the version history attached to it. The comments and suggestions are also not copied."
- **Lượt tìm:** `make a copy of a document comments and version history` → context: B:212:3.9:1, B:211:3.9:2, B:216:3.9:1
- **Agent:** `answered` — No — when a copy is made of any version of a document, it is saved as a new Doc without the version history attached, and the comments and suggestions are also not copied [B:212:3.9:1].
  - `[B:212:3.9:1]` (trang 212): "Having copies of the same file, but as different versions, is an option if you want to download these versions to your business's computer desktop or hard drive, instead of keeping them online. Having a different version can also be useful if you want to send this version to a client or any third party. When a copy is made of any version of a document, it is saved as a new Doc, without the version history attached to it. The comments and suggestions are also not copied.…"
- **Chấm:** context `2` · answer `2` · citations `D` · lý do: chunk p212 chua nguyen cau evidence, tra loi du 2 y 

### I1 · q18 — có đáp án
- **Câu hỏi:** With desktop Word, how many earlier versions of a file can I open, and what is required?
- **Đáp án chuẩn:** The last 25 versions, but only if the file is stored on OneDrive (and you are signed in to your Microsoft account).
- **Evidence chuẩn (trang 215):** "You will be able to access the last 25 versions of your file on OneDrive (that is, if your file is stored on OneDrive)"
- **Lượt tìm:** `Word open earlier versions of a file version history` → context: B:216:3.9:1, B:215:3.9:0, B:216:3.9:0
- **Agent:** `answered` — With desktop Word, you must sign in to your Microsoft account and store the file on OneDrive, which lets you access the last 25 versions of your file [B:215:3.9:0].
  - `[B:215:3.9:0]` (trang 215): "Figure 3.73 The version history in Microsoft Word desktop is activated if the document is located in OneDrive. (Used with permission from Microsoft) If you have a desktop version of Word, you have to sign in to your Microsoft account. You will be able to access the last 25 versions of your file on OneDrive (that is, if your file is stored on OneDrive), as you can see in Figure 3.74. 3.9 • Versions and Version History 205…"
- **Chấm:** context `2` · answer `2` · citations `D` · lý do: chunk p215 co 25 versions va dieu kien OneDrive, tra loi du dieu kien

### I1 · q19 — có đáp án
- **Câu hỏi:** Why can wider line spacing help when several people are reviewing a draft?
- **Đáp án chuẩn:** Double-spacing gives better visibility of the edits and makes revisions in progress easier to see.
- **Evidence chuẩn (trang 163):** "This allows for better visibility for the changes or edits, and makes it easier to see the revisions in progress."
- **Lượt tìm:** `wider line spacing reviewers comments draft`; `wider line spacing reviewers comments draft multiple people` → context: B:156:3.2:1, B:190:3.7:0, B:157:3.2:0
- **Agent:** `abstain` — Không đủ bằng chứng để trả lời.
- **Chấm:** context `0` · answer `0` · citations `(không có)` · lý do: query viet lai khong ra chunk p163, context khong co evidence, agent tu choi

### I1 · q20 — có đáp án
- **Câu hỏi:** In Microsoft Word, where do you go to adjust the margins of a page?
- **Đáp án chuẩn:** The Layout tab, then the Margins icon.
- **Evidence chuẩn (trang 155):** "To adjust the margins of a page, go to the Layout tab."
- **Lượt tìm:** `Word adjust page margins Layout tab Margins` → context: B:155:3.2:0, B:153:3.2:2, B:153:3.2:3
- **Agent:** `answered` — Go to the Layout tab, select the Margins icon, and choose from the drop-down menu (or choose Custom Margins at the bottom to set your own) [B:155:3.2:0].
  - `[B:155:3.2:0]` (trang 155): "You may encounter projects that need different margins on different pages, or unconventional margins—that is, custom margins. To adjust the margins of a page, go to the Layout tab. Select the Margins icon, and a drop-down menu will appear. The default margin is Normal (1 inch on all sides), but this can be adjusted via the prepopulated options, such as for different layouts with narrower margins. If you want to set your own margins, choose the Custom Margins option at the bottom of the drop-down…"
- **Chấm:** context `2` · answer `2` · citations `D` · lý do: chunk p155 dung evidence, tra loi Layout tab va margins icon

### I1 · q21 — THIẾU BẰNG CHỨNG
- **Câu hỏi:** Can a user export only the images embedded in a document?
- **Vì sao thiếu:** Searched extracted text of PDF p.148-218 for 'export', 'extract', 'save image': 0 hits. Images are only inserted/formatted, never exported. Written by the student.
- **Lượt tìm:** `export only images embedded in document` → context: B:153:3.1:0, B:180:3.5:0, B:174:3.4:1
- **Agent:** `abstain` — Không đủ bằng chứng để trả lời.
- **Chấm:** abstain `D` · citations `(không có)` · lý do: pdf khong noi ve export anh, agent tu choi, khong doan

### I1 · q22 — THIẾU BẰNG CHỨNG
- **Câu hỏi:** Can I keep editing a Google Doc while offline, without internet?
- **Vì sao thiếu:** Book only says Docs autosaves 'as long as you are connected to the internet' (p.207); 'offline' has 0 hits. Near-topic trap: answer would be a guess.
- **Lượt tìm:** `Google Docs offline editing` → context: B:198:3.8:0, B:184:3.6:2, B:181:3.6:1
- **Agent:** `abstain` — Không đủ bằng chứng để trả lời.
- **Chấm:** abstain `D` · citations `(không có)` · lý do: pdf khong co offline, agent tu choi, khong doan

