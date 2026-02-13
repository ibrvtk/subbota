from random import choices
from string import ascii_lowercase, digits
from datetime import datetime
from aiosqlite import connect

from game import Player
from bot.config import DATABASE_DB, DATABASE_SQL



async def db_create_database() -> None:
    '''
    `src/database/scheme.sql`
    '''
    try:
        async with connect(DATABASE_DB) as db:
            with open(DATABASE_SQL, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            await db.executescript(sql_script)
            await db.commit()

    except Exception as e:
        print(f"error: database: db_create_database(): {e}")

async def db_create(player_1: Player, player_2: Player) -> None:
    id = ''.join(choices(ascii_lowercase + digits, k=6))

    try:
        async with connect(DATABASE_DB) as db:
            await db.execute(f"INSERT INTO game (id) VALUES (?)", (id, int(datetime.now().timestamp()), player_1.name, player_2.name))
            await db.commit()

    except Exception as e:
        print(f"error: database: db_create(): {e}")

async def db_read(arg, sql_select: str = '*', sql_where: str = 'id', arg_and = None, sql_and: str = None, check_exist: bool = False) -> tuple | int | str | bool | None:
    '''
    `SELECT {sql_select} FROM game WHERE {sql_where} = ?{sql_and_params}`  
    `sql_and_params = f" AND {sql_and} = ?"`  
    `params = (arg, arg_and)`  
    `*and*` будет только если соответствующие переменные были переданы. Иначе просто без них.
    '''
    if sql_select != '*' and sql_where != 'id' and check_exist:
        raise ValueError("src/database: db_read(): check_existence doesn't work with sql_select and sql_where")
    if (arg_and is not None and sql_and is None) or (arg_and is None and sql_and is not None):
        raise ValueError("src/database: db_read(): arg_and and sql_and must both be None or not None")

    sql_and_params = ""
    params = (arg,)

    if arg_and is not None and sql_and is not None:
        sql_and_params = f" AND {sql_and} = ?"
        params = (arg, arg_and)

    try:
        async with connect(DATABASE_DB) as db:
            if not check_exist:
                async with db.execute(f"SELECT {sql_select} FROM game WHERE {sql_where} = ?{sql_and_params}", params) as cursor:
                    data = await cursor.fetchone()

                    if sql_select.__contains__(','):
                        return data

                    return data[0] if data else None

            else:
                async with db.execute(f"SELECT id FROM game WHERE {sql_where} = ?{sql_and_params}", params) as cursor:
                    data = await cursor.fetchone()

                    if not data:
                        return False

                    return True

    except Exception as e:
        print(f"error: database: db_read(): {e}")
        return None

async def db_update(arg_set, arg_where, sql_set: str, sql_where: str = 'id', arg_and = None, sql_and: str = None) -> None:
    '''
    `UPDATE game SET {sql_set} = ? WHERE {sql_where} = ?{sql_and_params}`  
    `sql_and_params = f" AND {sql_and} = ?"`  
    `params = (arg_set, arg_where, arg_and)`  
    `*and*` будет только если соответствующие переменные были переданы. Иначе просто без них.
    '''
    if arg_and and not sql_and or not arg_and and sql_and:
        raise ValueError("src/database: db_read(): arg_and and sql_and must both be None or not None")

    sql_and_params = ""
    params = (arg_set, arg_where)

    if arg_and is not None and sql_and is not None:
        sql_and_params = f" AND {sql_and} = ?"
        params = (arg_set, arg_where, arg_and)

    try:
        async with connect(DATABASE_DB) as db:
            await db.execute(f"UPDATE game SET {sql_set} = ? WHERE {sql_where} = ?{sql_and_params}", params)
            await db.commit()

    except Exception as e:
        print(f"error: database: db_update(): {e}")

async def db_delete(id: str) -> None:
    async with connect(DATABASE_DB) as db:
        await db.execute(f"DELETE FROM game WHERE id = ?", id)
        await db.commit()


async def db_read_users() -> list | None:
    try:
        async with connect(DATABASE_DB) as db:
            async with db.execute("SELECT id FROM game",) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    except Exception as e:
        print(f"error: database: db_get_all_users(): {e}")
        return None