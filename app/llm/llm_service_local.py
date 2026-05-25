import ollama

def ask_llm_local(context: str, question: str,name: str):

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

    response = ollama.chat(
        model=name,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]