from fastapi import Request,Response,APIRouter,HTTPException,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..models.Applicant import ApplicantLogin,ApplicantRegister,change_applicant_password
from ..utils.password_setups import verify_password,change_password
from ..utils.token_setup import generate_access_token,generate_refresh_token,verfiy_applicant_JWT
from dotenv import dotenv_values
from ..utils.Exception_handling import handle_try_except
import os

config=dotenv_values(".env")

templates=Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..","templates"))

auth_router=APIRouter()


@auth_router.get("/applicant_register")
async def register_page(req:Request,response_class:HTMLResponse):
    return templates.TemplateResponse(
        request=req,name="applicant_register.html"
    )



@auth_router.get("/applicant_login")
async def login_page(req:Request,reponse_class:HTMLResponse):
    return templates.TemplateResponse(request=req,name="applicant_login.html")







## Tested OK
@auth_router.post("/applicant_register")
async def register(request:Request,user:ApplicantRegister):
    '''
    1 get details from frontend to backend
    2 check all the details
    3 check if there is already user with same user_name or email
    4 if it is unique encrypt password and save
    5 send respone     
    '''
    try:
        database=request.app.mongo_db
        existing_user=database["User"].find({"$or":[{"name":user.username},{"email":user.email}] },{"_id":False})
        list_user=await existing_user.to_list()
        
        if(len(list_user)>0):
            raise HTTPException(status_code=401, detail="Username or email is incorrect")
        
        saved_user=await database["User"].insert_one(user.model_dump())
        return {"Data":user,"Saved_User_Id":str(saved_user.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=401,detail=f"Registration Failed {e}")



## Tested OK
@auth_router.post("/applicant_login")
async def login(req:Request,res:Response,user:ApplicantLogin):
    try:
        database=req.app.mongo_db
        
        if(user.username== False and user.email==False):
            raise HTTPException(status_code=401,detail="Username and Email both are empty")

        existing_user= await database["User"].find_one({"$or":[{"username":user.username},{"email":user.email}]})
        print("saved_user ",type(existing_user),existing_user)
        if(not existing_user ):
            print("I am here")
            raise HTTPException(status_code=401, detail="Username or email is incorrect")
        
        is_password_correct=verify_password(user.password,existing_user["password"])

        if(not is_password_correct):
            raise HTTPException(status_code=401, detail="Password is incorrect")
        
        user_id=str(existing_user["_id"])
        username=existing_user["username"]

        payload={"id":user_id,"username":username}
        access_token=generate_access_token(payload)
        refresh_token=generate_refresh_token(payload)

        await database["User"].update_one({"_id":existing_user["_id"]},{"$set":{"refresh_token":refresh_token}})

        res.set_cookie(key="access-token",
                    value=access_token,
                    secure=True,
                    httponly=True,
                    path="/")
        res.set_cookie(key="refresh-token",
                    value=refresh_token,
                    path="/",
                    secure=True,
                    httponly=True)

        return {"message":"Login Successfull"}
    except Exception as e:
        raise HTTPException(status_code=401,detail=f"Login Failed {e}")



## Tested OK
@auth_router.post("/logout")
async def logout(req:Request,res:Response,payload=Depends(verfiy_applicant_JWT)):
    try:
        await req.app.mongo_db["User"].update_one({"_id":payload["_id"]},{"$unset":{"refresh_token":""}})
        res.delete_cookie(key="access-token",path="/")
        res.delete_cookie(key="refresh-token",path="/")
        return {"Message":"Account logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")


## Tested OK
@auth_router.post("/applicant-change-password")
@handle_try_except
async def applicant_change_password(req:Request,res:Response,pass_details:change_applicant_password,payload=Depends(verfiy_applicant_JWT)):
    result= await change_password(req,res,"User",str(payload["_id"]),pass_details.current_password,pass_details.new_password)
    print("result ",result)
    if not result:
        raise HTTPException(status_code=501,detail="Password change unsuccessfull")
    return {"message":"Password changed successfully"}

