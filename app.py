from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room
# Make sure to import HackathonKit and ProjectIdea
from models import db, Theme, ProjectIdea, TechStack, ApiRecommendation, PitchTip, ChatMessage, ChatRoom, HackathonKit 
import random
import string

# --- App Initialization ---
app = Flask(__name__)
app.config['SECRET_key'] = 'a-very-secret-key-that-you-should-change'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackathon_catalyst.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Extension Initialization ---
db.init_app(app)
socketio = SocketIO(app)


# --- HTTP Routes ---
@app.route('/')
def home():
    themes = Theme.query.order_by(Theme.name).all()
    return render_template('home.html', themes=themes)

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/generate', methods=['POST'])
def generate_idea():
    data = request.get_json()
    theme_id = data.get('theme_id')
    difficulty = data.get('difficulty')

    if not theme_id:
        return jsonify({'error': 'Theme ID is required'}), 400

    # 1. Start query on ProjectIdea model
    query = ProjectIdea.query.filter_by(theme_id=theme_id)
    
    # 2. Join the HackathonKit to get the related data
    query = query.join(HackathonKit)

    # 3. FIX: If a difficulty is specified, filter the ProjectIdea model explicitly
    if difficulty:
        # We must use ProjectIdea.difficulty to tell SQLAlchemy to filter the *first* joined table
        query = query.filter(ProjectIdea.difficulty == difficulty) 

    # Fetch up to 3 random ideas along with their kits
    ideas = query.order_by(db.func.random()).limit(3).all()
    
    if not ideas:
        return jsonify({'error': 'No ideas found for this theme and difficulty. Try another combination!'}), 404

    # Loop and package the pre-linked kit for each idea
    response_data = []
    for idea in ideas:
        # FIX: The relationship 'kit_link' is returning a list. Check if it's a list and get the first item.
        # This occurs due to conflicting backrefs in models.py causing SQLAlchemy to treat the relationship as one-to-many.
        kit = idea.kit
        if isinstance(kit, list) and len(kit) > 0:
            kit = kit[0]
        elif isinstance(kit, list) and len(kit) == 0:
             # Handle case where the kit link is missing after join filter
             continue
        
        # Package the idea and its pre-linked kit together
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


# --- NEW API ROUTES FOR SECURE ROOMS ---
@app.route('/api/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('room_name').strip()
    
    if not room_name:
        return jsonify({'error': 'Room name cannot be empty.'}), 400

    # Check if the room name already exists
    existing_room = ChatRoom.query.filter_by(room_name=room_name).first()
    if existing_room:
        return jsonify({'error': f"Room name '{room_name}' already taken."}), 409
    
    # Generate a unique secret code (e.g., a 6-character alphanumeric string)
    secret_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Create and save the new room
    new_room = ChatRoom(room_name=room_name, secret_code=secret_code)
    db.session.add(new_room)
    db.session.commit()
    
    return jsonify({
        'message': 'Room created successfully!',
        'room_name': new_room.room_name,
        'secret_code': new_room.secret_code
    }), 201

@app.route('/api/join_room', methods=['POST'])
def join_room_with_code():
    data = request.get_json()
    room_name = data.get('room_name').strip()
    secret_code = data.get('secret_code').strip()

    if not room_name or not secret_code:
        return jsonify({'error': 'Room name and secret code are required to join.'}), 400

    # Find the room and validate the secret code
    room = ChatRoom.query.filter_by(room_name=room_name, secret_code=secret_code).first()
    
    if not room:
        return jsonify({'error': 'Invalid room name or secret code.'}), 401
    
    return jsonify({
        'message': 'Successfully joined room!',
        'room_name': room.room_name
    }), 200


# --- SocketIO Real-Time Events ---
@socketio.on('join')
def on_join(data):
    username = data.get('username', 'Anonymous')
    team_id = data['team_id']
    join_room(team_id)
    emit('status', {'msg': f'{username} has entered the room.'}, room=team_id)

@socketio.on('send_message')
def on_send_message(data):
    team_id = data['team_id']
    
    message = ChatMessage(
        team_id=team_id, 
        username=data['username'], 
        message=data['message']
    )
    db.session.add(message)
    db.session.commit()
    
    emit('new_message', {
        'username': message.username,
        'message': message.message,
        'timestamp': message.timestamp.strftime('%I:%M %p')
    }, room=team_id)


# --- Main Execution ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
