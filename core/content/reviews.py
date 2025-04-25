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

    text = (
        f"📚 <b>{review.get('book_title', 'Без названия')}</b> <i>by {review.get('book_author')}</i>\n\n"
        f"📅 {review.get('publication_dt', 'Дата не указана')}\n"
        f"✍️ {review.get('byline', 'Автор не указан')}\n"
        f"{review.get('summary', 'Описание отсутствует.')}\n"
        f"🔗 <a href='{review.get('url', '')}'>Читать полностью</a>"
    )

    keyboard = InlineKeyboardMarkup(row_width=3)

    return text, keyboard
