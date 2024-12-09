from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/thetadata', methods=['POST'])
def handle_request():
    data = request.get_json()

    # Extract the components from the request
    method = data.get('method')
    url = data.get('url')
    config = data.get('config', {})
    params = data.get('params', {})  # Additional query parameters
    headers = data.get('headers', {})  # Additional headers

    
    try:
        # Make the HTTP request using the given method, url, and additional parameters
        response = requests.request(
            method,
            url,
            params=params,
            headers=headers,
            **config
        )        
        # Format and return the response
        return jsonify({
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'data': response.json(),
            'text': response.text
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000)
 