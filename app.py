from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = 'AIzaSyAIhSFUE5i4NYnve8LJXoN8pxhcIMrgmJA'  # Replace 'YOUR_API_KEY' with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/api/gen', methods=['GET'])
def generate_response():
    query = request.args.get('prompt')
    if not query:
        return jsonify({'error': 'Missing prompt parameter'}), 400

    try:
        response = genai.generate_text(
            model="models/gemini-1.5-flash-latest",
            prompt=query,
            temperature=0.7,
            max_output_tokens=1024
        )

        return jsonify({'response': response.text})
    except Exception as e:
        error_message = str(e)
        if "400" in error_message:
            return jsonify({'error': 'Invalid request or model name'}), 400
        elif "401" in error_message:
            return jsonify({'error': 'Unauthorized - check your API key'}), 401
        else:
            return jsonify({'error': f'An error occurred: {e}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
