import aiohttp
import asyncio
import json


async def get_vacancies(**kwargs):
    headers = {"User-Agent": "api-test-agent"}
    params = {}
    params.update(kwargs)
    url = "https://api.hh.ru/vacancies"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            return await response.json()


async def main():

    salary = 1_000

    params = {
        "page": 1,
        "per_page": 3,
        "text": "c++",
        "search_field": ["name", "description"],  # name, company_name, description
        "experience": ["between1And3"],  # noExperience, between1And3, between3And6, moreThan6,
        "employment": ["project", "part"],  # full, part, project, volunteer, probation,
        "only_with_salary": "True",
        "order_by": "publication_time", # publication_time, salary_desc, salary_asc, relevance
    }

    if salary is not None:
        params.update({"salary": salary})

    vacancies = await get_vacancies(**params)
    print(vacancies)
    with open("test.json", "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(main())
