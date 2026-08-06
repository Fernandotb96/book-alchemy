from data_models import db, Author, Book
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


# For creating the tables, we must execute the next two lines ONLY ONCE
# with app.app_context():
#     db.create_all()


def parse_date(date_str):
    """Convert 'YYYY-MM-DD' into a date or None if empty."""
    if not date_str:
        return None
    return datetime.strptime(date_str, '%Y-%m-%d').date()


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
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


if __name__ == '__main__':
    app.run(debug=True)
