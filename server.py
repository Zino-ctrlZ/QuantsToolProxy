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
        # Return the entire response content
        return jsonify({
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.content.decode(response.encoding if response.encoding else 'utf-8'),
            'data': response.json() if response.headers.get('Content-Type') == 'application/json' else response.text,
            'text': response.text,
            'url': response.url,
            'reason': response.reason,
            'elapsed': response.elapsed.total_seconds(),
            'cookies': response.cookies.get_dict(),
            'history': [r.url for r in response.history],
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000)
 