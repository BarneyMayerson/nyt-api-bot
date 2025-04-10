from loader import create_bot

if __name__ == "__main__":
    bot = create_bot()

    try:
        print("✅ Бот запущен! (Ctrl+C для остановки)")
        bot.polling(non_stop=True, skip_pending=True)
    except KeyboardInterrupt:
        print("\n🛑 Получен сигнал остановки...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        bot.stop_polling()
        print("🔴 Бот полностью остановлен")
