from fastapi import  Request,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os


job_description = """We are looking for a Machine Learning Engineer with experience in Python , SQL , AWS , and deploying deep learning models using TensorFlow ."""

router =APIRouter()


templates=Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


@router.get("/")
def home(req:Request,response_class=HTMLResponse):
    # return {"msg":"hello world from FastAPI!!!!"}
    return templates.TemplateResponse(
        request=req,name="index.html"
    )






































# @router.post("/file_upload")
# async def file_upload2(req:Request,my_file:UploadFile=File(...)):
    
#     message="File Saved successfully"

#     ## Check File Storing directory make a new file path
#     my_file_name = my_file.filename
#     upload_dir = os.path.join(os.getcwd(), "app", "public")  # safer
#     os.makedirs(upload_dir, exist_ok=True)  # make sure folder exists
#     file_path = os.path.join(upload_dir, my_file_name)

#     ## write data to file path
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(my_file.file, buffer)
#         print("Saved!!!",file_path)

#     ## Based on JD match the stored resume and get the score
#     keyword_score,embedding_score=resume_parsing(file_path,job_description)

#     is_score_caluculated=False
#     if(keyword_score or embedding_score):
#         is_score_caluculated=True ## is score is caluculated then st flag true which help the frontend and debug
    
#     return templates.TemplateResponse(
#         "file_upload.html",
#         {"request":req, "message":message,"score_flag":is_score_caluculated,"keyword_score":keyword_score,"embedding_score":embedding_score}
       
#     )
    

