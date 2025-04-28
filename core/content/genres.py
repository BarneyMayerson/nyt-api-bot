from typing import List
from telebot.types import InlineKeyboardMarkup
from core.keyboards.genre_menu import genre_menu_kb


def genres_menu_message(
    genres: List[str], page: int = 0, per_page: int = 8
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Формирует сообщение о списке жанров.

    Args:
        genres (List): список жанров.
        page (int): номер страницы.
        per_page (int): количество элементов на странице.

    Returns:
        tuple: (текст_приветствия, клавиатура).
    """
    text = f"Выберите жанр (стр. {page+1}/{len(genres) // per_page + 1}):"

    return text, genre_menu_kb(genres=genres, page=page, per_page=per_page)
