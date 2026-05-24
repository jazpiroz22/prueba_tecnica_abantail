from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(context: str, question: str):

    prompt = f"""
Eres un asistente RAG.

Responde SOLO usando el contexto proporcionado.

Si no está en el contexto, di "No hay información suficiente".

Siempre incluye la fuente en tu respuesta usando este formato:

- [SOURCE: nombre_del_documento]

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content