from telebot import TeleBot
from telebot.types import Message

from handlers.common.welcome import get_welcome_message


def bot_start(bot: TeleBot, message: Message) -> None:
    """
    Обрабатывает команду /start, отправляя приветственное сообщение пользователю.
    Включает полное имя пользователя из Telegram.

    Args:
        bot: Экземпляр Telegram бота для отправки сообщений
        message: Входящее сообщение с командой /start

    Returns:
        None: Функция не возвращает значение, только отправляет сообщение

    Example:
        Когда пользователь с именем "Иван Петров" отправляет "/start",
        бот отвечает: "Привет, Иван Петров!"

    Note:
        Использует message.from_user.full_name для получения полного имени,
        которое может содержать как имя, так и фамилию пользователя.
    """
    text, keyboard = get_welcome_message()
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)
