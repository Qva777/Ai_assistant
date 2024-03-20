import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

from rout_handlers import AIHandler, Parser
from config import Config

# Cross-Origin Resource Sharing
app = Flask(__name__)
CORS(app)

#  connect open AI key
client = OpenAI(api_key=Config.OPENAI_API_KEY)
ai_handler = AIHandler()

#  configuration for logging
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('../app.log')
app.logger.addHandler(handler)


@app.route('/query', methods=['POST'])
def handle_query():
    """ Handles POST """

    # Get user message from
    user_message = request.json.get('user_message')
    app.logger.info("Received user message: %s", user_message)

    # Get user message from
    response = Parser.extract_info_user_message(user_message)
    print("Response: %s", response)

    # AI DATA
    query_result = ai_handler.handle(response)

    return jsonify({'ai_response': query_result})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
