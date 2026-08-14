from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, status



from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    #  calculating expiry time 
    expire = datetime.now(timezone.utc) + timedelta(
       minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})  #adding the expiry time in dictionary of data 

    # creating JWT token by jwt.encode()
    encoded_jwt = jwt.encode(
    to_encode,
    SECRET_KEY,
    algorithm=ALGORITHM,
   )

    return encoded_jwt 

# Verifying the Token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )