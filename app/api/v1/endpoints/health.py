from fastapi import APIRouter

from app.core.database import get_supabase

router = APIRouter()


@router.get("/")
async def health_check():
    try:
        client = get_supabase()
        client.table("nodes").select("id", count="exact").limit(1).execute()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "database": db_status,
        "version": "0.1.0",
    }
