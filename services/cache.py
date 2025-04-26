from time import time
from typing import Dict, List, Optional


class ReviewCache:
    def __init__(self):
        self._storage: Dict[int, Dict] = {}
        self._ttl = 3600
        print("Cache has been initiated.")

    def set(self, chat_id: int, reviews: Dict):
        self._storage[chat_id] = {"reviews": reviews, "expires": time() + self._ttl}

    def get(self, chat_id: int) -> Optional[List[Dict]]:
        data = self._storage.get(chat_id)

        if data and data["expires"] > time():
            return data["reviews"]

        return None

    def get_storage(self):
        return self._storage
