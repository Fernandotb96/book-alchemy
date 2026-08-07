import os
from data_models import db, Author, Book
from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


def create_tables():
    """Create the database tables. Execute ONLY ONCE."""
    with app.app_context():
        db.create_all()


def parse_date(date_str):
    """Convert 'YYYY-MM-DD' into a date or None if empty."""
    if not date_str:
        return None
    return datetime.strptime(date_str, '%Y-%m-%d').date()


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Show the add-author form and handle new author submission."""
    if request.method == 'POST':
        name = request.form['name']
        birth_date = parse_date(request.form.get('birthdate'))
        date_of_death = parse_date(request.form.get('date_of_death'))

        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )
        db.session.add(new_author)
        db.session.commit()
        return render_template('add_author.html', message="Author added successfully!")

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Show the add-book form and handle new book submission."""
    authors = Author.query.all()

    if request.method == 'POST':
        title = request.form['title']
        publication_year = int(request.form['publication_year'])
        isbn = request.form.get('isbn', None)
        author_id = request.form['author_id']

        new_book = Book(
            title=title,
            publication_year=publication_year,
            isbn=isbn,
            author_id=author_id
        )
        db.session.add(new_book)
        db.session.commit()
        return render_template('add_book.html', message="Book added successfully!", authors=authors)

    return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    """Show the library's book list, with optional search and sorting."""
    sort_by = request.args.get('sort_by', 'title')
    search_query = request.args.get('search', '').strip()
    message = request.args.get('message')  # Comes from the delete redirect, if any

    query = Book.query

    if search_query:
        query = query.filter(Book.title.ilike(f'%{search_query}%'))

    if sort_by == 'author':
        books = query.join(Author).order_by(Author.name).all()
    else:
        books = query.order_by(Book.title).all()

    if search_query and not books and not message:
        message = f'No books found matching "{search_query}".'

    return render_template(
        'home.html',
        books=books,
        sort_by=sort_by,
        search_query=search_query,
        message=message
    )


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book by ID and its author if they have no other books left."""
    book = Book.query.get_or_404(book_id)
    book_title = book.title
    author = book.author

    db.session.delete(book)
    db.session.commit()

    # If the author has no other books left, delete the author too
    remaining_books = Book.query.filter_by(author_id=author.id).count()
    if remaining_books == 0:
        db.session.delete(author)
        db.session.commit()

    return redirect(url_for('home', message=f'Book "{book_title}" was successfully deleted.'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
