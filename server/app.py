# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, WorkoutHistory

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitfusion.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

# Initialize extensions
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

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    user = User(email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)

    return jsonify({"msg": "Bad email or password"}), 401

# ---------------- WORKOUT GENERATOR ---------------- #

@app.route('/api/generate', methods=['POST'])
@jwt_required()
def generate_workout():
    user_id = get_jwt_identity()
    data = request.json
    time = data.get('time')
    goal = data.get('goal')
    equipment = data.get('equipment')

    # Simple generated workout
    workout = f"{time} mins of {goal} workout using {equipment or 'bodyweight'}"

    # Save workout to history
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

if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0', port=5000)
# Note: In production, set debug=False and use a proper WSGI server like Gunicorn.
# Example: gunicorn app:app --bind

