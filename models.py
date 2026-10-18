from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from encryption import encrypt_data, decrypt_data


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')

    # Телефон хранится зашифрованным (Fernet)
    _phone = db.Column('phone', db.String(256))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def phone(self):
        return decrypt_data(self._phone)

    @phone.setter
    def phone(self, value):
        self._phone = encrypt_data(value)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TutorProfile(db.Model):
    __tablename__ = 'tutor_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    bio = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('profile', uselist=False))


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    # Ссылка на комнату Jitsi Meet — генерируется при создании урока
    video_room = db.Column(db.String(128))

    tutor = db.relationship('User', foreign_keys=[tutor_id], backref='lessons_as_tutor')
    student = db.relationship('User', foreign_keys=[student_id], backref='lessons_as_student')


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    # comment хранится уже очищённым через bleach.clean() — XSS невозможен
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tutor = db.relationship('User', foreign_keys=[tutor_id])
    student_user = db.relationship('User', foreign_keys=[student_id])


# ──────────────────────────────────────────────
# Чат (защита от XSS: сообщения экранируются через bleach перед сохранением)
# ──────────────────────────────────────────────
class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship('ChatMessage', backref='chat', lazy='dynamic',
                               order_by='ChatMessage.sent_at')
    lesson = db.relationship('Lesson', backref=db.backref('chat', uselist=False))


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Текст сохраняется только после bleach.clean() — теги скриптов удаляются
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User')


# ──────────────────────────────────────────────
# Платёжные транзакции
# ──────────────────────────────────────────────
class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')   # pending / paid / failed
    # Номер транзакции хранится ЗАШИФРОВАННЫМ (Fernet) — данные платежа в БД не в открытом виде
    _transaction_ref = db.Column('transaction_ref', db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    lesson = db.relationship('Lesson', backref=db.backref('payment', uselist=False))
    payer = db.relationship('User')

    @property
    def transaction_ref(self):
        return decrypt_data(self._transaction_ref)

    @transaction_ref.setter
    def transaction_ref(self, value):
        self._transaction_ref = encrypt_data(value)