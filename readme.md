# RAG System — Julen Azpiroz

Este repositorio implementa un sistema de **Retrieval-Augmented Generation (RAG)** capaz de procesar documentos en formato `.pdf`, `.md` y `.txt`, y responder preguntas en lenguaje natural basándose exclusivamente en la información contenida en dichos documentos.

El sistema convierte los documentos en conocimiento consultable mediante técnicas de *chunking*, *embeddings*, *BM25* y *retrievals*; utiliza un modelo de lenguaje (LLM) para generar respuestas contextualizadas.

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

## Ejecución con Docker

### 1. Construir imagen

```bash
docker build -t rag-chat .
```

Para poder ejecutar el contendero, primero hay que modificar el arhivo `venv`, como se especifica más abajo, una vez configurado correctamente, ejecutar:

### 2. Ejecutar contenedor
```bash
docker run -it --env-file .env rag-chat
```

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
python3 -m app.main config.json
```

El archivo `config.json` es OPCIONAL, se puede ejecutar el código con una serie de parametros por defecto, pero si el usuario desea cambiar ciertos parametros puede hacerlo modificando los valores de `config.json`

Los parametros son los siguientes:

- data_dir: Directorio que contiene los documentos que utilizará el sistema como base de conocimiento. En dichi directorio se pueden introducir archivos `.pdf`, `.md` y `.txt`.
- top_k: Número de chunks más relevantes recuperados durante el retrieval y enviados al LLM.
- chunk_size: Tamaño máximo (en caracteres) de cada chunk generado durante el proceso de segmentación.
- chunk_overlap: El número de caracteres del chunk_overlap (Es la cantidad de texto que se repite entre chunks consecutivos, como asegurar que ninguna idea importante se parte por la mitad.)
- llm_mode: Especificar si se pretende utilizar un LLM local, o un LLM online, los valores son:  `online` o `local`. Para utilizar adecuadamente cada uno de ellos, seguid las instrucciones detalladas en este fichero `readme.md`
- online_model: Nombre del modelo online a utilizar, por defecto esta etablecido: `llama-3.1-8b-instant`, se recomienda no cambiar este parámetro.
- local_model: Nombre del modelo local a utilizar, por defecto esta etablecido: `llama3.1:8b`.

### Obtener la API key

Lo único que habrá que hacer para poder utilizar el modelo Groq de forma online, es obtener una API key, y escribirla en el fichero `.env_example`.
Primero hay que dirigirse a la página: https://console.groq.com/home, loggearse (se puede hacer con email personal), una vez logeado, clickar en donde pone `API KEYS` arriba a la derecha, clicar en `Create API Key`, insertar un nombre cualquiera, avanzar, y el contenido que se genera copiarlo y pegar en el fichero `.env_example` donde poner `GROQ_API_KEY`.

Despues creamos el archivo `.env` como copia de `.env_example` o, renombramos `.env_example` a `.env`.
```bash
cp .env.example .env
```
Por último, asegurarse de que el parametro del `config.json` "llm_mode" esté marcado con "online".


## Uso con modelos locales (Ollama)

Para ejecutar el RAG a traves de un LLM local, primero se habrá de instalar la librería ollama:

```bash
sudo snap install ollama
```

Despues, habrá que descargar el modelo, este proceso descarga un modelo de 4.9Gb de peso. Se recomienda usar conexión ethernet si se procede con este procedimiento.

```bash
ollama pull llama3.1:8b
```

Asegurarse de que está correctamente descargado:
```bash
ollama list
```

Debería aparecer algo así como:
```
NAME           ID              SIZE      MODIFIED
llama3.1:8b    46e0c10c039e    4.9 GB    18 minutes ago
```

Por último, asegurarse de que el parametro del `config.json` "llm_mode" esté marcado con "local". Este modelo tardá algo más de tiempo con respecto al modelo online.