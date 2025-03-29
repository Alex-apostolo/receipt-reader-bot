from fastapi import APIRouter

oauth_router = APIRouter()

@oauth_router.get("/callback")
async def oauth_callback():
    return {"message": "OAuth callback received"}
