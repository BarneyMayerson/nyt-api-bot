from telebot import TeleBot
from telebot.types import Message
from core.constants import MenuButtons, Messages
from core.keyboards.main_menu import main_menu_kb
from handlers.genres import setup_genres_handlers
from handlers.genre import setup_genre_handlers
from handlers.reviews import setup_reviews_handlers


def setup_all_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text and msg.text not in MenuButtons)
    def preserve_keyboard(message: Message):
        bot.send_message(
            chat_id=message.chat.id,
            text=Messages.USE_MENU,
            reply_markup=main_menu_kb(),
        )

    setup_genres_handlers(bot=bot)
    setup_genre_handlers(bot=bot)
    setup_reviews_handlers(bot=bot)
