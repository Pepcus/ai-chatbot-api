from fastapi import HTTPException, Header
from app_config import api_client_id, api_client_secret
import base64

def is_authorized_request(auth: str = Header(None)):
    if not auth:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        auth_type, encoded_credentials = auth.split(" ")
        if auth_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        decoded_credentials = base64.b64decode(encoded_credentials).decode()
        client_id, client_secret = decoded_credentials.split(":")
        if (client_id == api_client_id and client_secret == api_client_secret) :
            return True
        return False

    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")