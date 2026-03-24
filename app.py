import eventlet
eventlet.monkey_patch()
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Theme, ProjectIdea, TechStack, ApiRecommendation, PitchTip, ChatMessage, ChatRoom, HackathonKit, User
import random
import string
import os

# --- App Initialization ---
app = Flask(__name__)

# --- Configuration ---
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-key') 

db_url = os.environ.get("DATABASE_URL")
if db_url is None:
    db_url = 'sqlite:///hackathon_catalyst.db'
elif db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Extension Initialization ---
db.init_app(app)
socketio = SocketIO(app)

# --- Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # FIXED: Updated to modern SQLAlchemy 2.0 syntax to remove the warning
    return db.session.get(User, int(user_id))

# --- HTTP Routes ---

@app.route('/')
def home():
    return render_template('home.html', user=current_user)

@app.route('/toolkit')
@login_required
def toolkit():
    
    themes = Theme.query.order_by(Theme.name).all()
    
    return render_template('toolkit.html', themes=themes)

@app.route('/chat')
@login_required
def chat():
    
    return render_template('chat.html', username=current_user.username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="User already exists!")
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('home'))
        
        return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- API Routes ---

@app.route('/api/generate', methods=['POST'])
def generate_idea():
    data = request.get_json()
    theme_id = data.get('theme_id')
    difficulty = data.get('difficulty')

    if not theme_id:
        return jsonify({'error': 'Theme ID is required'}), 400

    query = ProjectIdea.query.filter_by(theme_id=theme_id).join(HackathonKit)

    if difficulty:
        query = query.filter(ProjectIdea.difficulty == difficulty)

    ideas = query.order_by(db.func.random()).limit(3).all()
    
    if not ideas:
        return jsonify({'error': 'No ideas found for this theme.'}), 404

    response_data = []
    for idea in ideas:
        kit = idea.kit
        if isinstance(kit, list) and len(kit) > 0:
            kit = kit[0]
        elif isinstance(kit, list) and len(kit) == 0:
             continue
        
        idea_package = {
            'idea': {
                'title': idea.title,
                'description': idea.description,
                'difficulty': idea.difficulty
            },
            'kit': {
                'stack': {'name': kit.stack.name, 'frontend': kit.stack.frontend, 'backend': kit.stack.backend, 'database': kit.stack.database},
                'api': {'name': kit.api.name, 'description': kit.api.description, 'url': kit.api.url} if kit.api else None,
                'tip': {'tip': kit.tip.tip} if kit.tip else None,
            }
        }
        response_data.append(idea_package)

    return jsonify(response_data)

@app.route('/api/create_room', methods=['POST'])
@login_required
def create_room():
    data = request.get_json()
    room_name = data.get('room_name', '').strip()
    secret_code = data.get('secret_code', '').strip()
    
    if not room_name or not secret_code:
        return jsonify({'error': 'Room name and secret code are required.'}), 400

    existing_room = ChatRoom.query.filter_by(room_name=room_name).first()
    if existing_room:
        return jsonify({'error': f"Room '{room_name}' already exists."}), 409
    
    new_room = ChatRoom(room_name=room_name, secret_code=secret_code)
    db.session.add(new_room)
    db.session.commit()
    
    return jsonify({
        'message': 'Room created successfully!',
        'room_name': new_room.room_name,
        'secret_code': new_room.secret_code
    }), 201

@app.route('/api/join_room', methods=['POST'])
@login_required
def join_room_with_code():
    data = request.get_json()
    room_name = data.get('room_name', '').strip()
    secret_code = data.get('secret_code', '').strip()

    if not room_name or not secret_code:
        return jsonify({'error': 'Room name and secret code are required.'}), 400

    room = ChatRoom.query.filter_by(room_name=room_name, secret_code=secret_code).first()
    
    if not room:
        return jsonify({'error': 'Invalid room name or secret code.'}), 401
    
    return jsonify({
        'message': 'Successfully joined room!',
        'room_name': room.room_name
    }), 200

# --- SocketIO Events ---
active_users = {}

@socketio.on('join')
def on_join(data):
    username = current_user.username if current_user.is_authenticated else data.get('username', 'Anonymous')
    team_id = data.get('team_id')
    
    if not team_id:
        return

    # CRITICAL FIX: Save info to session so we can access it on disconnect
    session['room'] = team_id
    session['username'] = username

    join_room(team_id)
    
    if team_id not in active_users:
        active_users[team_id] = []
    
    if username not in active_users[team_id]:
        active_users[team_id].append(username)
    
    emit('update_user_list', {'users': active_users[team_id]}, room=team_id)
    emit('status', {'msg': f'{username} has entered the room.'}, room=team_id)

@socketio.on('leave')
def on_leave(data):
    # We can try to get data from the manual payload, or fallback to session
    username = data.get('username') or session.get('username')
    team_id = data.get('team_id') or session.get('room')
    
    if team_id:
        leave_room(team_id)
        
        if team_id in active_users and username in active_users[team_id]:
            active_users[team_id].remove(username)
            
        emit('update_user_list', {'users': active_users.get(team_id, [])}, room=team_id)
        emit('status', {'msg': f'{username} has left the room.'}, room=team_id)

@socketio.on('disconnect')
def on_disconnect():
    # Retrieve the data we saved in the session during 'join'
    username = session.get('username')
    team_id = session.get('room')

    if team_id and username:
        leave_room(team_id)
        
        if team_id in active_users and username in active_users[team_id]:
            # Only try to remove if they are actually in the list
            try:
                active_users[team_id].remove(username)
            except ValueError:
                pass # User might have already been removed
            
        emit('update_user_list', {'users': active_users.get(team_id, [])}, room=team_id)
        emit('status', {'msg': f'{username} has gone offline.'}, room=team_id)

@socketio.on('send_message')
def on_send_message(data):
    team_id = data.get('team_id')
    if not team_id:
        return
    
    username = current_user.username if current_user.is_authenticated else "Anonymous"
    
    # 1. Get Current UTC Time (For Database)
    now_utc = datetime.now(timezone.utc)
    
    # 2. Calculate IST for the Chat Window Display (UTC + 5:30)
    ist_offset = timedelta(hours=5, minutes=30)
    now_ist = now_utc + ist_offset
    
    # 3. Format it nicely (e.g., "11:05 AM")
    formatted_time_str = now_ist.strftime('%I:%M %p')
    
    # 4. Store in Database
    message = ChatMessage(
        team_id=team_id, 
        username=username, 
        message=data.get('message', ''),
        timestamp=now_utc 
    )
    db.session.add(message)
    db.session.commit()
    
    # 5. Emit SINGLE message to EVERYONE (including sender)
    # We removed 'include_self=False' so the sender sees the confirmation.
    emit('new_message', {
        'username': message.username,
        'message': message.message,
        'timestamp': formatted_time_str
    }, room=team_id)

# --- Runner ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)