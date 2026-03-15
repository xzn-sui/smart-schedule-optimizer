from app.database import engine, SessionLocal, Base
from app import db_models  # ensures tables are registered before create_all
from app.db_models import Course, Section

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing data
db.query(Section).delete()
db.query(Course).delete()

# Courses
courses = [
    Course(id="cmsc330", code="CMSC330", name="Programming Languages"),
    Course(id="cmsc216", code="CMSC216", name="Introduction to Computer Systems"),
    Course(id="stat400", code="STAT400", name="Probability and Statistics"),
    Course(id="math241", code="MATH241", name="Calculus III"),
    Course(id="econ305", code="ECON305", name="Intermediate Microeconomics"),
    Course(id="engl101", code="ENGL101", name="Academic Writing"),
    Course(id="psyc100", code="PSYC100", name="Introduction to Psychology"),
]

# Sections
sections = [
    # CMSC330
    Section(id="cmsc330-1", course_id="cmsc330", days="MW",  start_time="10:00", end_time="11:15", professor="Dr. Smith",    rating=4.2),
    Section(id="cmsc330-2", course_id="cmsc330", days="MW",  start_time="12:00", end_time="13:15", professor="Dr. Johnson",  rating=3.1),
    Section(id="cmsc330-3", course_id="cmsc330", days="TRF", start_time="14:00", end_time="14:50", professor="Dr. Chen",     rating=4.7),

    # CMSC216
    Section(id="cmsc216-1", course_id="cmsc216", days="MWF", start_time="09:00", end_time="09:50", professor="Dr. Park",     rating=3.9),
    Section(id="cmsc216-2", course_id="cmsc216", days="TR",  start_time="11:00", end_time="12:15", professor="Dr. Adams",    rating=4.4),
    Section(id="cmsc216-3", course_id="cmsc216", days="MW",  start_time="15:00", end_time="16:15", professor="Dr. Kim",      rating=2.8),

    # STAT400
    Section(id="stat400-1", course_id="stat400", days="TR",  start_time="09:30", end_time="10:45", professor="Dr. Williams", rating=3.8),
    Section(id="stat400-2", course_id="stat400", days="TR",  start_time="13:00", end_time="14:15", professor="Dr. Patel",    rating=4.5),
    Section(id="stat400-3", course_id="stat400", days="MWF", start_time="08:00", end_time="08:50", professor="Dr. Lee",      rating=2.9),

    # MATH241
    Section(id="math241-1", course_id="math241", days="MWF", start_time="10:00", end_time="10:50", professor="Dr. Nguyen",   rating=4.0),
    Section(id="math241-2", course_id="math241", days="TR",  start_time="14:00", end_time="15:15", professor="Dr. Okafor",   rating=3.3),
    Section(id="math241-3", course_id="math241", days="MWF", start_time="12:00", end_time="12:50", professor="Dr. Russo",    rating=4.6),

    # ECON305
    Section(id="econ305-1", course_id="econ305", days="MW",  start_time="11:00", end_time="12:15", professor="Dr. Garcia",   rating=4.1),
    Section(id="econ305-2", course_id="econ305", days="TR",  start_time="15:30", end_time="16:45", professor="Dr. Brown",    rating=3.5),
    Section(id="econ305-3", course_id="econ305", days="MWF", start_time="13:00", end_time="13:50", professor="Dr. Davis",    rating=4.8),

    # ENGL101
    Section(id="engl101-1", course_id="engl101", days="MWF", start_time="09:00", end_time="09:50", professor="Dr. Hall",     rating=4.3),
    Section(id="engl101-2", course_id="engl101", days="TR",  start_time="12:30", end_time="13:45", professor="Dr. Martin",   rating=3.7),
    Section(id="engl101-3", course_id="engl101", days="MW",  start_time="16:00", end_time="17:15", professor="Dr. Clark",    rating=2.6),

    # PSYC100
    Section(id="psyc100-1", course_id="psyc100", days="MWF", start_time="11:00", end_time="11:50", professor="Dr. Turner",   rating=4.9),
    Section(id="psyc100-2", course_id="psyc100", days="TR",  start_time="09:30", end_time="10:45", professor="Dr. White",    rating=3.2),
    Section(id="psyc100-3", course_id="psyc100", days="MW",  start_time="14:00", end_time="15:15", professor="Dr. Scott",    rating=4.0),
]

db.add_all(courses)
db.add_all(sections)
db.commit()
db.close()

print("Database seeded successfully.")
