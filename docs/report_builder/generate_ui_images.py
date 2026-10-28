# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMG_DIR = '/home/pdvdanya/Agy_Projects/Me/Course_work/docs/report_builder/images'

def draw_browser_frame(ax, title):
    # Browser window header
    ax.add_patch(patches.Rectangle((0, 0.92), 1.0, 0.08, fc="#E0E0E0", ec="#BDBDBD", lw=1))
    ax.add_patch(patches.Circle((0.03, 0.96), 0.012, fc="#E74C3C", ec="none"))
    ax.add_patch(patches.Circle((0.06, 0.96), 0.012, fc="#F1C40F", ec="none"))
    ax.add_patch(patches.Circle((0.09, 0.96), 0.012, fc="#2ECC71", ec="none"))
    
    # Address bar
    ax.add_patch(patches.FancyBboxPatch((0.15, 0.935), 0.70, 0.05, boxstyle="round,pad=0.005", fc="#FFFFFF", ec="#CCCCCC", lw=0.8))
    ax.text(0.18, 0.95, f"https://tutorplatform.edu{title}", fontsize=8, color="#555555")

    # Navbar
    ax.add_patch(patches.Rectangle((0, 0.85), 1.0, 0.07, fc="#0D6EFD", ec="none"))
    ax.text(0.04, 0.875, "🎓 TutorPlatform", fontsize=10, fontweight='bold', color="#FFFFFF")
    ax.text(0.30, 0.875, "Преподаватели    Мои уроки    Профиль", fontsize=8.5, color="#E0E0E0")
    ax.text(0.80, 0.875, "Выйти (student1@tutor.ru)", fontsize=8, color="#E0E0E0")

def draw_fig_3_2():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    ax.axis('off')
    draw_browser_frame(ax, "/")
    
    # Hero section
    ax.add_patch(patches.FancyBboxPatch((0.05, 0.45), 0.90, 0.35, boxstyle="round,pad=0.02", fc="#F8F9FA", ec="#E9ECEF", lw=1))
    ax.text(0.50, 0.68, "Найди идеального репетитора", fontsize=14, fontweight='bold', ha='center', color="#212529")
    ax.text(0.50, 0.58, "Безопасная платформа для онлайн-обучения.\nВидеосвязь, удобная оплата и надежная защита ваших персональных данных.", fontsize=9, ha='center', color="#6C757D")
    ax.add_patch(patches.FancyBboxPatch((0.40, 0.48), 0.20, 0.07, boxstyle="round,pad=0.01", fc="#0D6EFD", ec="none"))
    ax.text(0.50, 0.51, "Начать поиск", fontsize=9.5, fontweight='bold', color="#FFFFFF", ha='center')

    # 3 Cards
    cards = [
        (0.05, "🔒 Безопасность", "Шифрование данных (Fernet)\nи защита транзакций"),
        (0.38, "📹 Видеосвязь", "Встроенные защищенные\nуроки Jitsi Meet"),
        (0.71, "📅 Расписание", "Интерактивный календарь\nFullCalendar v6")
    ]
    for x, h, b in cards:
        ax.add_patch(patches.FancyBboxPatch((x, 0.12), 0.24, 0.28, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#DEE2E6", lw=1))
        ax.text(x+0.12, 0.31, h, fontsize=9.5, fontweight='bold', ha='center', color="#0D6EFD")
        ax.text(x+0.12, 0.20, b, fontsize=8, ha='center', color="#495057")

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_3_2_ui_index.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_3_2_ui_index.png")

def draw_fig_3_3():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    ax.axis('off')
    draw_browser_frame(ax, "/tutors")
    
    # Filter card
    ax.add_patch(patches.FancyBboxPatch((0.05, 0.67), 0.90, 0.15, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#DEE2E6", lw=1))
    ax.text(0.08, 0.76, "🔍 Фильтр: Предмет [ Математика       ]    Макс. цена [ 2500 ]    [ Найти ]", fontsize=8.5, color="#212529")

    # Tutor Cards
    tutors = [
        (0.05, "Математика (ЕГЭ / ОГЭ)", "2000 ₽/час", "tutor1@tutor.ru", "Опыт 8 лет. Подготовка к профилю."),
        (0.52, "Математический анализ", "2500 ₽/час", "tutor2@tutor.ru", "Преподаватель университета.")
    ]
    for x, subj, rate, email, bio in tutors:
        ax.add_patch(patches.FancyBboxPatch((x, 0.20), 0.43, 0.42, boxstyle="round,pad=0.01", fc="#FFFFFF", ec="#DEE2E6", lw=1))
        ax.text(x+0.03, 0.54, subj, fontsize=9.5, fontweight='bold', color="#0D6EFD")
        ax.add_patch(patches.FancyBboxPatch((x+0.28, 0.53), 0.12, 0.05, boxstyle="round,pad=0.005", fc="#198754", ec="none"))
        ax.text(x+0.34, 0.55, rate, fontsize=7.5, color="#FFFFFF", ha='center')
        ax.text(x+0.03, 0.46, email, fontsize=8, color="#6C757D")
        ax.text(x+0.03, 0.38, bio, fontsize=8, color="#212529")
        
        # Buttons
        ax.add_patch(patches.FancyBboxPatch((x+0.03, 0.24), 0.17, 0.06, boxstyle="round,pad=0.005", fc="#0D6EFD", ec="none"))
        ax.text(x+0.115, 0.265, "📅 Записаться", fontsize=7.5, color="#FFFFFF", ha='center')
        ax.add_patch(patches.FancyBboxPatch((x+0.22, 0.24), 0.17, 0.06, boxstyle="round,pad=0.005", fc="#F8F9FA", ec="#6C757D", lw=0.8))
        ax.text(x+0.305, 0.265, "⭐ Отзывы", fontsize=7.5, color="#212529", ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_3_3_ui_tutors.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_3_3_ui_tutors.png")

def draw_fig_3_4():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    ax.axis('off')
    draw_browser_frame(ax, "/calendar")
    
    ax.text(0.05, 0.78, "📅 Мои уроки (FullCalendar)", fontsize=11, fontweight='bold', color="#212529")
    
    # Calendar Grid simulation
    ax.add_patch(patches.Rectangle((0.05, 0.18), 0.90, 0.56, fc="#FFFFFF", ec="#DEE2E6", lw=1))
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    for idx, d in enumerate(days):
        x = 0.05 + idx * (0.90 / 7)
        ax.add_patch(patches.Rectangle((x, 0.68), 0.90/7, 0.06, fc="#F8F9FA", ec="#DEE2E6", lw=0.5))
        ax.text(x + 0.90/14, 0.70, d, fontsize=8, ha='center', color="#495057")

    # Calendar Events
    ax.add_patch(patches.FancyBboxPatch((0.19, 0.45), 0.11, 0.06, boxstyle="round,pad=0.005", fc="#198754", ec="none"))
    ax.text(0.245, 0.47, "14:00 Оплачен\nМатематика", fontsize=6.5, color="#FFFFFF", ha='center')
    
    ax.add_patch(patches.FancyBboxPatch((0.45, 0.32), 0.11, 0.06, boxstyle="round,pad=0.005", fc="#0D6EFD", ec="none"))
    ax.text(0.505, 0.34, "16:00 Запланирован\nФизика", fontsize=6.5, color="#FFFFFF", ha='center')

    # Action table row at bottom
    ax.text(0.05, 0.10, "Ближайший урок: 25.10.2026 14:00 (tutor1@tutor.ru) — [📹 Видео] [💬 Чат] [💳 Оплатить]", fontsize=8, color="#212529")

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_3_4_ui_calendar.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_3_4_ui_calendar.png")

def draw_fig_3_5():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    ax.axis('off')
    draw_browser_frame(ax, "/video/15")
    
    # Video container
    ax.add_patch(patches.Rectangle((0.05, 0.18), 0.90, 0.62, fc="#1C1C1C", ec="#000000", lw=1))
    ax.text(0.50, 0.52, "📹 Jitsi Meet WebRTC Video Call", fontsize=13, fontweight='bold', color="#FFFFFF", ha='center')
    ax.text(0.50, 0.44, "Комната: tutor-platform-7a8f9b2c (Шифрование DTLS-SRTP включено)\nДоступ только авторизованным участникам урока", fontsize=8.5, color="#AAAAAA", ha='center')
    
    # Call controls
    controls = [("🎤 Микрофон", "#333333"), ("📷 Камера", "#333333"), ("🖥️ Экран", "#333333"), ("❌ Завершить", "#DC3545")]
    for idx, (label, col) in enumerate(controls):
        cx = 0.30 + idx * 0.11
        ax.add_patch(patches.FancyBboxPatch((cx, 0.22), 0.09, 0.06, boxstyle="round,pad=0.005", fc=col, ec="none"))
        ax.text(cx+0.045, 0.245, label, fontsize=6.5, color="#FFFFFF", ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_3_5_ui_video.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_3_5_ui_video.png")

def draw_fig_3_6():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    ax.axis('off')
    draw_browser_frame(ax, "/chat/15")
    
    # Chat container
    ax.add_patch(patches.Rectangle((0.15, 0.12), 0.70, 0.70, fc="#FFFFFF", ec="#DEE2E6", lw=1))
    ax.add_patch(patches.Rectangle((0.15, 0.75), 0.70, 0.07, fc="#0D6EFD", ec="none"))
    ax.text(0.18, 0.775, "💬 Диалог: tutor1@tutor.ru ↔ student1@tutor.ru", fontsize=9, fontweight='bold', color="#FFFFFF")
    
    # Message 1 (tutor)
    ax.add_patch(patches.FancyBboxPatch((0.18, 0.60), 0.38, 0.09, boxstyle="round,pad=0.01", fc="#F8F9FA", ec="#CED4DA", lw=0.8))
    ax.text(0.20, 0.64, "Здравствуйте! Подготовили вопросы к занятию?", fontsize=8, color="#212529")
    ax.text(0.20, 0.61, "tutor1@tutor.ru · 13:55", fontsize=6.5, color="#6C757D")

    # Message 2 (student - XSS payload sanitized)
    ax.add_patch(patches.FancyBboxPatch((0.44, 0.44), 0.38, 0.11, boxstyle="round,pad=0.01", fc="#0D6EFD", ec="none"))
    ax.text(0.46, 0.50, "Да, отправил задачи.\n[XSS-тег <script> удален bleach]", fontsize=8, color="#FFFFFF")
    ax.text(0.46, 0.46, "Вы · 13:58", fontsize=6.5, color="#E0E0E0")

    # Input bar
    ax.add_patch(patches.FancyBboxPatch((0.18, 0.16), 0.52, 0.07, boxstyle="round,pad=0.005", fc="#FFFFFF", ec="#CED4DA", lw=1))
    ax.text(0.20, 0.185, "Введите сообщение...", fontsize=8, color="#6C757D")
    ax.add_patch(patches.FancyBboxPatch((0.72, 0.16), 0.10, 0.07, boxstyle="round,pad=0.005", fc="#0D6EFD", ec="none"))
    ax.text(0.77, 0.185, "Отправить", fontsize=8, color="#FFFFFF", ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_3_6_ui_chat.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_3_6_ui_chat.png")

def draw_fig_3_7():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    ax.axis('off')
    draw_browser_frame(ax, "/admin")
    
    ax.text(0.05, 0.78, "🔒 Панель администратора (Модерация и аудит)", fontsize=11, fontweight='bold', color="#212529")
    
    # Table header
    headers = [("ID", 0.05, 0.06), ("Студент / Репетитор", 0.12, 0.25), ("Сумма", 0.38, 0.12), ("Статус", 0.51, 0.12), ("ID транзакции (Fernet)", 0.64, 0.31)]
    ax.add_patch(patches.Rectangle((0.05, 0.66), 0.90, 0.06, fc="#212529", ec="none"))
    for h, x, w in headers:
        ax.text(x+0.02, 0.68, h, fontsize=7.5, fontweight='bold', color="#FFFFFF")

    # Rows
    rows = [
        ("1", "student1@tutor.ru", "1500 ₽", "paid (Оплачен)", "gAAAAABmX3r... (Зашифровано)"),
        ("2", "student2@tutor.ru", "2000 ₽", "paid (Оплачен)", "gAAAAABmY8k... (Зашифровано)"),
        ("3", "student3@tutor.ru", "2500 ₽", "pending (Ожидает)", "—")
    ]
    for idx, (rid, users, amt, st, ref) in enumerate(rows):
        y = 0.58 - idx * 0.07
        bg = "#F8F9FA" if idx % 2 == 0 else "#FFFFFF"
        ax.add_patch(patches.Rectangle((0.05, y), 0.90, 0.07, fc=bg, ec="#DEE2E6", lw=0.5))
        ax.text(0.06, y+0.02, rid, fontsize=7.5, color="#212529")
        ax.text(0.13, y+0.02, users, fontsize=7.5, color="#212529")
        ax.text(0.39, y+0.02, amt, fontsize=7.5, color="#198754", fontweight='bold')
        ax.text(0.52, y+0.02, st, fontsize=7.5, color="#0D6EFD")
        ax.text(0.65, y+0.02, ref, fontsize=7, color="#6C757D")

    # Review moderation note
    ax.add_patch(patches.FancyBboxPatch((0.05, 0.15), 0.90, 0.15, boxstyle="round,pad=0.01", fc="#FFF3CD", ec="#FFECB5", lw=1))
    ax.text(0.08, 0.23, "🛡️ Модерация отзывов: 2000 отзывов проверено на XSS/спам. Доступна кнопка безвозвратного удаления.", fontsize=8, color="#664D03")

    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'fig_3_7_ui_admin.png'), bbox_inches='tight')
    plt.close()
    print("✅ Создан fig_3_7_ui_admin.png")

if __name__ == '__main__':
    draw_fig_3_2()
    draw_fig_3_3()
    draw_fig_3_4()
    draw_fig_3_5()
    draw_fig_3_6()
    draw_fig_3_7()
    print("Все UI-иллюстрации успешно сгенерированы!")
