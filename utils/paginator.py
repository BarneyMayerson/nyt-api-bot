from typing import List, Tuple
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Paginator:
    def __init__(
        self,
        data: List[any],
        items_per_page: int = 8,
        prefix: str = "page",
        callback_prefix: str = "item",
    ) -> None:
        self.data = data
        self.items_per_page = items_per_page
        self.prefix = prefix
        self.callback_prefix = callback_prefix

    def _total_pages(self) -> int:
        """
        Вычисляет общее количество страниц.

        Returns:
            int: количество страниц.
        """
        return (len(self.data) + self.items_per_page - 1) // self.items_per_page

    def _make_simple_pagination_keyboard(self, page: int = 0) -> InlineKeyboardMarkup:
        """
        Создает клавиатуру с простой пагинацией.

        Args:
            page (int): номер страницы.

        Returns:
            InlineKeyboardMarkup: готовую клавиатуру.
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

    def get_page(self, page: int = 0) -> Tuple[List[any], int]:
        """
        Получает элементы для страницы.

        Args:
            page (int): номер страницы.

        Returns:
            Tuple: (элементы_страницы, всего_страниц).
        """
        start = page * self.items_per_page
        end = start + self.items_per_page

        return self.data[start:end], self._total_pages()

    def create_keyboard(self, page: int = 0) -> InlineKeyboardMarkup:
        """
        Создает полную клавиатуру с элементами и пагинацией.

        Args:
            page (int): номер страницы.

        Returns:
            InlineKeyboardMarkup: готовую клавиатуру.
        """
        kb = InlineKeyboardMarkup(row_width=2)
        page_items, _ = self.get_page(page=page)

        for item in page_items:
            kb.add(
                InlineKeyboardButton(
                    text=item,
                    callback_data=f"{self.callback_prefix}:{item}",
                )
            )

        # Добавляем пагинацию
        pagination_kb = self._make_simple_pagination_keyboard(page)
        if pagination_kb.keyboard:
            kb.row(*pagination_kb.keyboard[0])

        return kb
