import logging

from aiogram import F, Router, flags, types
from aiogram.filters import Command, and_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from handlers.logic import is_integer, is_valid_search_field, is_valid_experience, is_valid_order, send_data_to_user

from states.states import Session

router = Router()


@router.message(Command("help"))
async def help_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )

        await msg.answer("Helping...")

    except Exception as error:
        logging.error(
            f"ошибка: {error} в help_handler",
            exc_info=True,
        )
        await state.clear()


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )

        await msg.answer("Здравствуйте! Я помогу вам найти вакансию. Напишите /help для подробной инструкции.")

    except Exception as error:
        logging.error(
            f"ошибка: {error} в start_handler",
            exc_info=True,
        )
        await state.clear()


@router.message(StateFilter(None), Command("update_data"))
async def update_data_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text} "
        )
        await msg.reply("введите ключевые слова для поиска вакансии")
        await state.set_state(Session.ask_text)


    except Exception as error:
        logging.error(
            f"ошибка: {error} в update_data_handler",
            exc_info=True,
        )
        await state.clear()


@router.message(Session.ask_text)
async def text_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )
        if len(msg.text) > 0:
            await state.update_data(
                text=msg.text,
            )
            await msg.reply("хотети ли вы ввести фильтры поиска? (введите да или нет)")
            await state.set_state(Session.ask_filters)
        else:
            await msg.reply("напишите ключевые слова для поиска вакансии")

    except Exception as error:
        logging.error(
            f"ошибка: {error} в text_handler",
            exc_info=True,
        )
        await state.clear()


@router.message(Session.ask_filters)
async def filters_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )
        if msg.text.lower() == "да":
            await state.update_data(
                filters="True",
            )
            await msg.reply("укажите желаемую запрлату в рублях (просто число например 60000)")
            await state.set_state(Session.ask_salary)
        elif msg.text.lower() == "нет":
            await state.update_data(
                filters="False",
            )
            await msg.reply("подождите, вакансии сейчас будут показаны")
            await state.set_state(Session.get_data)

            is_done = await send_data_to_user(msg, state)

            if is_done:
                logging.info(f"вакансии успешно отправлены у пользоват {msg.from_user.id}")
            else:
                await msg.answer("ошибка отправки вакансий")
                logging.error(f"ошибка отправки вакансий у пользователя {msg.from_user.id}")
            await state.clear()

        else:
            await msg.reply("напишите да или нет")


    except Exception as error:
        logging.error(
            f"ошибка: {error} в filters_handler",
            exc_info=True,
        )
        await state.clear()

@router.message(Session.ask_salary)
async def salary_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )
        if is_integer(msg.text):
            await state.update_data(
                salary=msg.text,
            )
            await msg.reply("укажите сколько вакансий вы хотите получить (от 1 до 100)")
            await state.set_state(Session.ask_count)
        else:
            await msg.reply("напишите просто число")


    except Exception as error:
        logging.error(
            f"ошибка: {error} в salary_handler",
            exc_info=True,
        )
        await state.clear()


@router.message(Session.ask_count)
async def count_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )
        if is_integer(msg.text) and int(msg.text) > 0 and int(msg.text) <= 100:
            await state.update_data(
                per_page=int(msg.text),
            )
            await msg.reply("укажите поле поиска (название вакансии, название компании, описание вакансии), если хотите указать несколько, то отправьте их через пробел, например name company_name description")
            await state.set_state(Session.ask_search_field)
        else:
            await msg.reply("напишите просто число")


    except Exception as error:
        logging.error(
            f"ошибка: {error} в count_handler",
            exc_info=True,
        )
        await state.clear()


@router.message(Session.ask_search_field)
async def search_field_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )
        if is_valid_search_field(msg.text):
            await state.update_data(
                search_field=msg.text.split(),
            )
            await msg.reply("укажите с каким опытом работы вы ищите вакансии (нет опыта, от 1 до 3, от 3 до 6, больше 6 лет опыта) если хотите указать несколько, то отправьте их через пробел например noExperience between1And3 between3And6 moreThan6")
            await state.set_state(Session.ask_experience)
        else:
            await msg.reply("напишите поля для поиска через пробел на английском языке как в примере выше")


    except Exception as error:
        logging.error(
            f"ошибка: {error} в search_field_handler",
            exc_info=True,
        )
        await state.clear()


@router.message(Session.ask_experience)
async def experience_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )
        if is_valid_experience(msg.text):
            await state.update_data(
                experience=msg.text.split(),
            )
            await msg.reply("вы хотите получить только вакансии с указанной зарплатой (напишите да или нет)")
            await state.set_state(Session.ask_only_with_salary)
        else:
            await msg.reply("напишите опыт работы через пробел на английском языке как в примере выше")

    except Exception as error:
        logging.error(
            f"ошибка: {error} в experience_handler",
            exc_info=True,
        )
        await state.clear()


@router.message(Session.ask_only_with_salary)
async def only_with_salary_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )
        if msg.text.lower() == "да":
            await state.update_data(
                only_with_salary="True",
            )
            await msg.reply("укажите порядок сортировки вакансий  (время публикации, убывание зарплаты, возрастание зарплаты, схожесть с ключевыми словами). нужно написать что-то одно из этого списка: publication_time, salary_desc, salary_asc, relevance. Например salary_desc")
            await state.set_state(Session.ask_order_by)
        elif msg.text.lower() == "нет":
            await state.update_data(
                only_with_salary="False",
            )
            await msg.reply("укажите порядок сортировки вакансий  (время публикации, убывание зарплаты, возрастание зарплаты, схожесть с ключевыми словами). нужно написать что-то одно из этого списка: publication_time, salary_desc, salary_asc, relevance. Например salary_desc")
            await state.set_state(Session.ask_order_by)
        else:
            await msg.reply("напишите да или нет")

    except Exception as error:
        logging.error(
            f"ошибка: {error} в only_with_salary_handler",
            exc_info=True,
        )
        await state.clear()

@router.message(Session.ask_order_by)
async def order_by_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )
        if is_valid_order(msg.text):
            await state.update_data(
                order_by=msg.text,
            )
            await msg.reply("подождите, вакансии сейчас будут показаны")
            await state.set_state(Session.get_data)

            is_done = await send_data_to_user(msg, state)

            if is_done:
                logging.info(f"вакансии успешно отправлены у пользоват {msg.from_user.id}")
            else:
                await msg.answer("ошибка отправки вакансий")
                logging.error(f"ошибка отправки вакансий у пользователя {msg.from_user.id}")
            await state.clear()

        else:
            await msg.reply("напишите порядок сортировки вакансий на английском языке как в примере выше")


    except Exception as error:
        logging.error(
            f"ошибка: {error} в order_by_handler",
            exc_info=True,
        )
        await state.clear()



@router.message(Session.get_data)
async def get_data_handler(msg: Message, state: FSMContext):
    try:
        logging.info(
            f" user_id = {msg.from_user.id}  отправил сообщение {msg.text}"
        )

        await msg.reply("подождите, вакансии сейчас будут показаны")
          

    except Exception as error:
        logging.error(
            f"ошибка: {error} в get_data_handler",
            exc_info=True,
        )
        await state.clear()