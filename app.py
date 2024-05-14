from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
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
            account_type = request.form.get('account_type')
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE login = %s OR email = %s", (login, email))
            if cur.fetchone():
                return jsonify(success=False, message='Логин или почта уже существуют')
            cur.execute("INSERT INTO users (name, login, password, email, account_type) VALUES (%s, %s, %s, %s, %s)", (name, login, password, email, account_type))
            mysql.connection.commit()
            flash('Registration successful.')
            session['loggedin'] = True
            session['id'] = cur.lastrowid
            session['login'] = login
            session['account_type'] = account_type  # Сохраняем тип аккаунта в сессии
            return jsonify(success=True, message='Регистрация успешна', redirect_url=url_for('personal_account'))
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
                session['account_type'] = user[4]  # Загружаем тип аккаунта из базы данных
                flash('Login successful.')
                return jsonify(success=True, message='Вход в систему успешен', redirect_url=url_for('personal_account'))
            else:
                flash('Login unsuccessful.')
                return jsonify(success=False, message='Неверный логин или пароль')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

def translate_account_type(account_type):
    if account_type == 'employer':
        return 'Работодатель'
    elif account_type == 'employee':
        return 'Работник'
    else:
        return 'Неизвестный тип аккаунта'

@app.route('/personalaccount')
def personal_account():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT account_type FROM users WHERE login = %s", (session['login'],))
        account_type = cur.fetchone()[0]
        session['account_type'] = account_type  # Сохраняем тип аккаунта в сессии
        return render_template('personalaccount.html', translate_account_type=translate_account_type)  # Передаем функцию в шаблон
    else:
        flash('You must be logged in to view that page.')
        return redirect(url_for('home'))

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