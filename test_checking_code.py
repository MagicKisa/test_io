import pytest
from cryptoApi import get_source_code
from handlers.checking_code import cmd_check, meth_chosen, method_not_chosen, platform_chosen, address_entered, \
    code_entered, available_methods, available_platforms
from handlers.checking_code import CheckCode
from aiogram_tests.types.dataset import MESSAGE
from aiogram import F
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler


@pytest.fixture
def crypto_address():
    address = "0x9D6dB6382444b70a51307A4291188f60D4EEF205"
    return address


@pytest.fixture
def crypto_platform():
    platform = "BNB"
    return platform


@pytest.fixture
def crypto_code(crypto_platform, crypto_address):
    code = get_source_code(platform=crypto_platform, address=crypto_address)
    return code


@pytest.mark.asyncio
async def test_cmd_check():
    requester = MockedBot(MessageHandler(cmd_check))
    calls = await requester.query(MESSAGE.as_object(text="Проверить код криптовалюты"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Выберите способ:"


@pytest.mark.asyncio
async def test_meth_chosen():
    requester = MockedBot(request_handler=
                          MessageHandler(meth_chosen,
                                         F.text.in_(available_methods),
                                         state=CheckCode.choosing_method
                                         )
                          )
    calls = await requester.query(MESSAGE.as_object(text=available_methods[0]))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Спасибо. Теперь, введите код:"

    calls = await requester.query(MESSAGE.as_object(text=available_methods[1]))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Спасибо. Выберите платформу:"


@pytest.mark.asyncio
async def test_meth_not_chosen():
    requester = MockedBot(request_handler=MessageHandler(method_not_chosen, state=CheckCode.choosing_method))
    calls = await requester.query(MESSAGE.as_object(text='smth else'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Такого способа нет, выберите из этих:"


@pytest.mark.asyncio
@pytest.mark.parametrize("platform", [c for c in available_platforms])
async def test_platform_chosen(platform):
    requester = MockedBot(request_handler=
                          MessageHandler(platform_chosen,
                                         F.text.in_(available_platforms),
                                         state=CheckCode.choosing_platform)
                          )
    calls = await requester.query(MESSAGE.as_object(text=platform))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Отлично, теперь введите адрес контракта:"


@pytest.mark.asyncio
async def test_address_entered(crypto_address, crypto_platform):
    requester = MockedBot(request_handler=
                          MessageHandler(address_entered,
                                         F.text,
                                         state=CheckCode.entering_address,
                                         state_data={'platform': crypto_platform}
                                         )
                          )
    calls = await requester.query(MESSAGE.as_object(text=crypto_address))

    answer_message = calls.send_message.fetchone().text
    assert (len("По коду криптовалюта схожа с теми, из которых активно = 0.00%") <= len(answer_message)
            <= len("По коду криптовалюта схожа с теми, из которых активно = 100.00%"))

    calls = await requester.query(MESSAGE.as_object(text="lolik"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Не получилось извлечь код введите корректный адрес контракта."


@pytest.mark.asyncio
async def test_code_entered(crypto_code):
    requester = MockedBot(request_handler=
                          MessageHandler(code_entered,
                                         state=CheckCode.entering_code)
                          )

    calls = await requester.query(MESSAGE.as_object(text=crypto_code))
    answer_message = calls.send_message.fetchone().text
    assert (len("По коду криптовалюта схожа с теми, из которых активно = 0.00%") <= len(answer_message)
            <= len("По коду криптовалюта схожа с теми, из которых активно = 100.00%"))
