from flask import Flask, request, jsonify
import socket
import requests
from urllib.parse import urlparse
import time
app = Flask(__name__)

def get_ip_from_url(url):
    try:
        # Parse the URL to extract the hostname
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        if hostname:
            # Resolve the IP address using socket.gethostbyname
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        else:
            return None
    except socket.gaierror as e:
        return None

def is_localhost_ip(ip_address):
    return ip_address == '127.0.0.1' or ip_address == '::1'



@app.route('/', methods=['GET'])
def home():
    return "your flag is w3434."

# API Endpoint to resolve IP from a given URL (GET request)
@app.route('/resolve-ip', methods=['GET'])
def resolve_ip():
    url = request.args.get('url')  # Get the 'url' query parameter from the request

    if not url:
        return jsonify({"error": "URL is required"}), 400

    ip_address = get_ip_from_url(url)
    if ip_address:
        if is_localhost_ip(ip_address):
            return jsonify({"error": "Localhost IP addresses are not allowed"}), 400

        file_contents = requests.get(url).text
        return file_contents
    else:
        return jsonify({"error": "Failed to resolve IP"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
