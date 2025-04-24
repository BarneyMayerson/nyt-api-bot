import os
from typing import Optional

from dotenv import find_dotenv, load_dotenv


def _load_env() -> None:
    """
    Загружает переменные окружения из .env файла.
    """
    if not find_dotenv():
        exit("Не найден файл переменных окружения")
    load_dotenv()


_load_env()


class Config:
    """
    Класс для работы с конфигурацией приложения.
    Содержит настройки и методы валидации конфигурации.
    """

    TELEGRAM_TOKEN: Optional[str] = os.getenv("TELEGRAM_TOKEN")
    NYT_API_KEY: Optional[str] = os.getenv("NYT_API_KEY")

    @classmethod
    def validate(cls):
        """
        Проверяет, что все необходимые переменные окружения установлены.

        Raises:
            ValueError: Если отсутствуют обязательные переменные окружения.
        """
        if not all([cls.TELEGRAM_TOKEN, cls.NYT_API_KEY]):
            raise ValueError("Отсутствуют все необходимые переменные окружения")
