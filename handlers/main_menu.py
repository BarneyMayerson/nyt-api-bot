from telebot import TeleBot
from telebot.types import Message
from core.constants import MenuButtons, Messages
from core.keyboards.main_menu import main_menu_kb
from handlers.genres import show_genres_page


def setup_main_menu_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text and msg.text not in MenuButtons)
    def preserve_keyboard(message: Message):
        bot.send_message(
            chat_id=message.chat.id,
            text=Messages.USE_MENU,
            reply_markup=main_menu_kb(),
        )

    @bot.message_handler(func=lambda msg: msg.text == MenuButtons.BESTSELLERS)
    def handle_bestsellers(message):
        """
        Обрабатывает кнопку со списком бестселлеров.
        """
        show_genres_page(bot=bot, chat_id=message.chat.id)
