from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI (SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

# Create the database tables (run this once)
with app.app_context():
    db.create_all()

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Book API with ORM!"})

# Get all books
@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()  # Fetch all books from the database
    return jsonify([{"id": book.id, "title": book.title, "author": book.author} for book in books])

# Get a book by ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)  # Fetch book by ID
    if book:
        return jsonify({"id": book.id, "title": book.title, "author": book.author})
    return jsonify({"error": "Book not found"}), 404

# Add a new book
@app.route("/books", methods=["POST"])
def add_book():
    new_book = request.json
    title = new_book.get("title")
    author = new_book.get("author")
    
    if title and author:
        book = Book(title=title, author=author)
        db.session.add(book)  # Add book to the session
        db.session.commit()  # Commit the transaction
        return jsonify({"id": book.id, "title": book.title, "author": book.author}), 201
    return jsonify({"error": "Invalid data"}), 400

# Update a book by ID
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get(book_id)  # Fetch book by ID
    if book:
        data = request.json
        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        db.session.commit()  # Commit the transaction
        return jsonify({"id": book.id, "title": book.title, "author": book.author})
    return jsonify({"error": "Book not found"}), 404

# Delete a book by ID
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)  # Fetch book by ID
    if book:
        db.session.delete(book)  # Delete the book
        db.session.commit()  # Commit the transaction
        return jsonify({"message": "Book deleted"}), 200
    return jsonify({"error": "Book not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)