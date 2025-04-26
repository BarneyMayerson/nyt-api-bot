from typing import List, Dict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def reviews_menu_message(
    reviews: List[Dict], page: int = 0
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Формирует сообщение о списке жанров.

    Args:
        reviews (List): список рецензий.
        page (int): номер страницы.

    Returns:
        tuple: (текст_приветствия, клавиатура).
    """
    review = reviews[page]

    # print(f"Page in reviews_menu_message = {page}")
    # print(f"Review = {review}")

    text = (
        f"📚 <b>{review.get('book_title', 'Без названия')}</b> <i>by {review.get('book_author')}</i>\n\n"
        f"📅 {review.get('publication_dt', 'Дата не указана')}\n"
        f"✍️ {review.get('byline', 'Автор не указан')}\n"
        f"{review.get('summary', 'Описание отсутствует.')}\n"
        f"🔗 <a href='{review.get('url', '')}'>Читать полностью</a>"
    )

    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = []

    if page > 0:
        buttons.append(
            InlineKeyboardButton("⬅️ Назад", callback_data=f"review_prev:{page - 1}")
        )

    buttons.append(
        InlineKeyboardButton(f"{page+1}/{len(reviews)}", callback_data="dummy")
    )

    if page < len(reviews) - 1:
        buttons.append(
            InlineKeyboardButton("Вперед ➡️", callback_data=f"review_next:{page + 1}")
        )

    keyboard.add(*buttons)

    return text, keyboard
