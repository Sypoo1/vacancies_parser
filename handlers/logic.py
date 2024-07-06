from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import aiohttp
import asyncio
from database.cursor import insert_data, get_vacancies_data, delete_user_vacancies


def get_data_from_vacancies(vacancies: dict) -> dict:
    data = {}
    items = []
    if vacancies is not None:
        for item in vacancies["items"]:


            new_dict = {
                "name": item["name"],
                "url": item["alternate_url"],
                "area": item["area"]["name"],
            }
            if item["salary"] is not None:
                new_dict.update(
                    {
                        "salary_currency": item["salary"].get("currency"),
                        "salary_from": item["salary"].get("from"),
                        "salary_to": item["salary"].get("to"),
                        "salary_gross": item["salary"].get("gross"),
                    }
                )
            else:
                new_dict.update(
                    {
                        "salary_currency": None,
                        "salary_from": None,
                        "salary_to": None,
                        "salary_gross": None,
                    }
                )
            items.append(new_dict)

    data["items"] = items
    data["found"] = vacancies["found"]
    data["alternate_url"] = vacancies["alternate_url"]
    return data


def is_integer(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_valid_search_field(s: str) -> bool:
    try:
        s = s.split()
        if len(s) <= 0 or len(s) > 3:
            return False
        for item in s:
            if item not in ["name", "company_name", "description"]:
                return False
        return True
    except Exception as e:
        return False


def is_valid_experience(s: str) -> bool:
    try:
        s = s.split()
        if len(s) <= 0 or len(s) > 4:
            return False
        for item in s:
            if item not in [
                "noExperience",
                "between1And3",
                "between3And6",
                "moreThan6",
            ]:
                return False
        return True
    except Exception as e:
        return False


def is_valid_order(s: str) -> bool:
    try:
        for item in ["publication_time", "salary_desc", "salary_asc", "relevance"]:
            if item == s:
                return True

        return False
    except Exception as e:
        return False


async def send_data_to_user(msg: Message, state: FSMContext) -> bool:
    try:
        user_input = await state.get_data()
        user_id = msg.from_user.id

        params = {
            "text": user_input["text"],
        }


        if user_input["filters"] == "True":
            params["per_page"] = int(user_input["per_page"])
            params["salary"] = int(user_input["salary"])
            params["search_field"] = user_input["search_field"]
            params["experience"] = user_input["experience"]
            params["only_with_salary"] = user_input["only_with_salary"]
            params["order_by"] = user_input["order_by"]

        vacancies = await get_vacancies(**params)



        data = get_data_from_vacancies(vacancies)

        if data["found"] == 0:
            await msg.answer("Таких вакансий не найдено")
            return True

        await delete_user_vacancies(user_id)
        await insert_data(user_id, data)
        new_data = await get_vacancies_data(user_id)


        messages = format_vacancies(new_data)

        for message in messages:
            await msg.answer(message)
            await asyncio.sleep(0.5)

        return True
    except Exception as e:
        return False


async def get_vacancies(**kwargs):
    headers = {"User-Agent": "api-test-agent"}
    params = {}
    params.update(kwargs)
    url = "https://api.hh.ru/vacancies"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            return await response.json()


def format_vacancies(vacancies):
    max_message_length = 4096  # Максимальная длина сообщения в Телеграмме
    messages = []
    current_message = ""

    for vacancy in vacancies:
        vacancy_str = (
            f"Название: {vacancy['name']}\n"
            f"Ссылка: {vacancy['url']}\n"
            f"Город: {vacancy['area']}\n"
            f"Валюта: {vacancy['salary_currency'] or 'Не указана'}\n"
            f"Зарплата от: {vacancy['salary_from'] or 'Не указана'}\n"
            f"Зарплата до: {vacancy['salary_to'] or 'Не указана'}\n"
            f"Доход Gross: {'Да' if vacancy['salary_gross'] else 'Нет'}\n"
            "\n"
        )

        if len(current_message) + len(vacancy_str) > max_message_length:
            messages.append(current_message)
            current_message = vacancy_str
        else:
            current_message += vacancy_str

    if current_message:
        messages.append(current_message)

    return messages


