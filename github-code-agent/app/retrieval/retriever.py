import os

from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings

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

collection = chroma_client.get_collection(
    name="codebase"
)


def retrieve_relevant_code(query: str, n_results: int = 5):

    query_embedding = embedding_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    documents = []

    for i in range(len(results["documents"][0])):

        documents.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    return documents