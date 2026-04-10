from tortoise import Tortoise
from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

async def init_db():
    await Tortoise.init(
        db_url=f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
        modules={'models': ['database.models']},
    )
    await Tortoise.generate_schemas()

    await migrate_db()

async def migrate_db():
    conn = Tortoise.get_connection("default")
    await conn.execute_query("ALTER TABLE admins_resumes DROP COLUMN IF EXISTS foreign_language, DROP COLUMN IF EXISTS foreign_language_level")
    await conn.execute_query("ALTER TABLE admins_resumes ADD COLUMN IF NOT EXISTS foreign_languages JSONB")

    await conn.execute_query("ALTER TABLE tg_users ALTER COLUMN full_name TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE tg_users ALTER COLUMN branch TYPE VARCHAR(255)")

    await conn.execute_query("ALTER TABLE teacher_resumes ALTER COLUMN subject TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE teacher_resumes ALTER COLUMN experience TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE teacher_resumes ALTER COLUMN working_time TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE teacher_resumes ALTER COLUMN position TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE teacher_resumes ALTER COLUMN salary TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE teacher_resumes ALTER COLUMN last_work_place TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE teacher_resumes ALTER COLUMN why_leave_work TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE teacher_resumes ALTER COLUMN last_work_place_phone TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE teacher_resumes ALTER COLUMN why_choice_us TYPE VARCHAR(255)")

    await conn.execute_query("ALTER TABLE admins_resumes ALTER COLUMN job TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE admins_resumes ALTER COLUMN experience TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE admins_resumes ALTER COLUMN working_time TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE admins_resumes ALTER COLUMN last_work_place TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE admins_resumes ALTER COLUMN why_leave_work TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE admins_resumes ALTER COLUMN last_work_place_phone TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE admins_resumes ALTER COLUMN why_choice_us TYPE VARCHAR(255)")

    await conn.execute_query("ALTER TABLE vacancies_text ALTER COLUMN name TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE subjects ALTER COLUMN name TYPE VARCHAR(255)")
    await conn.execute_query("ALTER TABLE sertificates ALTER COLUMN name TYPE VARCHAR(255)")

async def close_db():
    await Tortoise.close_connections()
    