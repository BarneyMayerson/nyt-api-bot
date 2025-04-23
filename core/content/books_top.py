from typing import List, Dict


def books_top_message(genre: str, books: List[Dict]) -> str:
    """
    Формирует сообщение со списком книг.

    Args:
        genre (str): выбранный жанр
        books (List): список книг.

    Returns:
        str: книги с указанием рейтинга, названия и автора.
    """
    book_list = "\n".join(
        [
            f"{book['rank']:02}. 📖 {book['title']} (<i>{book['author']}</i>)"
            for book in books
        ]
    )

    return f"Топ-{len(books)} в жанре <b>{genre}</b>:\n\n{book_list}"
