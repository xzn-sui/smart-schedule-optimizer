from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import ScheduleRequest, ScheduleResult
from app.services.scheduler import generate_schedules
from app.database import get_db
from app import data

router = APIRouter(tags=["schedules"])


@router.post("/generate-schedules", response_model=list[ScheduleResult])
def create_schedules(request: ScheduleRequest, db: Session = Depends(get_db)):
    if not request.courses:
        raise HTTPException(status_code=400, detail="No courses provided")
    unknown = [code for code in request.courses if data.get_course_by_code(code, db) is None]
    if unknown:
        raise HTTPException(status_code=404, detail=f"Unknown course codes: {unknown}")
    results = generate_schedules(request.courses, db)
    return results
