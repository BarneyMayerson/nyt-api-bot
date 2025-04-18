from telebot import TeleBot


def setup_main_menu_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text == "📊 Список бестселлеров")
    def handle_bestsellers(message):
        bot.send_message(message.chat.id, "Загружаю список бестселлеров...")

    @bot.message_handler(func=lambda msg: msg.text == "🔍 Поиск рецензий")
    def handle_reviews(message):
        bot.send_message(message.chat.id, "Введите название книги для поиска рецензий:")
