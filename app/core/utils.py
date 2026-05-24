import re
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


# Cargar .txt
def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

#Leer .pdf
def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Limpiar texto
    text = re.sub(r"\s+\n\s+", "\n", text)
    text = re.sub(r"\n+", "\n", text)

    return text

def tokenize(text):
    return re.findall(r"\w+", text.lower()) # Mejora para BM25
    #return text.lower().split()


#Función chunk
def split_text(text: str,size=250,overlap=50,function=len) -> list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        length_function=function,
    )

    chunks = splitter.split_text(text)

    return chunks


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):
    return model.encode(text)