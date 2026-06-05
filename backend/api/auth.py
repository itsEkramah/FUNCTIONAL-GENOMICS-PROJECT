from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/login")
async def login():
    return {"token": "dummy-token", "status": "authenticated"}
