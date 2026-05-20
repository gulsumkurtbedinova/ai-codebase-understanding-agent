from app.ingestion.github_loader import clone_repository

from fastapi import FastAPI
from pydantic import BaseModel

from app.core.llm import client

from app.parsing.code_parser import load_code_files

from app.embeddings.embedder import store_documents

from app.agents.codebase_agent import ask_codebase

app = FastAPI()


class ChatRequest(BaseModel):
    message: str

class RepoRequest(BaseModel):
    repo_url: str

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "GitHub Code Agent is running"}


@app.post("/chat")
def chat(request: ChatRequest):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }

@app.post("/ingest")
def ingest_repository(request: RepoRequest):

    repo_path = clone_repository(request.repo_url)

    return {
        "status": "success",
        "repo_path": repo_path
    }


@app.get("/files")
def get_files():

    documents = load_code_files("repos/fastapi")

    return {
        "total_files": len(documents),
        "sample": documents[:3]
    }

@app.post("/index")
def index_repository():

    documents = load_code_files(
        "repos/fastapi"
    )

    store_documents(documents)

    return {
        "status": "indexed",
        "documents": len(documents)
    }


@app.post("/ask")
def ask_repository(request: QuestionRequest):

    answer = ask_codebase(
        request.question
    )

    return {
        "answer": answer
    }