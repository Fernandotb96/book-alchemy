# Book Alchemy 📚

A small Flask + SQLAlchemy web application for managing a personal library of
books and authors.

This project was built as a hands-on exercise for the **MSIT programming
course**, to practice and review core concepts of **Flask**,
**SQLAlchemy (ORM)**, and **Object-Oriented Programming (OOP)** in a small,
end-to-end web application.

## Features

- Add authors (name, birthdate, optional date of death)
- Add books (title, publication year, optional ISBN, linked to an author)
- View all books in a clean, card-based layout
- Search books by title
- Sort books by title or by author
- Delete a book — if it was the author's last remaining book, the author is
  removed too

## Tech Stack

- **Python 3**
- **Flask** — web framework and routing
- **Flask-SQLAlchemy** — ORM for modeling and querying the database
- **SQLite** — lightweight file-based database
- **Jinja2** — HTML templating
- **HTML / CSS** — no frontend framework, plain custom styling

## Project Structure

```
book_alchemy/
├── app.py              # Flask app: routes and request handling
├── data_models.py       # SQLAlchemy ORM models: Author and Book
├── static/
│   └── style.css        # Styling for all pages
├── templates/
│   ├── home.html         # Book list, search and sort
│   ├── add_author.html   # Form to add a new author
│   └── add_book.html     # Form to add a new book
└── data/
    └── library.sqlite    # SQLite database (created at runtime)
```

## Data Model

The app uses two related SQLAlchemy models, defined as Python classes in
`data_models.py`:

- **`Author`** — `id`, `name`, `birth_date`, `date_of_death`
- **`Book`** — `id`, `title`, `publication_year`, `isbn`, `author_id`

Each `Book` belongs to one `Author`, and each `Author` can have many `Book`s
(a one-to-many relationship, set up via `db.relationship` / `backref`).

## Setup & Installation

1. **Clone the repository** and move into the project folder.

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install flask flask-sqlalchemy
   ```

4. **Create the database tables** (only needed once, on the first run). 
   In `app.py`, execute the following function:
   ```python
   create_tables()
   ```
   Run the function once so the `data/library.sqlite` file and its tables get
   created, then run the program again to populate the database with some
   initial data.


5. **Run the app**:
   ```bash
   python app.py
   ```

6. Open your browser at **http://localhost:5000**.

## Usage

- Go to `/add_author` to register a new author.
- Go to `/add_book` to add a new book and link it to an existing author.
- The home page (`/`) lists all books, and lets you search by title or sort
  by title/author using the links at the top.
- Each book card has a **Delete** button to remove it from the library.

## About This Project

This is a learning project built to practice:

- Modeling real-world entities (`Author`, `Book`) as Python classes with
  SQLAlchemy's ORM, including relationships between tables
- Building a multipage app with Flask routing and `GET`/`POST` request
  handling
- Rendering dynamic HTML with Jinja2 templates
- Basic CRUD operations (Create, Read, Delete) against a relational database

As a course project, it intentionally keeps some things simple — for
example, there's minimal input validation and no authentication or CSRF
protection. These would be good next steps for anyone extending it beyond a
learning context.