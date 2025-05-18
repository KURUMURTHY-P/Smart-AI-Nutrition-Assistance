from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils.gemini_handler import analyze_text_and_image, is_food_image, chat_with_gemini
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import google.generativeai as genai
import os
from config import Config
import base64
from datetime import datetime
    

app = Flask(__name__)


app.config.from_object(Config)



db = SQLAlchemy(app)

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    goal = db.Column(db.String(200))
    allergies = db.Column(db.Text)
    preferences = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Gemini Setup
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
chat_model = genai.GenerativeModel("gemini-1.5-flash")
chat_session = chat_model.start_chat()


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}



@app.route('/', methods=['GET', 'POST'])
def home():
    response = None
    prompt = ""
    image_data = None

    if request.method == 'POST':
        prompt = request.form.get("prompt", "")
        image = request.files.get("image")

        if image and image.filename != "":
            # Read and encode the image
            image_data = base64.b64encode(image.read()).decode('utf-8')
            image.seek(0)

            # Assuming you have a function to check if the image is of food
            is_food, description = is_food_image(image)
            if not is_food:
                response = "Please upload food images only."

            else:
                # Assuming you have a function to analyze text and image
                response = analyze_text_and_image(prompt, image)
        elif prompt:
            # Assuming you have a function to handle text-only prompts
            response = chat_with_gemini(prompt)
        else:
            response = "Please provide a prompt or upload an image."

    return render_template("index.html", response=response, prompt=prompt, image_data=image_data)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form.get('age')
        gender = request.form.get('gender')
        #goal = request.form.get('goal')
        goal = request.form.get('health_goal')
        allergies = request.form.get('allergies')
        #preferences = request.form.get('preferences')
        preferences = request.form.get('food_preference')


        # Check for existing email
        if User.query.filter_by(email=email).first():
            return "Email already registered. Please login or use a different email."

        new_user = User(
            name=name, email=email, password=password,
            age=age, gender=gender, goal=goal,
            allergies=allergies, preferences=preferences
        )
        db.session.add(new_user)
        db.session.commit()

        return render_template('success.html', user=new_user)  # ✅ FIXED LINE

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
@login_required
def chat_post():
    data = request.get_json()
    user_message = data['message']
    response = chat_session.send_message(user_message)
    return jsonify({"reply": response.text})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
