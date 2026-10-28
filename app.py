from datetime import datetime, timedelta, timezone
import secrets
import bleach
from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from extensions import db, csrf
import models
from models import User, TutorProfile, Lesson, Review, Chat, ChatMessage, Payment, UserSession
from forms import (
    RegisterForm, LoginForm, ReviewForm, ChatMessageForm,
    BookLessonForm, SearchForm, PaymentForm,
    UserChangePasswordForm, AdminChangePasswordForm, ChangeRoleForm
)


# Стартовые системные учетные записи:
# Owner (Супер-админ): owner@tutor.ru / owner123
# Admin (Администратор): admin@tutor.ru / admin123

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
csrf.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def ensure_system_accounts():
    """Гарантирует существование стартовых учетных записей (owner, admin, tutor1, student1)."""
    owner = User.query.filter_by(email='owner@tutor.ru').first()
    if not owner:
        owner = User(email='owner@tutor.ru', role='owner', phone='+79991110001')
        owner.set_password('owner123')
        db.session.add(owner)
    elif owner.role != 'owner':
        owner.role = 'owner'

    admin = User.query.filter_by(email='admin@tutor.ru').first()
    if not admin:
        admin = User(email='admin@tutor.ru', role='admin', phone='+79991110002')
        admin.set_password('admin123')
        db.session.add(admin)
    elif admin.role not in ('admin', 'owner'):
        admin.role = 'admin'

    tutor1 = User.query.filter_by(email='tutor1@tutor.ru').first()
    if not tutor1:
        tutor1 = User(email='tutor1@tutor.ru', role='tutor', phone='+79991110003')
        tutor1.set_password('tutor123')
        db.session.add(tutor1)
        db.session.flush()
        prof = TutorProfile(user_id=tutor1.id, subject='Математика и Информатика', hourly_rate=1500, bio='Опытный преподаватель высшей математики.')
        db.session.add(prof)

    student1 = User.query.filter_by(email='student1@tutor.ru').first()
    if not student1:
        student1 = User(email='student1@tutor.ru', role='student', phone='+79991110004')
        student1.set_password('student123')
        db.session.add(student1)

    db.session.commit()


with app.app_context():
    db.create_all()
    ensure_system_accounts()


# ─────────────────────────────────────────────
# ПРОВЕРКА СЕССИЙ С ТОКЕНОМ НА 5 МИНУТ
# ─────────────────────────────────────────────
@app.before_request
def validate_session():
    """
    Проверяет валидность токена сессии:
    1. Токен должен присутствовать в сессии.
    2. Сессия должна существовать в БД и быть активной (is_active=True).
    3. Время жизни токена — ровно 5 минут. При истечении или отзыве пользователь разлогинивается.
    """
    if request.endpoint in ('static', 'logout', 'login', 'register'):
        return

    if current_user.is_authenticated:
        token = session.get('auth_token')
        if not token:
            logout_user()
            session.pop('auth_token', None)
            flash('Сессия авторизации не найдена. Пожалуйста, войдите снова.', 'warning')
            return redirect(url_for('login'))

        user_sess = UserSession.query.filter_by(token=token).first()
        if not user_sess or not user_sess.is_active:
            logout_user()
            session.pop('auth_token', None)
            flash('Ваша сессия была завершена администратором или отозвана.', 'danger')
            return redirect(url_for('login'))

        if user_sess.is_expired():
            user_sess.is_active = False
            db.session.commit()
            logout_user()
            session.pop('auth_token', None)
            flash('Срок действия токена авторизации (5 минут) истек. Пожалуйста, войдите снова.', 'info')
            return redirect(url_for('login'))


@app.context_processor
def inject_session_info():
    """Предоставляет информацию о текущей сессии и оставшемся времени в шаблоны."""
    if current_user.is_authenticated:
        token = session.get('auth_token')
        if token:
            user_sess = UserSession.query.filter_by(token=token, is_active=True).first()
            if user_sess and not user_sess.is_expired():
                return {'current_session': user_sess}
    return {'current_session': None}


# ─────────────────────────────────────────────
# ГЛАВНАЯ
# ─────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ─────────────────────────────────────────────
# АВТОРИЗАЦИЯ
# ─────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
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
    if current_user.is_authenticated and request.method == 'GET':
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            logout_user()
            session.pop('auth_token', None)
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session.permanent = True
            
            # Генерация токена сессии с временем жизни ровно 5 минут
            token = secrets.token_urlsafe(32)
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            expires_at = now + timedelta(minutes=5)
            
            user_sess = UserSession(
                user_id=user.id,
                token=token,
                created_at=now,
                expires_at=expires_at,
                is_active=True,
                ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
                user_agent=request.user_agent.string[:255] if request.user_agent else None
            )
            db.session.add(user_sess)
            db.session.commit()
            
            session['auth_token'] = token
            flash('Авторизация успешна! Сессия активна с токеном на 5 минут.', 'success')
            return redirect(url_for('index'))
        flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    token = session.get('auth_token')
    if token:
        user_sess = UserSession.query.filter_by(token=token).first()
        if user_sess:
            user_sess.is_active = False
            db.session.commit()
    logout_user()
    session.pop('auth_token', None)
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))


# ─────────────────────────────────────────────
# ПРОФИЛЬ
# ─────────────────────────────────────────────
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_profile = TutorProfile.query.filter_by(user_id=current_user.id).first()
    password_form = UserChangePasswordForm()

    if request.method == 'POST' and 'update_bio' in request.form:
        new_bio = request.form.get('bio', '')
        safe_bio = bleach.clean(new_bio, tags=[], strip=True)
        if user_profile:
            user_profile.bio = safe_bio
        else:
            user_profile = TutorProfile(user_id=current_user.id, subject='Не указан', hourly_rate=0, bio=safe_bio)
            db.session.add(user_profile)
        db.session.commit()
        flash('Биография обновлена', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', profile=user_profile, password_form=password_form)


@app.route('/profile/change_password', methods=['POST'])
@login_required
def profile_change_password():
    """Смена собственного пароля пользователем (или админом)."""
    form = UserChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Неверный текущий пароль!', 'danger')
            return redirect(url_for('profile'))

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Ваш пароль успешно изменён!', 'success')
        return redirect(url_for('profile'))

    for error_list in form.errors.values():
        for error in error_list:
            flash(f'Ошибка: {error}', 'danger')
    return redirect(url_for('profile'))


# ─────────────────────────────────────────────
# ПОИСК ПРЕПОДАВАТЕЛЕЙ
# ─────────────────────────────────────────────
@app.route('/tutors')
def tutors():
    form = SearchForm(request.args, meta={'csrf': False})
    query = db.session.query(User, TutorProfile)\
        .join(TutorProfile, User.id == TutorProfile.user_id)\
        .filter(User.role == 'tutor')

    subject = request.args.get('subject', '').strip()
    max_price = request.args.get('max_price', '').strip()

    if subject:
        query = query.filter(TutorProfile.subject.ilike(f'%{subject}%'))
    if max_price:
        try:
            query = query.filter(TutorProfile.hourly_rate <= float(max_price))
        except ValueError:
            pass

    tutors_list = query.all()
    return render_template('tutors.html', tutors=tutors_list, form=form,
                           subject=subject, max_price=max_price)


# ─────────────────────────────────────────────
# ЗАПИСЬ НА УРОК (создание Lesson)
# ─────────────────────────────────────────────
@app.route('/book/<int:tutor_id>', methods=['GET', 'POST'])
@login_required
def book_lesson(tutor_id):
    tutor = User.query.get_or_404(tutor_id)
    if tutor.role != 'tutor':
        abort(404)
    form = BookLessonForm()
    if form.validate_on_submit():
        room_name = f"tutor-platform-{secrets.token_hex(8)}"
        lesson = Lesson(
            tutor_id=tutor.id,
            student_id=current_user.id,
            date=form.lesson_date.data,
            status='scheduled',
            video_room=room_name,
        )
        db.session.add(lesson)
        db.session.commit()
        flash('Урок успешно запланирован!', 'success')
        return redirect(url_for('calendar'))
    return render_template('book_lesson.html', form=form, tutor=tutor)


# ─────────────────────────────────────────────
# КАЛЕНДАРЬ УРОКОВ
# ─────────────────────────────────────────────
@app.route('/calendar')
@login_required
def calendar():
    if current_user.role == 'tutor':
        lessons = Lesson.query.filter_by(tutor_id=current_user.id).order_by(Lesson.date).all()
    else:
        lessons = Lesson.query.filter_by(student_id=current_user.id).order_by(Lesson.date).all()
    return render_template('calendar.html', lessons=lessons)


# ─────────────────────────────────────────────
# ВИДЕОСВЯЗЬ (Jitsi Meet)
# ─────────────────────────────────────────────
@app.route('/video/<int:lesson_id>')
@login_required
def video_call(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    # Доступ только участникам урока
    if current_user.id not in (lesson.tutor_id, lesson.student_id):
        abort(403)
    return render_template('video_call.html', lesson=lesson,
                           room=lesson.video_room)


# ─────────────────────────────────────────────
# ЧАТ (с защитой от XSS через bleach)
# ─────────────────────────────────────────────
@app.route('/chat/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def chat(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if current_user.id not in (lesson.tutor_id, lesson.student_id):
        abort(403)

    # Создаём чат-комнату, если её нет
    if not lesson.chat:
        new_chat = Chat(lesson_id=lesson.id)
        db.session.add(new_chat)
        db.session.commit()

    chat_obj = lesson.chat
    form = ChatMessageForm()

    if form.validate_on_submit():
        # ── XSS-защита: очищаем текст от HTML-тегов до сохранения в БД ──
        safe_content = bleach.clean(
            form.content.data,
            tags=[],          # никакие теги не разрешены
            strip=True
        )
        msg = ChatMessage(chat_id=chat_obj.id, sender_id=current_user.id, content=safe_content)
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('chat', lesson_id=lesson_id))

    messages = chat_obj.messages.all()
    return render_template('chat.html', lesson=lesson, messages=messages, form=form)


# ─────────────────────────────────────────────
# ОТЗЫВЫ (с защитой от XSS через bleach)
# ─────────────────────────────────────────────
@app.route('/reviews/<int:tutor_id>', methods=['GET', 'POST'])
@login_required
def reviews(tutor_id):
    tutor = User.query.get_or_404(tutor_id)
    form = ReviewForm()

    if form.validate_on_submit():
        # ── XSS-защита: очищаем комментарий перед сохранением ──
        safe_comment = bleach.clean(
            form.comment.data,
            tags=[],
            strip=True
        )
        review = Review(
            tutor_id=tutor.id,
            student_id=current_user.id,
            rating=form.rating.data,
            comment=safe_comment,
        )
        db.session.add(review)
        db.session.commit()
        flash('Отзыв опубликован!', 'success')
        return redirect(url_for('reviews', tutor_id=tutor_id))

    tutor_reviews = Review.query.filter_by(tutor_id=tutor_id)\
        .order_by(Review.created_at.desc()).all()
    return render_template('reviews.html', tutor=tutor, reviews=tutor_reviews, form=form)


# ─────────────────────────────────────────────
# ПЛАТЁЖНЫЕ ТРАНЗАКЦИИ
# ─────────────────────────────────────────────
@app.route('/pay/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def pay_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    # Только студент этого урока может платить
    if current_user.id != lesson.student_id:
        abort(403)

    # Проверяем, нет ли уже оплаченного платежа
    existing = Payment.query.filter_by(lesson_id=lesson.id, status='paid').first()
    if existing:
        flash('Этот урок уже оплачен.', 'info')
        return redirect(url_for('calendar'))

    tutor_profile = TutorProfile.query.filter_by(user_id=lesson.tutor_id).first()
    amount = tutor_profile.hourly_rate if tutor_profile else 0
    form = PaymentForm()

    if form.validate_on_submit():
        # Валидация суммы — защита от подмены суммы на клиенте
        if abs(float(form.amount.data) - amount) > 0.01:
            flash('Ошибка: сумма платежа не совпадает. Транзакция отклонена.', 'danger')
            return redirect(url_for('pay_lesson', lesson_id=lesson_id))

        # Генерация уникального ID транзакции (в реальной системе — ответ платёжного шлюза)
        transaction_id = secrets.token_urlsafe(32)

        payment = Payment(
            lesson_id=lesson.id,
            payer_id=current_user.id,
            amount=amount,
            status='paid',
        )
        # ── ID транзакции сохраняется ЗАШИФРОВАННЫМ в БД (Fernet) ──
        payment.transaction_ref = transaction_id

        lesson.status = 'paid'
        db.session.add(payment)
        db.session.commit()

        flash(f'Оплата успешна! Транзакция #{transaction_id[:12]}...', 'success')
        return redirect(url_for('calendar'))

    return render_template('payment.html', lesson=lesson, amount=amount, form=form)


# ─────────────────────────────────────────────
# ПАНЕЛЬ АДМИНИСТРАТОРА И ВЛАДЕЛЬЦА
# ─────────────────────────────────────────────
@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role not in ('admin', 'owner'):
        abort(403)
    users = User.query.order_by(User.id).all()
    reviews_list = Review.query.order_by(Review.created_at.desc()).all()
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    sessions = UserSession.query.order_by(UserSession.created_at.desc()).limit(100).all()
    return render_template(
        'admin.html',
        users=users,
        reviews=reviews_list,
        payments=payments,
        sessions=sessions
    )


@app.route('/admin/users/<int:user_id>/logout', methods=['POST'])
@login_required
def admin_logout_user(user_id):
    """
    Принудительный разлогин пользователя администратором или овнером.
    Админ может разлогинить только обычного пользователя (или себя).
    Овнер может разлогинить любого пользователя (включая админов).
    """
    if current_user.role not in ('admin', 'owner'):
        abort(403)

    target_user = User.query.get_or_404(user_id)
    if not current_user.can_logout_user(target_user):
        flash('Администратор не может разлогинить других администраторов и владельца!', 'danger')
        abort(403)

    # Деактивируем все активные сессии пользователя
    active_sessions = UserSession.query.filter_by(user_id=target_user.id, is_active=True).all()
    session_count = len(active_sessions)
    for s in active_sessions:
        s.is_active = False
    db.session.commit()

    # Если разлогинен текущий пользователь
    if target_user.id == current_user.id:
        logout_user()
        session.pop('auth_token', None)
        flash('Вы вышли из системы.', 'info')
        return redirect(url_for('login'))

    flash(f'Пользователь {target_user.email} успешно разлогинен (завершено активных сессий: {session_count}).', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/admin/sessions/<int:session_id>/revoke', methods=['POST'])
@login_required
def admin_revoke_session(session_id):
    """Отзыв конкретной сессии по ID токена."""
    if current_user.role not in ('admin', 'owner'):
        abort(403)

    sess = UserSession.query.get_or_404(session_id)
    target_user = sess.user
    if not current_user.can_logout_user(target_user):
        flash('Недостаточно прав для отзыва сессии этого пользователя!', 'danger')
        abort(403)

    sess.is_active = False
    db.session.commit()

    if sess.token == session.get('auth_token'):
        logout_user()
        session.pop('auth_token', None)
        flash('Ваша сессия была отозвана.', 'info')
        return redirect(url_for('login'))

    flash(f'Сессия #{sess.id} пользователя {target_user.email} успешно отозвана.', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/admin/users/<int:user_id>/change_password', methods=['POST'])
@login_required
def admin_change_password(user_id):
    """
    Смена пароля:
    - Админ может менять пароль себе и обычным юзерам,
      но НЕ может менять пароли других админов и овнера.
    - Овнер может менять пароль кому угодно.
    """
    if current_user.role not in ('admin', 'owner'):
        abort(403)

    target_user = User.query.get_or_404(user_id)
    if not current_user.can_manage_user(target_user):
        flash('Администратор не может менять пароль другим администраторам и владельцу!', 'danger')
        abort(403)

    new_password = request.form.get('new_password', '').strip()
    if len(new_password) < 6:
        flash('Пароль должен содержать минимум 6 символов!', 'danger')
        return redirect(url_for('admin_panel'))

    target_user.set_password(new_password)

    # При смене пароля отзываем существующие сессии целевого пользователя
    if target_user.id == current_user.id:
        current_token = session.get('auth_token')
        UserSession.query.filter(UserSession.user_id == target_user.id, UserSession.token != current_token).update({'is_active': False})
    else:
        UserSession.query.filter_by(user_id=target_user.id).update({'is_active': False})

    db.session.commit()
    flash(f'Пароль для {target_user.email} успешно изменён.', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """
    Удаление учетной записи:
    - Админ может удалять обычных юзеров, но НЕ может удалять других админов и овнера.
    - Овнер может удалять любых пользователей и админов (кроме прямого удаления самого себя).
    """
    if current_user.role not in ('admin', 'owner'):
        abort(403)

    target_user = User.query.get_or_404(user_id)
    if not current_user.can_delete_user(target_user):
        flash('Недостаточно прав для удаления этой учетной записи!', 'danger')
        abort(403)

    email = target_user.email

    # Каскадное удаление всех зависимых данных во избежание ошибок внешних ключей
    UserSession.query.filter_by(user_id=target_user.id).delete()

    lessons = Lesson.query.filter(
        (Lesson.tutor_id == target_user.id) | (Lesson.student_id == target_user.id)
    ).all()
    for lesson in lessons:
        Review.query.filter_by(lesson_id=lesson.id).delete()
        Payment.query.filter_by(lesson_id=lesson.id).delete()
        if lesson.chat:
            ChatMessage.query.filter_by(chat_id=lesson.chat.id).delete()
            db.session.delete(lesson.chat)
        db.session.delete(lesson)

    Review.query.filter((Review.student_id == target_user.id) | (Review.tutor_id == target_user.id)).delete()
    ChatMessage.query.filter_by(sender_id=target_user.id).delete()
    Payment.query.filter_by(payer_id=target_user.id).delete()
    TutorProfile.query.filter_by(user_id=target_user.id).delete()

    db.session.delete(target_user)
    db.session.commit()

    flash(f'Учетная запись {email} успешно удалена со всеми связанными данными.', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/admin/users/<int:user_id>/change_role', methods=['POST'])
@login_required
def admin_change_role(user_id):
    """Смена роли пользователя — доступно исключительно супер-админу (овнеру)."""
    if current_user.role != 'owner':
        flash('Только супер-админ (владелец) имеет право изменять роли пользователей!', 'danger')
        abort(403)

    target_user = User.query.get_or_404(user_id)
    new_role = request.form.get('role', '').strip()
    if new_role not in ('student', 'tutor', 'admin', 'owner'):
        flash('Недопустимая роль!', 'danger')
        return redirect(url_for('admin_panel'))

    if target_user.id == current_user.id and new_role != 'owner':
        flash('Владелец не может понизить свою собственную роль.', 'warning')
        return redirect(url_for('admin_panel'))

    old_role = target_user.role
    target_user.role = new_role
    db.session.commit()
    flash(f'Роль пользователя {target_user.email} успешно изменена с "{old_role}" на "{new_role}".', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/admin/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    if current_user.role not in ('admin', 'owner'):
        abort(403)
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Отзыв удалён.', 'success')
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)