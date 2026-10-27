import unittest

import app as bookstore


class BookstoreApiTests(unittest.TestCase):
    def setUp(self):
        self.original_books = bookstore.books.copy()
        self.addCleanup(self.restore_books)
        self.client = bookstore.app.test_client()

    def restore_books(self):
        bookstore.books.clear()
        bookstore.books.update(self.original_books)

    def test_home_returns_api_info(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "message": "Online Bookstore REST API",
                "endpoints": {
                    "list_books": "GET /books",
                    "get_book": "GET /books/<id>",
                    "add_book": "POST /books",
                },
            },
        )

    def test_get_books_returns_json_inventory(self):
        response = self.client.get("/books")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.get_json(), list(bookstore.books.values()))

    def test_get_book_returns_matching_book(self):
        response = self.client.get("/books/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), bookstore.books[1])

    def test_get_missing_book_returns_404(self):
        response = self.client.get("/books/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Book not found."})

    def test_post_book_adds_valid_book(self):
        payload = {
            "title": "  Dune  ",
            "author": " Frank Herbert ",
            "price": 12.5,
        }

        response = self.client.post("/books", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                "id": max(self.original_books) + 1,
                "title": "Dune",
                "author": "Frank Herbert",
                "price": 12.5,
            },
        )
        self.assertIn(response.get_json()["id"], bookstore.books)

    def test_post_book_rejects_invalid_price(self):
        response = self.client.post(
            "/books",
            json={"title": "Dune", "author": "Frank Herbert", "price": -1},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Price must be a finite, non-negative number."},
        )

    def test_post_book_rejects_non_json_request(self):
        response = self.client.post("/books", data="not json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(), {"error": "Request body must be JSON."}
        )


if __name__ == "__main__":
    unittest.main()
