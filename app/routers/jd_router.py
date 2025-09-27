from fastapi import APIRouter,Request,Response,HTTPException,Depends,BackgroundTasks
from ..utils.Exception_handling import handle_try_except
from ..utils.token_setup import verfiy_recuriter_JWT
from ..models.JD import JobDescription
from ..utils.background_task import find_jd_resume_score
from bson import ObjectId

router=APIRouter()


# get all jd
@handle_try_except
@router.get("/list-jd")
async def get_all_jd(req:Request):
    database = req.app.mongo_db
    jd_cursor = database["job_description"].find(projection={"_id":0})
    jd_list = await jd_cursor.to_list()
    if(len(jd_list)<1):
        raise HTTPException(status_code=501,detail="No Resume returned from DB!")
    return {"Message":"Success","jd_list":jd_list}

# get jd with given id
@handle_try_except
@router.get("/list-jd/{jd_id}")
async def get_jd(req:Request,jd_id:str):
    database=req.app.mongo_db
    saved_jd=await database["job_description"].find_one({"_id":ObjectId(jd_id)},projection={"_id":0})
    if not saved_jd:
        raise HTTPException(status_code=501,detail="No JD fetched based on given id")
    return {"Message":"Success","Data":saved_jd}

# get jd with experience greater equal to
@handle_try_except
@router.get("/list_jd/{experience}")
async def get_jd_by_exp(req:Request,experience:float):
    database=req.app.mongo_db
    jd_cursor = database["job_description"].find({"required_experience":{"$gt":experience}})
    jd_list=await jd_cursor.to_list()
    if not jd_list:
        raise HTTPException(status_code=501,detail="No JD match given experience criteria")
    return {"Message":"Success","Data":jd_list}

# get jd for given role
@handle_try_except
@router.get("/list-jd/{role}")
async def get_jd_by_role(req:Request,role:str):
    database=req.app.mongo_db
    jd_cursor = database["job_description"].find({"required_experience":role})
    jd_list=await jd_cursor.to_list()
    if not jd_list:
        raise HTTPException(status_code=501,detail="No JD match given job role criteria")
    return {"Message":"Success","Data":jd_list}

## get jd posted by specific recruiter
@router.get("/list-jd")
async def list_jd_of_recruiter(req:Request,payload=Depends(verfiy_recuriter_JWT)):
    database=req.app.mongo_db
    id = payload["_id"]
    jd_cursor = database["job_description"].find({"recruiter_id":ObjectId(id)})
    jd_list=await jd_cursor.to_list()

    if(len(jd_list)<1):
        raise HTTPException(status_code=501,detail="No jd found with given recruiter id")
    return {"Message":"Success","Data":jd_list}



# post resume
@handle_try_except
@router.post("/post-jd")
async def post_jd(req:Request,res:Response,job_desc:JobDescription,background_tasks:BackgroundTasks,payload=Depends(verfiy_recuriter_JWT)):
    id = payload["_id"]
    database = req.app.mongo_db
    job_desc.recruiter_id=id
    saved_jd = await database["job_description"].insert_one(job_desc.model_dump())
    if not saved_jd:
        raise HTTPException(status_code=501,detail="Data unable to be saved")
    background_tasks.add_task(find_jd_resume_score,req,str(saved_jd.inserted_id),job_desc)
    return {"message":"Data saved Successfully","saved_id":str(saved_jd.inserted_id)}



# delete specific jd

# update given jd

