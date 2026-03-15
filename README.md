# Smart Schedule Optimizer

A web app that helps UMD students build their semester schedule. You pick the courses you want to take, and it finds every valid combination of sections that don't conflict — ranked by your preferences and professor ratings.

Built this because manually cross-referencing Testudo sections to avoid time conflicts is tedious, especially when you're taking 4-5 courses with multiple sections each.

## How it works

1. Search and select courses you want to take
2. Hit "Generate Schedules"
3. The backend pulls all available sections for each course, brute-forces every possible combination, filters out conflicts, and ranks the results by a score that accounts for early classes, Friday classes, long gaps between classes, and professor ratings
4. Results show up as a visual weekly timetable alongside a table with professor names and ratings

## Tech stack

- **Frontend:** React + Vite
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL with SQLAlchemy
- **Course data:** Fetched from the [umd.io](https://umd.io) public API (real UMD sections)
- **Professor ratings:** Randomly generated for now, will integrate RateMyProfessor later

## Features

- Real Fall 2025 UMD course and section data
- Search courses by code or name
- Conflict detection across all section combinations
- Schedule scoring (penalizes early classes, Fridays, long gaps — rewards good professors)
- Visual weekly timetable for each result
- Color-coded by course

## Running locally

**Backend:**
```bash
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload
```

**Frontend** (separate terminal):
```bash
cd frontend
npm run dev
```

Open http://localhost:5173

## Importing course data

```bash
cd backend
.\venv\Scripts\activate
./venv/Scripts/python.exe import_courses.py
```

Pulls all courses for departments defined in `import_courses.py` from the umd.io API and loads them into PostgreSQL.

## Project structure

```
backend/
  main.py               — FastAPI app entry point
  import_courses.py     — fetches real UMD data from umd.io
  app/
    models.py           — Pydantic models (API shapes)
    db_models.py        — SQLAlchemy models (DB tables)
    database.py         — connection setup
    data.py             — DB query functions
    routers/            — API endpoints
    services/
      scheduler.py      — conflict detection + scoring logic

frontend/
  src/
    App.jsx             — main UI component
    App.css             — styles
```

## Planned

- AWS deployment (EC2 + RDS + S3)
- Real professor ratings from RateMyProfessor
- Import all departments, not just a preset list
- Handle lecture + discussion sections as a combined unit
