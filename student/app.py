
import math

from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample student records
students = [
    {"id": 1, "name": "sai", "course": "CSE"},
    {"id": 2, "name": "nikki", "course": "ECE"}
]

# Sample book inventory
books = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "price": 12.99},
    {"id": 2, "title": "Pride and Prejudice", "author": "Jane Austen", "price": 9.99}
]

# GET: Retrieve all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

# POST: Register a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Name and course are required"
        }), 400

    name = data.get('name')
    course = data.get('course')
    if (
        not isinstance(name, str)
        or not name.strip()
        or not isinstance(course, str)
        or not course.strip()
    ):
        return jsonify({
            "error": "Name and course are required"
        }), 400

    new_id = max(
        (student["id"] for student in students),
        default=0
    ) + 1

    new_student = {
        "id": new_id,
        "name": name.strip(),
        "course": course.strip()
    }

    students.append(new_student)

    return jsonify(new_student), 201


# GET: Retrieve all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200


# GET: Retrieve a specific book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((item for item in books if item["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book), 200


# POST: Add a book to the inventory
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "error": "Title, author, and a valid price are required"
        }), 400

    title = data.get('title')
    author = data.get('author')
    price = data.get('price')
    if (
        not isinstance(title, str)
        or not title.strip()
        or not isinstance(author, str)
        or not author.strip()
        or isinstance(price, bool)
        or not isinstance(price, (int, float))
        or not math.isfinite(price)
        or price < 0
    ):
        return jsonify({
            "error": "Title, author, and a valid price are required"
        }), 400

    new_id = max((book["id"] for book in books), default=0) + 1
    new_book = {
        "id": new_id,
        "title": title.strip(),
        "author": author.strip(),
        "price": price
    }
    books.append(new_book)
    return jsonify(new_book), 201


if __name__ == '__main__':
    app.run(debug=False)
