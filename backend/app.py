from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel
import requests

embeddings_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./watched_documents/chroma_db", embedding_function = embeddings_model)

retriever = vectorstore.as_retriever()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryResponse(BaseModel):
    question: str

    @app.post("/ask")
    def generate_response(request: QueryResponse):
        question = request.question
        # Fetch relevant docs
        relevant_docs = retriever.get_relevant_documents(question)

        context = "\n\n".join(doc.page_content for doc in relevant_docs)

        # Create prompt
        prompt = f"""Use the following context to answer the question.

            Context:
            {context}

            Question: {question}
            Answer:"""

        try:
            # Call locally hosted ollama model with prompt
            res = requests.post("http://localhost:11434/api/generate", json= {
                "model": "mistral",
                "prompt": prompt,
                "stream": false
            })

            # Raise request to check for exceptions
            res.raise_for_status()
            answer = res.json()["response"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ollama call failed: {str(e)}")

        # Return model response as JSON
        return {"answer": answer}

    