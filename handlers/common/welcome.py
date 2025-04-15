from telebot.types import ReplyKeyboardMarkup

from utils.keyboards import main_menu_kb


def get_welcome_message() -> tuple[str, ReplyKeyboardMarkup]:
    """
    Возвращает:
        tuple: (текст_приветствия, клавиатура)
    """
    text = (
        "📚 Добро пожаловать в NYT Books Bot!\n"
        "Я помогу вам найти актуальные бестселлеры "
        "и рецензии из\nThe New York Times."
    )
    return text, main_menu_kb()
