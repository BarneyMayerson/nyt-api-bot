from typing import List, Tuple
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Paginator:
    def __init__(
        self, data: List[any], items_per_page: int = 8, prefix: str = "page"
    ) -> None:
        self.data = data
        self.items_per_page = items_per_page
        self.prefix = prefix

    def _total_pages(self) -> int:
        """
        Вычисляет общее количество страниц.

        Returns:
            int: количество страниц.
        """
        return (len(self.data) + self.items_per_page - 1) // self.items_per_page

    def get_page(self, page: int = 0) -> Tuple[List[any], int]:
        """
        Получает элементы для страницы

        Args:
            page (int): Номер страницы.

        Returns:
            Tuple: (элементы_страницы, всего_страниц).
        """
        start = page * self.items_per_page
        end = start + self.items_per_page

        return self.data[start:end], self._total_pages()

    def create_keyboard(self, page: int = 0) -> InlineKeyboardMarkup:
        """
        Создает клавиатуру с простой пагинацией

        Args:
            page (int): Номер страницы

        Returns:
            InlineKeyboardMarkup: Готовую клавиатуру
        """
        kb = InlineKeyboardMarkup(row_width=2)
        _, total_pages = self.get_page(page)
        buttons = []

        if page > 0:
            buttons.append(
                InlineKeyboardButton("◀ Назад", callback_data=f"{self.prefix}:{page-1}")
            )

        if page < total_pages - 1:
            buttons.append(
                InlineKeyboardButton(
                    "Вперед ▶", callback_data=f"{self.prefix}:{page+1}"
                )
            )

        if buttons:
            kb.row(*buttons)

        return kb
