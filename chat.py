import sys
import json

from app.core.utils import split_text, generate_embedding, load_pdf, build_bm25_index, tokenize
from sklearn.metrics.pairwise import cosine_similarity
from app.core.llm_service_groq import ask_llm

from rank_bm25 import BM25Okapi
import nltk
import numpy as np


def load_config(config_path: str):

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_index(pdf_path, chunk_size, chunk_overlap):
    text = load_pdf(pdf_path)
    chunks = split_text(text,chunk_size,chunk_overlap)
    embeddings = generate_embedding(chunks)

    return chunks, embeddings

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

    tokenized_chunks = [tokenize(c) for c in chunks]

    bm25 = BM25Okapi(tokenized_chunks)

    return bm25, tokenized_chunks

# Retrieval hibrido -> embeddings + BM25
def retrieve(question, embeddings, bm25, top_k=5):

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
    #final_indices = list(set(top_emb) | set(top_bm25))

    return top_indices

# While true (infinito) del chat
def chat_loop(chunks, embeddings, bm25, top_k):

    print("\n🤖 RAG Chat iniciado. Escribe 'exit' o 'quit' para salir.\n")

    while True:

        question = input("🧑 Tú: ")

        if question.lower() in ["exit", "quit"]:
            break

        top_indices = retrieve(question, embeddings, bm25, top_k)

        context = "\n\n".join([chunks[i] for i in top_indices])

        answer = ask_llm(context, question)

        print("\n🤖 Bot:\n", answer)

        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":


    if len(sys.argv) < 2:
            print("")
            print(50*"-")
            print("")
            print("Ejecutando chat con parámetros por defecto: ")
            chunks, embeddings = build_index("./data/PFG_Julen_Azpiroz.pdf",250, 50)

            chat_loop(chunks, embeddings, 5)
    else: 

        print("")
        print(50*"-")
        print("")
        print("Ejecutando chat con parámetros específicos: ")

        config_path = sys.argv[1]
        config = load_config(config_path)
        pdf_path = config["pdf_path"]
        chunk_size = config["chunk_size"]
        chunk_overlap = config["chunk_overlap"]
        
        chunks, embeddings = build_index(pdf_path, chunk_size, chunk_overlap)

        bm25, tokenized_chunks = build_bm25_index(chunks)

        top_k_indices = config["top_k"]

        chat_loop(chunks, embeddings, bm25, top_k_indices)