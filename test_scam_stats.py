import pytest
from handlers.scam_stats import info_row, handle_info, handle_stats, info_dict
from aiogram_tests.types.dataset import MESSAGE
from aiogram import F
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler


@pytest.mark.asyncio
async def test_handle_stats():
    requester = MockedBot(request_handler=
                          MessageHandler(handle_stats, F.text == "Статистика скама в криптовалютах")
                          )
    calls = await requester.query(MESSAGE.as_object(text="Статистика скама в криптовалютах"))
    answer_message = calls.send_photo.fetchone().caption
    assert len(answer_message) == len("*Эти цифры основаны на отчетах о мошенничестве,"
                                      " поступивших в рамках сети потребительского мониторинга "
                                      "FTC (Consumer Sentinel Network), где в качестве метода оплаты"
                                      " указана криптовалюта. Категория мошенничества, связанного с "
                                      "инвестициями, включает в себя следующие подкатегории: инвестиции в искусство,"
                                      " драгоценности и редкие монеты; семинары и консультации по инвестициям, торговля"
                                      " акциями и товарными фьючерсами, а также различные виды инвестиций. Доклады,"
                                      " предоставленные участниками данных из сети Sentinel, исключены."
                                      "\n Чтобы получить информацию по картинке, используйте меню")


@pytest.mark.parametrize("info", [info for info in info_row])
@pytest.mark.asyncio
async def test_handle_info(info):
    requester = MockedBot(request_handler=
                          MessageHandler(handle_info, F.text.in_(info_row))
                          )
    calls = await requester.query(MESSAGE.as_object(text=info))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == info_dict[info]

