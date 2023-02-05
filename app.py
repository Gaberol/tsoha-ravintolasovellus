from flask import render_template, request, redirect, url_for, session
from user import User
from restaurant import Restaurant
from index import app, db

@app.route('/')
def index():
    if 'username' in session:
        restaurants = Restaurant.query.all()
        return render_template('index.html', restaurants=restaurants)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['is_admin'] = user.is_admin
            return redirect(url_for('index'))
        return 'Invalid username/password'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('index'))

@app.route('/add_restaurant', methods=['GET', 'POST'])
def add_restaurant():
    if 'is_admin' in session and session['is_admin']:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            restaurant = Restaurant(name=name, description=description)
            db.session.add(restaurant)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('add_restaurant.html')
    return 'You are not authorized to access this page'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
