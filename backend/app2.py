from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# Create a Flask application
app = Flask(__name__)

# Configure the SQLite database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize SQLAlchemy
db = SQLAlchemy(app)

#classes

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.Text, nullable=False)

    @classmethod
    def get_max_loan_time(cls, book_type):
        if (book_type == '1'):
            return 10  # up to 10 days
        elif (book_type == '2'):
            return 5   # up to 5 days
        elif (book_type == '3'):
            return 2   # up to 2 days
        else:
            return None  # handle invalid book types gracefully

    def __repr__(self):
        return f"<Book(id={self.id}, name='{self.name}', author='{self.author}', year_published={self.year_published}, book_type='{self.book_type}')>"

# Define the Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', city='{self.city}', age={self.age})>"

# Define the Loan model
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.Text, nullable=False)
    return_date = db.Column(db.Text)

    customer = db.relationship('Customer', backref='loans')
    book = db.relationship('Book', backref='loans')

    def __repr__(self):
        return f"<Loan(id={self.id}, cust_id={self.cust_id}, book_id={self.book_id}, loan_date='{self.loan_date}', return_date='{self.return_date}')>"

# Create all tables in the database (if they don't exist)
with app.app_context():
    db.create_all()

#routes and endpoints
@app.route('/')
def home():
    return 'Hello, this is a test endpoint!'

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
