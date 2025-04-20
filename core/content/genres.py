from typing import List
from telebot.types import InlineKeyboardMarkup
from core.keyboards.genres_menu import genres_menu_kb


def genres_menu_message(genres: List[str]) -> tuple[str, InlineKeyboardMarkup]:
    text = "Выберите жанр"

    return text, genres_menu_kb(genres=genres)
