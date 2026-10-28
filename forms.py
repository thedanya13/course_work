from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, TextAreaField,
                     IntegerField, FloatField, DateTimeLocalField, SelectField)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class SearchForm(FlaskForm):
    """Форма поиска преподавателя — GET-параметры, CSRF отключён для удобства."""
    subject = StringField('Предмет', validators=[Optional()])
    max_price = FloatField('Макс. цена (₽/час)', validators=[Optional()])
    submit = SubmitField('Найти')


class BookLessonForm(FlaskForm):
    """Форма записи на урок."""
    lesson_date = DateTimeLocalField('Дата и время урока',
                                     format='%Y-%m-%dT%H:%M',
                                     validators=[DataRequired()])
    submit = SubmitField('Записаться')


class ReviewForm(FlaskForm):
    """Форма отзыва. Поле comment очищается от XSS в маршруте."""
    rating = IntegerField('Оценка (1–5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Комментарий', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Оставить отзыв')


class ChatMessageForm(FlaskForm):
    """Форма сообщения чата. Поле content очищается от XSS в маршруте."""
    content = TextAreaField('Сообщение', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Отправить')


class PaymentForm(FlaskForm):
    """Форма оплаты урока. Сумма дополнительно проверяется на сервере."""
    amount = FloatField('Сумма (₽)', validators=[DataRequired()])
    submit = SubmitField('Оплатить')


class UserChangePasswordForm(FlaskForm):
    """Форма смены собственного пароля пользователем в профиле."""
    old_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6, message='Пароль должен содержать не менее 6 символов')])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('new_password', message='Пароли должны совпадать')])
    submit = SubmitField('Сменить пароль')


class AdminChangePasswordForm(FlaskForm):
    """Форма смены пароля администратором / овнером."""
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6, message='Пароль должен содержать не менее 6 символов')])
    submit = SubmitField('Сохранить пароль')


class ChangeRoleForm(FlaskForm):
    """Форма смены роли пользователя (доступно только супер-админу / овнеру)."""
    role = SelectField('Новая роль', choices=[
        ('student', 'Студент'),
        ('tutor', 'Преподаватель'),
        ('admin', 'Администратор'),
        ('owner', 'Супер-админ (Овнер)')
    ], validators=[DataRequired()])
    submit = SubmitField('Сохранить роль')