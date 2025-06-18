# 🧠 RAG File Watcher + FastAPI Q&A (PDF/Text to Vector Store)

This project allows you to ask questions over your **local PDF or text files** using a local LLM via Ollama, FastAPI, and ChromaDB. Just drop your files into the `documents/` folder — they’ll be **automatically indexed**, and you can ask questions using a simple web or API interface.

## 📦 Features

- 📂 Monitors folder for `.pdf` and `.txt` files  
- ✂️ Splits documents into chunks (500 characters w/ overlap)  
- 🧠 Embeds with `all-MiniLM-L6-v2` using HuggingFace  
- 🧱 Stores embeddings in persistent ChromaDB  
- 🌐 Queries via FastAPI and local LLM (Ollama)  
- 💬 Chat UI integration using [chatbot-ui](https://github.com/mckaywrigley/chatbot-ui)

## 🗂️ Project Structure

## ⚙️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/rag-project.git
cd rag-project
```

### 2. Create a virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 🔌 Requirements

- Python 3.8+  
- [Ollama](https://ollama.com) installed locally  
- Models like `llama3` or any other supported local LLM

## 🚀 Run the App (Step-by-Step)

### ✅ Step 1: Start Ollama
```bash
ollama run llama3
```

### ✅ Step 2: Run the File Watcher
```bash
python watch_and_index.py
```

### ✅ Step 3: Run the FastAPI Server
```bash
uvicorn main:app --reload
```

### ✅ Step 4: Head over to frontend directory in your terminal and run:
```bash
npm install
npm run chat
```


---

🔗 [LinkedIn](https://www.linkedin.com/in/khalidalhabbash)
