from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)


genai.configure(api_key='AIzaSyCjlhjKevHstddTPlt1Qjfg3XloMQOV-Zc')        # Google Gemini API key

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


def get_response_from_ai(user_input):                 # Function to get response from AI
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)
    return response.text


@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    bot_reply = get_response_from_ai(user_input)

    clean_reply = bot_reply.replace('```', '').replace('**', '')  # Remove backticks and asterisks

    return jsonify({'reply': clean_reply.strip()})  # strip any extra whitespace


@app.route('/')
def initiate_chat():
    return render_template('chatbot.html')


if __name__ == '__main__':
    app.run(debug=True)
