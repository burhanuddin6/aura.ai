# 🧠 Multi-Modal Knowledge Graph Builder using LLMs

This project demonstrates the construction of a **Knowledge Graph** from **multi-modal data sources** like YouTube subtitles, Reddit threads, and official PDFs using **LLMs and embeddings**, with storage in a **Neo4j** graph database.

---

## 📦 Features

- Scrape and parse data from **YouTube**, **Reddit**, and **Web PDFs**
- Normalize and merge into unified **JSON format**
- Construct graph schema using **LLMs**
- Store graph data in **Neo4j** using **Cypher**
- Interface with frontend UI for chat and visualization

---

## 🚀 Project Structure

```
├── backend/         ← Python API to interface with the graph
├── common/          ← Shared utilities like LLMs and handlers
├── Data/            ← Contains scraped and merged data
├── frontend/        ← React + Tailwind frontend interface
├── graphrag/        ← Core KG builder pipeline, LLM graph builder, indexers
├── ipnyb_files/     ← Notebooks for experimentation
├── .env             ← Environment configuration
├── requirements.txt ← Python dependencies
```

---

## 🔧 Prerequisites

1. **Install Neo4j** and run on your local machine  
   👉 [Download Neo4j](https://neo4j.com/download/)

2. **Enable APOC Plugin (Awesome Procedures On Cypher)**  
   - Go to Neo4j Desktop → Plugins → Install APOC
   - Ensure it's enabled in `neo4j.conf`:
     ```
     dbms.security.procedures.unrestricted=apoc.*
     dbms.security.procedures.allowlist=apoc.*
     ```

3. **Configure Azure Keys**  
   - Set up your Azure environment
   - Place your keys in the `.env` file

---

## 📄 .env Configuration

```env
LLM_MODEL_NAME=deepseek-r1:7b
EMBEDDING_MODEL_NAME=nomic-embed-text
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=12345678
KG_BUILDER_LLM_MODEL_NAME=llama3.1:8b
KG_BUILDER_EMBEDDING_MODEL_NAME=nomic-embed-text
```

---

## 💾 Data Collection (Apple Vision Pro Example)

- **YouTube:** Subtitles downloaded as `.srt`, converted to `.json`
- **Reddit:** API bot fetches threads and comments
- **Documentation:** Scraper crawls and converts Apple VisionOS docs

Merged result: `Data/VisionPro/merged.json`

---

## ⚙️ How to Run

1. **Populating GraphDB Using Graph-Indexing**
   ```bash
   python graphrag/test_add_data.py
   ```

2. **Creating A Vector-Index On The Populated Nodes**
   ```bash
   python graphrag/create_vector_index.py
   ```

3. **Running The CLI Application**
   ```bash
   python3 -m streamlit run graphrag/graphrag.py
   ```

4. **Running Streamlit Application**
   ```bash
   python3 -m streamlit run app.py
   ```

