from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard

router = Router()


# Клавиатура с основными кнопками
kb = make_row_keyboard(["Статистика скама в криптовалютах", "Проверить код криптовалюты",
                        "Посмотреть в explorer"])


# Хэндлер на команду /start
@router.message(Command('start'))
async def handle_start(message: Message):
    await message.answer(
        "Привет! Я бот для помощи в сфере криптовалют.\n"
        "Я могу помочь тремя способами - \n"
        "Первый - рассказать о скаме в криптовалютах. \n"
        "Второй - проверить криптовалюту по адресу или коду контракта "
        "на схожесть с мошенническими с помощью методами машинного обучения. \n"
        "Третий - получить ссылки блокчейн-эксплореров. \n"
        "Выбери одну из кнопок в меню(если запутались используйте /cancel):",
        reply_markup=kb
    )

# Нетрудно догадаться, что следующие два хэндлера можно 
# спокойно объединить в один, но для полноты картины оставим так


# default_state - это то же самое, что и StateFilter(None)
@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Для начала нажмите /start",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
