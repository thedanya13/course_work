from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from extensions import db
import models
from models import User, TutorProfile
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Пользователь с таким email уже существует', 'danger')
            return redirect(url_for('register'))
        
        
        new_user = User(email=form.email.data, role='student')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/tutors')
def tutors():
    tutors_list = db.session.query(User, TutorProfile)\
        .join(TutorProfile, User.id == TutorProfile.user_id)\
        .filter(User.role == 'tutor')\
        .all()
    return render_template('tutors.html', tutors=tutors_list)

if __name__ == '__main__':
    app.run(debug=True)