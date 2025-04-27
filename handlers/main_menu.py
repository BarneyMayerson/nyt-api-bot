from typing import Optional
from telebot import TeleBot
from core.content.genres import genres_menu_message
from core.content.reviews import reviews_menu_message
from services.cache import ReviewCache
from services.nyt_api import NYTBooksAPI

api = NYTBooksAPI()
genres = api.get_bestseller_genres()
review_cache = ReviewCache()


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
    book_title: str,
    page: int = 0,
    message_id: Optional[int] = None,
    force_api: bool = False,
):
    """
    Показывает страницу с жанрами.

    Args:
        bot (TeleBot): экземпляр бота.
        chat_id (int): ID чата.
        book_title (str):  название книги.
        page (int): номер страницы (начинается с 0).
        message_id (int): ID сообщения.
        force_api (bool): флаг принудительного запроса к API.
    """

    # Пытаемся получить данные из кэша (если не force_api)
    cached_reviews = (
        None
        if force_api
        else review_cache.get_reviews(chat_id=chat_id, book_title=book_title)
    )
    print(review_cache.get(chat_id=chat_id))
    print(f"cached_data = {cached_reviews}")

    if cached_reviews:
        print("Using cached data")
        reviews = cached_reviews
    else:
        print("Fetching from API")
        api_response = api.search_reviews(title=book_title)

        if not api_response.get("results"):
            bot.send_message(
                chat_id=chat_id,
                text="😕 Рецензии не найдены. Попробуйте другое название.",
            )

            return

        reviews = api_response["results"]
        review_cache.set(chat_id=chat_id, book_title=book_title, reviews=reviews)

    text, keyboard = reviews_menu_message(reviews=reviews, page=page)

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

        show_reviews_page(
            bot=bot,
            chat_id=message.chat.id,
            # book_title="1Q84",
            book_title="Gone Girl",
            force_api=True,
        )

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
            cached_data = review_cache.get(call.message.chat.id)

            if not cached_data:
                bot.answer_callback_query(
                    call.id, "❌ Данные устарели", show_alert=True
                )

                return

            show_reviews_page(
                bot=bot,
                chat_id=call.message.chat.id,
                book_title=cached_data["book_title"],
                page=page,
                message_id=call.message.message_id,
            )

        except Exception:
            bot.answer_callback_query(
                call.id, "❌ Не удалось загрузить страницу REVIEWS", show_alert=True
            )
