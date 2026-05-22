```
Documento
   ↓
Extracción texto
   ↓
Chunking
```

# Proximos pasos:

## embeddings + retrieval + LLM


```
Pregunta usuario
↓
Embedding pregunta
↓
Similarity search
↓
Top chunks
↓
Prompt al LLM
↓
Respuesta final
```

## Objetivos:

### Parametrizar función chunk.py -> split_text()

## Notas:

### Activar entorno virtual

```
python -m venv venv 
source venv/bin/activate
```


### Instalar modelo Ollama3.1:8b
```
curl -fsSL https://ollama.com/install.sh | sh
```


### Teoria
```
¿Qué es chunk_overlap?

Es la cantidad de texto que se repite entre chunks consecutivos, como asegurar que ninguna idea importante se parte por la mitad.
```