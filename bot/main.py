"""
Основная точка запуска Telegram проложения.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import BotCommand

from bot.keyboards import keyboard_for_start, keyboard_for_choose_test
from bot_config import TG_TOKEN

bot = Bot(token=TG_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())


async def set_commands(bot_type: Bot):
    commands = [
        BotCommand(command="/start", description="Меню бота")
    ]
    await bot_type.set_my_commands(commands)


async def on_startup():
    logging.info("Bot start working...")


async def on_shutdown():
    logging.warning("Shutting down..")


class CreateTest(StatesGroup):
    waiting_fot_test_name = State()


class MainState(StatesGroup):
    start_state = State()
    choose_test = State()
    choose_create_test = State()


@dp.message_handler(Command('start'), state="*")
async def cmd_hello(message: types.Message, state: FSMContext):
    await state.finish()
    content = f"Выберите что Вам нужно, {message.from_user.full_name}:"

    await message.answer(
        content,
        reply_markup=keyboard_for_start.keyboard_for_start,
    )

    await message.delete()

    await state.set_state(MainState.start_state.state)


@dp.message_handler(Text(equals="Пройти тест"), state=MainState.start_state)
async def go_to_test(message: types.Message, state: FSMContext):
    await message.answer("Выбери нужный тест:")
    await state.set_state(MainState.choose_test.state)


@dp.message_handler(Text(equals="Создать тест"), state=MainState.start_state)
async def create_test(message: types.Message, state: FSMContext):
    keyboard_for_choose_create_test = keyboard_for_choose_test.choose_test_keyboard
    await message.answer("Хотите создать тест:", reply_markup=keyboard_for_choose_create_test)
    await state.set_state(MainState.choose_create_test.state)


@dp.message_handler(Text(equals="Профиль"), state=MainState.start_state)
async def show_profile(message: types.Message, state: FSMContext):
    await message.answer(
        "Вот твой профиль:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()


@dp.message_handler(Text(equals="Тех. Поддержка"), state=MainState.start_state)
async def tech_help(message: types.Message, state: FSMContext):
    await message.answer(
        "Для поддержки напишите на почту - ...",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()


# @dp.message_handler()
# async def echo(message: Message):
#     response = requests.post(f"http://0.0.0.0:9000/?msg={message.text}")
#     ans = json.loads(response.text).get("args")
#     await message.answer(f"{ans['up']}, {ans['low']}, {ans['base']}")

async def main():
    await set_commands(bot)
    await dp.skip_updates()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
