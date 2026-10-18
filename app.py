import secrets
import bleach
from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from extensions import db
import models
from models import User, TutorProfile, Lesson, Review, Chat, ChatMessage, Payment
from forms import (
    RegisterForm, LoginForm, ReviewForm, ChatMessageForm,
    BookLessonForm, SearchForm, PaymentForm
)

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


# ─────────────────────────────────────────────
# ПРОФИЛЬ
# ─────────────────────────────────────────────
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_profile = TutorProfile.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        new_bio = request.form.get('bio', '')
        if user_profile:
            user_profile.bio = new_bio
        else:
            user_profile = TutorProfile(user_id=current_user.id, subject='Не указан', hourly_rate=0, bio=new_bio)
            db.session.add(user_profile)
        db.session.commit()
        flash('Биография обновлена', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', profile=user_profile)


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
# ПАНЕЛЬ АДМИНИСТРАТОРА
# ─────────────────────────────────────────────
@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        abort(403)
    users = User.query.all()
    reviews_list = Review.query.order_by(Review.created_at.desc()).all()
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('admin.html', users=users, reviews=reviews_list, payments=payments)


@app.route('/admin/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    if current_user.role != 'admin':
        abort(403)
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Отзыв удалён.', 'success')
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)