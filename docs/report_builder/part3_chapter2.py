# -*- coding: utf-8 -*-

CHAPTER_2 = """# 2 ПРОЕКТНАЯ ЧАСТЬ. АРХИТЕКТУРА И МОДЕЛИРОВАНИЕ ЗАЩИЩЁННОЙ ИНФОРМАЦИОННОЙ СИСТЕМЫ

## 2.1 Общая трехуровневая архитектура системы

Проектирование защищённой информационной системы «TutorPlatform» базируется на принципах модульности, минимизации привилегий и разделения обязанностей (Separation of Concerns). Архитектура системы декомпозирована на три независимых взаимодействующих эшелона: уровень представления (Presentation Tier), уровень бизнес-логики и приложений (Application Logic Tier) и уровень хранения данных (Data Storage Tier).

На рисунке 2.1 представлена подробная схема взаимодействия компонентов трехуровневой архитектуры с выделением контуров безопасности и модулей защиты.

```mermaid
graph TD
    subgraph ClientTier["1. Клиентский уровень (Presentation Tier)"]
        Browser["Веб-браузер пользователя (Клиент)"]
        UI_Components["Bootstrap 5 UI + FullCalendar JS"]
        IframeJitsi["Jitsi Meet WebRTC IFrame"]
        Browser --> UI_Components
        Browser --> IframeJitsi
    end

    subgraph SecurityPerimeter["Контур безопасности HTTP / WSGI"]
        HTTPS_Term["TLS / HTTPS Защищенный канал"]
        CookieEngine["Безопасные Cookies: HttpOnly, Secure, SameSite=Lax"]
        CSRF_Engine["Flask-WTF CSRF Token Validator"]
    end

    subgraph AppTier["2. Уровень бизнес-логики (Application Logic Tier)"]
        FlaskCore["Ядро Flask (WSGI Application)"]
        LoginMgr["Flask-Login (Сессии и RBAC контроль)"]
        Router["Модуль маршрутизации и валидации (app.py)"]
        Sanitizer["XSS Санитайзер (bleach.clean)"]
        PaymentValidator["Валидатор сумм транзакций (Price Guard)"]
        CryptoEngine["Криптографический модуль (Fernet / AES-128-CBC)"]
        Hasher["Хеш-модуль паролей (PBKDF2-HMAC-SHA256)"]

        FlaskCore --> LoginMgr
        FlaskCore --> Router
        Router --> Sanitizer
        Router --> PaymentValidator
        Router --> CryptoEngine
        Router --> Hasher
    end

    subgraph DataTier["3. Уровень персистентных данных (Data Storage Tier)"]
        SQLAlchemyORM["Flask-SQLAlchemy ORM (Подготовленные запросы)"]
        PG_Database[("СУБД PostgreSQL 14+")]
        Tables[("Таблицы: users, tutor_profiles, lessons, reviews, chats, chat_messages, payments")]
        EncryptedFields[("Зашифрованные атрибуты: phone, transaction_ref, password_hash")]

        SQLAlchemyORM --> PG_Database
        PG_Database --> Tables
        Tables --> EncryptedFields
    end

    subgraph ExternalServices["Внешние доверенные сервисы"]
        JitsiMeetServer["Сервер Jitsi Meet (meet.jit.si) WebRTC / DTLS-SRTP"]
    end

    UI_Components <==> HTTPS_Term
    HTTPS_Term <==> CookieEngine
    CookieEngine <==> CSRF_Engine
    CSRF_Engine <==> FlaskCore

    Router <==> SQLAlchemyORM
    IframeJitsi <==> JitsiMeetServer
```

*Рисунок 2.1 – Трехуровневая архитектура защищенной веб-системы «TutorPlatform»*

Назначение и функции архитектурных уровней:
1. **Клиентский уровень (Presentation Tier).** Представляет собой адаптивный веб-интерфейс, функционирующий на стороне браузера пользователя (клиента). Реализован с использованием семантической разметки HTML5, стилей CSS3 (фреймворк Bootstrap 5) и скриптовых компонентов JavaScript. Для визуализации расписания интегрирована библиотека FullCalendar, формирующая интерактивные представления (сетка месяца, недели, список событий). Отображение видеоуроков осуществляется через изолированный контейнер `iframe`, взаимодействующий с медиасервером Jitsi Meet по защищенным WebRTC-каналам. Клиентская часть не содержит конфиденциальной бизнес-логики и не принимает авторизационных решений.
2. **Контур безопасности HTTP / WSGI.** Обеспечивает первичную фильтрацию и защиту сетевого трафика. Включает механизм сессионных cookie с жестко зафиксированными флагами безопасности: `HttpOnly = True` (запрет доступа к cookie из клиентского JavaScript, блокирующий кражу сессии через XSS), `SameSite = 'Lax'` (защита от несанкционированной отправки сессионных cookie при переходах со сторонних ресурсов, блокирующая CSRF), а также модуль сквозной валидации криптографических CSRF-токенов во всех POST-запросах.
3. **Уровень бизнес-логики (Application Logic Tier).** Центральный модуль системы на базе Python/Flask. Выполняет обработку маршрутов, диспетчеризацию запросов, контроль ролевой модели RBAC (декоратор `@login_required` и проверки `current_user.role`), санитизацию входящего текста библиотекой bleach, строгую сверку стоимости уроков, криптографические преобразования (симметричное шифрование Fernet и хеширование Werkzeug) и трансляцию бизнес-сущностей в ORM-модели.
4. **Уровень хранения данных (Data Storage Tier).** Реляционная база данных PostgreSQL под управлением Flask-SQLAlchemy. Доступ к базе данных изолирован от внешней сети и возможен исключительно через ORM с использованием параметризованных запросов. На физическом уровне данные разделены на открытые служебные атрибуты и зашифрованные поля, хранящие шифротексты персональных данных.

## 2.2 Ролевая модель доступа и матрица разграничения прав (RBAC)

Для обеспечения принципа наименьших привилегий (Principle of Least Privilege) в информационной системе спроектирована ролевая модель разграничения доступа (Role-Based Access Control, RBAC). Модель определяет четыре категории субъектов доступа:

1. **Гость (Guest) / Анонимный субъект.** Неаутентифицированный посетитель веб-сайта. Имеет право просматривать лендинговую страницу, каталог репетиторов и открытую информацию об их специализации и ценах. Доступ к контактным данным, бронированию, чатам, видеосвязи и оплате строго заблокирован.
2. **Ученик / Клиент (Student).** Аутентифицированный пользователь с ролью `student`. Обладает правами на заполнение собственного профиля, поиск преподавателей, подачу заявок на бронирование уроков, проведение безопасной оплаты, участие в запланированных видеоконференциях (только в рамках своих уроков), переписку в чате урока и публикацию отзывов с оценками.
3. **Репетитор / Преподаватель (Tutor).** Аутентифицированный пользователь с ролью `tutor`. Обладает расширенным профилем: указание преподаваемой дисциплины, почасовой ставки, профессиональной биографии. Имеет доступ к личному календарю занятий, участию в назначенных видеосессиях, общению в чатах с закрепленными учениками. Не имеет прав на покупку уроков у других репетиторов под данной учетной записью.
4. **Администратор (Admin).** Привилегированный субъект системы с ролью `admin`. Осуществляет мониторинг базы данных пользователей, аудит журнала финансовых транзакций (с дешифрованием идентификаторов транзакций для сверки), а также превентивную модерацию и безвозвратное удаление некорректных или спам-отзывов. Не имеет доступа к открытым паролям пользователей (пароли хранятся исключительно в виде односторонних хешей).

Формализованная матрица разграничения доступа субъектов к операциям и объектам информационной системы представлена в таблице 2.1.

*Таблица 2.1 – Матрица разграничения прав доступа (RBAC)*

| Объект / Операция системы | Гость | Ученик (Student) | Репетитор (Tutor) | Администратор (Admin) |
| :--- | :---: | :---: | :---: | :---: |
| **Просмотр главной страницы (`/`)** | ✅ | ✅ | ✅ | ✅ |
| **Регистрация нового аккаунта (`/register`)** | ✅ | ❌ | ❌ | ❌ |
| **Аутентификация в системе (`/login`)** | ✅ | ❌ | ❌ | ❌ |
| **Выход из системы (`/logout`)** | ❌ | ✅ | ✅ | ✅ |
| **Просмотр каталога преподавателей (`/tutors`)** | ✅ | ✅ | ✅ | ✅ |
| **Редактирование профиля/био (`/profile`)** | ❌ | ✅ (Базовый) | ✅ (Ставка/Био) | ❌ |
| **Бронирование урока (`/book/<id>`)** | ❌ | ✅ | ❌ | ❌ |
| **Просмотр персонального календаря (`/calendar`)** | ❌ | ✅ (Свои уроки) | ✅ (Свои уроки) | ❌ |
| **Доступ к видеокомнате (`/video/<id>`)** | ❌ | ✅ (Только участник) | ✅ (Только участник) | ❌ |
| **Обмен сообщениями в чате (`/chat/<id>`)** | ❌ | ✅ (Только участник) | ✅ (Только участник) | ❌ |
| **Оплата занятия (`/pay/<id>`)** | ❌ | ✅ (Только плательщик) | ❌ | ❌ |
| **Публикация отзыва (`/reviews/<id>`)** | ❌ | ✅ | ❌ | ❌ |
| **Доступ к панели управления (`/admin`)** | ❌ | ❌ | ❌ | ✅ |
| **Просмотр журнала оплат и сумм** | ❌ | ❌ | ❌ | ✅ |
| **Удаление/модерация отзывов** | ❌ | ❌ | ❌ | ✅ |

Управление жизненным циклом занятия и статусами платежей подчиняется строгой диаграмме состояний, представленной на рисунке 2.2.

```mermaid
stateDiagram-v2
    [*] --> Scheduled: Студент бронирует урок (/book)
    state Scheduled {
        [*] --> Unpaid: Урок внесен в календарь
        Unpaid --> VideoChatReady: Сгенерирована комната Jitsi
    }

    Scheduled --> Paid: Успешная оплата (/pay)\nСерверная сверка суммы
    state Paid {
        [*] --> TransactionEncrypted: Fernet шифрование ref
        TransactionEncrypted --> Confirmed: Статус lesson.status = 'paid'
    }

    Paid --> Completed: Урок проведен преподавателем
    Scheduled --> Cancelled: Отмена занятия участником
    Paid --> Cancelled: Отмена с возвратом средств

    Completed --> Reviewed: Студент оставляет отзыв (/reviews)
    Reviewed --> [*]
    Cancelled --> [*]
```

*Рисунок 2.2 – Диаграмма состояний жизненного цикла урока и оплаты*

Переход между состояниями контролируется серверной бизнес-логикой: невозможно оплатить уже оплаченный или отмененный урок, а доступ к видеокомнате строго ограничен участниками, зафиксированными в объекте `Lesson`.

## 2.3 Проектирование базы данных

База данных информационной системы «TutorPlatform» разработана в реляционной парадигме с обеспечением третьей нормальной формы (3NF), что исключает избыточность данных и аномалии модификации.

### Концептуальная и логическая модели

В системе выделено 7 основных сущностей:
1. `User` (Пользователи системы: логин, пароль, роль, зашифрованный телефон).
2. `TutorProfile` (Профиль преподавателя: дисциплина, почасовая ставка, биография).
3. `Lesson` (Занятие: преподаватель, студент, дата/время, статус, идентификатор видеокомнаты).
4. `Review` (Отзывы: репетитор, студент, числовая оценка, очищенный текст комментария).
5. `Chat` (Чат-комната, жестко привязанная к конкретному уроку).
6. `ChatMessage` (Сообщения чата: отправитель, время, санитизированный текст).
7. `Payment` (Финансовые транзакции: урок, плательщик, сумма, зашифрованный номер транзакции, статус).

Логическая взаимосвязь сущностей представлена на ER-диаграмме (рисунок 2.3).

```mermaid
erDiagram
    User ||--o| TutorProfile : "имеет профиль (1:1)"
    User ||--o{ Lesson : "ведет как tutor (1:N)"
    User ||--o{ Lesson : "посещает как student (1:N)"
    User ||--o{ Review : "получает отзывы (1:N)"
    User ||--o{ Review : "пишет отзывы (1:N)"
    User ||--o{ ChatMessage : "отправляет сообщения (1:N)"
    User ||--o{ Payment : "оплачивает (1:N)"

    Lesson ||--|| Chat : "содержит (1:1)"
    Lesson ||--o| Payment : "оплачивается через (1:1)"
    Lesson ||--o{ Review : "оценивается (1:N)"
    Chat ||--o{ ChatMessage : "состоит из (1:N)"

    User {
        int id PK
        string email UK "Индекс, NOT NULL"
        string password_hash "PBKDF2-HMAC-SHA256"
        string role "student / tutor / admin"
        string phone "Fernet AES-128 шифротекст"
        datetime created_at
    }

    TutorProfile {
        int id PK
        int user_id FK "UK, NOT NULL"
        string subject "Предмет, NOT NULL"
        float hourly_rate "Почасовая ставка"
        text bio "Очищенный bleach текст"
    }

    Lesson {
        int id PK
        int tutor_id FK "NOT NULL"
        int student_id FK "NOT NULL"
        datetime date "Дата и время"
        string status "scheduled / paid / completed"
        string video_room "Уникальный токен Jitsi"
    }

    Review {
        int id PK
        int tutor_id FK "NOT NULL"
        int student_id FK "NOT NULL"
        int lesson_id FK "NULLable"
        int rating "Оценка от 1 до 5"
        text comment "Санитизированный текст"
        datetime created_at
    }

    Chat {
        int id PK
        int lesson_id FK "UK, NOT NULL"
        datetime created_at
    }

    ChatMessage {
        int id PK
        int chat_id FK "NOT NULL"
        int sender_id FK "NOT NULL"
        text content "Санитизированный текст"
        datetime sent_at
    }

    Payment {
        int id PK
        int lesson_id FK "UK, NOT NULL"
        int payer_id FK "NOT NULL"
        float amount "Проверенная сумма"
        string status "pending / paid / failed"
        string transaction_ref "Fernet AES-128 шифротекст"
        datetime created_at
    }
```

*Рисунок 2.3 – ER-диаграмма реляционной базы данных платформы «TutorPlatform»*

### Физическая модель базы данных

Физическая модель описывает структуру таблиц, типы данных PostgreSQL, ограничения целостности и индексы.

*Таблица 2.2 – Спецификация таблицы `users` (Пользователи системы)*
| Имя атрибута | Тип данных PostgreSQL | Ограничения целостности | Назначение и безопасность |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | `PRIMARY KEY` | Уникальный суррогатный ключ пользователя |
| `email` | `VARCHAR(120)` | `NOT NULL, UNIQUE` | Учетный email, B-Tree индекс для быстрого логина |
| `password_hash` | `VARCHAR(256)` | `NOT NULL` | Стойкий хеш PBKDF2-HMAC-SHA256 с солью |
| `role` | `VARCHAR(20)` | `NOT NULL, DEFAULT 'student'` | Роль в системе (student, tutor, admin) |
| `phone` | `VARCHAR(256)` | `NULLABLE` | Зашифрованный номер телефона (Fernet ciphertext) |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Метка времени регистрации |

*Таблица 2.3 – Спецификация таблицы `tutor_profiles` (Профили преподавателей)*
| Имя атрибута | Тип данных PostgreSQL | Ограничения целостности | Назначение и безопасность |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | `PRIMARY KEY` | Уникальный ключ профиля |
| `user_id` | `INTEGER` | `NOT NULL, UNIQUE, FK -> users(id)` | Связь 1:1 с пользователем |
| `subject` | `VARCHAR(100)` | `NOT NULL` | Преподаваемый предмет (индексируется при поиске) |
| `hourly_rate` | `DOUBLE PRECISION` | `NOT NULL` | Базовая ставка за 60 минут занятия |
| `bio` | `TEXT` | `NULLABLE` | Описание репетитора, санитизированное через bleach |

*Таблица 2.4 – Спецификация таблицы `lessons` (Запланированные уроки)*
| Имя атрибута | Тип данных PostgreSQL | Ограничения целостности | Назначение и безопасность |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | `PRIMARY KEY` | Идентификатор урока |
| `tutor_id` | `INTEGER` | `NOT NULL, FK -> users(id)` | Внешний ключ преподавателя |
| `student_id` | `INTEGER` | `NOT NULL, FK -> users(id)` | Внешний ключ ученика |
| `date` | `TIMESTAMP` | `NOT NULL` | Дата и время проведения занятия |
| `status` | `VARCHAR(20)` | `DEFAULT 'scheduled'` | Статус урока: scheduled, paid, completed, cancelled |
| `video_room` | `VARCHAR(128)` | `NULLABLE` | Псевдослучайный идентификатор видеокомнаты |

*Таблица 2.5 – Спецификация таблицы `reviews` (Отзывы и рейтинги)*
| Имя атрибута | Тип данных PostgreSQL | Ограничения целостности | Назначение и безопасность |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | `PRIMARY KEY` | Идентификатор отзыва |
| `tutor_id` | `INTEGER` | `NOT NULL, FK -> users(id)` | Внешний ключ преподавателя |
| `student_id` | `INTEGER` | `NOT NULL, FK -> users(id)` | Внешний ключ автора отзыва |
| `lesson_id` | `INTEGER` | `NULLABLE, FK -> lessons(id)` | Ссылка на подтвержденный урок |
| `rating` | `INTEGER` | `NOT NULL, CHECK (rating BETWEEN 1 AND 5)` | Оценка по шкале от 1 до 5 звезд |
| `comment` | `TEXT` | `NULLABLE` | Отзыв, очищенный от HTML-тегов bleach |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Дата и время публикации |

*Таблица 2.6 – Спецификация таблицы `chats` и `chat_messages`*
| Таблица / Поле | Тип данных PostgreSQL | Ограничения целостности | Описание |
| :--- | :--- | :--- | :--- |
| **chats.id** | `SERIAL` | `PRIMARY KEY` | Идентификатор диалога |
| **chats.lesson_id** | `INTEGER` | `NOT NULL, UNIQUE, FK -> lessons(id)` | Привязка чата к конкретному уроку |
| **chat_messages.id** | `SERIAL` | `PRIMARY KEY` | Идентификатор сообщения |
| **chat_messages.chat_id**| `INTEGER` | `NOT NULL, FK -> chats(id)` | Внешний ключ диалога |
| **chat_messages.sender_id**| `INTEGER` | `NOT NULL, FK -> users(id)` | Автор сообщения |
| **chat_messages.content** | `TEXT` | `NOT NULL` | Текст сообщения (очищенный от XSS) |
| **chat_messages.sent_at** | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Метка времени отправки |

*Таблица 2.7 – Спецификация таблицы `payments` (Платёжные транзакции)*
| Имя атрибута | Тип данных PostgreSQL | Ограничения целостности | Назначение и безопасность |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | `PRIMARY KEY` | Идентификатор транзакции |
| `lesson_id` | `INTEGER` | `NOT NULL, UNIQUE, FK -> lessons(id)` | Оплачиваемый урок |
| `payer_id` | `INTEGER` | `NOT NULL, FK -> users(id)` | Внешний ключ плательщика (студента) |
| `amount` | `DOUBLE PRECISION` | `NOT NULL` | Сверенная с тарифом сумма списания |
| `status` | `VARCHAR(20)` | `DEFAULT 'pending'` | Статус платежа (pending, paid, failed) |
| `transaction_ref`| `VARCHAR(512)` | `NULLABLE` | Зашифрованный токен транзакции (Fernet) |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Время фиксации платежа |

## 2.4 Спецификация персональных данных и криптографическая схема защиты

В соответствии с требованиями Федерального закона № 152-ФЗ «О персональных данных», обрабатываемая в системе информация классифицирована по категориям конфиденциальности:
- **Общедоступные данные:** email (используется для входа и связи), преподаваемый предмет, почасовая ставка, текст биографии репетитора, публичные отзывы.
- **Данные ограниченного доступа (Персональные данные):** номера телефонов пользователей, хеши паролей, персональная история занятий и платежей.
- **Критически конфиденциальные данные:** идентификаторы платёжных транзакций (`transaction_ref`), связывающие систему с внешними банковскими шлюзами.

Для исключения утечки критических данных при прямом дампе базы данных спроектирована схема шифрования на прикладном уровне (Application-Level Field Encryption). В качестве криптографического стандарта выбрана спецификация Fernet из библиотеки `cryptography`.

Структура бинарного токена Fernet строго регламентирована и состоит из следующих полей:
$$\text{Fernet Token} = \text{Version (8 бит)} \parallel \text{Timestamp (64 бита)} \parallel \text{IV (128 бит)} \parallel \text{Ciphertext (переменная длина)} \parallel \text{HMAC (256 бит)}$$

Криптографические свойства используемой схемы:
1. **Симметричный ключ:** 256-битный составной ключ, закодированный в формате Base64 URL-safe. Первые 128 бит используются для кода аутентификации HMAC-SHA256, оставшиеся 128 бит служат ключом блочного шифра AES-128.
2. **Алгоритм шифрования:** AES (FIPS 197) в режиме сцепления блоков шифра CBC (Cipher Block Chaining). Для каждого нового шифрования генерируется непредсказуемый 16-байтный вектор инициализации ($IV$), что исключает совпадение шифротекстов для одинаковых телефонных номеров.
3. **Целостность и аутентичность:** Вычисление имитовставки HMAC-SHA256 по заголовку и шифротексту. Любая попытка несанкционированной модификации байтов зашифрованного поля в базе данных приводит к немедленной ошибке `cryptography.fernet.InvalidToken` и предотвращает обработку поврежденных данных.
4. **Безопасное хранение ключа:** Мастер-ключ шифрования `ENCRYPTION_KEY` никогда не сохраняется в кодовой базе репозитория и изолирован в защищённом конфигурационном файле окружения `.env`.

Интеграция шифрования в объектную модель SQLAlchemy реализована с помощью механизма свойств Python (`@property` и `@setter`), что обеспечивает абсолютную прозрачность для модулей бизнес-логики:
- При присвоении значения `user.phone = "+7 (999) 000-11-22"` вызывается метод-сеттер, шифрующий строку по алгоритму Fernet и сохраняющий шифротекст в закрытое поле `_phone`.
- При чтении атрибута `user.phone` метод-геттер извлекает шифротекст из `_phone`, дешифрует его с использованием секретного ключа и возвращает открытую строку.
- Прямой SQL-запрос `SELECT phone FROM users;` возвращает исключительно нечитаемый массив Base64-символов вида `gAAAAABm...`, гарантируя конфиденциальность при компрометации сервера БД.

## 2.5 Моделирование сценариев взаимодействия и защищённой видеосвязи

Для детального описания динамики функционирования системы разработаны диаграммы последовательности (Sequence Diagrams) для двух критически важных с точки зрения безопасности сценариев.

### Сценарий 1: Бронирование, серверная верификация суммы, оплата и генерация видеокомнаты

На рисунке 2.4 представлен процесс защищенного бронирования и проведения платежа с контролем Price Tampering.

```mermaid
sequenceDiagram
    autonumber
    actor Student as Ученик (Браузер)
    participant Flask as Сервер (Flask app.py)
    participant Validator as Валидатор сумм
    participant Fernet as Криптомодуль Fernet
    participant DB as СУБД PostgreSQL
    participant Jitsi as Сервер Jitsi Meet

    Student->>Flask: GET /book/12 (Выбор даты и репетитора)
    Flask->>DB: Запрос профиля репетитора (ставка 1500 руб.)
    DB-->>Flask: TutorProfile(hourly_rate=1500)
    Flask-->>Student: Отображение формы с CSRF-токеном

    Student->>Flask: POST /book/12 (Дата занятия + CSRF)
    Flask->>Flask: Генерация токена комнаты secrets.token_hex(8)
    Flask->>DB: INSERT into lessons (status='scheduled', video_room='tutor-platform-a1b2')
    DB-->>Flask: Lesson ID=45 сохранен
    Flask-->>Student: 302 Redirect -> /calendar

    Student->>Flask: POST /pay/45 (Попытка оплаты, amount=1500 + CSRF)
    Flask->>Validator: Сверка: |form.amount - tutor.rate| <= 0.01
    alt Сумма изменена злоумышленником (Price Tampering)
        Validator-->>Flask: Несовпадение суммы!
        Flask-->>Student: Flash('Ошибка: сумма не совпадает!') Abort
    else Сумма корректна
        Validator-->>Flask: Валидация успешна
        Flask->>Flask: Генерация transaction_id = secrets.token_urlsafe(32)
        Flask->>Fernet: encrypt_data(transaction_id)
        Fernet-->>Flask: Зашифрованный токен gAAAAAB...
        Flask->>DB: INSERT into payments (amount=1500, ref=gAAAAAB..., status='paid')
        Flask->>DB: UPDATE lessons SET status='paid' WHERE id=45
        Flask-->>Student: 302 Redirect -> /calendar ('Оплата успешна!')
    end

    Student->>Flask: GET /video/45 (Переход к видеоуроку)
    Flask->>Flask: Проверка доступа: current_user.id in (tutor_id, student_id)
    alt Чужой пользователь (IDOR атака)
        Flask-->>Student: HTTP 403 Forbidden
    else Участник урока
        Flask-->>Student: Рендеринг video_call.html (iframe room='tutor-platform-a1b2')
        Student->>Jitsi: WebRTC подключение по зашифрованному каналу
    end
```

*Рисунок 2.4 – Диаграмма последовательности бронирования, оплаты и входа в видеокомнату*

### Сценарий 2: Отправка сообщения в чат с двухконтурной нейтрализацией Stored XSS

На рисунке 2.5 проиллюстрирован механизм обработки входящих текстовых сообщений, исключающий сохранение и исполнение внедренного JavaScript-кода.

```mermaid
sequenceDiagram
    autonumber
    actor Attacker as Пользователь / Атакующий
    participant Browser as Клиентский браузер
    participant Route as Маршрут Flask (/chat/45)
    participant Bleach as Модуль bleach.clean()
    participant DB as СУБД PostgreSQL
    participant Jinja as Шаблонизатор Jinja2
    actor Victim as Ученик / Собеседник

    Attacker->>Browser: Ввод вредоносного пейлоада:\n<script>alert('XSS')</script>Привет!
    Browser->>Route: POST /chat/45 (content, CSRF-токен)
    Route->>Route: Проверка авторизации и участия в уроке
    Route->>Bleach: bleach.clean(content, tags=[], strip=True)
    Note over Bleach: Удаление дескрипторов <script> и </script>\nОстается чистый текст: "alert('XSS')Привет!"
    Bleach-->>Route: Безопасная строка: "alert('XSS')Привет!"
    Route->>DB: INSERT into chat_messages (content="alert('XSS')Привет!")
    DB-->>Route: Запись сохранена
    Route-->>Browser: 302 Redirect -> /chat/45

    Victim->>Route: GET /chat/45 (Загрузка чата)
    Route->>DB: SELECT * FROM chat_messages WHERE chat_id=...
    DB-->>Route: Список сообщений
    Route->>Jinja: Рендеринг шаблона chat.html
    Note over Jinja: Второй контур защиты:\nАвтоматическое экранирование символов &, <, >, "\n{{ msg.content }}
    Jinja-->>Victim: HTML-документ с безопасным текстом
    Note over Victim: Браузер отображает строку как обычный текст.\nСкрипт не исполняется, атака XSS полностью сорвана!
```

*Рисунок 2.5 – Диаграмма последовательности нейтрализации Stored XSS-атаки в чате*

Таким образом, спроектированные архитектурные решения и криптографические цепочки обеспечивают замкнутый контур безопасности, предотвращающий реализацию угроз на всех этапах жизненного цикла информации.
"""

print("Part 3: Chapter 2 defined successfully.")
