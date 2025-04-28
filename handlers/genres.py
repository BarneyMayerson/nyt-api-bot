from typing import Optional
from telebot import TeleBot
from core.constants import Errors
from core.content.genres import genres_menu_message
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


def setup_genres_handler(bot: TeleBot):
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
                callback_query_id=call.id,
                text=Errors.FAILED_TO_LOAD_PAGE,
                show_alert=True,
            )
