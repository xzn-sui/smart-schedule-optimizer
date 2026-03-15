# Smart Schedule Optimizer

A web app that helps UMD students build their semester schedule. Pick your courses, and it finds every valid section combination without time conflicts — ranked by professor ratings, gaps, and early/Friday classes.

**Live:** http://smart-schedule-frontend.s3-website.us-east-2.amazonaws.com

## Stack

- **Frontend:** React + Vite, hosted on AWS S3
- **Backend:** FastAPI (Python), running on AWS EC2
- **Database:** PostgreSQL on AWS RDS
- **Course data:** Real UMD sections from the [umd.io](https://umd.io) API

## Structure

```
backend/
  main.py               — FastAPI entry point
  import_courses.py     — pulls real UMD data from umd.io
  app/
    models.py           — Pydantic models
    db_models.py        — SQLAlchemy models
    database.py         — DB connection
    data.py             — DB query helpers
    routers/            — API endpoints
    services/
      scheduler.py      — conflict detection + scoring

frontend/
  src/
    App.jsx             — main UI
    App.css             — styles
```

## Running locally

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173
