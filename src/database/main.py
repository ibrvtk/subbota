from os import getenv
from sqlite3 import connect, Row

PATH_DATABASE_DB=getenv("PATH_DATABASE_DB")
PATH_DATABASE_SQL=getenv("PATH_DATABASE_SQL")

def db_create_database() -> None:
    '''
    Функция создания БД. Читает scheme.sql файл.
    `src/database/scheme.sql`
    '''
    try:
        with connect(PATH_DATABASE_DB, timeout=20) as db:
            with open(PATH_DATABASE_SQL, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            db.executescript(sql_script)
            db.commit()

    except Exception as e:
        print(f"error: database: db_create_database(): {e}")

def create_session(session_id: str, attacker_side: str) -> None:
    '''Создаёт запись сессии в БД.'''
    try:
        with connect(PATH_DATABASE_DB, timeout=20) as db:
            db.execute("INSERT OR REPLACE INTO session (id, attacker_side) VALUES (?, ?)", (session_id, attacker_side,))

    except Exception as e:
        print(f"error: database: create_session(): {e}")

def set_choice(session_id: str, player_priority: int, choice: str) -> bool:
    field = "p1_choice" if player_priority == 1 else "p2_choice"
    try:
        with connect(PATH_DATABASE_DB, timeout=20) as db:
            player_result = db.execute(f"SELECT {field} FROM session WHERE id = ?", (session_id,)).fetchone()
            if player_result and player_result[0] is None:
                db.execute(f"UPDATE session SET {field} = ? WHERE id = ?", (choice, session_id,))
                return True
            return False

    except Exception as e:
        print(f"error: database: set_choice(): {e}")

def get_session_data(session_id: str) -> Row:
    try:
        with connect(PATH_DATABASE_DB, timeout=20) as db:
            db.row_factory = Row
            return db.execute("SELECT * FROM session WHERE id = ?", (session_id,)).fetchone()

    except Exception as e:
        print(f"error: database: get_session_data(): {e}")

def clear_choices(session_id: str, next_attacker_side: int) -> None:
    try:
        with connect(PATH_DATABASE_DB, timeout=20) as db:
            db.execute("UPDATE session SET p1_choice = NULL, p2_choice = NULL, attacker_side = ? WHERE id = ?", (next_attacker_side, session_id,))

    except Exception as e:
        print(f"error: database: clear_choices(): {e}")