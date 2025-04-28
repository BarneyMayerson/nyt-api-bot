from telebot import TeleBot
from telebot.types import BotCommand
from handlers.commands.help import bot_help
from handlers.commands.start import bot_start
from handlers.commands.hello_world import bot_hello_world
from config.config import Config
from handlers.main_menu import setup_main_menu_handlers
from handlers.genres import setup_genres_handlers
from handlers.genre import setup_genre_handlers
from handlers.reviews import setup_reviews_handlers

DEFAULT_COMMANDS: tuple[tuple[str, str], ...] = (
    ("start", "Запуск бота"),
    ("help", "Справка о командах бота"),
    ("hello_world", "Тестовая команда"),
)


def set_default_commands(bot) -> None:
    """
    Устанавливает стандартные команды меню бота.

    Args:
        bot (TeleBot): экземпляр телеграм-бота.

    Note:
        Команды берутся из DEFAULT_COMMANDS в формате (command, description).
    """
    bot.set_my_commands(
        [BotCommand(command=cmd, description=desc) for cmd, desc in DEFAULT_COMMANDS]
    )


def setup_handlers(bot: TeleBot) -> None:
    """
    Регистрирует обработчики команд бота.

    Args:
        bot (TeleBot): экземпляр телеграм-бота.

    Includes:
        - /help: показывает список команд.
        - /start: приветственное сообщение.
        - /hello_world: тестовая команда (с алиасом /hello-world).
    """
    bot.message_handler(commands=["help"])(
        lambda message: bot_help(
            bot=bot,
            message=message,
            commands=DEFAULT_COMMANDS,
            additional_text="Дополнительный текст описания команд",
        )
    )
    bot.message_handler(commands=["start"])(
        lambda message: bot_start(bot=bot, message=message)
    )
    bot.message_handler(commands=["hello_world", "hello-world"])(
        lambda message: bot_hello_world(bot=bot, message=message)
    )

    setup_main_menu_handlers(bot=bot)
    setup_genres_handlers(bot=bot)
    setup_genre_handlers(bot=bot)
    setup_reviews_handlers(bot=bot)


def create_bot() -> TeleBot:
    """
    Создает и настраивает экземпляр телеграм-бота.

    Returns:
        TeleBot: настроенный экземпляр бота.

    Steps:
        1. Валидирует конфигурацию
        2. Создает экземпляр бота
        3. Настраивает обработчики
        4. Устанавливает команды меню
    """
    Config.validate()
    bot = TeleBot(token=Config.TELEGRAM_TOKEN)
    setup_handlers(bot=bot)
    set_default_commands(bot=bot)

    return bot
