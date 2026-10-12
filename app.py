from flask import Flask, render_template
from config import Config
from extensions import db
import models
from models import User, TutorProfile

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tutors')
def tutors():
    
    tutors_list = db.session.query(User, TutorProfile)\
        .join(TutorProfile, User.id == TutorProfile.user_id)\
        .filter(User.role == 'tutor')\
        .all()
        
    return render_template('tutors.html', tutors=tutors_list)

if __name__ == '__main__':
    app.run(debug=True)