from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

from models import db, User, WorkoutHistory, Workout, WorkoutExercise

# Initialize app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitfusion.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

# Extensions
db.init_app(app)
jwt = JWTManager(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "FitFusion API is running!"

# ---------------- AUTH ---------------- #
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password or not name:
        return jsonify({"msg": "Email, password, and name are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    user = User(email=email, name=name, password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token, user={"name": user.name, "email": user.email}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    print("Login Request:", data)

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        print("No user found with email:", data['email'])
    elif not check_password_hash(user.password, data['password']):
        print("Password mismatch for user:", data['email'])
    else:
        print("Login successful for:", user.email)

    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)

    return jsonify({"msg": "Incorrect email or password"}), 401

# ---------------- PROFILE INFO ---------------- #
@app.route('/api/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"name": user.name, "email": user.email})

# ---------------- WORKOUT GENERATOR ---------------- #
@app.route('/api/generate', methods=['POST'])
@jwt_required()
def generate_workout():
    user_id = get_jwt_identity()
    data = request.json
    time = data.get('time')
    goal = data.get('goal')
    equipment = data.get('equipment')

    workout = f"{time} mins of {goal} workout using {equipment or 'bodyweight'}"

    entry = WorkoutHistory(user_id=user_id, workout=workout)
    db.session.add(entry)
    db.session.commit()

    return jsonify({"workout": workout})

# ---------------- WORKOUT HISTORY ---------------- #
@app.route('/api/history', methods=['GET'])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    history = WorkoutHistory.query.filter_by(user_id=user_id).order_by(WorkoutHistory.timestamp.desc()).all()

    result = [
        {"workout": w.workout, "time": w.timestamp.strftime("%Y-%m-%d %H:%M")}
        for w in history
    ]
    return jsonify(result)

# ---------------- WORKOUT LOGGING ---------------- #
@app.route('/api/workouts', methods=['POST'])
@jwt_required()
def log_workout():
    user_id = get_jwt_identity()
    data = request.json
    workout_date = datetime.strptime(data.get('date'), "%Y-%m-%d") if data.get('date') else datetime.utcnow()
    exercises = data.get('exercises', [])

    workout = Workout(user_id=user_id, date=workout_date)
    db.session.add(workout)
    db.session.flush()

    for ex in exercises:
        workout_ex = WorkoutExercise(
            workout_id=workout.id,
            name=ex['name'],
            sets=ex['sets'],
            reps=ex['reps'],
            weight=ex.get('weight')
        )
        db.session.add(workout_ex)

    db.session.commit()
    return jsonify({"msg": "Workout logged successfully"}), 201

# ---------------- APP ENTRY ---------------- #
if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    port = int(os.getenv('PORT', 5001))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
