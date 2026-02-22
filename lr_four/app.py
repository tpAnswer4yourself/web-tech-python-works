from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from models import Role, User, db
from database import init_db
from werkzeug.security import check_password_hash, generate_password_hash
import os
from validate_reg_data import validate_reg_data

app = Flask(__name__)
app.config['SECRET_KEY'] = '123123123'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'users.db')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app=app)
login_manager.login_view = 'login_form'
login_manager.login_message = 'Для доступа к запрашиваемой странице необходимо пройти процедуру аутентификации!'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user_from_bd(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/task')
def task():
    return render_template('task.html')

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        remember = request.form.get('rememberme') == 'on'
        
        existing_user: User = User.query.filter_by(login = login).first()
        if existing_user and existing_user.check_password(password):
            login_user(existing_user, remember=remember)
            flash('Авторизация прошла успешно!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль!', 'danger')
            return(render_template('login.html', method='GET'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def reg_form():
    if request.method == 'POST':
        login = request.form.get('login').strip()
        first_name = request.form.get('first_name').strip()
        last_name = request.form.get('last_name').strip()
        middle_name = request.form.get('middle_name').strip() or None
        password = request.form.get('password', '')
        
        errors = validate_reg_data(login, password, first_name, last_name, middle_name)
        
        if not errors:
            #ПРОВЕРКА НА СУЩЕСТВУЮЩЕГО ЮЗЕРА!
            existing_user = User.query.filter_by(login=login).first()
            if existing_user:
                flash('Логин уже занят! Попробуйте ввести другой!', 'danger')
                return render_template('register.html', method='GET')
            
            new_user = User(
                login = login,
                first_name = first_name,
                last_name = last_name,
                middle_name = middle_name
                )
            
            new_user.set_password(password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Вы зарегистрировались!', 'success')
                return redirect(url_for('login_form'))
        
            except ValueError as e:
                db.session.rollback()
                flash(f'Ошибка при регистрации: {str(e)}', 'danger')
                
        else:
            return render_template('register.html', errors=errors)
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из аккаунта!', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def my_profile():   
    user_info = {
        'id': current_user.id,
        'login': current_user.login,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'middle_name': current_user.middle_name,
        'role': current_user.role_id,
        'created_at': current_user.created_at
    }
    
    return (render_template('profile.html', user=user_info))

@app.route('/user/<int:user_id>')
def user_page(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    return (render_template('user.html', user=user))
    

if __name__ == '__main__':
    try:
        init_db(app)
        app.run(debug=True)
    except ValueError as e:
        print("Ошибка:", e)