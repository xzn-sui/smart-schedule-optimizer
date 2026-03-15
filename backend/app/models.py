from pydantic import BaseModel


class Course(BaseModel):
    id: str
    code: str
    name: str


class Section(BaseModel):
    id: str
    course_id: str
    days: str        # e.g. "MW", "TR", "MWF"
    start_time: str  # e.g. "10:00"
    end_time: str    # e.g. "11:15"
    professor: str
    rating: float    # 1.0 - 5.0


class ScheduleRequest(BaseModel):
    courses: list[str]           # list of course codes
    preferences: dict | None = None


class ScheduleResult(BaseModel):
    score: int
    sections: list[Section]
