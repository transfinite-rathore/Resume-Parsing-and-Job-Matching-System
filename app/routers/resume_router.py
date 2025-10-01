from fastapi import APIRouter,Request,File,UploadFile,HTTPException,Depends,BackgroundTasks
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
import os
import shutil
from ResumerParsing.main import parsed_resume_details
from app.utils.token_setup import verfiy_applicant_JWT
from ..cloudinary_setup.config import upload_pdf_to_cloudinary,delete_pdf_from_cloudinary
from ..models.Resume import Resume
from ..utils.Exception_handling import handle_try_except
from ..utils.background_task import extract_resume_details

router =APIRouter()
templates=Jinja2Templates(directory=os.path.join(os.path.dirname(__file__),"templates"))

'''
2. Applicant APIs
Route	Method	Functionality	Secured	Accessed By	Permissions
/applicant/resume/upload	POST	Upload resume file	✅ Yes	Applicant	Applicant only
/applicant/resume/parse	POST	Parse resume using NLP → JSON	✅ Yes	Applicant	Applicant only
/applicant/resume/{id}	GET	View specific parsed resume	✅ Yes	Applicant	Only owner
/applicant/resumes	GET	List all resumes uploaded	✅ Yes	Applicant	Only owner
/jobs	GET	Browse/search jobs (with filters)	❌ No	Applicant	Public but filtering needs Applicant login for personalization
/jobs/match	GET	Get best-fit jobs (resume vs jobs matching)	✅ Yes	Applicant	Applicant only
/jobs/apply/{job_id}	POST	Apply to a job	✅ Yes	Applicant	Applicant only
/applications	GET	View jobs applied to + status	✅ Yes	Applicant	Only owner


'''



##TESTED OK
@router.get("/file_upload")
def file_upload(req:Request,response_class=HTMLResponse):
    return templates.TemplateResponse(
        request=req,name="file_upload.html"
    )


## TESTED OK
@router.post("/file_upload")
async def file_upload3(req:Request,my_file:UploadFile=File(...)):

    ## Check File Storing directory make a new file path
    my_file_name = my_file.filename.replace(" ","_")
    upload_dir = os.path.join(os.getcwd(), "app", "public")  
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, my_file_name)
    print("ksfks ",file_path)
    ## write data to file path
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(my_file.file, buffer)
        print("Saved!!!",file_path)

    redirect_url=req.url_for("save_resume",file_path=file_path)
    return RedirectResponse(url=redirect_url,status_code=307)


## TESTED OK
@router.post("/save_resume/{file_path}")
async def save_resume(req:Request,file_path:str,background_tasks:BackgroundTasks,payload=Depends(verfiy_applicant_JWT)):
    try:
        user_id=payload["_id"]
        if not user_id:
            raise HTTPException(status_code=401,detail="user not found error")
        file_url,public_id= upload_pdf_to_cloudinary(file_path=file_path)
        
        database=req.app.mongo_db
        
        await database["User"].update_one({"_id":user_id},{"$set":{"resume_url":file_url}})

        # exsiting_user["_id"]=

        user_resume=Resume(applicant_id=user_id,url=file_url,cloudinary_public_id=public_id,is_active=True)
 
        saved_resume=await database["resume"].insert_one(user_resume.model_dump())

        if(not saved_resume):
            raise HTTPException(status_code=501,detail="Resume could saved to DB")
        background_tasks.add_task(extract_resume_details,req,file_path,str(saved_resume.inserted_id))
        return {"message":"Resume saved sucessfully"}
    except Exception as e:
        raise HTTPException(status_code=401,detail=f"Resume saved failed {e}")


@router.post("/resume_review/{file_path}")
async def extracted_details(req:Request,file_path):
    details=parsed_resume_details(file_path)
    return templates.TemplateResponse(
        "resume_review.html",
        {
            "request":req,**details
        }
    
    )


@router.post("/delete_resume/{resume_id}")
@handle_try_except
async def delete_resume(req:Request,file_name:str,resume_id:str,payload=Depends(verfiy_applicant_JWT)):
    cloud_res=delete_pdf_from_cloudinary(file_name=file_name.strip())
    if(cloud_res["result"]!="ok"):
        raise HTTPException(status_code=501,detail="File not Deleted")    
    
    deleted_data=await req.app.mongo_db["resume"].find_one_and_delete({"cloudinary_public_id":file_name})
    exsiting_data=await req.app.mongo_db["User"].find_one({"_id":deleted_data["applicant_id"]})

    if not exsiting_data:
        raise HTTPException(status_code=501,detail="No linked Account found with given resume")
    
    if "resume_url" in exsiting_data.keys():
        if exsiting_data["resume_url"]==deleted_data["url"]:
            await req.app.mongo_db["User"].update_one({"_id":exsiting_data["_id"]},{"$unset":"resume_url"})
    return {"Success":"Resume Deletion completely"}


## TESTED OK
## List all resumes
@router.get("/list_all_resumes")
@handle_try_except
async def list_resumes(req:Request,job_profile:str=None):
    query={}
    if job_profile:
        query["profile"]=job_profile
    result_cursor=req.app.mongo_db["resume"].find(query,projection={"_id":0,"id":0})
    result_cursor_list=await result_cursor.to_list()
    print(result_cursor_list)
    if(len(result_cursor_list)==0):
        return {"message":"No Resume Found"}
    return {"Data":result_cursor_list}


## List resume based on resume_id
@router.get("/list_resume/{resume_id}")
@handle_try_except
async def list_resume(req:Request,resume_id:str):
    database=req.app.mongo_db
    saved_resume=await database["resume"].find_one({"_id":ObjectId(resume_id)},projection={"_id":0})
    if not saved_resume:
        raise HTTPException(status_code=501,detail="No resume fetched based on given id")
    return {"Message":"Success","Data":saved_resume}


## Filter resume based on job_profile for specific applicant
@router.get("/applicat_resumes")
@handle_try_except
async def applicant_all_resume(req:Request,job_profile:str=None,payload=Depends(verfiy_applicant_JWT)):
    user_id=payload["_id"]
    database=req.app.mongo_db
    query={}
    query["applicant_id"]=ObjectId(user_id)
    if job_profile:
        query["profile"]=job_profile
    result_cursor=database["resume"].find(query,{"_id":0})
    result_list=await result_cursor.to_list()
    if(len(result_list)==0):
        return {"message":"No Resume Found for given Applicant"}
    return {"Data":result_list}


