from ..models.JD import JobDescription
from fastapi import Request,Response,HTTPException
from .Exception_handling import handle_try_except
from ResumerParsing.main import parsed_resume_details
import re
from bson import ObjectId
from ResumerParsing.encodding import score_by_matched_keywords,encoding_score

## Tested OK
@handle_try_except
async def find_jd_resume_score(req:Request,id:str,jd:JobDescription):
    experience=jd.required_experience
    jd_content=jd.description
    database=req.app.mongo_db
    pipeline=[

        {
            
            "$lookup":{
            "from":"User",
            "localField":"applicant_id",
            "foreignField":"_id",
            "as":"applicant"
            }
           
        },
        {"$unwind":"$applicant"},
        {"$match":{
            "applicant.experience_in_years":{"$gte":experience}
        }}
    ]
    shortlisted_resume = await  database["resume"].aggregate(pipeline)
    resume_list= await shortlisted_resume.to_list()
    
    best_score=0
    best_resume_id=""
    for resume in resume_list:
        resume_details=resume["details"]
        score_by_words=score_by_matched_keywords(jd_content,resume_details)
        score_by_encodding=encoding_score(jd_content,resume_details)
        avg_score=(score_by_words+score_by_encodding)/2
        if avg_score>best_score:
            best_score=avg_score
            best_resume_id=resume["_id"]
    await database["job_description"].update_one({"_id":ObjectId(id)},{"$set":{"best_match":best_resume_id,"best_score":float(best_score)}})



## Tested OK
@handle_try_except
async def extract_resume_details(req:Request,file_path:str,id:str):
    details=parsed_resume_details(file_path)
    combined_details=""
    for content in details["details"].values():
        for content_item in content:
            combined_details+=re.sub(r"[^a-zA-Z0-9,.]", " ", content_item)+" "
    database=req.app.mongo_db
    await database["resume"].update_one({"_id":ObjectId(id)},{"$set":{"details":combined_details}})
    print("Resume updated ")

