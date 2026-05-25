#%%

from pypdf import PdfReader
from app.core.chunk import split_text
from app.core.embedding_service import generate_embedding
from app.llm.llm_service_groq import ask_llm
from sklearn.metrics.pairwise import cosine_similarity

from app.core.utils import split_text, load_pdf

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# %%


text = load_text("./data/test.txt")
print(text)

pdf = load_pdf("./data/PFG_Julen_Azpiroz.pdf")
chunks = split_text(pdf)

print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:5]):
    print(f"\n--- Chunk {i} ---\n")
    print(chunk)
    
# %%

# EMBEDDING

embeddings = generate_embedding(chunks)

print("len de embeddings: "+str(len(embeddings)))
print("len de embeddings[0]: "+str(len(embeddings[0])))
print("len de embeddings[100]: "+str(len(embeddings[100])))
print("len de embeddings[200]: "+str(len(embeddings[200])))

# %%

# RETRIEVAL

question1 = load_text("./data/pregunta1.txt") # Que redes conoce
question2 = load_text("./data/pregunta2.txt") # Cuales se analizan en el documento
question3 = load_text("./data/pregunta3.txt") # Qué modelos se analizaron
question1_embedding = generate_embedding(question1)
question2_embedding = generate_embedding(question2)
question3_embedding = generate_embedding(question3)

similarities = cosine_similarity(
    [question3_embedding],
    embeddings
)[0]

print("similarities: " +str(similarities))

top_k = 5 #

top_indices = similarities.argsort()[-top_k:][::-1]

for idx in top_indices:
    print("\n====================")
    print(f"Chunk index: {idx}")
    print(f"Similarity: {similarities[idx]}")
    print("====================")
    print(chunks[idx])

# %%

#####################################

# LLM -> OPEN-AI

context = "\n\n".join([chunks[idx] for idx in top_indices])
response = ask_llm(context, question3)

print(response)

# %%
