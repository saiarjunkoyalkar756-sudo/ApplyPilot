import os
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
from services.shared.logging import get_logger

logger = get_logger("services.shared.vector")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

COLLECTION_NAME = "job_matches"

def ensure_collection():
    try:
        qdrant.get_collection(COLLECTION_NAME)
    except Exception:
        logger.info("creating_qdrant_collection", name=COLLECTION_NAME)
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

def get_embedding(text: str):
    if not text:
        return [0.0] * 1536
    response = client.embeddings.create(
        input=text.replace("\n", " "),
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def upsert_job_vector(job_id: str, title: str, description: str):
    ensure_collection()
    text = f"{title} {description}"
    vector = get_embedding(text)
    
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=job_id,
                vector=vector,
                payload={"type": "job", "title": title}
            )
        ]
    )

def search_similar_jobs(resume_embedding, limit=20):
    ensure_collection()
    search_result = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=resume_embedding,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(key="type", match=models.MatchValue(value="job"))
            ]
        ),
        limit=limit
    )
    return search_result
