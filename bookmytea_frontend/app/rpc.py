from uuid import UUID

import requests
from jsonrpcclient import request, parse, Ok, Error

AUTH_HOST = "localhost:5000"
CORE_HOST = "localhost:5001"


def core_client(method_name: str, params: dict) -> dict[str: str]:
    """
    Функция для выполнения клиентских запросов к основному микросервису
    :param method_name: Название метода
    :param params: Параметры для метода
    """
    response = requests.post(f'http://{CORE_HOST}/api/v1/jsonrpc/client',
                             json=request(method_name, params=params))
    parsed = parse(response.json())
    if isinstance(parsed, Ok):
        return parsed.result
    elif isinstance(parsed, Error):
        raise Exception(parsed.message)


def core_admin(method_name: str, params: dict) -> dict[str: str]:
    """
    Функция для выполнения админских запросов к микросервису авторизации
    :param method_name: Название метода
    :param params: Параметры для метода
    """
    response = requests.post(f'http://{CORE_HOST}/api/v1/jsonrpc/admin',
                             json=request(method_name, params=params))
    parsed = parse(response.json())
    if isinstance(parsed, Ok):
        return parsed.result
    elif isinstance(parsed, Error):
        raise Exception(parsed.message)


def auth(method_name: str, params: dict) -> dict[str: str]:
    """
    Функция для выполнения запросов к микросервису авторизации
    :param method_name: Название метода
    :param params: Параметры для метода
    """
    response = requests.post(f'http://{AUTH_HOST}/api/v1/jsonrpc/auth',
                             json=request(method_name, params=params))
    parsed = parse(response.json())
    if isinstance(parsed, Ok):
        return parsed.result
    elif isinstance(parsed, Error):
        raise Exception(parsed.message)


if __name__ == "__main__":
    print(core_client("get_user", {"user_id": ""}))
