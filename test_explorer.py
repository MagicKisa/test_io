import pytest
from handlers.explorer import handle_explorers, handle_explorers_choice, explorers_row, expl_dict, urls_row
from aiogram_tests.types.dataset import MESSAGE
from aiogram import F
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler


@pytest.fixture
def explorers():
    explorers = explorers_row
    return explorers


@pytest.fixture
def urls():
    urls = urls_row
    return urls


@pytest.mark.asyncio
async def test_handle_explorers():
    requester = MockedBot(MessageHandler(handle_explorers, F.text == "Посмотреть в explorer"))
    calls = await requester.query(MESSAGE.as_object(text="Посмотреть в explorer"))

    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Выберите интересующую платформу из меню:"


@pytest.mark.parametrize("explorer", [x for x in explorers_row])
@pytest.mark.asyncio
async def test_handle_explorers_choice(explorer, explorers):
    requester = MockedBot(MessageHandler(handle_explorers_choice, F.text.in_(explorers)))
    calls = await requester.query(MESSAGE.as_object(text=explorer))

    answer_message = calls.send_message.fetchone().text
    assert answer_message == expl_dict[explorer]
