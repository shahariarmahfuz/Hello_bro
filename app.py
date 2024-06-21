from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import logging

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get('API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/gen', methods=['GET'])
def generate_response():
    query = request.args.get('ask')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    api_url = 'https://api.gemini.com/v1/completions'  
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        "prompt": query,
        "max_tokens": 100 
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status() 
        response_data = response.json()
        return jsonify(response_data)

    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}")
        return jsonify({'error': f'HTTP Error: {errh}'}), errh.response.status_code
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Error Connecting: {errc}")
        return jsonify({'error': f'Error Connecting: {errc}'}), 503 
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")
        return jsonify({'error': f'Timeout Error: {errt}'}), 504
    except requests.exceptions.RequestException as err:
        logger.error(f"Oops: Something Else: {err}")
        return jsonify({'error': f'Oops: Something Else: {err}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  
    app.run(host='0.0.0.0', port=port)
  
