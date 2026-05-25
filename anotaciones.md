#

```
--------------------------------------------------

Ejecutando chat con parámetros específicos: 

🤖 RAG Chat iniciado. Escribe 'exit' o 'quit' para salir.

🧑 Tú: Quién es el autor del documento?

🤖 Bot:
 No tengo suficiente información para determinar quién es el autor del documento. El contexto proporcionado solo menciona el contenido del documento, pero no menciona el autor.

--------------------------------------------------

🧑 Tú: Quien es el director del documento?

🤖 Bot:
 El director del documento es Roberto Santana Hermida.

--------------------------------------------------
```

#
## Anotaciones de teoria

### chunks

Fragmentos de texto o de documente (como un array de arrays de texto) 

### chunk_overlap

Es la cantidad de texto que se repite entre chunks consecutivos, como asegurar que ninguna idea importante se parte por la mitad.

### Embeddings

Representación vectorial de los chunks

### Retrieving

Busqueda de los K chunks más relevantes, acaba siendo el input del LLM 

### BM25

Búsqueda léxica basada en frecuencia de términos. Más preciso para terminos como nobmres, titulos, etc.