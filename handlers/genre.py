from telebot import TeleBot
from services.nyt_api import NYTBooksAPI
from core.content.books_top import books_top_message

api = NYTBooksAPI()


def setup_genre_handlers(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("genre:"))
    def handle_genre_selection(call):
        """
        Обрабатывает кнопку с жанром.
        """
        genre = call.data.split(":")[1]
        books = NYTBooksAPI().get_bestseller_list(genre)

        text = books_top_message(genre=genre, books=books)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
        )
