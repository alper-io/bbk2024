from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Initialize the database
def init_db():
    if not os.path.exists('database.db'):
        with sqlite3.connect('database.db') as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    email TEXT
                )
            ''')
            conn.commit()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the User Service API!"})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    with sqlite3.connect('database.db') as conn:
        conn.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (data['username'], data['email'])
        )
        conn.commit()
    return jsonify({"message": "User created"}), 201

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    with sqlite3.connect('database.db') as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
    if user:
        return jsonify({"username": user[1], "email": user[2]}), 200
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
