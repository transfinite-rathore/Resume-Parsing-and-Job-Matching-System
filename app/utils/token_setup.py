from fastapi import Request,Response,HTTPException
import jwt
from dotenv import dotenv_values
from datetime import datetime, timedelta, timezone
from bson import ObjectId


config=dotenv_values(".env")


## Tested OK
def generate_access_token(data:dict):
    data["exp"]=datetime.now(timezone.utc) + timedelta(days=int(config["ACCESS_TOKEN_EXPIRY"]))
    return jwt.encode(data,config["ACCESS_TOKEN_SECRET"],config["ALGORITHM"])

## Tested OK
def generate_refresh_token(data:dict):
    data["exp"]=datetime.now(timezone.utc) + timedelta(days=int(config["REFRESH_TOKEN_EXPIRY"]))
    return jwt.encode(data,config["REFRESH_TOKEN_SECRET"],config["ALGORITHM"])


## Tested OK
async def verfiy_applicant_JWT(req:Request):
    try:
        access_token=req.cookies.get("access-token")
        if(not access_token):
            raise HTTPException(status_code=401,detail="Authentication token is missing")
        
        payload=jwt.decode(access_token,config["ACCESS_TOKEN_SECRET"],config["ALGORITHM"])

        saved_user= await req.app.mongo_db["User"].find_one({"_id":ObjectId(payload["id"])},{"username":1})
        if(not saved_user):
            raise HTTPException(status_code=401, detail="Unauthorized Authentication Token")
        return saved_user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

## Tested OK
async def verfiy_recuriter_JWT(req:Request):
    try:
        access_token=req.cookies.get("access-token")
        if(not access_token):
            raise HTTPException(status_code=401,detail="Authentication token is missing")
        
        payload=jwt.decode(access_token,config["ACCESS_TOKEN_SECRET"],config["ALGORITHM"])

        saved_user= await req.app.mongo_db["recruiter"].find_one({"_id":ObjectId(payload["_id"])},{"email":1})
        if(not saved_user):
            raise HTTPException(status_code=401, detail="Unauthorized Authentication Token")
        return saved_user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")