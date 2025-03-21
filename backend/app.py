
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai 
import requests

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "II"


GENESIS_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Initialize conversation history
conversation_history = []

@app.route("/api/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    print("Received message:", user_message)

    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you rephrase?"})

    try:
        conversation_history.append({"role": "user", "content": user_message})

    
        prompt = "\n".join([f"{entry['role']}: {entry['content']}" for entry in conversation_history])
        print(f"Prompt being sent to the model: {prompt}")

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(GENESIS_API_URL, json=payload, headers=headers)

        print(f"API Response: {response.json()}")

        if response.status_code == 200:
            api_response = response.json()
            print("API Response JSON:", api_response)
            bot_response = api_response['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            bot_response = "Sorry, something went wrong with the API call."

        conversation_history.append({"role": "Twaine", "content": bot_response})

        print("Bot response:", bot_response)

    except Exception as e:
        print(f"Error during API call: {e}")
        bot_response = "Oops! Something went wrong. Try again later."

    # Return the bot's response in JSON format
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)