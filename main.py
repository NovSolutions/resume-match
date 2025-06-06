from fastapi import FastAPI
from relevanceai import Client
import os

app = FastAPI()
client = Client(api_key=os.environ["RELEVANCE_AI_API_KEY"])

@app.get("/")
def read_root():
    return {"message": "FastAPI + Relevance AI is live!"}

@app.post("/match")
def match_resume(data: dict):
    resume = data["resume"]
    job = data["job"]

    client.insert_documents(
        dataset_id="resume-matching",
        documents=[
            {"_id": "resume", "text": resume},
            {"_id": "job", "text": job}
        ]
    )

    match = client.vector_query(
        dataset_id="resume-matching",
        vector_fields=["text"],
        query_vector_fields={"text": resume},
        filters={"_id": {"$eq": "job"}},
        page_size=1
    )

    return {"match_score": match["results"][0]["_score"]}
