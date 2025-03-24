import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai 
import requests
import random

app = Flask(_name_)
CORS(app)

GEMINI_API_KEY = "AIzaSyDhvYjjCg_JiwV7ZRch-Akaf2BLdIk8lG4"


GENESIS_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Initialize conversation history
conversation_history = []
quotes = [
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Do what you can, with what you have, where you are. – Theodore Roosevelt",
    "Opportunities don't happen. You create them. – Chris Grosser",
    "It does not matter how slowly you go as long as you do not stop. – Confucius",
    "Hardships often prepare ordinary people for an extraordinary destiny. – C.S. Lewis",
    "If you want to go fast, go alone. If you want to go far, go together. – African Proverb",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Your time is limited, so don’t waste it living someone else’s life. – Steve Jobs",
    "Dream big, start small, act now. – Robin Sharma"
]

# Initialize user goal data
user_goals = {}

def track_goal(user_id, goal):
    if user_id not in user_goals:
        user_goals[user_id] = {
            'goal': goal,
            'progress': 0
        }

def update_goal_progress(user_id, progress):
    if user_id in user_goals:
        user_goals[user_id]['progress'] = progress

def get_goal_progress(user_id):
    if user_id in user_goals:
        goal_info = user_goals[user_id]
        return f"Your goal: {goal_info['goal']}\nProgress: {goal_info['progress']}%"
    else:
        return "You haven't set a goal yet."

def get_daily_wisdom():
    
    quote = random.choice(quotes)
    formatted_quote = f"<strong><em style='color: #00ffff;'>{quote}</em></strong>"
    return formatted_quote

def process_journal_entry(user_id, entry):
    return f"Your reflection: '{entry}' has been noted. Keep up the great work! Here's a tip for today: 'Consistency is key to progress.'"

@app.route("/api/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    user_id = request.json.get("user_id")
    print("Received message:", user_message)

    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you rephrase?"})

    try:
        if "set goal" in user_message.lower():
            goal = user_message.lower().replace("set goal", "").strip()
            track_goal(user_id, goal)
            return jsonify({"response": f"Goal '{goal}' has been set! I’ll check in with you daily on your progress."})

        if "progress" in user_message.lower():
            progress = int(user_message.split()[-1])  
            update_goal_progress(user_id, progress)
            return jsonify({"response": f"Your progress is now {progress}%!"})

        if "goal progress" in user_message.lower():
            return jsonify({"response": get_goal_progress(user_id)})

        # Handle journal entry
        if "journal" in user_message.lower():
            journal_entry = user_message.lower().replace("journal", "").strip()
            return jsonify({"response": process_journal_entry(user_id, journal_entry)})

        # Respond with wisdom of the day
        if "wisdom" in user_message.lower():
            return jsonify({"response": get_daily_wisdom()})

        conversation_history.append({"role": "user", "content": user_message})

        prompt = "\n".join([f"{entry['role']}: {entry['content']}" for entry in conversation_history])
        print(f"Prompt being sent to the model: {prompt}")

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "top_p": 0.9,
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"}
            ]
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(GENESIS_API_URL, json=payload, headers=headers)

        print(f"API Response: {response.json()}")

        if response.status_code == 200:
            api_response = response.json()
            print("API Response JSON:", api_response)
            bot_response = api_response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '').strip()

            if "goal" in user_message.lower():
                final_response = get_goal_progress(user_id)
            else:
                try:
                    bot_response_json = json.loads(bot_response)
                    final_response = bot_response_json.get("response", "I couldn't understand that.") + "\n\n" + bot_response_json.get("quote", "")
                except json.JSONDecodeError:
                    final_response = f"{bot_response}\n\n{get_daily_wisdom()}"

        else:
            final_response = "Sorry, something went wrong with the API call."

        conversation_history.append({"role": "Twaine", "content": final_response})

        print("Final bot response:", final_response)
        return jsonify({"response": final_response})
    except Exception as e:
        print(f"Error during API call: {e}")
        final_response = "Oops! Something went wrong. Try again later."

        return jsonify({"response": final_response})

if _name_ == "_main_":
    app.run(debug=True)
