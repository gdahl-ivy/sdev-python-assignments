from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.title} written by {self.author} published by {self.publisher}"
    
    def to_json(self):
        return {'title': self.title, 'author': self.author, 'publisher': self.publisher}

@app.route('/')
def index():
    return 'Books API home page'

@app.route('/books')
def get_books():
    title_arg = request.args.get('title')
    author_arg = request.args.get('author')
    publisher_arg = request.args.get('publisher')

    query = Book.query
    if title_arg is not None:
        query = query.filter_by(title=title_arg)
    if author_arg is not None:
        query = query.filter_by(author=author_arg)
    if publisher_arg is not None:
        query = query.filter_by(publisher=publisher_arg)
    
    books = query.all()

    return {'books': list(map(Book.to_json, books))}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return book.to_json()

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(title=request.json['title'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return abort(404)
    db.session.delete(book)
    db.session.commit()
    return '', 204

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if book is None:
        return abort(404)
    book.title = request.json['title']
    book.author = request.json['author']
    book.publisher = request.json['publisher']
    db.session.commit()
    return '', 204

# .venv\Scripts\activate
# set FLASK_APP=M04 rest api tutorial.py
# set FLASK_ENV=development
# flask run