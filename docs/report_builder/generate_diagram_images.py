# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMG_DIR = '/home/pdvdanya/Agy_Projects/Me/Course_work/docs/report_builder/images'
os.makedirs(IMG_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def draw_fig_1_1():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
    ax.axis('off')
    
    # Subgraph backgrounds
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.55), 0.45, 0.42, boxstyle="round,pad=0.02", fc="#EBF5FB", ec="#2980B9", lw=1.5))
    ax.text(0.04, 0.93, "Ученик (Клиент)", fontsize=11, fontweight='bold', color="#1B4F72")
    
    ax.add_patch(patches.FancyBboxPatch((0.52, 0.55), 0.45, 0.42, boxstyle="round,pad=0.02", fc="#FEF9E7", ec="#F39C12", lw=1.5))
    ax.text(0.54, 0.93, "Репетитор (Сотрудник)", fontsize=11, fontweight='bold', color="#7D6608")
    
    ax.add_patch(patches.FancyBboxPatch((0.02, 0.05), 0.58, 0.45, boxstyle="round,pad=0.02", fc="#EAFAF1", ec="#27AE60", lw=1.5))
    ax.text(0.04, 0.46, "Защищенная платформа TutorPlatform", fontsize=11, fontweight='bold', color="#145A32")
    
    ax.add_patch(patches.FancyBboxPatch((0.65, 0.05), 0.32, 0.45, boxstyle="round,pad=0.02", fc="#FDEDEC", ec="#E74C3C", lw=1.5))
    ax.text(0.67, 0.46, "Администратор", fontsize=11, fontweight='bold', color="#78281F")
    
    # Client boxes
    boxes_client = [
        (0.05, 0.82, "1. Поиск репетитора по предмету и цене"),
        (0.05, 0.73, "2. Бронирование даты и слота урока"),
        (0.05, 0.64, "3. Оплата и видеосвязь Jitsi Meet")
    ]
    for x, y, t in boxes_client:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.39, 0.065, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#3498DB", lw=1))
        ax.text(x+0.015, y+0.02, t, fontsize=8.5, color="#2C3E50")
        
    # Tutor boxes
    boxes_tutor = [
        (0.55, 0.82, "1. Профиль, ставка и предмет"),
        (0.55, 0.73, "2. Контроль расписания (FullCalendar)"),
        (0.55, 0.64, "3. Проведение видеоурока и чат")
    ]
    for x, y, t in boxes_tutor:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.39, 0.065, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#F1C40F", lw=1))
        ax.text(x+0.015, y+0.02, t, fontsize=8.5, color="#2C3E50")

    # Platform boxes
    boxes_plat = [
        (0.05, 0.36, "Параметризованный поиск репетиторов (ORM SQL)"),
        (0.05, 0.26, "Серверная верификация цены и Fernet-шифрование транзакций"),
        (0.05, 0.16, "Генерация комнат WebRTC Jitsi Meet + санитизация bleach"),
        (0.05, 0.07, "Агрегация оценок и вычисление доверенного рейтинга")
    ]
    for x, y, t in boxes_plat:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.52, 0.065, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#2ECC71", lw=1))
        ax.text(x+0.015, y+0.02, t, fontsize=8.5, color="#2C3E50")

    # Admin boxes
    boxes_adm = [
        (0.68, 0.33, "Модерация отзывов"),
        (0.68, 0.21, "Аудит зашифрованных оплат"),
        (0.68, 0.09, "Управление доступом")
    ]
    for x, y, t in boxes_adm:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.26, 0.08, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#E74C3C", lw=1))
        ax.text(x+0.015, y+0.025, t, fontsize=8.5, color="#2C3E50")

    # Arrows
    arrow_props = dict(arrowstyle="->", lw=1.5, color="#7F8C8D")
    ax.annotate("", xy=(0.25, 0.55), xytext=(0.25, 0.44), arrowprops=arrow_props)
    ax.annotate("", xy=(0.75, 0.55), xytext=(0.55, 0.44), arrowprops=arrow_props)
    ax.annotate("", xy=(0.65, 0.25), xytext=(0.60, 0.25), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_1_1_business_process.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_1_1_business_process.png")

def draw_fig_1_2():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    ax.axis('off')
    
    # Left column: Threats
    ax.text(0.05, 0.95, "Векторы угроз OWASP Top-10 для EdTech", fontsize=11, fontweight='bold', color="#C0392B")
    threats = [
        "A01: Нарушение контроля доступа (IDOR, эскалация прав)",
        "A02: Криптографические ошибки (утечка открытых ПДн)",
        "A03: Инъекции (внедрение вредоносного SQL-кода)",
        "A04: Небезопасный дизайн (манипуляция ценой Price Tampering)",
        "A07: Ошибки идентификации (слабые сессии, CSRF)",
        "Stored XSS (внедрение скриптов в чатах и отзывах)",
        "CSRF (подделка межсайтовых POST-запросов)"
    ]
    for idx, t in enumerate(threats):
        y = 0.82 - idx * 0.115
        ax.add_patch(patches.FancyBboxPatch((0.02, y), 0.44, 0.08, boxstyle="round,pad=0.01", fc="#FDEDEC", ec="#E74C3C", lw=1.2))
        ax.text(0.03, y+0.025, t, fontsize=8, color="#78281F")

    # Right column: Defenses
    ax.text(0.55, 0.95, "Архитектурные механизмы нейтрализации", fontsize=11, fontweight='bold', color="#27AE60")
    defenses = [
        "Декораторы RBAC (@login_required, abort(403), сверка user_id)",
        "Симметричное шифрование Fernet (AES-128-CBC) + PBKDF2 соль",
        "SQLAlchemy ORM (строго параметризованные запросы драйвера)",
        "Серверная верификация суммы с float-допуском |form - db| <= 0.01",
        "Werkzeug secure password hash + флаги cookies HttpOnly/SameSite",
        "Двухконтурная очистка: bleach.clean(strip=True) + Jinja2 escaping",
        "Flask-WTF криптографические токены Synchronizer Token Pattern"
    ]
    for idx, d in enumerate(defenses):
        y = 0.82 - idx * 0.115
        ax.add_patch(patches.FancyBboxPatch((0.52, y), 0.46, 0.08, boxstyle="round,pad=0.01", fc="#EAFAF1", ec="#2ECC71", lw=1.2))
        ax.text(0.53, y+0.025, d, fontsize=8, color="#145A32")

        # Connection line
        ax.annotate("", xy=(0.52, y+0.04), xytext=(0.46, y+0.04),
                    arrowprops=dict(arrowstyle="->", lw=1.2, color="#2980B9"))

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_1_2_owasp.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_1_2_owasp.png")

def draw_fig_2_1():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    ax.axis('off')

    # Tier 1: Client
    ax.add_patch(patches.FancyBboxPatch((0.03, 0.72), 0.94, 0.24, boxstyle="round,pad=0.02", fc="#EBF5FB", ec="#2980B9", lw=1.5))
    ax.text(0.05, 0.91, "1. Клиентский уровень (Presentation Tier)", fontsize=11, fontweight='bold', color="#1B4F72")
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.75), 0.40, 0.13, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#3498DB", lw=1))
    ax.text(0.08, 0.82, "Веб-браузер пользователя (Клиент)\nBootstrap 5 UI + FullCalendar JS", fontsize=9, color="#2C3E50")
    ax.add_patch(patches.FancyBboxPatch((0.52, 0.75), 0.42, 0.13, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#3498DB", lw=1))
    ax.text(0.54, 0.82, "Jitsi Meet WebRTC IFrame\n(Защищенный видеопоток DTLS-SRTP)", fontsize=9, color="#2C3E50")

    # Tier 2: App & Security
    ax.add_patch(patches.FancyBboxPatch((0.03, 0.34), 0.94, 0.33, boxstyle="round,pad=0.02", fc="#EAFAF1", ec="#27AE60", lw=1.5))
    ax.text(0.05, 0.62, "2. Уровень бизнес-логики и контур безопасности (Application & Security Tier)", fontsize=11, fontweight='bold', color="#145A32")
    
    app_boxes = [
        (0.06, 0.48, 0.28, "Flask Core WSGI\napp.py / extensions.py"),
        (0.36, 0.48, 0.28, "Контроль RBAC и сессий\nFlask-Login + Cookies"),
        (0.66, 0.48, 0.28, "CSRF Токены\nFlask-WTF CSRFProtect"),
        (0.06, 0.37, 0.28, "Санитайзинг XSS\nbleach.clean(strip=True)"),
        (0.36, 0.37, 0.28, "Валидация платежей\nPrice Tampering Guard"),
        (0.66, 0.37, 0.28, "Криптомодуль Fernet\nAES-128-CBC + HMAC-SHA256")
    ]
    for x, y, w, t in app_boxes:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, 0.09, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#2ECC71", lw=1))
        ax.text(x+0.015, y+0.03, t, fontsize=8, color="#2C3E50")

    # Tier 3: Data Tier
    ax.add_patch(patches.FancyBboxPatch((0.03, 0.03), 0.94, 0.26, boxstyle="round,pad=0.02", fc="#FEF9E7", ec="#F39C12", lw=1.5))
    ax.text(0.05, 0.24, "3. Уровень персистентных данных (Data Storage Tier)", fontsize=11, fontweight='bold', color="#7D6608")
    
    ax.add_patch(patches.FancyBboxPatch((0.06, 0.06), 0.40, 0.14, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#F1C40F", lw=1))
    ax.text(0.08, 0.12, "СУБД PostgreSQL 14+ (SQLAlchemy ORM)\nusers, tutor_profiles, lessons, reviews,\nchats, chat_messages, payments", fontsize=8.5, color="#2C3E50")
    
    ax.add_patch(patches.FancyBboxPatch((0.52, 0.06), 0.42, 0.14, boxstyle="round,pad=0.01", fc="#FDEDEC", ec="#E74C3C", lw=1))
    ax.text(0.54, 0.12, "Зашифрованное хранилище ПДн:\n_phone: Fernet AES-128 (IV + HMAC)\n_transaction_ref: Fernet AES-128\npassword_hash: PBKDF2-HMAC-SHA256", fontsize=8.5, color="#78281F")

    # Connecting vertical arrows
    ax.annotate("", xy=(0.26, 0.67), xytext=(0.26, 0.72), arrowprops=dict(arrowstyle="<->", lw=2, color="#2980B9"))
    ax.annotate("", xy=(0.26, 0.29), xytext=(0.26, 0.34), arrowprops=dict(arrowstyle="<->", lw=2, color="#27AE60"))
    ax.annotate("", xy=(0.73, 0.29), xytext=(0.73, 0.34), arrowprops=dict(arrowstyle="<->", lw=2, color="#E67E22"))

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_2_1_architecture.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_2_1_architecture.png")

def draw_fig_2_2():
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=200)
    ax.axis('off')
    
    # State boxes
    states = [
        (0.05, 0.5, "Создание брони\n(/book)\n[Статус: scheduled]", "#3498DB", "#EBF5FB"),
        (0.38, 0.5, "Оплата занятия\n(/pay + Fernet)\n[Статус: paid]", "#27AE60", "#EAFAF1"),
        (0.72, 0.5, "Урок проведен\n(Видеоконференция)\n[Статус: completed]", "#8E44AD", "#F4ECF7"),
        (0.38, 0.1, "Занятие отменено\n(Возврат средств)\n[Статус: cancelled]", "#E74C3C", "#FDEDEC")
    ]
    for x, y, t, ec, fc in states:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.23, 0.25, boxstyle="round,pad=0.02", fc=fc, ec=ec, lw=1.8))
        ax.text(x+0.015, y+0.08, t, fontsize=9, fontweight='bold', color="#2C3E50", ha='left')

    # Arrows
    arr = dict(arrowstyle="->", lw=1.8, color="#2C3E50")
    ax.annotate("Оплата студентом\n|price - rate| <= 0.01", xy=(0.38, 0.62), xytext=(0.28, 0.62), arrowprops=arr, fontsize=8)
    ax.annotate("Подтверждение урока", xy=(0.72, 0.62), xytext=(0.61, 0.62), arrowprops=arr, fontsize=8)
    ax.annotate("Отмена до оплаты", xy=(0.38, 0.22), xytext=(0.23, 0.5), arrowprops=arr, fontsize=8)
    ax.annotate("Отмена после оплаты", xy=(0.49, 0.35), xytext=(0.49, 0.5), arrowprops=arr, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_2_2_statediagram.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_2_2_statediagram.png")

def draw_fig_2_3():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=200)
    ax.axis('off')

    # Tables representation
    tables = [
        (0.03, 0.55, 0.28, 0.40, "users", [
            "id: int [PK]", "email: varchar [UK]", "password_hash: str",
            "role: varchar", "phone: Fernet(str)", "created_at: datetime"
        ], "#2980B9", "#EBF5FB"),
        
        (0.36, 0.55, 0.28, 0.40, "tutor_profiles", [
            "id: int [PK]", "user_id: int [FK, UK]", "subject: varchar",
            "hourly_rate: float", "bio: text (bleach)"
        ], "#27AE60", "#EAFAF1"),
        
        (0.69, 0.55, 0.28, 0.40, "lessons", [
            "id: int [PK]", "tutor_id: int [FK]", "student_id: int [FK]",
            "date: datetime", "status: varchar", "video_room: str (hex)"
        ], "#8E44AD", "#F4ECF7"),
        
        (0.03, 0.05, 0.28, 0.42, "reviews", [
            "id: int [PK]", "tutor_id: int [FK]", "student_id: int [FK]",
            "lesson_id: int [FK]", "rating: int (1-5)", "comment: text", "created_at: datetime"
        ], "#D35400", "#FBEEE6"),
        
        (0.36, 0.05, 0.28, 0.42, "chats / chat_messages", [
            "chats.id: int [PK]", "chats.lesson_id: int [FK]",
            "msg.id: int [PK]", "msg.chat_id: int [FK]",
            "msg.sender_id: int [FK]", "msg.content: text", "msg.sent_at: datetime"
        ], "#16A085", "#E8F8F5"),
        
        (0.69, 0.05, 0.28, 0.42, "payments", [
            "id: int [PK]", "lesson_id: int [FK, UK]", "payer_id: int [FK]",
            "amount: float", "status: varchar", "transaction_ref: Fernet(str)", "created_at: datetime"
        ], "#C0392B", "#FDEDEC")
    ]

    for x, y, w, h, name, fields, ec, fc in tables:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01", fc=fc, ec=ec, lw=1.5))
        ax.text(x+0.02, y+h-0.05, f"Таблица {name}", fontsize=9.5, fontweight='bold', color=ec)
        for idx, f in enumerate(fields):
            ax.text(x+0.02, y+h-0.10 - idx*0.045, f, fontsize=8, color="#2C3E50")

    # Link lines
    ax.annotate("", xy=(0.36, 0.75), xytext=(0.31, 0.75), arrowprops=dict(arrowstyle="<->", lw=1.5, color="#2C3E50"))
    ax.annotate("", xy=(0.69, 0.75), xytext=(0.64, 0.75), arrowprops=dict(arrowstyle="<->", lw=1.5, color="#2C3E50"))
    ax.annotate("", xy=(0.17, 0.47), xytext=(0.17, 0.55), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2C3E50"))
    ax.annotate("", xy=(0.50, 0.47), xytext=(0.75, 0.55), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2C3E50"))
    ax.annotate("", xy=(0.83, 0.47), xytext=(0.83, 0.55), arrowprops=dict(arrowstyle="<->", lw=1.5, color="#2C3E50"))

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_2_3_erdiagram.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_2_3_erdiagram.png")

def draw_fig_2_4():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    ax.axis('off')

    # Lifelines
    actors = [
        (0.12, "Ученик (Браузер)"), (0.37, "Сервер Flask (app.py)"),
        (0.63, "Криптомодуль Fernet"), (0.88, "СУБД PostgreSQL")
    ]
    for x, label in actors:
        ax.text(x, 0.93, label, fontsize=9.5, fontweight='bold', ha='center', color="#1B4F72")
        ax.plot([x, x], [0.08, 0.90], linestyle='--', color="#BDC3C7", lw=1.2)

    # Sequence steps
    steps = [
        (0.12, 0.37, 0.82, "1. POST /book/<id> (выбор даты занятия + CSRF)", "->", "#2980B9"),
        (0.37, 0.88, 0.74, "2. INSERT lesson (status='scheduled', video_room=token)", "->", "#27AE60"),
        (0.12, 0.37, 0.64, "3. POST /pay/<id> (попытка оплаты, amount=1500 + CSRF)", "->", "#2980B9"),
        (0.37, 0.37, 0.56, "4. Сверка цены: |form.amount - tutor.rate| <= 0.01 (OK)", "self", "#F39C12"),
        (0.37, 0.63, 0.46, "5. encrypt_data(transaction_id) -> Fernet AES-128", "->", "#8E44AD"),
        (0.63, 0.37, 0.38, "6. Возврат шифротекста gAAAAABm...", "<-", "#8E44AD"),
        (0.37, 0.88, 0.28, "7. INSERT payment(ref=cipher) & UPDATE lesson paid", "->", "#27AE60"),
        (0.12, 0.37, 0.18, "8. GET /video/<id> (проверка прав current_user)", "->", "#2980B9"),
        (0.37, 0.12, 0.10, "9. Рендеринг Jitsi Meet iframe (доступ разрешен)", "<-", "#27AE60")
    ]

    for x1, x2, y, text, direction, col in steps:
        if direction == "->":
            ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", lw=1.5, color=col))
            ax.text((x1+x2)/2, y+0.015, text, fontsize=7.5, ha='center', color="#2C3E50")
        elif direction == "<-":
            ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", lw=1.5, color=col))
            ax.text((x1+x2)/2, y+0.015, text, fontsize=7.5, ha='center', color="#2C3E50")
        elif direction == "self":
            ax.add_patch(patches.FancyBboxPatch((x1-0.08, y-0.03), 0.16, 0.05, boxstyle="round,pad=0.01", fc="#FEF9E7", ec=col, lw=1))
            ax.text(x1, y-0.015, text, fontsize=7.5, ha='center', color="#7D6608")

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_2_4_seq_booking.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_2_4_seq_booking.png")

def draw_fig_2_5():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    ax.axis('off')

    actors = [
        (0.12, "Атакующий (Браузер)"), (0.37, "Сервер Flask (app.py)"),
        (0.63, "Модуль bleach / Jinja2"), (0.88, "Браузер Жертвы")
    ]
    for x, label in actors:
        ax.text(x, 0.93, label, fontsize=9.5, fontweight='bold', ha='center', color="#1B4F72")
        ax.plot([x, x], [0.08, 0.90], linestyle='--', color="#BDC3C7", lw=1.2)

    steps = [
        (0.12, 0.37, 0.78, "1. Ввод пейлоада: <script>alert('XSS')</script>Привет!", "->", "#C0392B"),
        (0.37, 0.63, 0.65, "2. bleach.clean(content, tags=[], strip=True)", "->", "#27AE60"),
        (0.63, 0.37, 0.52, "3. Удаление <script>, возврат безопасного текста: 'alert('XSS')Привет!'", "<-", "#27AE60"),
        (0.37, 0.37, 0.40, "4. INSERT into chat_messages (чистый текст сохранен)", "self", "#2980B9"),
        (0.88, 0.37, 0.28, "5. Жертва открывает GET /chat/<lesson_id>", "<-", "#2C3E50"),
        (0.37, 0.88, 0.16, "6. Jinja2 автоэкранирование {{ msg.content }} -> Безопасный HTML", "->", "#27AE60")
    ]

    for x1, x2, y, text, direction, col in steps:
        if direction in ("->", "<-"):
            ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", lw=1.5, color=col))
            ax.text((x1+x2)/2, y+0.02, text, fontsize=7.5, ha='center', color="#2C3E50")
        elif direction == "self":
            ax.add_patch(patches.FancyBboxPatch((x1-0.12, y-0.03), 0.24, 0.05, boxstyle="round,pad=0.01", fc="#EBF5FB", ec=col, lw=1))
            ax.text(x1, y-0.015, text, fontsize=7.5, ha='center', color="#1B4F72")

    # Success badge
    ax.add_patch(patches.FancyBboxPatch((0.72, 0.02), 0.26, 0.08, boxstyle="round,pad=0.01", fc="#EAFAF1", ec="#27AE60", lw=1.5))
    ax.text(0.85, 0.05, "Результат:\nСкрипт не исполняется!", fontsize=8, fontweight='bold', color="#145A32", ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_2_5_seq_xss.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_2_5_seq_xss.png")

def draw_fig_3_1():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=200)
    ax.axis('off')

    # Core box
    ax.add_patch(patches.FancyBboxPatch((0.05, 0.40), 0.50, 0.55, boxstyle="round,pad=0.02", fc="#EBF5FB", ec="#2980B9", lw=1.5))
    ax.text(0.08, 0.90, "Ядро веб-приложения (Python / Flask)", fontsize=10.5, fontweight='bold', color="#1B4F72")
    
    modules = [
        "app.py (Маршруты, RBAC, bleach, валидация)",
        "models.py (User, TutorProfile, Lesson, Chat, Payment)",
        "forms.py (Register, Login, BookLesson, Payment)",
        "encryption.py (Fernet AES-128 шифрование/дешифрование)",
        "config.py (SECRET_KEY, HTTPONLY cookies)",
        "extensions.py (db = SQLAlchemy(), csrf = CSRFProtect())"
    ]
    for idx, m in enumerate(modules):
        ax.text(0.08, 0.81 - idx*0.07, f"• {m}", fontsize=8, color="#2C3E50")

    # DB box
    ax.add_patch(patches.FancyBboxPatch((0.62, 0.55), 0.33, 0.40, boxstyle="round,pad=0.02", fc="#FEF9E7", ec="#F39C12", lw=1.5))
    ax.text(0.65, 0.89, "База данных (PostgreSQL)", fontsize=10, fontweight='bold', color="#7D6608")
    ax.text(0.65, 0.80, "• 7 реляционных таблиц\n• Индексы email, user_id\n• Зашифрованные поля\n• 5000+ уроков (seed_db.py)", fontsize=8, color="#2C3E50")

    # Client box
    ax.add_patch(patches.FancyBboxPatch((0.05, 0.05), 0.90, 0.28, boxstyle="round,pad=0.02", fc="#EAFAF1", ec="#27AE60", lw=1.5))
    ax.text(0.08, 0.26, "Клиентские шаблоны и статика (templates / static)", fontsize=10, fontweight='bold', color="#145A32")
    ax.text(0.08, 0.12, "• base.html (навигация и flash)  • index.html (лендинг)  • tutors.html (каталог)\n• calendar.html (FullCalendar v6)  • video_call.html (Jitsi)  • chat.html (XSS-safe)\n• payment.html (защищенная форма)  • admin.html (панель управления)", fontsize=8, color="#2C3E50")

    # Connector arrows
    ax.annotate("", xy=(0.62, 0.75), xytext=(0.55, 0.75), arrowprops=dict(arrowstyle="<->", lw=1.8, color="#2980B9"))
    ax.annotate("", xy=(0.30, 0.33), xytext=(0.30, 0.40), arrowprops=dict(arrowstyle="<->", lw=1.8, color="#27AE60"))

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_3_1_modules.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_3_1_modules.png")

if __name__ == '__main__':
    draw_fig_1_1()
    draw_fig_1_2()
    draw_fig_2_1()
    draw_fig_2_2()
    draw_fig_2_3()
    draw_fig_2_4()
    draw_fig_2_5()
    draw_fig_3_1()
    print("Все изображения успешно сгенерированы!")
