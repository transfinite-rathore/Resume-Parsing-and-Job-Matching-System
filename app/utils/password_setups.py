from passlib.context import CryptContext
from ..utils.Exception_handling import handle_try_except
from fastapi import Request,HTTPException,Response
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

##Tested OK
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

##Tested OK
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@handle_try_except
async def change_password(req:Request,res:Response,collection_name:str,_id:str,current_password:str,new_password:str):
    collection=req.app.mongo_db[collection_name]
    existing_user=await collection.find_one({"_id":ObjectId(_id)})
    is_password_correct=verify_password(current_password,existing_user["password"])

    if not is_password_correct:
        raise HTTPException(status_code=401,detail="")
    
    ackn_result=await collection.update_one({"_id":ObjectId(_id)},{"$set":{"password":hash_password(new_password)},"$unset":{"refresh_token":""}})

    res.delete_cookie(key="access-token",
                      path="/")
    res.delete_cookie(key="refresh-token",
                      path="/")

    return ackn_result.acknowledged