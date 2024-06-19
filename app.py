from flask import Flask, render_template, request, session, url_for, redirect, flash, abort, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash 
import logging

logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = 'static/img/resources'
app = Flask(__name__)
app.secret_key = 'gggforforgg' # Замените 'your_secret_key' на ваш секретный ключ
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Настройка подключения к MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Maxonbd15)'
app.config['MYSQL_DB'] = 'PlanBApp'

mysql = MySQL(app)

#################################################
# Глобальные функции
#################################################
def translate_account_type(account_type, org_name=None):
    curr_redirect_url = ''
    if account_type == 'employer':
        curr_redirect_url = 'personal_account'
    elif account_type == 'employee':
        curr_redirect_url = 'work'
    else:
        return False
    if org_name is not None:
        curr_redirect_url += '_org'
    return curr_redirect_url

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
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT u.id, u.login, ur.role_code, ur.role_name, o.org_name " +
                "FROM t_users AS u " +
                "JOIN t_user_roles AS ur ON u.account_type = ur.role_code " +
                "LEFT JOIN t_organization AS o ON u.id_org = o.id " +
                "WHERE u.login = %s AND u.password = %s", (login, password))
    user = cur.fetchone()
    if user:
        session['loggedin'] = True
        session['id'] = user[0]
        session['login'] = user[1]
        session['account_type'] = user[2]
        session['account_type_name'] = user[3]
        session['org_name'] = user[4]
        session['user_id'] = user[0]  # Сохраняем user_id в сессии
        flash('Login successful.')
        page = translate_account_type(user[2], user[4])
        if page:
            return redirect(url_for(page, org_name=user[4]))
    else:
        return abort(401)

@app.route('/register', methods=['GET','POST'])
def register():
    name = request.form.get('name')
    login = request.form.get('login')
    password = request.form.get('password')
    email = request.form.get('email')
    account_type = request.form.get('account_type')
    if not name or not login or not password or not email or not account_type:
        flash('Пожалуйста, заполните все поля')
        return abort(400)
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM t_users WHERE login = %s", (login,))
        user = cur.fetchall()
        if len(user) > 0:
            flash('Пользователь с таким логином уже существует.')
            return abort(400)
        else:
            # Маппинг ФИО (можно без отчества)
            try:
                fio_arr = name.split(' ')
                last_name = fio_arr[0]
                first_name = fio_arr[1]
                second_name = fio_arr[2]
            except ValueError:
                second_name = None
            cur.execute("INSERT INTO t_users (login, password, email, last_name, first_name, second_name, account_type) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                (login, password, email, last_name, first_name, second_name, account_type))
            mysql.connection.commit()
            cur.execute("SELECT role_name FROM t_user_roles WHERE role_code = %s", (account_type, ))
            account_type_name = cur.fetchone()[0]
            user_id = cur.lastrowid
            print(user_id)
            cur.close()
            flash('Registration successful.')
            login = request.form.get('login')
            password = request.form.get('password')
            cur = mysql.connection.cursor()
            cur.execute("SELECT u.id, u.login, ur.role_code, ur.role_name, o.org_name " +
                        "FROM t_users AS u " +
                        "JOIN t_user_roles AS ur ON u.account_type = ur.role_code " +
                        "LEFT JOIN t_organization AS o ON u.id_org = o.id " +
                        "WHERE u.login = %s AND u.password = %s", (login, password))
            user = cur.fetchone()
            if user:
                session['loggedin'] = True
                session['id'] = user[0]
                session['login'] = user[1]
                session['account_type'] = user[2]
                session['account_type_name'] = user[3]
                session['org_name'] = user[4]
                session['user_id'] = user[0]  # Сохраняем user_id в сессии
                flash('Login successful.')
                page = translate_account_type(user[2], user[4])
                if page:
                    return redirect(url_for(page, org_name=user[4]))
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
    

def get_organization_by_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT o.* FROM t_organization o JOIN t_users u ON o.id = u.id_org WHERE u.id = %s", (user_id,))
    organization = cur.fetchone()
    return organization

@app.route('/work', methods=['GET'])
def work():
    if 'loggedin' in session:
        user_id = session['id']
        invitations = get_invitations(user_id)
        organization = get_organization_by_user_id(user_id)
        print(invitations)
        print(organization)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM t_tasks WHERE id_fk = (SELECT id FROM t_organization WHERE org_name)")
        rows = cur.fetchall()
        tasks = [{'id': row[0], 'title': row[1], 'desc_text': row[2], 'date_deadline': row[3]} for row in rows]
        return render_template('work.html', invitations=invitations, organization=organization, tasks=tasks)
    else:
        flash('You must be logged in to view that page.')
        return redirect(url_for('home'))

@app.route('/add-task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    deadline = request.form.get('deadline')
    org_name = request.form.get('org_name')

    if not title or not description or not deadline or not org_name:
        flash('Please fill out all fields.')
        return redirect(request.referrer)

    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM t_organization WHERE org_name = %s", (org_name,))
    org_id = cur.fetchone()

    if not org_id:
        flash('Organization not found.')
        return redirect(request.referrer)

    cur.execute("INSERT INTO t_tasks (title, desc_text, date_deadline, id_fk) VALUES (%s, %s, %s, %s)",
            (title, description, deadline, org_id[0]))
    mysql.connection.commit()
    flash('Task added successfully.')
    return redirect(f'/personalaccount/{org_name}')


@app.route('/create_organization', methods=['POST'])
def create_organization():
    if 'user_id' not in session:
        flash('User not logged in')
        return redirect(url_for('login'))

    if request.method == 'POST':
        cur = mysql.connection.cursor()

        # Получение данных из формы
        org_name = request.form['org_name']
        org_desc = request.form['org_desc']
        org_num = request.form['legal_num']
        org_email = request.form['legal_email']

        cur.execute('SELECT id from t_users')

        id_user = session['user_id']  # Получение ID текущего пользователя из сессии
        cur.execute("INSERT INTO t_organization (org_name, org_desc, legal_num, legal_email, created_by) VALUES (%s, %s, %s, %s, %s)",
                    (org_name, org_desc, org_num, org_email, id_user))
        org_id = cur.lastrowid
        # Update the id_org column in the t_users table
        cur.execute("UPDATE t_users SET id_org = %s WHERE id = %s", (org_id, id_user))
        mysql.connection.commit()
        cur.execute("SELECT * FROM t_organization WHERE created_by = %s ORDER BY id DESC", (id_user,))
        organizations = cur.fetchone()
        # Получаем данные организации, которую только что создали
        cur.execute("SELECT org_name FROM t_organization WHERE created_by = %s ORDER BY id DESC LIMIT 1", (id_user,))
        organization = cur.fetchone()
        

        cur.close()

        if organization:
            session['org_name'] = organization[0]
            flash('Organization created successfully.')
            return redirect(url_for('personal_account_org', org_name=session['org_name']))
        else:
            flash('Failed to create organization.')
            return redirect(url_for('home'))


@app.route('/personalaccount/<org_name>', methods=['GET', 'POST'])
def personal_account_org(org_name):
    if session['loggedin'] is None:
        return redirect(url_for('home'))
    if session['org_name'] is None:
        return redirect(url_for('personal_account'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_tasks WHERE id_fk = (SELECT id FROM t_organization WHERE org_name = %s)", (org_name,))
    rows = cur.fetchall()
    tasks = [{'id': row[0], 'title': row[1], 'desc_text': row[2], 'date_deadline': row[3]} for row in rows]
    cur.execute("SELECT * FROM t_tasks WHERE id_fk = (SELECT id FROM t_organization WHERE org_name = %s)", (org_name,))
    return render_template('personalaccount.html', tasks=tasks)
    
@app.route('/work/<org_name>', methods=['GET', 'POST'])
def work_org(org_name):
    if session['loggedin'] is None:
        return redirect(url_for('home'))
    if session['org_name'] is None:
        return redirect(url_for('personal_account'))
    cur = mysql.connection.cursor()
    user_id = session['id']
    organization = get_organization_by_user_id(user_id)
    cur.execute("SELECT * FROM t_tasks WHERE id_fk = (SELECT id FROM t_organization WHERE org_name = %s)", (org_name,))
    rows = cur.fetchall()
    tasks = [{'id': row[0], 'title': row[1], 'desc_text': row[2], 'date_deadline': row[3]} for row in rows]
    cur.execute("SELECT * FROM t_tasks WHERE id_fk = (SELECT id FROM t_organization WHERE org_name = %s)", (org_name,))
    
    return render_template('work.html', tasks=tasks, organization=organization)

@app.route('/test-delete', methods=['POST'])
def test_delete():
    return 'OK', 200

@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM t_tasks WHERE id = %s", (task_id,))
        mysql.connection.commit()
        return 'OK', 200
    else:
        return 'Error: Invalid request', 400


@app.route('/send_invitation', methods=['POST'])
def send_invitation():
    employee_login = request.form.get('employee_login')
    # Проверяем, существует ли такой пользователь
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM t_users WHERE login = %s", (employee_login,))
    employee = cur.fetchone()
    if not employee:
        flash('Работник не найден.')
        return redirect(request.referrer)
    # Проверяем, есть ли у работника уже организация
    cur.execute("SELECT id_org FROM t_users WHERE login = %s", (employee_login,))
    employee_org = cur.fetchone()
    if employee_org[0]:
        flash('Работник уже состоит в организации.')
        return redirect(request.referrer)
    # Получаем идентификатор организации по имени из сессии
    org_name = session['org_name']
    cur.execute("SELECT id FROM t_organization WHERE org_name = %s", (org_name,))
    org = cur.fetchone()
    if not org:
        flash('Организация не найдена.')
        return redirect(request.referrer)
    org_id = org[0]

    # Отправляем заявку
    cur.execute("INSERT INTO t_invitations (from_user_id, to_user_id, organization_id, status) VALUES (%s, %s, %s, 'pending')",
                (session['id'], employee[0], org_id))
    mysql.connection.commit()
    flash('Приглашение отправлено.')
    return redirect(request.referrer)


@app.route('/accept_invitation/<int:invitation_id>', methods=['POST'])
def accept_invitation(invitation_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_invitations WHERE id = %s", (invitation_id,))
    invitation = cur.fetchone()
    if not invitation:
        return jsonify({'status': 'error', 'message': 'Invitation not found'}), 404

    # Обновляем данные пользователя, добавляем его в организацию
    cur.execute("UPDATE t_users SET id_org = %s WHERE id = %s", (invitation[3], session['id']))
    cur.execute("UPDATE t_invitations SET status = 'accepted' WHERE id = %s", (invitation[0],))
    mysql.connection.commit()

    # Получаем название организации из базы данных
    cur.execute("SELECT org_name FROM t_organization WHERE id = %s", (invitation[3],))
    org_name = cur.fetchone()[0]

    # Обновляем сессию с новым названием организации
    session['org_name'] = org_name

    # Проверяем, что у пользователя есть роль, которая соответствует странице, на которую мы хотим перенаправить
    if session['account_type'] == 'employee':
        # Если пользователь - работник, перенаправляем на страницу работы с учетом организации
        return redirect(url_for('work', org_name=org_name))
    else:
        # Если пользователь не является работником, перенаправляем на другую страницу (например, на личный кабинет)
        return redirect(url_for('personal_account'))

@app.route('/decline_invitation/<int:invitation_id>')
def decline_invitation(invitation_id):
    # Получаем информацию о заявке
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_invitations WHERE id = %s", (invitation_id,))
    invitation = cur.fetchone()
    if not invitation:
        flash('Заявка не найдена.')
        return redirect(request.referrer)
    # Обновляем статус заявки на "declined"
    cur.execute("UPDATE t_invitations SET status = 'declined' WHERE id = %s", (invitation_id,))
    mysql.connection.commit()
    flash('Заявка отклонена.')
    return redirect(request.referrer)


def get_invitations(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT i.*, u.login as from_user_login FROM t_invitations i JOIN t_users u ON i.from_user_id = u.id WHERE i.to_user_id = %s", (user_id,))
    invitations = cur.fetchall()
    return invitations

@app.route('/employees')
def employees():
    # Код для отображения employees.html
    return render_template('employees.html')

@app.route('/chat')
def chat():
    # Код для отображения chat.html
    return render_template('chat.html')

@app.route('/logout')
def logout():
    # Очист��а сессии
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('login', None)
    session.pop('account_type', None)
    session.pop('account_type_name', None)
    session.pop('org_name', None)
    # Перенаправление на главную страницу
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)

