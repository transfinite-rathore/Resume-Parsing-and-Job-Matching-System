from fastapi import FastAPI
from app.routers.home_router import router as home_router
from app.routers.resume_router import router
from app.routers.applicant_auth import auth_router
from app.routers.recruiter_auth import router as recruiter_router
from app.routers.jd_router import router as jd_router
from contextlib import asynccontextmanager
from app.cloudinary_setup.config import cloudinary_config
from app.DB.db_setup import startup_db_client,shutdown_db_client
import os
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def define_lifespan(app:FastAPI):
    await startup_db_client(app)
    await cloudinary_config(app)
    yield
    await shutdown_db_client(app)



run_app=FastAPI(lifespan=define_lifespan)

print("jhdafda ",os.path.join(os.path.dirname(__file__),"app","static"))
run_app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "./app/","static")),
    name="static"
)

run_app.include_router(router=home_router)
run_app.include_router(router=router,prefix="/api")
run_app.include_router(router=auth_router,prefix="/api")
run_app.include_router(router=recruiter_router,prefix="/api/recruiter")
run_app.include_router(router=jd_router,prefix="/api/recruiters")

