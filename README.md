@app.post("/match")
def match_resume(data: dict):
    resume = data["resume"]
    job = data["job"]

    client.datasets.documents.insert(
        dataset_id="resume-matching",
        documents=[
            {"_id": "resume", "text": resume},
            {"_id": "job", "text": job}
        ]
    )

    match = client.datasets.vector.search(
        dataset_id="resume-matching",
        query_vector={"text": resume},
        vector_fields=["text"],
        filters={"_id": {"$eq": "job"}},
        page_size=1
    )

    return {"match_score": match["results"][0]["_score"]}
