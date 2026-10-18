# Этап 3. Реализация механизмов защиты

## 1. Аутентификация и авторизация

### Хеширование паролей (Werkzeug pbkdf2:sha256)

```python
def set_password(self, password):
    self.password_hash = generate_password_hash(password)   # соль встроена автоматически

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

В БД пароли в открытом виде не хранятся. Алгоритм: **PBKDF2-HMAC-SHA256** с автоматической солью.

### Ограничение доступа по ролям (RBAC)

```python
@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        abort(403)
    ...
```

Матрица ролей: Гость / Ученик / Репетитор / Администратор.

---

## 2. Шифрование данных (Fernet / AES-128-CBC)

Конфиденциальные поля шифруются «на лету» перед сохранением в БД.

### Зашифрованные поля:
| Таблица | Поле | Тип защиты |
|---|---|---|
| `users` | `phone` | Fernet (симметричное) |
| `payments` | `transaction_ref` | Fernet (симметричное) |

```python
# encryption.py
fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    return fernet.decrypt(data.encode()).decode()
```

Через Python property шифрование/дешифрование прозрачно для кода маршрутов:

```python
payment.transaction_ref = transaction_id   # setter → encrypt_data()
print(payment.transaction_ref)             # getter → decrypt_data()
```

---

## 3. Защита от XSS в чатах и отзывах (bleach)

**Библиотека:** `bleach` — экранирует или удаляет HTML-теги из пользовательского ввода.

### В чате (`/chat/<lesson_id>`):

```python
import bleach

safe_content = bleach.clean(
    form.content.data,
    tags=[],      # никакие HTML-теги не разрешены
    strip=True    # теги удаляются, а не экранируются
)
msg = ChatMessage(..., content=safe_content)
```

### В отзывах (`/reviews/<tutor_id>`):

```python
safe_comment = bleach.clean(form.comment.data, tags=[], strip=True)
review = Review(..., comment=safe_comment)
```

**Двойная защита:**
1. **Серверная (bleach.clean):** теги удаляются до сохранения в БД.
2. **Шаблонная (Jinja2):** `{{ msg.content }}` автоматически экранирует `<`, `>`, `&`.

**Пример:** ввод `<script>alert(1)</script>` → в БД сохраняется `alert(1)`.

---

## 4. Защита платёжных транзакций

| Механизм | Реализация |
|---|---|
| Валидация суммы на сервере | `abs(form.amount - amount) > 0.01 → abort` |
| Шифрование ID транзакции | Fernet (AES-128) перед записью в БД |
| Проверка прав плательщика | `current_user.id != lesson.student_id → 403` |
| CSRF-защита формы | Flask-WTF: `{{ form.hidden_tag() }}` |
| Уникальный токен транзакции | `secrets.token_urlsafe(32)` |

```python
# Защита от подмены суммы через браузер (price tampering)
if abs(float(form.amount.data) - amount) > 0.01:
    flash('Ошибка: сумма платежа не совпадает. Транзакция отклонена.', 'danger')
    return redirect(...)

# Уникальный ID транзакции
transaction_id = secrets.token_urlsafe(32)

# Шифрование ID перед сохранением
payment.transaction_ref = transaction_id   # → Fernet.encrypt()
```

---

## 5. Безопасность сессий и защита от атак

### Cookie-параметры (`config.py`):

```python
SESSION_COOKIE_HTTPONLY = True   # недоступен из JavaScript (XSS-защита)
SESSION_COOKIE_SECURE = False    # True для HTTPS в продакшене
SESSION_COOKIE_SAMESITE = 'Lax' # защита от CSRF
```

### CSRF-токены во всех формах (Flask-WTF):

```html
<form method="post">
    {{ form.hidden_tag() }}   {# скрытое поле csrf_token #}
    ...
</form>
```

### SQL-инъекции:

Исключены через ORM (SQLAlchemy). Все запросы параметризованы:

```python
User.query.filter_by(email=form.email.data).first()
# → SELECT * FROM users WHERE email = ? -- значение подставляется безопасно
```
