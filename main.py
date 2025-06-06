from fastapi import FastAPI, HTTPException
from relevanceai import RelevanceClient
import os
from typing import List

app = FastAPI()
client = RelevanceClient(api_key=os.environ["RELEVANCE_AI_API_KEY"])

DATASET_ID = "recruit-mvp"

@app.post("/job")
def upload_job(job: dict):
    job_doc = {
        "_id": "job",
        "type": "job",
        "title": job["title"],
        "description": job["description"]
    }
    client.datasets.documents.insert(DATASET_ID, [job_doc])
    return {"status": "job saved"}

@app.post("/resumes")
def upload_resumes(resumes: List[dict]):
    docs = []
    for r in resumes:
        docs.append({
            "_id": r["id"],
            "type": "resume",
            "name": r["name"],
            "skills": r["skills"],
            "text": r["text"]
        })
    client.datasets.documents.insert(DATASET_ID, docs)
    return {"status": f"{len(docs)} resumes uploaded"}

@app.post("/match")
def match_candidates():
    job_doc = client.datasets.documents.list(DATASET_ID, filters={"_id": {"$eq": "job"}})
    if not job_doc["documents"]:
        raise HTTPException(404, "Job not found")

    job_text = job_doc["documents"][0]["description"]

    result = client.datasets.vector.search(
        dataset_id=DATASET_ID,
        query_vector={"text": job_text},
        vector_fields=["text"],
        filters={"type": {"$eq": "resume"}},
        page_size=5
    )
    return {"top_matches": result["results"]}

@app.get("/")
def root():
    return {"status": "AI Recruiting MVP live"}
