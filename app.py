from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-latest")

@app.route('/api/gen', methods=['GET'])
def generate_response():
    query = request.args.get('ask')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    
    try:
        response = model.generate_text(
            prompt=query,
            temperature=0.7,
            max_output_tokens=1024
        )
        return jsonify({'response': response.result})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
