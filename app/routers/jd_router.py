from fastapi import APIRouter,Request,Response,HTTPException,Depends,BackgroundTasks
from ..utils.Exception_handling import handle_try_except
from ..utils.token_setup import verfiy_recuriter_JWT
from ..models.JD import JobDescription
from ..utils.background_task import find_jd_resume_score
from bson import ObjectId
from typing import Optional

router=APIRouter()


# get all jd
@handle_try_except
@router.get("/jobs")
async def get_all_jobs(req:Request):
    database = req.app.mongo_db
    jd_cursor = database["job_description"].find(projection={"_id":0})
    jd_list = await jd_cursor.to_list()
    if(len(jd_list)<1):
        raise HTTPException(status_code=501,detail="No Resume returned from DB!")
    return {"Message":"Success","jd_list":jd_list}

# get jd with given id
@handle_try_except
@router.get("/job/{job_id}")
async def get_job(req:Request,job_id:str):
    database=req.app.mongo_db
    saved_jd=await database["job_description"].find_one({"_id":ObjectId(job_id)},projection={"_id":0})
    if not saved_jd:
        raise HTTPException(status_code=501,detail="No JD fetched based on given id")
    return {"Message":"Success","Data":saved_jd}


## Filter job descripiton based criteria
@handle_try_except
@router.get("/job")
async def get_job_based_on_filters(req:Request,experience:Optional[float]=None,role:Optional[str]=None):
    database=req.app.mongo_db
    query={}
    if experience:
        query["required_experience"]={"$gt":experience}
    if role:
        query["role"]=role
    job_cursor = database["job_description"].find(query)
    job_list= await job_cursor.to_list()

    if len(job_list)<1:
        raise HTTPException(status_code=501,detail="No JD match given experience criteria")
    return {"Message":"Success","Data":job_list}




## get jd posted by specific recruiter
@handle_try_except
@router.get("/job")
async def recruiter_jobs(req:Request,payload=Depends(verfiy_recuriter_JWT)):
    database=req.app.mongo_db
    id = payload["_id"]
    jd_cursor = database["job_description"].find({"recruiter_id":ObjectId(id)})
    jd_list=await jd_cursor.to_list()

    if(len(jd_list)<1):
        raise HTTPException(status_code=501,detail="No jd found with given recruiter id")
    return {"Message":"Success","Data":jd_list}



##best_match
@handle_try_except
@router.get("/job/{job_id}/best_match")
async def get_best_match_resume(req:Request,job_id:str,payload=Depends(verfiy_recuriter_JWT)):
    database=req.app.mongo_db
    job_cursor = database["job_description"].find({"_id":ObjectId(job_id),"recruiter_id":ObjectId(payload["id"])},projection={"best_match":1,"best_score":1})
    job_list= await job_cursor.to_list(length=1)

    if not job_list:
        raise HTTPException(status_code=404, detail="Job not found or no matches yet")
    best_match = job_list[0].get("best_match", [])
    best_score = job_list[0].get("best_score", None)

    return {"Best_match": best_match, "Best_score": best_score}


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
@handle_try_except
@router.delete("/job/{job_id}")
async def delete_job(req:Request,job_id:str,payload=Depends(verfiy_recuriter_JWT)):
    database=req.app.mongo_db

    deleted_job = await database["job_description"].find_one_and_delete({"_id":ObjectId(job_id),"recruiter_id":ObjectId(payload["id"])})
    if not deleted_job:
        raise HTTPException(status_code=404, detail="Job not found or you are not authorized to delete it")
    return {"message":"Deletion Success"}
    ...

# update given jd

