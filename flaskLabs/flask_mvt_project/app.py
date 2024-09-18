import jwt
from flask import Flask
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from flask_migrate import Migrate

from config import Config
from models import User, Book,db

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('register'))

        # Create new user and hash password
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('Invalid email or password.')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    # Show the user's books
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html', books=books)


@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))

    users = User.query.all()
    books = Book.query.all()
    return render_template('admin_dashboard.html', users=users, books=books)


@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        image = request.files['image']
        image_data = image.read() if image else None

        # Create new book
        new_book = Book(title=title, author=author, image=image_data, user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added!')
        return redirect(url_for('dashboard'))

    return render_template('add_book.html')


@app.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized action.')
        return redirect(url_for('dashboard'))

    db.session.delete(book)
    db.session.commit()
    flash('Book removed.')
    return redirect(url_for('dashboard'))


# Additional JWT Protected Route Example
from flask_jwt_extended import jwt_required


@app.route('/api/secure-data', methods=['GET'])
@jwt_required()
def secure_data():
    return {"message": "This is a protected route!"}


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Set the login view for login manager
    login_manager.login_view = 'login'
    app.run()
