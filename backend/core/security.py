from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    # Simple explicit API key validation can be added here
    # if not api_key_header or api_key_header != "your-secret-api-key":
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    #     )
    return api_key_header
