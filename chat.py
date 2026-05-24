import sys
import json
from pathlib import Path

from app.core.utils import split_text, generate_embedding, load_pdf, tokenize, load_text
from sklearn.metrics.pairwise import cosine_similarity
from app.core.llm_service_groq import ask_llm

from rank_bm25 import BM25Okapi
import nltk
import numpy as np

# Leer json
def load_config(config_path: str):

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Leer db de documentación
def load_documents(data_dir):
    files = Path(data_dir).rglob("*")

    texts = []

    for file in files:
        if file.suffix == ".pdf":
            text = load_pdf(file)
        elif file.suffix in [".md", ".txt"]:
            text = load_text(file)
        else:
            continue

        # Por cada documento, un json con el origne y el texto
        texts.append({
            "source": str(file),
            "text": text
        })

    return texts


# def build_index(pdf_path, chunk_size, chunk_overlap):
#     text = load_documents(pdf_path)
#     chunks = split_text(text,chunk_size,chunk_overlap)
#     embeddings = generate_embedding(chunks)

#     return chunks, embeddings


def build_index(data_dir, chunk_size, chunk_overlap):
    docs = load_documents(data_dir)

    chunks = []
    sources = []

    for doc in docs:
        doc_chunks = split_text(doc["text"], chunk_size, chunk_overlap)

        for c in doc_chunks:
            chunks.append({
                "text": c,
                "source": doc["source"]
            })
            # A cada chunk, le asignamos el origen del documento
            sources.append(doc["source"])  
            # Estan alineados los chunks y los sources, la fuente del índice i de chunk,
            # corresponde al índice i de fuentes (sources).

    texts = [c["text"] for c in chunks]
    embeddings = generate_embedding(texts)

    return chunks, embeddings, sources


# Sin BM25
# def retrieve(question, chunks, embeddings, top_k=5):

#     question_embedding = generate_embedding(question)

#     similarities = cosine_similarity(
#         [question_embedding],
#         embeddings
#     )[0]

#     top_indices = similarities.argsort()[-top_k:][::-1]

#     return top_indices, similarities

# BM25
def build_bm25_index(chunks):

    tokenized_chunks = [
        tokenize(chunk["text"]) 
        for chunk in chunks
    ]


    bm25 = BM25Okapi(tokenized_chunks)

    return bm25, tokenized_chunks

# Retrieval hibrido -> embeddings + BM25
def retrieve(question, chunks, embeddings, bm25, top_k=5):

    # --- EMBEDDINGS ---
    q_emb = generate_embedding(question)

    sim = cosine_similarity([q_emb], embeddings)[0]
    emb_norm = (sim - sim.min()) / (sim.max() - sim.min() + 1e-8)

    # --- BM25 ---
    tokenized_query = tokenize(question)
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_norm = bm25_scores / (bm25_scores.max() + 1e-8)

    # --- COMBINACIÓN SIMPLE (UNION) ---
    final_scores = 0.7 * emb_norm + 0.3 * bm25_norm
    top_indices = final_scores.argsort()[-top_k:][::-1]

    results = [chunks[i] for i in top_indices]

    return results
# While true (infinito) del chat
def chat_loop(chunks, embeddings, bm25, sources, top_k):

    print("\n🤖 RAG Chat iniciado. Escribe 'exit' o 'quit' para salir.\n")

    while True:

        question = input("🧑 Tú: ")

        if question.lower() in ["exit", "quit"]:
            break

        top_indices = retrieve(question, chunks,embeddings, bm25, top_k)

        # context = "\n\n".join([chunks[i] for i in top_indices])
        context = "\n\n".join([
            f"SOURCE: {r['source']}\nCONTENT:\n{r['text']}"
            for r in top_indices
        ])

        answer = ask_llm(context, question)

        print("\n🤖 Bot:\n", answer)

        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":


    if len(sys.argv) < 2:
            print("")
            print(50*"-")
            print("")
            print("Ejecutando chat con parámetros por defecto: ")
            #chunks, embeddings = build_index("./data/PFG_Julen_Azpiroz.pdf",250, 50)
            chunks, embeddings = build_index("./data/docs/",250, 50)
            chat_loop(chunks, embeddings, 5)
    else: 

        print("")
        print(50*"-")
        print("")
        print("Ejecutando chat con parámetros específicos: ")

        config_path = sys.argv[1]
        config = load_config(config_path)
        db_path = config["data_dir"]
        chunk_size = config["chunk_size"]
        chunk_overlap = config["chunk_overlap"]
        
        chunks, embeddings, sources = build_index(db_path, chunk_size, chunk_overlap)

        bm25, tokenized_chunks = build_bm25_index(chunks)

        top_k_indices = config["top_k"]

        chat_loop(chunks, embeddings, bm25, sources, top_k_indices)