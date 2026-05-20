# %%

import sys
print(sys.executable)

from pypdf import PdfReader
from app.core.chunk import split_text

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()




def load_pdf(path: str) -> str:
    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


text = load_text("./data/test.txt")
print(text)
# %%

pdf = load_pdf("./data/PFG_Julen_Azpiroz.pdf")
chunks = split_text(pdf)

print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i} ---\n")
    print(chunk)

# %%
print(pdf)
# %%
