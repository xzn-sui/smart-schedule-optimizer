from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import courses, schedules

app = FastAPI()
app.include_router(courses.router)
app.include_router(schedules.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://smart-schedule-frontend.s3-website.us-east-2.amazonaws.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}