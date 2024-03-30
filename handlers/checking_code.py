from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from predictor import predict_cluster_and_target_distribution
from cryptoApi import get_source_code

from keyboards.simple_row import make_row_keyboard
router = Router()


class CheckCode(StatesGroup):
    choosing_method = State()
    choosing_platform = State()
    entering_address = State()
    entering_code = State()


available_methods = ['По тексту кода', 'По адресу контракта']
available_platforms = ["Fantom", "BNB", "Core", "Arbitrum", "Base", "Polygon", "Ethereum"]


@router.message(StateFilter(None), F.text == "Проверить код криптовалюты")
async def cmd_check(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите способ:",
        reply_markup=make_row_keyboard(available_methods)
    )
    # Устанавливаем пользователю состояние "выбирает метод"
    await state.set_state(CheckCode.choosing_method)


@router.message(CheckCode.choosing_method,  F.text.in_(available_methods))
async def meth_chosen(message: Message, state: FSMContext):
    if message.text == available_methods[0]:
        await message.answer(
                            text="Спасибо. Теперь, введите код:"
        )
        await state.set_state(CheckCode.entering_code)
    else:
        await message.answer(
                            text="Спасибо. Выберите платформу:",
                            reply_markup=make_row_keyboard(available_platforms)
        )
        await state.set_state(CheckCode.choosing_platform)


@router.message(CheckCode.choosing_method)
async def method_not_chosen(message: Message):
    await message.answer("Такого способа нет, выберите из этих:",
                         reply_markup=make_row_keyboard(available_methods))


@router.message(CheckCode.choosing_platform,  F.text.in_(available_platforms))
async def platform_chosen(message: Message, state: FSMContext):
    await message.answer("Отлично, теперь введите адрес контракта:")
    data = await state.get_data()
    data['platform'] = message.text
    await state.update_data(data)
    await state.set_state(CheckCode.entering_address)


@router.message(CheckCode.entering_address,  F.text)
async def address_entered(message: Message, state: FSMContext):
    data = await state.get_data()
    platform = data['platform']
    source_code = get_source_code(message.text, platform)
    if source_code is None:
        await message.answer("Не получилось извлечь код введите корректный адрес контракта.")
        return
    await message.answer("Высчитываем результат")
    average_positive_probability = predict_cluster_and_target_distribution(source_code)
    # Вероятность того, что таргет равен 1
    probability_target_1 = average_positive_probability
    await message.answer(f"По коду криптовалюта схожа с теми, из которых активно = {probability_target_1 * 100:.2f}%")
    await state.clear()


@router.message(CheckCode.entering_code)
async def code_entered(message: Message, state: FSMContext):
    await message.answer("Высчитываем результат")
    source_code = message.text
    average_positive_probability = predict_cluster_and_target_distribution(source_code)
    # Вероятность того, что таргет равен 1
    probability_target_1 = average_positive_probability
    await message.answer(f"По коду криптовалюта схожа с теми, из которых активно = {probability_target_1 * 100:.2f}%")
    await state.clear()
