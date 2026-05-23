from app.core.utils import split_text, generate_embedding, load_pdf
from sklearn.metrics.pairwise import cosine_similarity
from app.core.llm_service_groq import ask_llm


def build_index(pdf_path):
    text = load_pdf(pdf_path)
    chunks = split_text(text,size=250,overlap=50)
    embeddings = generate_embedding(chunks)

    return chunks, embeddings

def retrieve(question, chunks, embeddings, top_k=5):

    question_embedding = generate_embedding(question)

    similarities = cosine_similarity(
        [question_embedding],
        embeddings
    )[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    return top_indices, similarities


def chat_loop(chunks, embeddings):

    print("\n🤖 RAG Chat iniciado. Escribe 'exit' o 'quit' para salir.\n")

    while True:

        question = input("🧑 Tú: ")

        if question.lower() in ["exit", "quit"]:
            break

        top_indices, similarities = retrieve(question, chunks, embeddings)

        context = "\n\n".join([chunks[i] for i in top_indices])

        answer = ask_llm(context, question)

        print("\n🤖 Bot:\n", answer)

        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":


    chunks, embeddings = build_index("./data/PFG_Julen_Azpiroz.pdf")

    chat_loop(chunks, embeddings)