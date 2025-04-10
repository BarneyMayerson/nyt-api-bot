from typing import List, Dict

import requests

from config.config import Config


class NYTBooksAPI:
    """
    Клиент для работы с API книг The New York Times.
    Предоставляет доступ к спискам бестселлеров и рецензиям на книги.

    Attributes:
        BASE_URL (str): Базовый URL API NYT Books версии 3
    """

    BASE_URL = "https://api.nytimes.com/svc/books/v3"

    @staticmethod
    def get_bestseller_genres() -> List[str]:
        """
        Получает все доступные категории (жанры) бестселлеров из API NYT.

        Returns:
            List[str]: Алфавитный список названий категорий
                     (например, ['hardcover-fiction', 'travel'])

        Raises:
            requests.exceptions.HTTPError: Если запрос к API не удался
            requests.exceptions.Timeout: Если превышено время ожидания
        """
        url = f"{NYTBooksAPI.BASE_URL}/lists/names.json"
        response = requests.get(url, params={"api-key": Config.NYT_API_KEY}, timeout=10)
        response.raise_for_status()

        return [genre["list_name"] for genre in response.json()["results"]]

    @staticmethod
    def get_bestseller_list(genre: str) -> List[Dict]:
        """
        Получает текущий список бестселлеров для указанной категории.

        Args:
            genre (str): Название категории из get_bestseller_genres()
                       (например, 'hardcover-fiction')

        Returns:
            List[Dict]: Список книг, где каждая книга представлена словарём с ключами:
                - title (str): Название книги
                - author (str): Автор
                - publisher (str): Издательство
                - description (str): Описание
                - amazon_product_url (str): Ссылка на Amazon
                - и другие поля

        Raises:
            ValueError: Если указана несуществующая категория
            requests.exceptions.HTTPError: При ошибках API
        """
        url = f"{NYTBooksAPI.BASE_URL}/lists/current/{genre}.json"
        response = requests.get(url, params={"api-key": Config.NYT_API_KEY}, timeout=10)
        response.raise_for_status()

        return response.json()["results"]["books"]

    @staticmethod
    def search_reviews(title: str) -> Dict:
        """
        Ищет рецензии на книгу по её названию.

        Args:
            title (str): Название книги для поиска

        Returns:
            Dict: Структура данных с рецензиями, содержащая ключи:
                - status (str): Статус запроса
                - copyright (str): Информация об авторских правах
                - num_results (int): Количество найденных рецензий
                - results (List[Dict]): Список рецензий, каждая содержит:
                    - book_title (str): Название книги
                    - publication_dt (str): Дата публикации
                    - summary (str): Текст рецензии
                    - url (str): Ссылка на полную рецензию
                    - и другие поля

        Note:
            Может возвращать пустые результаты даже для существующих книг
        """
        url = f"{NYTBooksAPI.BASE_URL}/reviews.json"
        response = requests.get(
            url, params={"title": title, "api-key": Config.NYT_API_KEY}, timeout=10
        )
        response.raise_for_status()

        return response.json()
