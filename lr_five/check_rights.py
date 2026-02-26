from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def check_rights(action):
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Для доступа необходимо авторизироваться!', 'warning')
                return redirect(url_for('login_form'))
            allowed_roles = {
                'create_user': ['admin'],
                'edit_user': ['admin'],
                'view_user': ['admin'],
                'delete_user': ['admin'],
                'view_all_visit': ['admin'],
                'edit_me': ['admin', 'user'],
                'view_me': ['admin', 'user']
                #журнал посещений, только свой еще
            }
            required_roles = allowed_roles.get(action, [])
            if not any(current_user.has_role(role) for role in required_roles):
                flash('У вас недостаточно прав для доступа к данной странице!', 'warning')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator    
    