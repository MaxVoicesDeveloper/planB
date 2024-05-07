from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'gggforforgg' # Замените 'your_secret_key' на ваш секретный ключ

# Настройка подключения к MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Maxonbd15)'
app.config['MYSQL_DB'] = 'PlanB'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'register':
            name = request.form.get('name')
            login = request.form.get('login')
            password = request.form.get('password')
            email = request.form.get('email')
            if not name or not login or not password or not email:
                flash('Please fill out all fields.')
            else:
                cur = mysql.connection.cursor()
                # Проверка наличия пользователя с таким логином
                cur.execute("SELECT * FROM users WHERE login = %s", [login])
                user = cur.fetchone()
                if user:
                    flash('Login already exists. Please choose a different one.')
                else:
                    cur.execute("INSERT INTO users (name, login, password, email) VALUES (%s, %s, %s, %s)", (name, login, password, email))
                    mysql.connection.commit()
                    flash('Registration successful.')
                    # Автоматический вход в систему после регистрации
                    session['loggedin'] = True
                    session['id'] = cur.lastrowid # Используйте ID последней вставленной строки
                    session['login'] = login
                    return redirect(url_for('home'))
        elif action == 'login':
            login = request.form.get('login')
            password = request.form.get('password')
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE login = %s AND password = %s", (login, password))
            user = cur.fetchone()
            if user:
                session['loggedin'] = True
                session['id'] = user[0]
                session['login'] = user[1]
                flash('Login successful.')
                return redirect(url_for('home'))
            else:
                flash('Login unsuccessful. Please check your login details.')
    return render_template('index.html')

@app.route('/logout')
def logout():
    # Очистка сессии
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('login', None)
    # Перенаправление на главную страницу
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)