# 🎓 TutorPlatform — Защищённая ИС «Онлайн-платформа репетиторов»

Курсовая работа по дисциплине **ТиМП**. Защищённое веб-приложение на стеке **Python / Flask / PostgreSQL**.

Тема: *Разработка защищённой информационной системы в сфере «Онлайн-платформа репетиторов»*.

---

## Ключевые возможности

- **Поиск преподавателей** — фильтрация по предмету и цене через ORM-запросы (нет SQL-инъекций).
- **Запись на урок** — студент выбирает репетитора и время, система создаёт урок и уникальную видеокомнату.
- **Видеосвязь** — интеграция с [Jitsi Meet](https://meet.jit.si); комната генерируется через `secrets.token_hex(8)`, доступ проверяется на сервере.
- **Календарь уроков** — интерактивный FullCalendar (месяц / неделя / список) + таблица с кнопками Видео / Чат / Оплатить.
- **Чат** — обмен сообщениями между учеником и репетитором в рамках урока.
- **Отзывы** — оценки и комментарии к преподавателям с модерацией администратором.
- **Оплата** — проведение транзакции с шифрованием ID и проверкой суммы на сервере.
- **Безопасные пароли** — соль + PBKDF2-HMAC-SHA256. В БД пароли в открытом виде не хранятся.
- **XSS-защита** — все пользовательские тексты (чат, отзывы) очищаются через `bleach.clean()` до сохранения в БД.
- **Шифрование данных** — телефоны и ID транзакций хранятся зашифрованными (Fernet / AES-128-CBC).
- **SQL-защита** — все запросы параметризованы через Flask-SQLAlchemy ORM.
- **CSRF** — Flask-WTF генерирует токен в каждой HTML-форме.
- **RBAC** — Гость / Ученик / Репетитор / Администратор, доступ к страницам проверяется декораторами.
- **Логирование** — сессии и транзакции фиксируются в БД.

---

## Структура проекта

```
course_work/
├── app.py                      Точка входа + все маршруты
├── models.py                   Модели БД (User, Lesson, Review, Chat, Payment)
├── forms.py                    WTForms-формы с CSRF-защитой
├── config.py                   Конфигурация (cookie, БД, ключи)
├── encryption.py               Fernet: шифрование/дешифрование полей
├── extensions.py               Инициализация SQLAlchemy
├── seed_db.py                  Заполнение БД тестовыми данными (5000+ записей)
├── requirements.txt            Зависимости Python
├── .env                        Секреты (не в git)
├── .gitignore
│
├── docs/
│   ├── Proekt.md               Этап 1: архитектура, матрица доступа, схема БД
│   ├── Etap2.md                Этап 2: базовый функционал, поиск, видео, календарь
│   └── Etap3_Zashita.md        Этап 3: механизмы ИБ (XSS, шифрование, CSRF...)
│
├── templates/
│   ├── base.html               Базовый шаблон (навигация, флеш-сообщения)
│   ├── index.html              Главная страница
│   ├── register.html           Регистрация
│   ├── login.html              Вход
│   ├── profile.html            Личный кабинет
│   ├── tutors.html             Поиск преподавателей
│   ├── book_lesson.html        Запись на урок
│   ├── calendar.html           Календарь уроков (FullCalendar)
│   ├── video_call.html         Видеозвонок (Jitsi Meet iframe)
│   ├── chat.html               Чат (с XSS-защитой)
│   ├── reviews.html            Отзывы (с XSS-защитой)
│   ├── payment.html            Оплата урока
│   └── admin.html              Панель администратора
│
└── static/
    └── css/
        └── style.css
```

---

## Быстрый старт

### Требования

- Python 3.10+
- PostgreSQL 14+

### Установка (Linux / macOS)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/thedanya13/course_work.git
cd course_work

# 2. Виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 3. Зависимости
pip install -r requirements.txt

# 4. Создать файл .env
cp .env.example .env   # или создать вручную (см. раздел ниже)

# 5. Заполнить БД тестовыми данными
python seed_db.py

# 6. Запустить
python app.py
```

### Установка (Windows)

```powershell
git clone https://github.com/thedanya13/course_work.git
cd course_work

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

# Создать .env (см. раздел ниже)

python seed_db.py
python app.py
```

Успешный запуск:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Файл `.env`

```dotenv
SECRET_KEY=замените-на-случайную-строку
DATABASE_URL=postgresql://user:password@localhost:5432/tutorplatform
ENCRYPTION_KEY=сгенерируется-автоматически-при-первом-запуске
```

> При первом запуске без `ENCRYPTION_KEY` в консоль выведется сгенерированный ключ — скопируйте его в `.env`.

---

## Стартовые пользователи

Создаются скриптом `seed_db.py`:

| Email | Пароль | Роль |
|---|---|---|
| `admin@tutor.ru` | `admin123` | admin |
| `tutor1@tutor.ru` | `tutor123` | tutor |
| `student1@tutor.ru` | `student123` | student |

---

## Безопасность

| Механизм | Реализация |
|---|---|
| Хеширование паролей | Соль + PBKDF2-HMAC-SHA256 (`werkzeug.security`) |
| Шифрование полей БД | Fernet / AES-128-CBC (`cryptography`) |
| XSS в чате и отзывах | `bleach.clean(tags=[], strip=True)` до записи в БД |
| SQL-инъекции | ORM-запросы Flask-SQLAlchemy (параметризация) |
| CSRF | Flask-WTF: скрытый токен в каждой форме |
| Защита сессионных cookie | `HttpOnly=True`, `SameSite=Lax` |
| RBAC | Проверка `current_user.role` + декоратор `@login_required` |
| Защита платежей | Серверная проверка суммы + шифрование ID транзакции |
| Уникальные токены | `secrets.token_urlsafe(32)` / `secrets.token_hex(8)` |
| Видеодоступ | Сервер проверяет участника урока перед показом комнаты |

**Для продакшена дополнительно:**
- Настроить HTTPS (TLS) и `SESSION_COOKIE_SECURE = True`.
- Ограничить rate-limit по IP (Flask-Limiter).
- Настроить CORS для конкретных доменов.
- Заменить Jitsi Meet публичный сервер на self-hosted.

---

## Тестирование безопасности

### Проверка XSS-защиты (чат / отзывы)

Введите в поле комментария или сообщения:

```
<script>alert('XSS')</script>
```

**Ожидаемый результат:** в БД сохранится строка `alert('XSS')` — теги удалены библиотекой `bleach`. Скрипт не выполняется.

### Проверка SQL-инъекций

```
Email: ' OR 1=1 --
Пароль: что угодно
```

**Ожидаемый результат:** `401 Неверный email или пароль` — ORM подставляет значение как параметр, не как часть запроса.

### Проверка RBAC

Попробуйте открыть `/admin` под учётной записью студента:

```
→ 403 Forbidden
```

Только пользователь с `role = 'admin'` получает доступ.

### Проверка защиты платежей (price tampering)

При попытке изменить сумму в форме оплаты через DevTools браузера:

```
→ "Ошибка: сумма платежа не совпадает. Транзакция отклонена."
```

Сумма берётся с сервера из профиля репетитора, а не из тела запроса.

---

## Решение проблем

### `sqlalchemy.exc.OperationalError` при запуске

**Причина:** PostgreSQL не запущен или неверные данные в `.env`.  
**Решение:** убедитесь, что PostgreSQL работает и `DATABASE_URL` указан верно.

### `cryptography.fernet.InvalidToken`

**Причина:** изменился `ENCRYPTION_KEY` в `.env` после того, как данные уже были зашифрованы.  
**Решение:** сбросьте базу данных и начните с чистого листа, либо верните старый ключ.

```bash
# Сбросить БД (PostgreSQL)
psql -U user -c "DROP DATABASE tutorplatform;"
psql -U user -c "CREATE DATABASE tutorplatform;"
python app.py  # пересоздаст таблицы
python seed_db.py
```

### `bleach` не установлен

```bash
pip install bleach==6.1.0
```

---

## Лицензия

Учебный проект. Сторонние библиотеки:
- [`Flask`](https://flask.palletsprojects.com/) — BSD.
- [`bleach`](https://github.com/mozilla/bleach) — Apache 2.0.
- [`cryptography`](https://cryptography.io/) — Apache 2.0 / BSD.
- [`FullCalendar`](https://fullcalendar.io/) — MIT.
- [`Jitsi Meet`](https://jitsi.org/) — Apache 2.0.
