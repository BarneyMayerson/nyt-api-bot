from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from typing import List


def genre_menu_kb(
    genres: List[str], page: int = 0, per_page: int = 8
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)

    # Вычисляем текущий срез жанров
    start_idx = page * per_page
    paginated_genres = genres[start_idx : start_idx + per_page]

    for genre in paginated_genres:
        kb.add(
            InlineKeyboardButton(
                text=genre.capitalize(), callback_data=f"genre:{genre}"
            )
        )

    # Добавляем пагинацию
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton("◀ Назад", callback_data=f"genres_page:{page-1}")
        )
    if len(genres) > start_idx + per_page:
        pagination_buttons.append(
            InlineKeyboardButton("Вперед ▶", callback_data=f"genres_page:{page+1}")
        )

    if pagination_buttons:
        kb.row(*pagination_buttons)

    return kb
