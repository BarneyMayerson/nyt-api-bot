from typing import Optional
from telebot import TeleBot
from core.content.genres import genres_menu_message
from core.content.reviews import reviews_menu_message
from services.nyt_api import NYTBooksAPI

api = NYTBooksAPI()
genres = api.get_bestseller_genres()


def show_genres_page(
    bot: TeleBot, chat_id: int, page: int = 0, message_id: Optional[int] = None
):
    """
    Показывает страницу с жанрами.

    Args:
        bot (TeleBot): экземпляр бота.
        chat_id (int): ID чата.
        page (int): номер страницы (начинается с 0).
        message_id (int): ID сообщения.
    """
    text, keyboard = genres_menu_message(genres=genres, page=page, per_page=8)

    if page == 0:
        # Для первой страницы - новое сообщение
        bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
    else:
        # Для последующих - редактируем существующее
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,  # Для callback-обработчика
            text=text,
            reply_markup=keyboard,
        )


def show_reviews_page(
    bot: TeleBot,
    chat_id: int,
    book_title: str = "Title",
    page: int = 0,
    message_id: Optional[int] = None,
):
    """
    Показывает страницу с жанрами.

    Args:
        bot (TeleBot): экземпляр бота.
        chat_id (int): ID чата.
        book_title (str):  название книги.
        page (int): номер страницы (начинается с 0).
        message_id (int): ID сообщения.
    """
    # reviews = api.search_reviews(title=book_title)
    reviews = {
        "status": "OK",
        "copyright": "Copyright (c) 2025 The New York Times Company.  All Rights Reserved.",
        "num_results": 3,
        "results": [
            {
                "url": "http://www.nytimes.com/2012/05/30/books/gone-girl-by-gillian-flynn.html",
                "publication_dt": "2012-05-30",
                "byline": "JANET MASLIN",
                "book_title": "Gone Girl",
                "book_author": "Gillian Flynn",
                "summary": "",
                "uuid": "00000000-0000-0000-0000-000000000000",
                "uri": "nyt://book/00000000-0000-0000-0000-000000000000",
                "isbn13": [
                    "9780297859383",
                    "9780297859390",
                    "9780297859406",
                    "9780307588364",
                    "9780307588371",
                    "9780307588388",
                    "9780385366755",
                    "9780553398380",
                    "9780553418354",
                    "9780553418361",
                    "9780606270175",
                    "9781410450951",
                    "9781594136054",
                ],
            },
            {
                "url": "http://www.nytimes.com/2012/06/17/books/review/gillian-flynns-gone-girl-and-more.html",
                "publication_dt": "2012-06-17",
                "byline": "MARILYN STASIO",
                "book_title": "Gone Girl",
                "book_author": "Gillian Flynn",
                "summary": "In Gillian Flynn’s “Gone Girl,” a young woman disappears on her fifth wedding anniversary — and her husband is suspected of murder.",
                "uuid": "00000000-0000-0000-0000-000000000000",
                "uri": "nyt://book/00000000-0000-0000-0000-000000000000",
                "isbn13": [
                    "9780297859383",
                    "9780297859390",
                    "9780297859406",
                    "9780307588364",
                    "9780307588371",
                    "9780307588388",
                    "9780385366755",
                    "9780553398380",
                    "9780553418354",
                    "9780553418361",
                    "9780606270175",
                    "9781410450951",
                    "9781594136054",
                ],
            },
            {
                "url": "http://www.nytimes.com/2012/05/30/books/gone-girl-by-gillian-flynn.html",
                "publication_dt": "2012-05-30",
                "byline": "JANET MASLIN",
                "book_title": "Gone Girl",
                "book_author": "Gillian Flynn",
                "summary": "“Gone Girl,” by Gillian Flynn, is a two-sided contest in which Nick and Amy Dunne tell conflicting stories.",
                "uuid": "00000000-0000-0000-0000-000000000000",
                "uri": "nyt://book/00000000-0000-0000-0000-000000000000",
                "isbn13": [
                    "9780297859383",
                    "9780297859390",
                    "9780297859406",
                    "9780307588364",
                    "9780307588371",
                    "9780307588388",
                    "9780385366755",
                    "9780553398380",
                    "9780553418354",
                    "9780553418361",
                    "9780606270175",
                    "9781410450951",
                    "9781594136054",
                ],
            },
        ],
    }

    if not reviews.get("results"):
        bot.send_message(chat_id, "😕 Рецензии не найдены. Попробуйте другое название.")

        return

    text, keyboard = reviews_menu_message(reviews=reviews["results"], page=page)

    if page == 0:
        # Для первой страницы - новое сообщение
        bot.send_message(
            chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode="HTML"
        )
    else:
        # Для последующих - редактируем существующее
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,  # Для callback-обработчика
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )


def setup_main_menu_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text == "📊 Список бестселлеров")
    def handle_bestsellers(message):
        """
        Обрабатывает кнопку со списком бестселлеров.
        """
        show_genres_page(bot=bot, chat_id=message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("genres_page:"))
    def handle_genres_pagination(call):
        """
        Обрабатывает кнопки переключение страниц пагинации с жанрами.
        """
        try:
            # Извлекаем номер страницы из callback_data
            page = int(call.data.split(":")[1])

            show_genres_page(
                bot=bot,
                chat_id=call.message.chat.id,
                page=page,
                message_id=call.message.message_id,  # Передаем ID сообщения для редактирования
            )

        except Exception:
            bot.answer_callback_query(
                call.id, "❌ Не удалось загрузить страницу", show_alert=True
            )

    @bot.message_handler(func=lambda msg: msg.text == "🔍 Поиск рецензий")
    def handle_reviews(message):
        """
        Обрабатывает кнопку поиска рецензий.
        """
        bot.send_message(
            chat_id=message.chat.id,
            text="📖 Введите название книги на английском для поиска:\n       (пример: 'Gone Girl')",
        )

        show_reviews_page(bot=bot, chat_id=message.chat.id, book_title="Gone Girl")

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(("review_prev:", "review_next:"))
    )
    def handle_reviews_pagination(call):
        """
        Обрабатывает кнопки переключение страниц с рецензиями.
        """
        try:
            direction, page = call.data.split(":")
            page = int(page)

            show_reviews_page(
                bot=bot,
                chat_id=call.message.chat.id,
                page=page,
                message_id=call.message.message_id,
            )

        except Exception:
            bot.answer_callback_query(
                call.id, "❌ Не удалось загрузить страницу REVIEWS", show_alert=True
            )
