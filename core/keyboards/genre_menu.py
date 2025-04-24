from telebot.types import InlineKeyboardMarkup
from typing import List
from utils.paginator import Paginator


def genre_menu_kb(
    genres: List[str], page: int = 0, per_page: int = 8
) -> InlineKeyboardMarkup:
    """
    Создает меню с жанрами.

    Args:
        genres (List): Список жанров.
        page (int): Номер страницы.
        per_page (int): Количество элементов на странице.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с вертикальным расположением кнопок.
    """
    paginator = Paginator(
        data=genres,
        items_per_page=per_page,
        prefix="genres_page",
        callback_prefix="genre",
    )

    return paginator.create_keyboard(page=page)
