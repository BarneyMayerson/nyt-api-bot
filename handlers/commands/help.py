from typing import Optional, Tuple
from telebot import TeleBot
from telebot.types import Message


def bot_help(
    bot: TeleBot,
    message: Message,
    commands: Tuple[Tuple[str, str], ...],
    additional_text: Optional[str] = None,
) -> None:
    """
    Формирует и отправляет пользователю список доступных команд бота с их описанием.
    Может включать дополнительный пояснительный текст перед списком команд.

    Args:
        bot (TeleBot: экземпляр работающего Telegram бота.
        message (Message): объект входящего сообщения, на которое нужно ответить
        commands (Tuple): кортеж кортежей, содержащий пары (имя_команды, описание)
                 Пример: (("start", "Запуск бота"), ("help", "Помощь")).
        additional_text (str): дополнительный текст, который будет добавлен перед списком команд.

    Returns:
        None: Функция не возвращает значение, только отправляет сообщение

    Raises:
        ValueError: Если передан пустой список команд

    Examples:
        >>> bot_help(bot, message, commands, "Доступные команды:")
        # Отправит сообщение:
        # Доступные команды:
        #
        # /start - Start bot
        # /help - Show help
    """
    if not commands:
        raise ValueError("Список команд не может быть пустым")

    command_list = [f"/{cmd} - {desc}" for cmd, desc in commands]
    base_text = "\n".join(command_list)

    final_text = f"{additional_text}\n\n{base_text}" if additional_text else base_text
    bot.reply_to(message, final_text)
