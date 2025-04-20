from typing import List
from telebot.types import InlineKeyboardMarkup
from core.keyboards.genre_menu import genre_menu_kb


def genres_menu_message(
    genres: List[str], page: int = 0, per_page: int = 8
) -> tuple[str, InlineKeyboardMarkup]:
    text = f"Выберите жанр (стр. {page+1}/{len(genres) // per_page + 1}):"

    return text, genre_menu_kb(genres=genres, page=page, per_page=per_page)
