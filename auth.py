from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests
from functools import lru_cache

# Your Cognito configuration
COGNITO_REGION = "us-east-2"
COGNITO_USER_POOL_ID = "us-east-2_4qSZVI2WH"
COGNITO_APP_CLIENT_ID = "223nnbea9edf3tach13ilck1mq"

# Construct the JWKs URL
COGNITO_JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"

security = HTTPBearer()

@lru_cache()
def get_jwks():
    """Fetch and cache the JSON Web Key Set from Cognito"""
    response = requests.get(COGNITO_JWKS_URL)
    return response.json()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify the JWT token from AWS Cognito
    
    Returns the decoded token payload if valid, raises HTTPException if invalid
    """
    token = credentials.credentials
    
    try:
        # Get the JWT headers to find the key id (kid)
        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']
        
        # Find the correct key from JWKS
        jwks = get_jwks()
        key = None
        for jwk_key in jwks['keys']:
            if jwk_key['kid'] == kid:
                key = jwk_key
                break
        
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token: key not found")
        
        # Verify and decode the token
        payload = jwt.decode(
            token,
            key,
            algorithms=['RS256'],
            audience=COGNITO_APP_CLIENT_ID,
            options={"verify_exp": True}
        )
        
        return payload
        
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

def get_current_user(token_payload: dict = Security(verify_token)):
    """
    Extract user information from the validated token
    
    Returns user email and sub (user ID)
    """
    return {
        "email": token_payload.get("email"),
        "sub": token_payload.get("sub"),
        "username": token_payload.get("cognito:username")
    }