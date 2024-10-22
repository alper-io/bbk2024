from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Payment model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Payment Service!"})

@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.json
    payment = Payment(amount=data['amount'], description=data['description'])
    db.session.add(payment)
    db.session.commit()
    return jsonify({"message": "Payment created", "id": payment.id}), 201

@app.route('/payments/<int:id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.get(id)
    if payment:
        return jsonify({"id": payment.id, "amount": payment.amount, "description": payment.description}), 200
    return jsonify({"message": "Payment not found"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
