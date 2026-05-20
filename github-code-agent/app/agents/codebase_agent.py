from app.retrieval.retriever import retrieve_relevant_code
from app.core.llm import client


def ask_codebase(question: str):

    documents = retrieve_relevant_code(question)

    context = "\n\n".join([
        doc["content"]
        for doc in documents
    ])

    prompt = f"""
You are an expert software architect and codebase analyst.

Answer the user's question about the repository.

QUESTION:
{question}

RELEVANT CODE:
{context}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content