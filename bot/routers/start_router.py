from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.keyboards import keyboard_for_start, keyboard_for_choose_test
from bot.main import dp


class CreateTest(StatesGroup):
    waiting_fot_test_name = State()


class MainState(StatesGroup):
    start_state = State()
    choose_test = State()
    choose_create_test = State()


@dp.message_handler(Command('start'), state="*")
async def cmd_hello(message: types.Message, state: FSMContext):
    print("+")
    content = f"Здравствуй, {message.from_user.full_name}"
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
