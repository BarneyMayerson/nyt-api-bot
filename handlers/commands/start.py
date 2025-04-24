from telebot import TeleBot
from telebot.types import Message

from core.content.welcome import welcome_message


def bot_start(bot: TeleBot, message: Message) -> None:
    """
    Обрабатывает команду /start, отправляя приветственное сообщение пользователю.

    Args:
        bot (TeleBot): Экземпляр Telegram бота для отправки сообщений.
        message (Message): Входящее сообщение с командой /start.

    Returns:
        None: Функция не возвращает значение, только отправляет сообщение.
    """
    text, keyboard = welcome_message()
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)
