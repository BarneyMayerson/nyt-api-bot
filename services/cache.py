import time
from typing import Dict, List, Optional


class ReviewCache:
    _instance = None
    _storage = {}

    def __new__(cls, ttl_seconds: int = 3600):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._ttl = ttl_seconds

        return cls._instance

    def __init__(self):
        pass

    def _clean_expired(self):
        """
        Удаляет просроченные записи.
        """
        now = time.time()
        expired_keys = [
            chat_id
            for chat_id, data in self._storage.items()
            if now - data["timestamp"] > self._ttl
        ]
        for key in expired_keys:
            del self._storage[key]

    def set(self, chat_id: int, book_title: str, reviews: Dict):
        """
        Сохраняет книгу и ее рецензии с timestamp.
        """
        self._clean_expired()  # Чистим перед добавлением
        self._storage[chat_id] = {
            "book_title": book_title,
            "reviews": reviews,
            "timestamp": time.time(),
        }

    def get(self, chat_id: int) -> Optional[Dict]:
        """Проверяет TTL перед возвратом данных"""
        data = self._storage.get(chat_id)

        if data and (time.time() - data["timestamp"] < self._ttl):
            return data

        return None

    def get_reviews(self, chat_id: int, book_title: str) -> Optional[List]:
        """
        Проверяет совпадение названия книги.
        """
        data = self.get(chat_id=chat_id)

        if data and data["book_title"] == book_title:
            return data["reviews"]

        return None

    def invalidate(self, chat_id: int = None):
        """
        Инвалидация кэша.
        """
        if chat_id is not None:
            self._storage.pop(chat_id, None)
        else:
            self._storage.clear()


review_cache = ReviewCache()
