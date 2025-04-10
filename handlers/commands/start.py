from telebot import TeleBot
from telebot.types import Message


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
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
