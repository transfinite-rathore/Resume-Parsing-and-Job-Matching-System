from fastapi import FastAPI
from app.routers.home_router import router
from app.routers.resume_router import router
from app.routers.applicant_auth import auth_router
from app.routers.recruiter_auth import router as recruiter_router
from app.routers.jd_router import router as jd_router
from contextlib import asynccontextmanager
from app.cloudinary_setup.config import cloudinary_config
from app.DB.db_setup import startup_db_client,shutdown_db_client

@asynccontextmanager
async def define_lifespan(app:FastAPI):
    await startup_db_client(app)
    await cloudinary_config(app)
    yield
    await shutdown_db_client(app)



run_app=FastAPI(lifespan=define_lifespan)

run_app.include_router(router=router)
run_app.include_router(router=router,prefix="/api")
run_app.include_router(router=auth_router,prefix="/api")
run_app.include_router(router=recruiter_router,prefix="/api/recruiter")
run_app.include_router(router=jd_router,prefix="/api/recruiter")

