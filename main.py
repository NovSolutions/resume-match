from fastapi import FastAPI, HTTPException
import os
import requests
from typing import List

app = FastAPI()

API_KEY = os.environ["RELEVANCE_AI_API_KEY"]
DATASET_ID = "recruit-mvp"
BASE_URL = "https://api.relevance.ai/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.post("/job")
def upload_job(job: dict):
    doc = {
        "_id": "job",
        "type": "job",
        "title": job["title"],
        "description": job["description"]
    }
    res = requests.post(
        f"{BASE_URL}/datasets/{DATASET_ID}/documents/insert",
        json={"documents": [doc]},
        headers=headers
    )
    if not res.ok:
        raise HTTPException(500, "Failed to insert job")
    return {"status": "job saved"}

@app.post("/resumes")
def upload_resumes(resumes: List[dict]):
    docs = [
        {
            "_id": r["id"],
            "type": "resume",
            "name": r["name"],
            "skills": r["skills"],
            "text": r["text"]
        }
        for r in resumes
    ]
    res = requests.post(
        f"{BASE_URL}/datasets/{DATASET_ID}/documents/insert",
        json={"documents": docs},
        headers=headers
    )
    if not res.ok:
        raise HTTPException(500, "Failed to insert resumes")
    return {"status": f"{len(docs)} resumes uploaded"}

@app.post("/match")
def match():
    # get job description
    res = requests.post(
        f"{BASE_URL}/datasets/{DATASET_ID}/documents/list",
        json={"filters": {"_id": {"$eq": "job"}}},
        headers=headers
    )
    job_doc = res.json().get("documents", [])
    if not job_doc:
        raise HTTPException(404, "Job not found")

    job_text = job_doc[0]["description"]

    search_payload = {
        "query_vector": {"text": job_text},
        "vector_fields": ["text"],
        "filters": {"type": {"$eq": "resume"}},
        "page_size": 5
    }

    match_res = requests.post(
        f"{BASE_URL}/datasets/{DATASET_ID}/vector/search",
        json=search_payload,
        headers=headers
    )

    if not match_res.ok:
        raise HTTPException(500, "Vector search failed")

    return {"matches": match_res.json().get("results", [])}

@app.get("/")
def root():
    return {"status": "MVP live via Relevance AI HTTP API"}

@app.get("/")
def root():
    return {"status": "AI Recruiting MVP live"}
