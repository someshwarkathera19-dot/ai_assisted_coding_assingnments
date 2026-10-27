import math
from typing import TypedDict

from flask import Flask, jsonify, request


class Book(TypedDict):
    id: int
    title: str
    author: str
    price: int | float


app = Flask(__name__)

books: dict[int, Book] = {
    1: {
        "id": 1,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "price": 14.99,
    },
    2: {
        "id": 2,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "price": 9.99,
    },
}


@app.get("/")
def home():
    return jsonify(
        {
            "message": "Online Bookstore REST API",
            "endpoints": {
                "list_books": "GET /books",
                "get_book": "GET /books/<id>",
                "add_book": "POST /books",
            },
        }
    )


@app.get("/books")
def get_books():
    return jsonify(list(books.values()))


@app.get("/books/<int:book_id>")
def get_book(book_id: int):
    book = books.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found."}), 404
    return jsonify(book)


@app.post("/books")
def add_book():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    required_fields = {"title", "author", "price"}
    provided_fields = set(payload)
    missing_fields = sorted(required_fields - provided_fields)
    unknown_fields = sorted(provided_fields - required_fields)
    if missing_fields or unknown_fields:
        return jsonify(
            {
                "error": "Book must include only title, author, and price.",
                "missing_fields": missing_fields,
                "unknown_fields": unknown_fields,
            }
        ), 400

    title = payload["title"]
    author = payload["author"]
    price = payload["price"]

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title must be a non-empty string."}), 400
    if not isinstance(author, str) or not author.strip():
        return jsonify({"error": "Author must be a non-empty string."}), 400
    if (
        isinstance(price, bool)
        or not isinstance(price, (int, float))
        or (isinstance(price, float) and not math.isfinite(price))
        or price < 0
    ):
        return jsonify({"error": "Price must be a finite, non-negative number."}), 400

    book_id = max(books, default=0) + 1
    book: Book = {
        "id": book_id,
        "title": title.strip(),
        "author": author.strip(),
        "price": price,
    }
    books[book_id] = book
    return jsonify(book), 201


if __name__ == "__main__":
    app.run()
