from flask import Flask, render_template, request, session, url_for, redirect, flash, abort
from flask_mysqldb import MySQL
#from werkzeug.security import generate_password_hash, check_password_hash 

app = Flask(__name__)
app.secret_key = 'gggforforgg' # Замените 'your_secret_key' на ваш секретный ключ

# Настройка подключения к MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'app_user'
app.config['MYSQL_PASSWORD'] = 'app_user'
app.config['MYSQL_DB'] = 'PlanBApp'

mysql = MySQL(app)

#################################################
# Глобальные функции
#################################################

def translate_account_type(account_type):
    if account_type == 'employer':
        return 'personal_account'
    elif account_type == 'employee':
        return 'work'
    else:
        return False
    
#################################################
# Функции перенаправлений Flask
#################################################

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
            cur.execute("SELECT u.id, u.login, ur.role_code, ur.role_name " +
                        "FROM t_users AS u, t_user_roles AS ur " +
                        "WHERE u.login LIKE %s AND u.password LIKE %s AND u.account_type = ur.role_code", (login, password))
            user = cur.fetchone()
            if user:
                session['loggedin'] = True
                session['id'] = user[0]
                session['login'] = user[1]
                session['account_type'] = user[2]
                session['account_type_name'] = user[3]
                flash('Login successful.')
                page = translate_account_type(user[2])
                if page:
                    return url_for(page) # Перенаправление на personal_account
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT u.id, u.login, ur.role_code, ur.role_name " +
                "FROM t_users AS u, t_user_roles AS ur " +
                "WHERE u.login LIKE %s AND u.password LIKE %s AND u.account_type = ur.role_code", (login, password))
    user = cur.fetchone()
    if user:
        session['loggedin'] = True
        session['id'] = user[0]
        session['login'] = user[1]
        session['account_type'] = user[2]
        session['account_type_name'] = user[3]
        flash('Login successful.')
        page = translate_account_type(user[2])
        if page:
            return redirect(url_for(page))
    else:
        return abort(401)

@app.route('/personalaccount', methods=['GET', 'POST'])
def personal_account():
    if 'loggedin' in session:
        if request.method == 'GET':
            return render_template('personalaccount.html')  # Передаем функцию в шаблон
    else:
        flash('You must be logged in to view that page.')
        return redirect(url_for('home'))
    
@app.route('/work', methods=['GET', 'POST'])
def work():
    if request.method == 'GET':
        return render_template('work.html')
    

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