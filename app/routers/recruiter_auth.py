from fastapi import Request,Response,Depends,HTTPException,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..models.Recuriter import Recruiter,RecuriterLogin,change_recuriter_password
from ..utils.Exception_handling import handle_try_except
from ..utils.password_setups import verify_password,change_password
from ..utils.token_setup import generate_access_token,generate_refresh_token,verfiy_recuriter_JWT
import os
router=APIRouter()

templates=Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..","templates"))


@router.get("/register")
async def register_page(req:Request,response_class=HTMLResponse):
    return templates.TemplateResponse(request=req,name="recruiter_register.html")

@router.get("/login")
async def login_page(req:Request,response_class=HTMLResponse):
    return templates.TemplateResponse(request=req,name="recruiter_login.html")


## Tested OK
@router.post("/register")
@handle_try_except
async def Register(req:Request,recuriter:Recruiter):
    database=req.app.mongo_db
    exsiting_data=await database["recruiter"].find_one({"email":recuriter.email})
    if(exsiting_data):
        raise HTTPException(status_code=401,detail=f"Company already exist with given {exsiting_data['email']}")
    
    saved_user = await database["recruiter"].insert_one(recuriter.model_dump())

    if(not str(saved_user.inserted_id)):
        raise HTTPException(status_code=501,detail="Issue while saving into Database")
    return {"Message":"Data Saved Successfully","id":str(saved_user.inserted_id)}


## Tested OK
@router.post("/login")
@handle_try_except
async def login(req:Request,res:Response,login_user:RecuriterLogin):

    collection=req.app.mongo_db["recruiter"]
    saved_user= await collection.find_one({"email":login_user.email})
    if not saved_user:
        raise HTTPException(status_code=501,detail=f"No user found with given {login_user.email}")
    is_pass_correct=verify_password(login_user.password,saved_user["password"])
    if not is_pass_correct:
        raise HTTPException(status_code=501,detail="Email or Password incorrect")
    payload={"_id":str(saved_user["_id"])}

    access_tk=generate_access_token(payload)
    refresh_tk=generate_refresh_token(payload)

    await collection.update_one({"_id":saved_user["_id"]},{"$set":{"refresh_token":refresh_tk}})

    res.set_cookie(key="access-token",
                   value=access_tk,
                   secure=True,
                   httponly=True,
                   path='/')
    res.set_cookie(key="refresh-token",
                   value=refresh_tk,
                   secure=True,
                   httponly=True,
                   path='/')


    return{"Message":"Login Successfull"}

## Tested OK
@router.post("/logout")
@handle_try_except
async def logout(req:Request,res:Response,payload=Depends(verfiy_recuriter_JWT)):
    
    await req.app.mongo_db["recruiter"].update_one({"_id":payload["_id"]},{"$unset":{"refresh_token":""}})
    res.delete_cookie(key="access-token",
                      path="/")
    res.delete_cookie(key="refresh-token",
                      path="/")
    return {"Message":"Account logged out successfully"}




@router.post("/change-password")
@handle_try_except
def applicant_change_password(req:Request,pass_details:change_recuriter_password,payload=Depends(verfiy_recuriter_JWT)):
    result=change_password(req,"recruiter",str(payload["_id"]),pass_details.current_password,pass_details.new_password)

    if not result:
        raise HTTPException(status_code=501,detail="Password change unsuccessfull")
    return {"message":"Password changed successfully"}

