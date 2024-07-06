from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

# Create a Flask application
app = Flask(__name__)

# Configure the SQLite database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.Text, nullable=False)

    @classmethod
    def get_max_loan_time(cls, book_type):
        if book_type == '1':
            return 10  # up to 10 days
        elif book_type == '2':
            return 5   # up to 5 days
        elif book_type == '3':
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

# CRUD endpoints for Book
@app.route('/newbooks', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(name=data['name'], author=data['author'], year_published=data.get('year_published'), book_type=data['book_type'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.__repr__() for book in books])

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.__repr__())

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.json
    book = Book.query.get_or_404(id)
    book.name = data['name']
    book.author = data['author']
    book.year_published = data.get('year_published')
    book.book_type = data['book_type']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

# CRUD endpoints for Customer
@app.route('/newcustomers', methods=['POST'])
def create_customer():
    data = request.json
    new_customer = Customer(name=data['name'], city=data['city'], age=data.get('age'))
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.__repr__() for customer in customers])

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.__repr__())

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    customer = Customer.query.get_or_404(id)
    customer.name = data['name']
    customer.city = data['city']
    customer.age = data.get('age')
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

# CRUD endpoints for Loan
@app.route('/newloans', methods=['POST'])
def create_loan():
    data = request.json
    new_loan = Loan(cust_id=data['cust_id'], book_id=data['book_id'], loan_date=data['loan_date'], return_date=data.get('return_date'))
    db.session.add(new_loan)
    db.session.commit()
    return jsonify({'message': 'Loan created successfully'}), 201

@app.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    return jsonify([loan.__repr__() for loan in loans])

@app.route('/loans/<int:id>', methods=['GET'])
def get_loan(id):
    loan = Loan.query.get_or_404(id)
    return jsonify(loan.__repr__())

@app.route('/loans/<int:id>', methods=['PUT'])
def update_loan(id):
    data = request.json
    loan = Loan.query.get_or_404(id)
    loan.cust_id = data['cust_id']
    loan.book_id = data['book_id']
    loan.loan_date = data['loan_date']
    loan.return_date = data.get('return_date')
    db.session.commit()
    return jsonify({'message': 'Loan updated successfully'})

@app.route('/loans/<int:id>', methods=['DELETE'])
def delete_loan(id):
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()
    return jsonify({'message': 'Loan deleted successfully'})

# Define a test endpoint
@app.route('/')
def home():
    return 'Hello, this is a test endpoint!'

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
