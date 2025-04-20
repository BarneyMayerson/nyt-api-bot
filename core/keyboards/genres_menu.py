from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from typing import List


def genres_menu_kb(genres: List[str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)

    for genre in genres:
        kb.add(
            InlineKeyboardButton(
                text=genre.capitalize(), callback_data=f"genre:{genre}"
            )
        )

    return kb
