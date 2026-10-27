import unittest

import app as student_api


class StudentApiTests(unittest.TestCase):
    def setUp(self):
        self.original_students = [
            student.copy() for student in student_api.students
        ]
        self.original_books = [
            book.copy() for book in student_api.books
        ]
        self.client = student_api.app.test_client()

    def tearDown(self):
        student_api.students[:] = self.original_students
        student_api.books[:] = self.original_books

    def test_get_students_returns_seeded_students_as_json(self):
        response = self.client.get('/students')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.original_students)

    def test_post_students_creates_student_and_returns_json(self):
        response = self.client.post(
            '/students',
            json={"name": "  Alex  ", "course": "  CSE  "}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {"id": 3, "name": "Alex", "course": "CSE"}
        )
        self.assertEqual(student_api.students[-1], response.get_json())

    def test_post_students_rejects_non_object_json(self):
        response = self.client.post(
            '/students',
            json=[{"name": "Alex", "course": "CSE"}]
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Name and course are required"}
        )

    def test_post_students_rejects_missing_or_blank_fields(self):
        for payload in (
            {"name": "Alex"},
            {"name": "  ", "course": "CSE"},
            {"name": "Alex", "course": 42},
        ):
            with self.subTest(payload=payload):
                response = self.client.post('/students', json=payload)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {"error": "Name and course are required"}
                )

    def test_get_books_returns_inventory_as_json(self):
        response = self.client.get('/books')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.original_books)

    def test_get_book_returns_matching_book_as_json(self):
        response = self.client.get('/books/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.original_books[0])

    def test_get_book_returns_json_404_for_unknown_id(self):
        response = self.client.get('/books/999')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Book not found"})

    def test_post_books_adds_book_and_returns_json(self):
        response = self.client.post(
            '/books',
            json={"title": "  Dune  ", "author": "  Frank Herbert  ", "price": 15.5}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                "id": 3,
                "title": "Dune",
                "author": "Frank Herbert",
                "price": 15.5
            }
        )
        self.assertEqual(student_api.books[-1], response.get_json())

    def test_post_books_rejects_invalid_book_data(self):
        for payload in (
            [{"title": "Dune", "author": "Frank Herbert", "price": 15.5}],
            {"title": "Dune", "author": "Frank Herbert"},
            {"title": "Dune", "author": "Frank Herbert", "price": True},
            {"title": " ", "author": "Frank Herbert", "price": 15.5},
        ):
            with self.subTest(payload=payload):
                response = self.client.post('/books', json=payload)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {
                        "error": "Title, author, and a valid price are required"
                    }
                )


if __name__ == '__main__':
    unittest.main()
