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
    params = {
        "text": "java",
        
    }
    vacancies = await get_vacancies(**params)
    print(vacancies)
    with open("test.json", "w", encoding="utf-8") as f:
        json.dump(vacancies, f, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(main())
