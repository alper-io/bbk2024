from flask import Flask, request, jsonify
import sqlite3
import os
import redis

app = Flask(__name__)

# Initialize Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

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
    # Optionally store in Redis for caching
    redis_client.set(data['username'], data['email'])
    return jsonify({"message": "User created"}), 201

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    # First check Redis cache
    email = redis_client.get(username)
    if email:
        return jsonify({"username": username, "email": email}), 200

    with sqlite3.connect('database.db') as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
    if user:
        # Cache the user data in Redis
        redis_client.set(user[1], user[2])
        return jsonify({"username": user[1], "email": user[2]}), 200
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
