from sqlalchemy.orm import Session
from app import db_models
from app.models import Course, Section


def _to_course(row: db_models.Course) -> Course:
    return Course(id=row.id, code=row.code, name=row.name)


def _to_section(row: db_models.Section) -> Section:
    return Section(
        id=row.id,
        course_id=row.course_id,
        days=row.days,
        start_time=row.start_time,
        end_time=row.end_time,
        professor=row.professor,
        rating=row.rating,
    )


def get_all_courses(db: Session) -> list[Course]:
    return [_to_course(r) for r in db.query(db_models.Course).all()]


def get_course_by_code(code: str, db: Session) -> Course | None:
    row = db.query(db_models.Course).filter(db_models.Course.code == code).first()
    return _to_course(row) if row else None


def get_course_by_id(course_id: str, db: Session) -> Course | None:
    row = db.query(db_models.Course).filter(db_models.Course.id == course_id).first()
    return _to_course(row) if row else None


def get_sections_for_course(course_id: str, db: Session) -> list[Section]:
    rows = db.query(db_models.Section).filter(db_models.Section.course_id == course_id).all()
    return [_to_section(r) for r in rows]
