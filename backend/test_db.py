# backend/test_db.py
from src.db_helper.dbconn import DBConn

if __name__ == "__main__":
    db = DBConn()

    # 1) List all tables
    tables = db.run_sql("""
        SELECT table_name
          FROM information_schema.tables
         WHERE table_schema = 'public';
    """)
    print("Tables in public schema:", tables)

    # 2) Query the 'data' table without referencing non-existent columns
    rows = db.run_sql("""
        SELECT uid,
               user_name,
               pwd,
               email,
               auth_type,
               userinfo,
               resumeinfo
          FROM data
         WHERE uid = %s;
    """, ("test",))  # replace "test" with your actual userId
    print("Row for uid='test':", rows)

    db.close()