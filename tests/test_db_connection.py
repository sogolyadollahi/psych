from sqlalchemy import text
from app.core.database import SessionLocal


print(">>> Creating DB session")

db = SessionLocal()

try:
    print(">>> Running SELECT 1")

    result = db.execute(text("SELECT 1"))

    print(">>> SELECT 1 result:", result.scalar())

    print(">>> Running supplements query")

    result = db.execute(
        text("""
            SELECT id, name, reminder_time, is_active
            FROM supplements
            LIMIT 10
        """)
    )

    rows = result.fetchall()

    print(">>> Supplements result:")
    for row in rows:
        print(row)

except Exception as exc:
    print(">>> DATABASE ERROR:", repr(exc))

finally:
    db.close()
    print(">>> DB session closed")