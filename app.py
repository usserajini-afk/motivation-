from flask import Flask, render_template, request, jsonify
import os
import json
import google.generativeai as genai

app = Flask(__name__)

# Set your API key here (replace with your actual Gemini API key from https://aistudio.google.com/app/apikey)
os.environ["GEMINI_API_KEY"] = "AIzaSyAiGNKEwwj0PnZL05yoxdUlU62cGaJgV1s"
# Some Google client libraries (including the GenAI client) also look for GOOGLE_API_KEY.
os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

system_instruction = """You are a motivational chatbot.
Your purpose is to provide motivational guidance and positive encouragement.
Only respond to questions or topics related to motivation, self-improvement, personal growth, overcoming challenges, or seeking positive advice.
If the user's question is not related to motivation or positive guidance (e.g., general knowledge, math, science, unrelated topics), politely decline and redirect them to ask about motivation.
Always respond with motivational content when appropriate, and encourage users in every life situation.
Never give negative or discouraging responses.
"""

CHAT_FILE = 'chats.json'

def load_chats():
    # Ensure the chat storage file exists and is valid JSON.
    if not os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, 'w') as f:
            json.dump({}, f)
        return {}

    try:
        with open(CHAT_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # If the file is corrupted, reset it.
        with open(CHAT_FILE, 'w') as f:
            json.dump({}, f)
        return {}

def save_chats(chats):
    with open(CHAT_FILE, 'w') as f:
        json.dump(chats, f)

chats = load_chats()  # Load chats from file on startup

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    # Use a supported model name for generateContent (gemini-1.5-flash is not available on v1beta API)
    model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction=system_instruction)
    print("Gemini model initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Gemini model: {e}")
    model = None

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    if model is None:
        return jsonify({"reply": "Sorry, the AI service is currently unavailable. Stay positive!"})

    data = request.json
    user_message = data.get("message", "")
    chat_id = data.get("chat_id", "default")

    try:
        response = model.generate_content(user_message)
        reply = response.text

        # Store the conversation
        if chat_id not in chats:
            chats[chat_id] = []
        chats[chat_id].append({'user': user_message, 'bot': reply})
        save_chats(chats)  # Save to file

        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"reply": "I'm here to motivate you! Let's try again with a positive mindset."})


@app.route("/history")
def history():
    print(f"Loaded chats: {chats}")  # Debug
    # Return list of chat ids with titles (first user message)
    history_list = []
    for chat_id, messages in chats.items():
        if messages:
            title = messages[0]['user'][:30] + "..." if len(messages[0]['user']) > 30 else messages[0]['user']
        else:
            title = "Empty Chat"
        history_list.append({'id': chat_id, 'title': title})
    print(f"History list: {history_list}")  # Debug
    return jsonify(history_list)


@app.route("/load_chat/<chat_id>")
def load_chat(chat_id):
    messages = chats.get(chat_id, [])
    return jsonify(messages)



if __name__ == "__main__":
    app.run(debug=True)