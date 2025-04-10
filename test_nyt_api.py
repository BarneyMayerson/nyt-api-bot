from services.nyt_api import NYTBooksAPI
import json


def test_nyt_api():
    """Комплексное тестирование NYT Books API с проверкой всех основных функций"""
    print("\n=== Начинаем тестирование NYT Books API ===")

    try:
        # 1. Тест получения жанров
        print("\n[1/3] Тестируем получение списка жанров...")
        genres = NYTBooksAPI.get_bestseller_genres()

        assert isinstance(genres, list), "Ожидался список жанров"
        assert len(genres) > 0, "Список жанров пуст"
        print(f"  Успешно! Получено {len(genres)} жанров")
        print("   Примеры жанров:", ", ".join(genres[:3]))

        # 2. Тест получения книг
        print("\n[2/3] Тестируем получение списка книг...")
        test_genre = (
            genres[0] if "hardcover-fiction" not in genres else "hardcover-fiction"
        )
        books = NYTBooksAPI.get_bestseller_list(test_genre)

        assert isinstance(books, list), "Ожидался список книг"
        assert len(books) > 0, "Список книг пуст"
        print(f"  Успешно! Получено {len(books)} книг в жанре '{test_genre}'")

        first_book = books[0]
        print("   Первая книга:")
        print(f"   Название: {first_book.get('title')}")
        print(f"   Автор: {first_book.get('author')}")
        print(f"   Описание: {first_book.get('description', '')[:50]}...")

        # 3. Тест поиска рецензий
        print("\n[3/3] Тестируем поиск рецензий...")
        test_title = "gone girl"
        reviews = NYTBooksAPI.search_reviews(test_title)

        assert isinstance(reviews, dict), "Ожидался словарь с результатами"
        print(f"  Успешно! Получены данные рецензий для '{test_title}'")
        print(f"   Найдено результатов: {reviews.get('num_results', 0)}")

        if reviews.get("results"):
            first_review = reviews["results"][0]
            print("   Пример рецензии:")
            print(f"   Дата: {first_review.get('publication_dt')}")
            print(f"   Ссылка: {first_review.get('url')}")

    except AssertionError as ae:
        print(f"  Ошибка проверки: {ae}")
    except Exception as e:
        print(f"  Критическая ошибка: {type(e).__name__}: {e}")
    else:
        print("\n=== Все тесты успешно пройдены! ===")
    finally:
        print("\n=== Тестирование завершено ===")


if __name__ == "__main__":
    test_nyt_api()
