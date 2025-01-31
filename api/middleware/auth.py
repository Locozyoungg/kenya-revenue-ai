from fastapi import Request, HTTPException

async def api_key_auth(request: Request):
    """Validate API keys for government services"""
    api_key = request.headers.get('X-API-KEY')
    if api_key != os.getenv('GOV_API_KEY'):
        raise HTTPException(
            status_code=401,
            detail="Invalid government credentials"
        )