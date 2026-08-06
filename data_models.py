from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey

db = SQLAlchemy()


class Author(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    birth_date = Column(Date)
    date_of_death = Column(Date)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f'<ID: {self.id} Author: {self.name}>'


class Book(db.Model):
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    title = Column(String(50), nullable=False)
    publication_year = Column(Integer, nullable=False)
    isbn = Column(String(50))

    def __repr__(self):
        return f'<ID: {self.id} Book {self.title}>'
