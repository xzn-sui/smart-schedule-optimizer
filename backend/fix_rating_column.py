from app.database import engine
import sqlalchemy

with engine.connect() as conn:
    conn.execute(sqlalchemy.text("ALTER TABLE sections ALTER COLUMN rating DROP NOT NULL"))
    conn.commit()
print("Done")
