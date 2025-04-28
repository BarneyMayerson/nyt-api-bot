from loader import create_bot
from core.constants import Messages

if __name__ == "__main__":
    bot = create_bot()

    try:
        print(Messages.BOT_STARTED)
        bot.polling(non_stop=True, skip_pending=True)
    except KeyboardInterrupt:
        print(Messages.BOT_GETTING_STOP)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        bot.stop_polling()
        print(Messages.BOT_STOPPED)
