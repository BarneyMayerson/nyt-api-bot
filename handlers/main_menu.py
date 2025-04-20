from telebot import TeleBot
from core.content.genres import genres_menu_message
from services.nyt_api import NYTBooksAPI

api = NYTBooksAPI()


def setup_main_menu_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text == "📊 Список бестселлеров")
    def handle_bestsellers(message):
        text, keyboard = genres_menu_message(api.get_bestseller_genres())

        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    @bot.message_handler(func=lambda msg: msg.text == "🔍 Поиск рецензий")
    def handle_reviews(message):
        bot.send_message(message.chat.id, "Введите название книги для поиска рецензий:")
