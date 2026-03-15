from itertools import product
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Section, ScheduleResult
from app import data


def _parse_time(t: str) -> datetime:
    return datetime.strptime(t, "%H:%M")


def _days_overlap(days_a: str, days_b: str) -> bool:
    return any(d in days_b for d in days_a)


def _times_overlap(sec_a: Section, sec_b: Section) -> bool:
    start_a = _parse_time(sec_a.start_time)
    end_a   = _parse_time(sec_a.end_time)
    start_b = _parse_time(sec_b.start_time)
    end_b   = _parse_time(sec_b.end_time)
    return start_a < end_b and start_b < end_a


def _has_conflict(sec_a: Section, sec_b: Section) -> bool:
    return _days_overlap(sec_a.days, sec_b.days) and _times_overlap(sec_a, sec_b)


def _score(sections: list[Section]) -> int:
    score = 100

    for sec in sections:
        # Penalty: early class before 09:00
        if _parse_time(sec.start_time).hour < 9:
            score -= 10

        # Penalty: class on Friday
        if "F" in sec.days:
            score -= 5

    # Penalty: long gaps between classes on the same day (>2 hours)
    for day in "MTWRF":
        day_sections = [s for s in sections if day in s.days]
        day_sections.sort(key=lambda s: _parse_time(s.start_time))
        for i in range(len(day_sections) - 1):
            gap_minutes = (
                _parse_time(day_sections[i + 1].start_time)
                - _parse_time(day_sections[i].end_time)
            ).total_seconds() / 60
            if gap_minutes > 120:
                score -= 5

    # Bonus: professor rating (avg rating scaled to 0-20 bonus points)
    avg_rating = sum(s.rating for s in sections) / len(sections)
    score += round((avg_rating - 1) / 4 * 20)

    return score


def generate_schedules(course_codes: list[str], db: Session) -> list[ScheduleResult]:
    # Resolve course codes -> course ids -> sections
    section_groups: list[list[Section]] = []
    for code in course_codes:
        course = data.get_course_by_code(code, db)
        if course is None:
            continue
        sections = data.get_sections_for_course(course.id, db)
        if sections:
            section_groups.append(sections)

    if not section_groups:
        return []

    valid: list[ScheduleResult] = []

    for combo in product(*section_groups):
        sections = list(combo)

        # Check all pairs for conflicts
        conflict = False
        for i in range(len(sections)):
            for j in range(i + 1, len(sections)):
                if _has_conflict(sections[i], sections[j]):
                    conflict = True
                    break
            if conflict:
                break

        if not conflict:
            valid.append(ScheduleResult(score=_score(sections), sections=sections))

    valid.sort(key=lambda r: r.score, reverse=True)
    return valid[:5]
