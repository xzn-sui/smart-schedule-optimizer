"""
Imports real course/section data from umd.io into the database.
Fetches all courses for each department listed in DEPARTMENTS.
Usage: python import_courses.py
"""
import re
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.database import engine, SessionLocal, Base
from app import db_models
from app.db_models import Course, Section

SEMESTER = "202508"  # Fall 2025
API = "https://api.umd.io/v1"
PER_PAGE = 100

# Departments to import
DEPARTMENTS = [
    "CMSC",   # Computer Science
    "MATH",   # Mathematics
    "STAT",   # Statistics
    "ENGL",   # English
    "ECON",   # Economics
    "PHYS",   # Physics
    "BIOL",   # Biology
    "CHEM",   # Chemistry
    "PSYC",   # Psychology
    "HIST",   # History
]

# Cache so the same professor always gets the same rating
professor_ratings: dict[str, float] = {}

def get_professor_rating(name: str) -> float:
    if name not in professor_ratings:
        import random
        professor_ratings[name] = round(random.uniform(2.5, 5.0), 1)
    return professor_ratings[name]


def convert_days(days_str: str) -> str | None:
    if not days_str or days_str.strip() == "":
        return None
    result = ""
    i = 0
    while i < len(days_str):
        chunk = days_str[i:i+2]
        if chunk == "Tu":
            result += "T"; i += 2
        elif chunk == "Th":
            result += "R"; i += 2
        elif chunk == "We":
            result += "W"; i += 2
        elif chunk == "Mo":
            result += "M"; i += 2
        elif chunk == "Fr":
            result += "F"; i += 2
        elif days_str[i] in "MWFT":
            result += days_str[i]; i += 1
        else:
            i += 1
    return result if result else None


def convert_time(time_str: str) -> str | None:
    if not time_str or time_str.strip() in ("", "TBA"):
        return None
    match = re.match(r"(\d+):(\d+)(am|pm)", time_str.strip().lower())
    if not match:
        return None
    h, m, period = int(match.group(1)), int(match.group(2)), match.group(3)
    if period == "pm" and h != 12:
        h += 12
    elif period == "am" and h == 12:
        h = 0
    return f"{h:02d}:{m:02d}"


def fetch_courses_for_dept(dept: str) -> list[dict]:
    """Fetch all courses for a department, paginating if needed."""
    all_courses = []
    page = 1
    while True:
        res = requests.get(f"{API}/courses", params={
            "dept_id": dept,
            "semester": SEMESTER,
            "per_page": PER_PAGE,
            "page": page,
        })
        if res.status_code != 200:
            break
        batch = res.json()
        if not batch:
            break
        all_courses.extend(batch)
        if len(batch) < PER_PAGE:
            break  # last page
        page += 1
    return all_courses


def fetch_sections(course_id: str) -> list[dict]:
    for attempt in range(3):
        res = requests.get(f"{API}/courses/sections", params={
            "course_id": course_id,
            "semester": SEMESTER,
        })
        if res.status_code == 200 and res.json():
            return res.json()
        time.sleep(1)
    return []


def process_sections(course_id: str, sections_data: list[dict]) -> list[Section]:
    """Convert raw API section data into Section DB objects."""
    results = []
    seen_times = set()  # deduplicate sections with identical lecture times

    for sec in sections_data:
        lecture_meeting = None
        for meeting in sec.get("meetings", []):
            if meeting.get("classtype", "").lower() != "discussion":
                lecture_meeting = meeting
                break

        if not lecture_meeting:
            continue

        days = convert_days(lecture_meeting.get("days", ""))
        start = convert_time(lecture_meeting.get("start_time", ""))
        end = convert_time(lecture_meeting.get("end_time", ""))

        if not days or not start or not end:
            continue

        # Skip duplicate lecture times for the same course
        time_key = (days, start, end)
        if time_key in seen_times:
            continue
        seen_times.add(time_key)

        instructors = sec.get("instructors", [])
        professor = instructors[0] if instructors else "Staff"
        rating = get_professor_rating(professor)

        section_id = f"{course_id.lower()}-{sec['section_id'].lower()}"
        results.append(Section(
            id=section_id,
            course_id=course_id.lower(),
            days=days,
            start_time=start,
            end_time=end,
            professor=professor,
            rating=rating,
        ))

    return results


def fetch_and_process(course: dict) -> tuple[Course, list[Section]]:
    """Fetch sections for a course and return DB objects ready to insert."""
    code = course["course_id"]
    db_course = Course(id=code.lower(), code=code, name=course["name"])
    sections_data = fetch_sections(code)
    sections = process_sections(code, sections_data)
    return db_course, sections


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(Section).delete()
    db.query(Course).delete()
    db.commit()

    # Step 1: fetch all course listings by department
    print("Fetching course listings by department...")
    all_courses = []
    for dept in DEPARTMENTS:
        courses = fetch_courses_for_dept(dept)
        print(f"  {dept}: {len(courses)} courses found")
        all_courses.extend(courses)
    print(f"Total: {len(all_courses)} courses across {len(DEPARTMENTS)} departments\n")

    # Step 2: fetch sections in parallel
    print("Fetching sections in parallel...")
    total_courses = 0
    total_sections = 0

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(fetch_and_process, c): c for c in all_courses}
        for future in as_completed(futures):
            db_course, sections = future.result()
            if not sections:
                continue
            db.merge(db_course)
            for sec in sections:
                db.merge(sec)
            db.commit()
            total_courses += 1
            total_sections += len(sections)
            print(f"  {db_course.code}: {len(sections)} sections")

    db.close()
    print(f"\nDone. {total_courses} courses with sections, {total_sections} total sections imported.")


if __name__ == "__main__":
    main()
