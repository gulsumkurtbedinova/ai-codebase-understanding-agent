import os

from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

import chromadb


load_dotenv()


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="codebase"
)


def store_documents(documents):

    for i, doc in enumerate(documents):

        embedding = embedding_model.embed_query(
            doc["content"][:8000]
        )

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[doc["content"]],
            metadatas=[
                {
                    "file_path": doc["file_path"]
                }
            ]
        )