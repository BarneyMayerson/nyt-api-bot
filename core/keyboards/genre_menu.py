from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from typing import List
from utils.paginator import Paginator


def genre_menu_kb(
    genres: List[str], page: int = 0, per_page: int = 8
) -> InlineKeyboardMarkup:
    paginator = Paginator(data=genres, prefix="genres_page")
    page_items, total_pages = paginator.get_page(page=page)

    kb = InlineKeyboardMarkup(row_width=2)

    for genre in page_items:
        kb.add(
            InlineKeyboardButton(
                text=genre.capitalize(), callback_data=f"genre:{genre}"
            )
        )

    kb.row(*paginator.create_keyboard(page).keyboard[0])

    return kb
