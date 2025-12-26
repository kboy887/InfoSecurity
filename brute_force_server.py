#!/usr/bin/env python3
"""
Lab 12: Brute-Force Attack - FastAPI Server
Simple login server for demonstrating brute-force attacks
"""

from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Hardcoded credentials for demonstration
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345admin"

@app.get("/", response_class=HTMLResponse)
def root():
    """Simple login page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <style>
            body { font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; }
            form { padding: 20px; border: 1px solid #ccc; border-radius: 5px; }
            input { margin: 10px 0; padding: 8px; width: 200px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <form method="post" action="/login">
            <h2>Login</h2>
            <div><input type="text" name="username" placeholder="Username" required></div>
            <div><input type="password" name="password" placeholder="Password" required></div>
            <div><button type="submit">Login</button></div>
        </form>
    </body>
    </html>
    """

@app.post("/login")
def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    """
    Login endpoint that checks username and password.
    Returns a secret token if credentials are correct.
    """
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {"status": "success", "message": "Login successful!", "token": "secret_token_12345"}
    return {"status": "error", "message": "Invalid credentials"}

if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("Brute-Force Demo Server")
    print("="*60)
    print(f"Username: {ADMIN_USERNAME}")
    print(f"Password: {ADMIN_PASSWORD}")
    print("Server running on http://127.0.0.1:8000")
    print("="*60)
    uvicorn.run(app, host="127.0.0.1", port=8000)

