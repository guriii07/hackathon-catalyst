import random
from app import app
# ADDED ChatRoom to the imports
from models import db, Theme, ProjectIdea, TechStack, ApiRecommendation, PitchTip, HackathonKit, ChatRoom 

def seed_data():
    with app.app_context():
        # This will delete all existing data and recreate the database structure.
        db.drop_all()
        db.create_all()

        # --- 1. Create Themes ---
        theme_ai = Theme(name="Artificial Intelligence")
        theme_health = Theme(name="Healthcare Tech")
        theme_fintech = Theme(name="FinTech")
        theme_sustain = Theme(name="Sustainability")
        theme_iot = Theme(name="Internet of Things (IoT)")
        theme_social = Theme(name="Social Good")
        theme_gamedev = Theme(name="Game Development")
        theme_education = Theme(name="Education Tech")

        db.session.add_all([theme_ai, theme_health, theme_fintech, theme_sustain, theme_iot, theme_social, theme_gamedev, theme_education])
        db.session.commit()

        # --- 2. Create Project Ideas (with difficulty) ---
        ideas = [
            # --- Artificial Intelligence (AI) ---
            # Beginner
            ProjectIdea(title="Simple Sentiment Analyzer", description="A web app that takes text input and classifies it as positive, negative, or neutral using a pre-trained machine learning model.", theme=theme_ai, difficulty='Beginner'),
            ProjectIdea(title="Basic Image Classifier", description="An app that identifies a single object (e.g., cat, dog, car) in an uploaded image using a basic neural network.", theme=theme_ai, difficulty='Beginner'),
            ProjectIdea(title="Spam Email Filter", description="A program that uses a simple Naive Bayes classifier to sort incoming emails into 'inbox' or 'spam' categories.", theme=theme_ai, difficulty='Beginner'),
            # Intermediate
            ProjectIdea(title="AI-Powered Fake News Detector", description="A browser extension that uses machine learning to detect and flag potential misinformation in real-time.", theme=theme_ai, difficulty='Intermediate'),
            ProjectIdea(title="Code Refactoring Assistant", description="An intelligent tool that suggests improvements and automatically refactors messy code to improve readability and performance.", theme=theme_ai, difficulty='Intermediate'),
            ProjectIdea(title="Music Recommender Engine", description="A system that recommends songs to a user based on their listening history and genre preferences using collaborative filtering.", theme=theme_ai, difficulty='Intermediate'),
            # Advanced
            ProjectIdea(title="AI Dungeon Master for RPGs", description="An AI that dynamically generates stories and challenges for a text-based RPG, adapting to player choices.", theme=theme_ai, difficulty='Advanced'),
            ProjectIdea(title="Real-Time Object Detection", description="A mobile or web app that can identify and label multiple objects in a live video stream.", theme=theme_ai, difficulty='Advanced'),
            ProjectIdea(title="Predictive Analytics for Churn", description="Build a model that analyzes customer behavior to predict which users are most likely to stop using a service.", theme=theme_ai, difficulty='Advanced'),

            # --- Healthcare Tech ---
            # Beginner
            ProjectIdea(title="Personalized Patient Symptom Tracker", description="An app that allows patients to track their symptoms over time, providing data visualizations for their doctors.", theme=theme_health, difficulty='Beginner'),
            ProjectIdea(title="Medication Reminder App", description="A simple mobile app that sends push notifications to remind users to take their medication on schedule.", theme=theme_health, difficulty='Beginner'),
            ProjectIdea(title="Health Blog with BMI Calculator", description="A basic website that provides health tips and includes a tool for users to calculate their Body Mass Index.", theme=theme_health, difficulty='Beginner'),
            # Intermediate
            ProjectIdea(title="Gamified Physical Therapy App", description="Uses a phone's camera to track physical therapy exercises, turning them into interactive and engaging games.", theme=theme_health, difficulty='Intermediate'),
            ProjectIdea(title="Mental Health Support Chatbot", description="An anonymous chatbot that provides support, coping strategies, and resources for mental well-being using NLP.", theme=theme_health, difficulty='Intermediate'),
            ProjectIdea(title="Fitness Data Dashboard", description="An app that integrates with wearables to display and visualize a user's fitness data, like steps, heart rate, and sleep quality.", theme=theme_health, difficulty='Intermediate'),
            # Advanced
            ProjectIdea(title="COVID-19 Diagnostic Assistant", description="An app that uses medical imaging (X-rays, CT scans) to help doctors identify potential cases of lung disease.", theme=theme_health, difficulty='Advanced'),
            ProjectIdea(title="Personalized Diet Planner", description="An intelligent app that recommends a daily meal plan based on a user's health goals, allergies, and dietary preferences.", theme=theme_health, difficulty='Advanced'),
            ProjectIdea(title="Predictive Disease Risk Assessment", description="Analyzes a user's lifestyle data and family history to estimate their risk of developing certain diseases over time.", theme=theme_health, difficulty='Advanced'),

            # --- FinTech ---
            # Beginner
            ProjectIdea(title="Budgeting App for Students", description="A mobile app that connects to bank accounts and helps students manage their spending with smart insights.", theme=theme_fintech, difficulty='Beginner'),
            ProjectIdea(title="Expense Tracker with Categories", description="A simple app to log daily expenses and visualize spending habits across different categories like food, transport, and bills.", theme=theme_fintech, difficulty='Beginner'),
            ProjectIdea(title="Cryptocurrency Price Alert", description="A script or small app that monitors a cryptocurrency's price and sends an alert when it crosses a certain threshold.", theme=theme_fintech, difficulty='Beginner'),
            # Intermediate
            ProjectIdea(title="Financial Portfolio Dashboard", description="A dashboard that allows users to track their investments across multiple platforms and visualize gains and losses in real-time.", theme=theme_fintech, difficulty='Intermediate'),
            ProjectIdea(title="Automated Savings Tool", description="An app that analyzes a user's spending patterns and automatically transfers small amounts of 'spare change' into a savings account.", theme=theme_fintech, difficulty='Intermediate'),
            ProjectIdea(title="P2P Lending Simulator", description="A simulation tool that shows users the potential risks and rewards of peer-to-peer lending based on various scenarios.", theme=theme_fintech, difficulty='Intermediate'),
            # Advanced
            ProjectIdea(title="Stock Market Trend Predictor", description="Uses historical data and sentiment analysis from news articles to predict short-term stock market trends.", theme=theme_fintech, difficulty='Advanced'),
            ProjectIdea(title="Decentralized Crowdfunding Platform", description="A platform using blockchain for transparent and secure crowdfunding of creative or community projects.", theme=theme_fintech, difficulty='Advanced'),
            ProjectIdea(title="Automated Fraud Detection System", description="A machine learning model that analyzes transaction data in real-time to detect and flag fraudulent activity.", theme=theme_fintech, difficulty='Advanced'),

            # --- Sustainability ---
            # Beginner
            ProjectIdea(title="Carbon Footprint Calculator", description="An app that tracks a user's daily activities (travel, diet, energy use) to calculate and suggest ways to reduce their carbon footprint.", theme=theme_sustain, difficulty='Beginner'),
            ProjectIdea(title="Gardening App with Tips", description="A mobile app that provides a plant database and offers tips on sustainable gardening and composting for beginners.", theme=theme_sustain, difficulty='Beginner'),
            ProjectIdea(title="Eco-Friendly Store Locator", description="A web app that uses a user's location to find nearby stores that sell sustainable and locally-sourced products.", theme=theme_sustain, difficulty='Beginner'),
            # Intermediate
            ProjectIdea(title="Community Recycling Rewards Program", description="A platform that tracks recycling efforts and rewards users with points redeemable at local, eco-friendly businesses.", theme=theme_sustain, difficulty='Intermediate'),
            ProjectIdea(title="Local Produce Marketplace", description="Connects local farmers directly with consumers to reduce food miles and support local agriculture.", theme=theme_sustain, difficulty='Intermediate'),
            ProjectIdea(title="Smart Energy Dashboard", description="An app that connects to smart meters to visualize and analyze household energy consumption patterns, suggesting ways to save power.", theme=theme_sustain, difficulty='Intermediate'),
            # Advanced
            ProjectIdea(title="Air Quality Monitor Network", description="A system that uses low-cost sensors to monitor real-time air quality in a community and displays the data on an interactive map.", theme=theme_sustain, difficulty='Advanced'),
            ProjectIdea(title="Renewable Energy Grid Optimizer", description="A simulation or model that optimizes the distribution of energy from various renewable sources to meet demand.", theme=theme_sustain, difficulty='Advanced'),
            ProjectIdea(title="AI-Powered Waste Sorter", description="A computer vision system that can identify and sort different types of waste (e.g., plastic, paper, metal) on a conveyor belt.", theme=theme_sustain, difficulty='Advanced'),

            # --- Internet of Things (IoT) ---
            # Beginner
            ProjectIdea(title="Smart Pantry Manager", description="Use barcode scanning or NFC tags to track food items in your pantry, generating recipes and shopping lists automatically.", theme=theme_iot, difficulty='Beginner'),
            ProjectIdea(title="IoT-Enabled Mood Lamp", description="A lamp that changes color based on an external data source, like the local weather, stock market trends, or a social media feed.", theme=theme_iot, difficulty='Beginner'),
            ProjectIdea(title="Temperature and Humidity Monitor", description="A device that uses a sensor to monitor a room's temperature and humidity and sends the data to a web dashboard or app.", theme=theme_iot, difficulty='Beginner'),
            # Intermediate
            ProjectIdea(title="Automated Plant Watering System", description="An IoT device that monitors soil moisture and sunlight, watering plants automatically and sending alerts to your phone.", theme=theme_iot, difficulty='Intermediate'),
            ProjectIdea(title="Smart Home Security Alert", description="A system using sensors to detect motion or an open door, which triggers an alert to a user's phone.", theme=theme_iot, difficulty='Intermediate'),
            ProjectIdea(title="Smart Parking Spot Finder", description="A system that uses sensors to detect free parking spots in a lot and displays them on a map for drivers.", theme=theme_iot, difficulty='Intermediate'),
            # Advanced
            ProjectIdea(title="Pet Activity Tracker", description="A smart collar that monitors a pet's activity levels, location, and sleep patterns, viewable on a mobile app.", theme=theme_iot, difficulty='Advanced'),
            ProjectIdea(title="Autonomous Drone Delivery System", description="A platform to control a drone for autonomous delivery within a small, controlled area, like a college campus.", theme=theme_iot, difficulty='Advanced'),
            ProjectIdea(title="Smart Traffic Management", description="An IoT system that analyzes traffic patterns using road sensors or cameras to adjust traffic light timings in real-time.", theme=theme_iot, difficulty='Advanced'),

            # --- Social Good ---
            # Beginner
            ProjectIdea(title="Volunteer Opportunity Matchmaker", description="A platform that connects volunteers with non-profits based on skills, interests, and availability, like a 'Tinder for volunteering'.", theme=theme_social, difficulty='Beginner'),
            ProjectIdea(title="Local Food Bank Finder", description="An app that helps people locate the nearest food banks and provides information on how to donate or receive help.", theme=theme_social, difficulty='Beginner'),
            ProjectIdea(title="Community Event Organizer", description="A platform for local communities to create and manage events like park cleanups, fundraising drives, and neighborhood watch meetings.", theme=theme_social, difficulty='Beginner'),
            # Intermediate
            ProjectIdea(title="Accessibility Mapper for Cities", description="Crowdsources data to map and rate the accessibility of public places (ramps, elevators, etc.) for people with disabilities.", theme=theme_social, difficulty='Intermediate'),
            ProjectIdea(title="Disaster Relief Communications Hub", description="A mobile app that allows users to send and receive critical updates during a natural disaster, even with limited internet connectivity.", theme=theme_social, difficulty='Intermediate'),
            ProjectIdea(title="Blood Donor Management Platform", description="A system for hospitals and blood banks to track donor information, schedule appointments, and send alerts when specific blood types are needed.", theme=theme_social, difficulty='Intermediate'),
            # Advanced
            ProjectIdea(title="Crisis Hotline AI Assistant", description="An AI tool that provides real-time support to crisis hotline operators by summarizing conversations and suggesting relevant resources.", theme=theme_social, difficulty='Advanced'),
            ProjectIdea(title="Human Trafficking Pattern Detector", description="A tool that uses data from social media and online forums to identify patterns and flag potential human trafficking activities.", theme=theme_social, difficulty='Advanced'),
            ProjectIdea(title="Decentralized Donation Tracker", description="A blockchain-based platform for transparently tracking how donated funds are used from start to finish.", theme=theme_social, difficulty='Advanced'),

            # --- Game Development ---
            # Beginner
            ProjectIdea(title="Simple 2D Platformer", description="Create a basic side-scrolling platformer with a character that can jump, collect items, and navigate a simple level.", theme=theme_gamedev, difficulty='Beginner'),
            ProjectIdea(title="Classic Arcade Game Remake", description="Recreate a classic arcade game like Pong, Snake, or Tetris from scratch to learn game physics and logic.", theme=theme_gamedev, difficulty='Beginner'),
            ProjectIdea(title="Interactive Fiction Game", description="A text-based adventure where the player makes choices that change the story, learning about game narrative design and state management.", theme=theme_gamedev, difficulty='Beginner'),
            # Intermediate
            ProjectIdea(title="Augmented Reality Board Game", description="Enhances a physical board game with AR elements, showing 3D models and animations through a phone's camera.", theme=theme_gamedev, difficulty='Intermediate'),
            ProjectIdea(title="Multiplayer Trivia Game", description="A real-time multiplayer game where players race to answer trivia questions correctly.", theme=theme_gamedev, difficulty='Intermediate'),
            ProjectIdea(title="Tower Defense Game", description="A game where players build towers and other defenses to stop waves of enemies from reaching a specific point on the map.", theme=theme_gamedev, difficulty='Intermediate'),
            # Advanced
            ProjectIdea(title="Procedural Level Generator", description="A tool that algorithmically generates unique and playable levels for a 2D platformer or dungeon crawler game.", theme=theme_gamedev, difficulty='Advanced'),
            ProjectIdea(title="Physics-Based Puzzle Game", description="A game that relies on complex physics simulations and requires players to manipulate objects to solve puzzles.", theme=theme_gamedev, difficulty='Advanced'),
            ProjectIdea(title="Multiplayer 3D Shooter", description="A fast-paced, real-time multiplayer shooter with basic movement, shooting, and a simple level.", theme=theme_gamedev, difficulty='Advanced'),

            # --- Education Tech ---
            # Beginner
            ProjectIdea(title="Interactive Coding Tutor for Kids", description="A gamified platform that teaches the basics of programming to children through visual puzzles and challenges.", theme=theme_education, difficulty='Beginner'),
            ProjectIdea(title="Flashcard App with Spaced Repetition", description="A simple app that uses a spaced repetition algorithm to help students memorize vocabulary or facts more effectively.", theme=theme_education, difficulty='Beginner'),
            ProjectIdea(title="Interactive Quiz and Poll App", description="A web app that allows a teacher to create live quizzes and polls for students to answer in real-time.", theme=theme_education, difficulty='Beginner'),
            # Intermediate
            ProjectIdea(title="AI-Powered Study Schedule Planner", description="An application that creates an optimized study schedule for a student based on their courses, exam dates, and learning pace.", theme=theme_education, difficulty='Intermediate'),
            ProjectIdea(title="Virtual Study Buddy Chatbot", description="A chatbot that helps students with homework by providing hints, explanations, and resources on various subjects.", theme=theme_education, difficulty='Intermediate'),
            ProjectIdea(title="Personalized Learning Path Generator", description="An app that creates a customized learning path for a student based on their strengths, weaknesses, and learning goals.", theme=theme_education, difficulty='Intermediate'),
            # Advanced
            ProjectIdea(title="AR Chemistry Lab Simulator", description="An app that lets students conduct virtual chemistry experiments safely using augmented reality.", theme=theme_education, difficulty='Advanced'),
            ProjectIdea(title="Automatic Grading System for Essays", description="A tool that uses natural language processing (NLP) to automatically grade and provide feedback on student essays.", theme=theme_education, difficulty='Advanced'),
            ProjectIdea(title="Sign Language Translator", description="A computer vision application that uses a camera to translate a few common sign language gestures into text or audio.", theme=theme_education, difficulty='Advanced'),
        ]
        db.session.add_all(ideas)
        
        # --- 3. Create Tech Stacks ---
        stacks = [
            TechStack(name="Python/Flask + Vanilla JS", frontend="HTML, TailwindCSS, JS", backend="Python (Flask)", database="SQLite"),
            TechStack(name="MERN Stack", frontend="React.js", backend="Node.js (Express)", database="MongoDB"),
            TechStack(name="JAMstack", frontend="Next.js/Gatsby", backend="Serverless Functions", database="FaunaDB/Supabase"),
            TechStack(name="Django + HTMX", frontend="HTMX (Dynamic HTML)", backend="Python (Django)", database="PostgreSQL"),
            TechStack(name="Vue.js + Firebase", frontend="Vue.js", backend="Firebase (BaaS)", database="Firestore"),
            # New stacks for game dev
            TechStack(name="Unity Game Engine", frontend="Unity (C#)", backend="Firebase/Photon", database="N/A"),
            TechStack(name="Unreal Engine", frontend="Unreal (Blueprints/C++)", backend="PlayFab/Google Cloud", database="N/A"),
            # New stack for desktop/native apps
            TechStack(name="Electron + React", frontend="React.js", backend="Node.js", database="SQLite/JSON"),
            # New stack for mobile apps
            TechStack(name="React Native + Expo", frontend="React Native", backend="Node.js/Firebase", database="Firestore/RealmDB"),
        ]
        db.session.add_all(stacks)
        
        # --- 4. Create API Recommendations ---
        apis = [
            # General-purpose APIs
            ApiRecommendation(name="Twilio API", url="https://www.twilio.com/", description="Programmatically make and receive phone calls, send and receive text messages.", theme=theme_social),
            ApiRecommendation(name="Google Maps API", url="https://developers.google.com/maps/documentation/javascript/overview", description="Embed maps and geolocation features into your application.", theme=theme_iot),
            ApiRecommendation(name="Stripe API", url="https://stripe.com/docs/api", description="Process payments and manage financial transactions easily.", theme=theme_fintech),
            ApiRecommendation(name="Hugging Face Inference API", url="https://huggingface.co/docs/api-inference/index", description="Easily integrate state-of-the-art machine learning models.", theme=theme_ai),
            ApiRecommendation(name="Web Speech API", url="https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API", description="Allows for voice recognition (speech-to-text) and speech synthesis (text-to-speech) in web apps.", theme=theme_education),
            ApiRecommendation(name="Plaid API", url="https://plaid.com/docs/", description="Connect securely to users' bank accounts to access transaction data.", theme=theme_fintech),
            ApiRecommendation(name="OpenWeatherMap API", url="https://openweathermap.org/api", description="Access current weather data for any location.", theme=theme_sustain),

            # Healthcare-specific APIs
            ApiRecommendation(name="Healthify API", url="https://developer.healthify.me/", description="Provides access to a database of foods, nutrients, and recipes.", theme=theme_health),
            ApiRecommendation(name="Infermedica API", url="https://developer.infermedica.com/", description="A medical diagnostic API that helps in preliminary symptom analysis.", theme=theme_health),
            
            # Game Development-specific APIs
            ApiRecommendation(name="RAWG Video Games Database API", url="https://rawg.io/apidocs", description="The largest open video game database with info on 500,000+ games.", theme=theme_gamedev),
            ApiRecommendation(name="Steam Web API", url="https://steamapi.doc.sp.se/", description="Get game and user data from the Steam platform.", theme=theme_gamedev),

            # Sustainability-specific APIs
            ApiRecommendation(name="Recycle Coach API", url="https://developer.recyclecoach.com/", description="Provides local recycling and waste disposal information.", theme=theme_sustain),

            # IoT-specific APIs
            ApiRecommendation(name="Particle IoT API", url="https://docs.particle.io/reference/cloud-apis/api/", description="Connect and manage IoT devices to a cloud platform.", theme=theme_iot),

            # Education-specific APIs
            ApiRecommendation(name="Open Trivia Database", url="https://opentdb.com/", description="A free to use database of trivia questions.", theme=theme_education),
            ApiRecommendation(name="Quizlet API", url="https://quizlet.com/api-access", description="Create and manage flashcards, study sets, and quizzes.", theme=theme_education),
        ]
        db.session.add_all(apis)

        # --- 5. Create Pitch Tips ---
        tips = [
            PitchTip(tip="Start with the problem. Clearly explain the pain point you are solving before you introduce your solution."),
            PitchTip(tip="Know your audience. Tailor your language and focus to what the judges will find most impressive (e.g., tech, business, design)."),
            PitchTip(tip="Show, don't just tell. A live demo, even if simple, is a thousand times more powerful than a slide deck."),
            PitchTip(tip="Keep it concise. You have limited time. Practice your pitch to be clear, compelling, and within the time limit."),
            PitchTip(tip="End with a strong vision. Briefly mention the future potential and what you would build next with more time."),
            PitchTip(tip="Explain your tech stack choices. Briefly justify why you chose your specific technologies for the problem at hand.")
        ]
        db.session.add_all(tips)
        
        # --- 6. Create Chat Rooms (NEW SECTION) ---
        # Add sample rooms so users can test the new secure join feature immediately
        chat_rooms = [
            ChatRoom(room_name="apollo-11", secret_code="LUNAR69"),
            ChatRoom(room_name="matrix-01", secret_code="NEO42"),
            ChatRoom(room_name="hal-9000", secret_code="DAISY")
        ]
        db.session.add_all(chat_rooms)

        # --- 7. Link Hackathon Kits (CRITICAL FOR TOOLKIT FUNCTIONALITY) ---
        all_ideas = ProjectIdea.query.all()
        all_stacks = TechStack.query.all()
        all_apis = ApiRecommendation.query.all()
        all_tips = PitchTip.query.all()

        for idea in all_ideas:
            selected_stack = random.choice(all_stacks)
            selected_tip = random.choice(all_tips)
            
            # Attempt to select a relevant API first
            selected_api = ApiRecommendation.query.filter_by(theme=idea.theme).first()
            if not selected_api:
                selected_api = random.choice(all_apis)
            
            kit = HackathonKit(
                idea=idea,
                stack=selected_stack,
                api=selected_api,
                tip=selected_tip
            )
            db.session.add(kit)
        
        # --- Final Commit ---
        db.session.commit()
        print("Database has been seeded successfully with expanded data! ✅")

if __name__ == '__main__':
    seed_data()
