from typing import Optional
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from core.constants import Errors, Messages, MenuButtons
from core.content.reviews import reviews_menu_message
from core.keyboards.main_menu import main_menu_kb
from services.cache import ReviewCache
from services.nyt_api import NYTBooksAPI

api = NYTBooksAPI()
review_cache = ReviewCache()
user_search_queries = {}


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

    if cached_reviews:
        reviews = cached_reviews
    else:
        api_response = api.search_reviews(title=book_title)

        if not api_response.get("results"):
            bot.send_message(
                chat_id=chat_id,
                text=Messages.REVIEWS_NOT_FOUND,
                reply_markup=main_menu_kb(),
            )

            return

        reviews = api_response["results"]
        review_cache.set(chat_id=chat_id, book_title=book_title, reviews=reviews)

    text, keyboard = reviews_menu_message(reviews=reviews, page=page)

    if page == 0:
        # Для первой страницы - новое сообщение
        bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        bot.send_message(
            chat_id=chat_id,
            text=Messages.SELECT_ACTION,
            reply_markup=main_menu_kb(),
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


def setup_reviews_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text == MenuButtons.REVIEWS)
    def handle_reviews(message: Message):
        """
        Обрабатывает кнопку поиска рецензий.
        """
        bot.send_message(
            chat_id=message.chat.id,
            text=Messages.ENTER_BOOK_TITLE,
            reply_markup=ReplyKeyboardRemove(),
        )

        bot.register_next_step_handler(message=message, callback=process_book_title)

    def process_book_title(message: Message):
        if message.text == "/cancel":
            bot.send_message(
                chat_id=message.chat.id,
                text=Errors.SEARCH_CANCELLED,
                reply_markup=main_menu_kb(),
            )

            return

        book_title = message.text.strip()

        if not book_title:
            bot.send_message(
                chat_id=message.chat.id,
                text=Errors.EMPTY_TITLE_NOT_ALLOWED,
                reply_markup=main_menu_kb(),
            )

            return

        if len(book_title) < 2:
            bot.send_message(
                chat_id=message.chat.id,
                text=Errors.TITLE_TOO_SHORT,
                reply_markup=main_menu_kb(),
            )

            return

        user_search_queries[message.chat.id] = book_title
        show_reviews_page(
            bot=bot,
            chat_id=message.chat.id,
            book_title=book_title,
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
                    callback_query_id=call.id,
                    text=Errors.DATA_OUT_OF_DATE,
                    show_alert=True,
                )

                return

            show_reviews_page(
                bot=bot,
                chat_id=call.message.chat.id,
                book_title=user_search_queries.get(call.message.chat.id),
                page=page,
                message_id=call.message.message_id,
            )

        except Exception:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text=Errors.FAILED_TO_LOAD_PAGE,
                show_alert=True,
            )
