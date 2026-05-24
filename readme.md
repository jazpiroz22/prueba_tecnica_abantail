# RAG System — Julen Azpiroz

Este repositorio implementa un sistema de **Retrieval-Augmented Generation (RAG)** capaz de procesar documentos en formato `.pdf`, `.md` y `.txt`, y responder preguntas en lenguaje natural basándose exclusivamente en la información contenida en dichos documentos.

El sistema convierte los documentos en conocimiento consultable mediante técnicas de *chunking*, *embeddings* y *BM25*, y utiliza un modelo de lenguaje (LLM) para generar respuestas contextualizadas.

---

## Pipeline del sistema

El sistema sigue este Pipeline de proceso

```
Carga de documentos (.pdf, .md, .txt)
↓
Extracción de texto
↓
Chunking (segmentación del texto en fragmentos)
↓
Generación de embeddings (Sentence Transformers)
↓
Indexación BM25 (búsqueda léxica)
↓
Consulta del usuario
↓
Retrieval híbrido:
- Similitud semántica (embeddings)
- BM25 (búsqueda por términos)
↓
Fusión de resultados (score ponderado)
↓
Selección de top-k chunks relevantes
↓
Construcción del contexto
↓
Generación de respuesta con LLM
↓
Respuesta final con fuentes
```
## Como activarlo usando docker

## Ejecutar código nativo (Python + entorno virtual)


Para ejecutar el proyecto de forma local, se recomienda utilizar un entorno virtual de Python (`venv`) para aislar las dependencias del sistema principal.

### 1. Crear entorno virtual

Ejecutar el siguiente comando desde la raíz del proyecto:

```bash
python3 -m venv venv
```

### 2. Activar entorno virtual

Una vez creado, activar el entorno virtual:

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

Todas las dependencias necesarias se encuentran definidas en el archivo requirements.txt.

Instalarlas mediante:
```bash
pip install -r requirements.txt
```
### 4. Ejecutar el sistema

Para iniciar el sistema RAG en modo chat:

```bash
python3 chat.py config.json
```

El archivo `config.json` es OPCIONAL, se puede ejecutar el código con una serie de parametros por defecto, pero si el usuario desea cambiar ciertos parametros puede hacerlo modificando los valores de `config.json`

Los parametros son los siguientes:

- data_dir: Directorio que contiene los documentos que utilizará el sistema como base de conocimiento. En dichi directorio se pueden introducir archivos `.pdf`, `.md` y `.txt`.
- top_k: Número de chunks más relevantes recuperados durante el retrieval y enviados al LLM.
- chunk_size: Tamaño máximo (en caracteres) de cada chunk generado durante el proceso de segmentación.
- chunk_overlap: El número de caracteres del chunk_overlap (Es la cantidad de texto que se repite entre chunks consecutivos, como asegurar que ninguna idea importante se parte por la mitad.)


### Instalar modelo Ollama3.1:8b
```
curl -fsSL https://ollama.com/install.sh | sh
```


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

