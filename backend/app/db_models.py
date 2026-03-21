from sqlalchemy import Column, String, Float, ForeignKey
from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id         = Column(String, primary_key=True)
    code       = Column(String, nullable=False, unique=True)
    name       = Column(String, nullable=False)


class Section(Base):
    __tablename__ = "sections"

    id         = Column(String, primary_key=True)
    course_id  = Column(String, ForeignKey("courses.id"), nullable=False)
    days       = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time   = Column(String, nullable=False)
    professor  = Column(String, nullable=False)
    rating     = Column(Float,  nullable=True)
