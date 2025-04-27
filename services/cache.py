import time
from typing import Dict, List, Optional


class ReviewCache:
    def __init__(self):
        self._storage: Dict[int, Dict] = {}
        self._ttl = 3600

    def set(self, chat_id: int, book_title: str, reviews: Dict):
        """Сохраняет книгу и ее рецензии с timestamp"""
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
        """Проверяет совпадение названия книги"""
        data = self.get(chat_id=chat_id)

        if data and data["book_title"] == book_title:
            return data["reviews"]

        return None

    def get_storage(self):
        return self._storage
