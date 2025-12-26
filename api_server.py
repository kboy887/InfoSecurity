#!/usr/bin/env python3
"""
Lab 10: Simple API Server for NGINX proxy_pass demonstration
This server will be proxied through NGINX
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# API endpoints
@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        "message": "API Server is running",
        "status": "active",
        "info": "This API is being served through NGINX reverse proxy",
        "endpoints": {
            "/": "This endpoint",
            "/api/data": "Get sample data",
            "/api/users": "Get users list",
            "/api/echo": "Echo request data",
            "/api/info": "Get server information"
        }
    })

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get sample data"""
    return jsonify({
        "data": [
            {"id": 1, "name": "Item 1", "value": 100},
            {"id": 2, "name": "Item 2", "value": 200},
            {"id": 3, "name": "Item 3", "value": 300}
        ],
        "total": 3
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get users list"""
    return jsonify({
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
            {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
        ]
    })

@app.route('/api/echo', methods=['GET', 'POST'])
def echo():
    """Echo request data"""
    return jsonify({
        "method": request.method,
        "headers": dict(request.headers),
        "args": dict(request.args),
        "data": request.get_json() if request.is_json else None,
        "form": dict(request.form) if request.form else None
    })

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get server information"""
    return jsonify({
        "server": "Flask API Server",
        "port": 5000,
        "proxy": {
            "x-real-ip": request.headers.get('X-Real-IP', 'Not set'),
            "x-forwarded-for": request.headers.get('X-Forwarded-For', 'Not set'),
            "x-forwarded-proto": request.headers.get('X-Forwarded-Proto', 'Not set'),
            "host": request.headers.get('Host', 'Not set')
        }
    })

@app.route('/api/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "uptime": "running"
    })

if __name__ == '__main__':
    print("="*60)
    print("API Server for NGINX proxy_pass demonstration")
    print("="*60)
    print("Server running on http://127.0.0.1:5000")
    print("This server should be accessed through NGINX on port 8080")
    print("")
    print("Available endpoints:")
    print("  http://localhost:5000/")
    print("  http://localhost:5000/api/data")
    print("  http://localhost:5000/api/users")
    print("  http://localhost:5000/api/info")
    print("="*60)
    
    app.run(host='127.0.0.1', port=5000, debug=True)

