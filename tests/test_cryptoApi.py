import pytest
import json
from cryptoApi import get_source_code, data_from_json, request_code, get_url_and_apikey


@pytest.fixture
def json_data():
    json_data = {"first": 1, "second": 2, "third": 3}
    with open('../testCryptoApiTest.json', 'w') as f:
        json.dump(json_data, f)
    return json_data


def test_address_none():
    with pytest.raises(ValueError) as e_info:
        get_source_code(None, True)


def test_platform_none():
    with pytest.raises(ValueError) as e_info:
        get_source_code(True, None)


def test_bad_address_and_platform():
    with pytest.raises(Exception) as e_info:
        get_source_code('kek0', 'lolix')


def test_data_from_json(json_data):
    read_json_data = data_from_json("testCryptoApiTest.json")
    assert read_json_data == json_data


def test_wrong_file_name():
    with pytest.raises(Exception) as e_info:
        data_from_json("testCryptoApiTes.json")


def test_request_code_without_params():
    with pytest.raises(Exception) as e_info:
        request_code(None, None)


def test_right_get_source_code():
    address = "0x9D6dB6382444b70a51307A4291188f60D4EEF205"
    platform = "BNB"

    assert get_source_code(address, platform) is not None


def test_apis_dict(json_data):
    apis_dict = data_from_json('apis_dict.json')
    assert apis_dict is not None


def test_call_request_code():
    address = "0x9D6dB6382444b70a51307A4291188f60D4EEF205"
    platform = "BNB"

    url, apikey = get_url_and_apikey(platform)
    params = {"module": "contract", "action": "getsourcecode", "address": address, "apikey": apikey}
    response = request_code(url, params=params)

    assert response is not None


def test_get_url_and_apikey():
    url, apikey = get_url_and_apikey("BNB")

    assert url is not None and apikey is not None

