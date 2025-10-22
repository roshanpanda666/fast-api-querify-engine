# routes/query_routes.py
from fastapi import APIRouter
from config.database import collection
from utils.serializers import serialize

router = APIRouter()

@router.get("/")
async def get_all_queries():
    try:
        data = [serialize(doc) for doc in collection.find({})]
        return {"count": len(data), "data": data}
    except Exception as e:
        return {"error": str(e)}
