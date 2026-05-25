from app.llm.llm_service_groq import ask_llm_groq
from app.llm.llm_service_local import ask_llm_local

def get_llm(llm_mode):

    if llm_mode == "online":
        return ask_llm_groq

    elif llm_mode == "local":
        return ask_llm_local

    else:
        raise ValueError(f"Modo LLM no soportado: {llm_mode}")