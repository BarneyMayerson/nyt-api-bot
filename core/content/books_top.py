from typing import List, Dict


def books_top_message(genre: str, books: List[Dict]) -> str:
    book_list = "\n".join(
        [
            f"{book['rank']:02}. 📖 {book['title']} (<i>{book['author']}</i>)"
            for book in books
        ]
    )

    return f"Топ-{len(books)} в жанре <b>{genre}</b>:\n\n{book_list}"
