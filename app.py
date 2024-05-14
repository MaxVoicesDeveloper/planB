from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'gggforforgg' # Замените 'your_secret_key' на ваш секретный ключ

# Настройка подключения к MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'app_user'
app.config['MYSQL_PASSWORD'] = 'app_user'
app.config['MYSQL_DB'] = 'PlanBApp'

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
                cur.execute("SELECT * FROM t_users WHERE login = %s", [login])
                user = cur.fetchone()
                if user:
                    flash('Registration successful.')
                    session['loggedin'] = True
                    session['id'] = cur.lastrowid
                    session['login'] = login
                    return redirect(url_for('personal_account')) # Перенаправление на personal_account
                else:
                    # Маппинг ФИО (можно без отчества)
                    last_name = ''
                    first_name = ''
                    try:
                        last_name, first_name, second_name = name.split(' ')
                    except ValueError:
                        last_name, first_name = name.split(' ')
                        second_name = ''

                    cur.execute("INSERT INTO t_users (login, password, email, last_name, first_name, second_name) VALUES (%s, %s, %s, %s, %s, %s)", 
                                (login, password, email, last_name, first_name, second_name))
                    mysql.connection.commit()
                    flash('Registration successful.')
                    session['loggedin'] = True
                    session['id'] = cur.lastrowid
                    session['login'] = login
                    return redirect(url_for('personal_account')) # Перенаправление на personal_account
        elif action == 'login':
            login = request.form.get('login')
            password = request.form.get('password')
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM t_users WHERE login = %s AND password = %s", (login, password))
            user = cur.fetchone()
            if user:
                session['loggedin'] = True
                session['id'] = user[0]
                session['login'] = user[1]
                flash('Login successful.')
                return redirect(url_for('personal_account')) # Перенаправление на personal_account
    return render_template('index.html')

@app.route('/personalaccount')
def personal_account():
    if 'loggedin' in session:
        return render_template('personalaccount.html')
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