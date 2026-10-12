import random
from faker import Faker
from datetime import datetime, timedelta
from app import app
from extensions import db
from models import User, TutorProfile, Lesson, Review

fake = Faker('ru_RU')

def seed_database():
    with app.app_context():
        # Очищаем базу (на всякий случай)
        db.drop_all()
        db.create_all()
        
        print("🌱 Начинаем генерацию данных...")
        
        # Создаем 100 пользователей
        users = []
        for i in range(100):
            user = User(
                email=fake.email(),
                role=random.choice(['student', 'tutor']),
                phone=fake.phone_number()
            )
            user.set_password('password123')  # Одинаковый пароль для всех
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Создано {len(users)} пользователей")
        
        # Создаем профили для репетиторов
        tutors = [u for u in users if u.role == 'tutor']
        subjects = ['Математика', 'Физика', 'Английский', 'Русский', 'Информатика', 'Химия']
        
        tutor_profiles = []
        for tutor in tutors:
            profile = TutorProfile(
                user_id=tutor.id,
                subject=random.choice(subjects),
                hourly_rate=random.uniform(500, 3000),
                bio=fake.text(max_nb_chars=200)
            )
            tutor_profiles.append(profile)
            db.session.add(profile)
        
        db.session.commit()
        print(f"✅ Создано {len(tutor_profiles)} профилей репетиторов")
        
        # Создаем 5000 уроков
        lessons = []
        students = [u for u in users if u.role == 'student']
        
        for _ in range(5000):
            if students and tutors:
                lesson = Lesson(
                    tutor_id=random.choice(tutors).id,
                    student_id=random.choice(students).id,
                    date=fake.date_time_between(start_date='-1y', end_date='+1y'),
                    status=random.choice(['scheduled', 'completed', 'cancelled'])
                )
                lessons.append(lesson)
                db.session.add(lesson)
        
        db.session.commit()
        print(f"✅ Создано {len(lessons)} уроков")
        
        # Создаем 2000 отзывов
        reviews = []
        completed_lessons = [l for l in lessons if l.status == 'completed']
        
        for lesson in completed_lessons[:2000]:  # Берем первые 2000 завершенных уроков
            review = Review(
                lesson_id=lesson.id,
                student_id=lesson.student_id,
                rating=random.randint(3, 5),
                comment=fake.text(max_nb_chars=150)
            )
            reviews.append(review)
            db.session.add(review)
        
        db.session.commit()
        print(f"✅ Создано {len(reviews)} отзывов")
        
        print("\n🎉 База данных успешно наполнена!")
        print(f"📊 Всего записей: {len(users) + len(tutor_profiles) + len(lessons) + len(reviews)}")

if __name__ == '__main__':
    seed_database()