import cloudinary
from dotenv import dotenv_values
from cloudinary import uploader
from fastapi import HTTPException
config=dotenv_values(".env")


async def cloudinary_config(app):
    cloudinary.config(
        cloud_name=config["CLOUD_NAME"],
        api_key=config["CLOUD_API_KEY"],
        api_secret=config["CLOUD_API_SECRET"]
    )
    print("Connection with cloudiary successfull!!")


def upload_pdf_to_cloudinary(file_path:str):
    try:
        upload_data= uploader.upload(file_path,resource_type="raw",use_filename=True)
        # print(upload_data)
        return upload_data["secure_url"],upload_data["public_id"]
    except Exception as e:
        raise HTTPException(status_code=501,detail=f'Upload failed {e}')
    

def delete_pdf_from_cloudinary(file_name:str):
    try:
        ackn_dict=uploader.destroy(file_name,resource_type="raw")
        return ackn_dict
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Deletion Failed {e}")