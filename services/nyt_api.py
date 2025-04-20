from typing import List, Dict
from functools import cache
import time

import requests

from config.config import Config


class NYTAPIError(Exception):
    """Кастомное исключение для ошибок API NYT"""

    pass


class NYTBooksAPI:
    """
    Клиент для работы с API книг The New York Times.
    Предоставляет доступ к спискам бестселлеров и рецензиям на книги.
    """

    def __init__(self) -> None:
        self.base_url = "https://api.nytimes.com/svc/books/v3"
        self.genres_endpoint = "/lists/names.json"
        self.genre_endpoint = "/lists/current/{genre}.json"
        self.review_endpoint = "/reviews.json"
        self._last_cache_reset = time.time()

    @cache
    def _get_genres_cached(self) -> List[str]:
        """
        Получает и кеширует все доступные категории (жанры) бестселлеров из API NYT.

        Returns:
            List[str]: Алфавитный список названий категорий
                     (например, ['hardcover-fiction', 'travel'])

        Raises:
            NYTAPIError: При ошибках API с деталями из ответа
        """
        response = self._api_request(method_endswith=self.genres_endpoint)

        return [genre["list_name"] for genre in response["results"]]

    def _api_request(self, method_endswith: str, **kwargs) -> Dict:
        """
        Базовый метод для выполнения запросов к NYT API.

        Args:
            method_endswith (str): Конечная часть URL (например, "/lists/names.json")
            **kwargs: Дополнительные параметры запроса

        Returns:
            Dict: Ответ API в формате JSON

        Raises:
            NYTAPIError: При ошибках API с деталями из ответа
        """
        url = f"{self.base_url}{method_endswith}"
        params = {"api-key": Config.NYT_API_KEY}

        if "params" in kwargs:
            params.update(kwargs["params"])

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # Хорошо бы учесть, что здесь может быть прокинута ошибка

            return response.json()
        except requests.exceptions.HTTPError as http_err:
            msg = f"Ошибка при обращении к NYT API: {http_err}"
            raise NYTAPIError(msg) from http_err

        except requests.exceptions.Timeout:
            raise NYTAPIError("Превышено время ожидания ответа от NYT API") from None

    def get_bestseller_genres(self, force_refresh: bool = False) -> List[str]:
        """
        Получает жанры с кэшированием на 12 часов

        Args:
            force_refresh: Принудительно обновить кэш

        Returns:
            Список жанров
        """
        # Сбрасываем кэш если прошло 12 часов или принудительное обновление
        if force_refresh or (
            time.time() - self._last_cache_reset > 43200
        ):  # 12 часов = 43200 секунд
            self._get_genres_cached.cache_clear()
            self._last_cache_reset = time.time()

        return self._get_genres_cached()

    def get_bestseller_list(self, genre: str) -> List[Dict]:
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
            NYTAPIError: При ошибках API с деталями из ответа
        """
        genre_endpoint = self.genre_endpoint.format(genre=genre)  # Подставили жанр
        response = self._api_request(method_endswith=genre_endpoint)  # Получили ответ

        return response["results"]["books"]

    def search_reviews(self, title: str) -> Dict:
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

        Raises:
            NYTAPIError: При ошибках API с деталями из ответа

        Note:
            Может возвращать пустые результаты даже для существующих книг
        """
        return self._api_request(
            method_endswith=self.review_endpoint, params={"title": title}
        )
