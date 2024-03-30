import pytest

from aiogram_tests import MockedBot
from handlers.common import handle_start, cmd_cancel_no_state, cmd_cancel
#from aiogram_tests.handler import CallbackQueryHandler
from aiogram_tests.handler import MessageHandler
from aiogram.filters import Command
from aiogram_tests.types.dataset import MESSAGE
#from aiogram_tests.types.dataset import CALLBACK_QUERY



@pytest.mark.asyncio
async def test_handle_start():
    requester = MockedBot(MessageHandler(handle_start, Command(commands=["start"])))
    calls = await requester.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert len(answer_message) == len(
        "Привет! Я бот для помощи в сфере криптовалют.\n"
        "Я могу помочь тремя способами - \n"
        "Первый - рассказать о скаме в криптовалютах. \n"
        "Второй - проверить криптовалюту по адресу или коду контракта "
        "на схожесть с мошенническими с помощью методами машинного обучения. \n"
        "Третий - получить ссылки блокчейн-эксплореров. \n"
        "Выбери одну из кнопок в меню(если запутались используйте /cancel):")


@pytest.mark.asyncio
async def test_cmd_cancel_no_state():
    requester = MockedBot(request_handler=MessageHandler(cmd_cancel_no_state, Command(commands=["cancel"]), state=None))
    calls = await requester.query(MESSAGE.as_object(text="/cancel"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Для начала нажмите /start"

    calls = await requester.query(MESSAGE.as_object(text="отмена"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Для начала нажмите /start"

    calls = await requester.query(MESSAGE.as_object(text="Отмена"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Для начала нажмите /start"


@pytest.mark.asyncio
async def test_cmd_cancel():
    requester = MockedBot(request_handler=MessageHandler(cmd_cancel, Command(commands=["cancel"])))
    calls = await requester.query(MESSAGE.as_object(text="/cancel"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Действие отменено"

    calls = await requester.query(MESSAGE.as_object(text="Отмена"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Действие отменено"