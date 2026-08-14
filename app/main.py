from fastapi import FastAPI
from app.core.database import engine
from contextlib import asynccontextmanager
from app.api.v1.auth import router as auth_router
from app.api.v1.job import router as job_router
from app.api.v1.resume import router as resume_router
from app.api.v1.interview import router as interview_router
from app.api.v1.feedback import router as feedback_router
from app.api.v1.application import router as application_router
from app.api.v1.candidate import router as candidate_router
from fastapi.openapi.utils import get_openapi


from sqlalchemy import text

# creating fastAPI application
app = FastAPI(
    title="CMS Backend API",
    description="Candidate Management System API",
)

# register routers
app.include_router(auth_router)
app.include_router(job_router)
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(feedback_router)
app.include_router(application_router)
app.include_router(candidate_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Remove 422 responses from Swagger documentation
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if isinstance(operation, dict) and "responses" in operation:
                operation["responses"].pop("422", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
