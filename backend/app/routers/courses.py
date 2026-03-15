from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Course, Section
from app.database import get_db
from app import data

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[Course])
def get_courses(db: Session = Depends(get_db)):
    return data.get_all_courses(db)


@router.get("/{course_id}/sections", response_model=list[Section])
def get_sections(course_id: str, db: Session = Depends(get_db)):
    course = data.get_course_by_id(course_id, db)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return data.get_sections_for_course(course_id, db)
