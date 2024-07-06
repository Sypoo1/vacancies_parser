import logging
from os import getenv

import psycopg
from dotenv import load_dotenv

# переменные окружения
load_dotenv()

HOST = getenv("PostgreSQL_host")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")


async def insert_data(user_id: int, data: dict) -> None:
    logging.info(f"вызвана функция insert_data для пользователя id={user_id}")
    try:
        async with await psycopg.AsyncConnection.connect(f"dbname={POSTGRES_DB} user={POSTGRES_USER} host={HOST} password={POSTGRES_PASSWORD}") as aconn:
            async with aconn.cursor() as acur:
                for item in data["items"]:
                    await acur.execute(
                    "INSERT INTO vacancies (id, user_id, name, url, salary_currency, salary_from, salary_to, salary_gross, area) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (user_id, item["name"], item["url"], item["salary_currency"], item["salary_from"], item["salary_to"], item["salary_gross"], item["area"]),
                    )
                    await aconn.commit()
            await aconn.close()

    except Exception as error:
        logging.error(f"ошибка: {error} в функции insert_data у пользователя {user_id}", exc_info=True)


async def get_vacancies_data(user_id: int) -> list[dict]:
    logging.info(f"вызывается функция get_vacancies_data для пользователя id={user_id}")
    try:
        async with await psycopg.AsyncConnection.connect(f"dbname={POSTGRES_DB} user={POSTGRES_USER} host={HOST} password={POSTGRES_PASSWORD}") as aconn:
            async with aconn.cursor() as acur:
                await acur.execute("SELECT * FROM vacancies WHERE user_id = %s", (user_id,))
                rows = await acur.fetchall()
                
                data = [dict(zip([column[0] for column in acur.description], row)) for row in rows]
                
                await aconn.close()
                return data

    except Exception as error:
        logging.error(f"ошибка при получении данных о вакансиях для пользователя {user_id}: {error}", exc_info=True)
        return []


async def delete_user_vacancies(user_id: int) -> None:
    logging.info(f"вызывается функция delete_user_vacancies для пользователя id={user_id}")
    try:
        async with await psycopg.AsyncConnection.connect(f"dbname={POSTGRES_DB} user={POSTGRES_USER} host={HOST} password={POSTGRES_PASSWORD}") as aconn:
            async with aconn.cursor() as acur:
                await acur.execute("DELETE FROM vacancies WHERE user_id = %s", (user_id,))
                await aconn.commit()
            await aconn.close()
            logging.info(f"Успешное удаление всех записей для пользователя id={user_id}")

    except Exception as error:
        logging.error(f"Ошибка при удалении записей для пользователя {user_id}: {error}", exc_info=True)