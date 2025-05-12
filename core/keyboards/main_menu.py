from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from core.constants import MenuButtons


def main_menu_kb() -> ReplyKeyboardMarkup:
    """
    Создает главное меню бота с кнопками:
    - Список бестселлеров
    - Поиск рецензий.

    Returns:
        ReplyKeyboardMarkup: клавиатура с вертикальным расположением кнопок.
    """
    keyboard = ReplyKeyboardMarkup(
        row_width=1,  # Количество кнопок в строке
        resize_keyboard=True,  # Подстраивает размер
        one_time_keyboard=False,  # Не скрывает клавиатуру после нажатия
    )
    keyboard.add(
        KeyboardButton(text=MenuButtons.BESTSELLERS),
        KeyboardButton(text=MenuButtons.REVIEWS),
    )

    return keyboard
