from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from config import Config

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

# Set OpenAI API key
openai.api_key = Config.OPENAI_API_KEY

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
        )

        return jsonify({"response": response["choices"][0]["message"]["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
