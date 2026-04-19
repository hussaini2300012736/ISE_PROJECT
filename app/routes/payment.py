from flask import Blueprint, request, jsonify, session
import stripe
from app.config import Config

payment_bp = Blueprint('payment', __name__)
stripe.api_key = Config.STRIPE_SECRET_KEY

@payment_bp.route('/payment/create', methods=['POST'])
def create_payment():
    data = request.json
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(data['amount']) * 100,  # convert to cents
            currency='usd',
            metadata={'booking_id': data['booking_id']}
        )
        return jsonify({'client_secret': intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/payment/confirm', methods=['POST'])
def confirm_payment():
    data = request.json
    try:
        intent = stripe.PaymentIntent.retrieve(data['payment_intent_id'])
        if intent.status == 'succeeded':
            return jsonify({'message': 'Payment successful'})
        return jsonify({'error': 'Payment not completed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/payment/offline', methods=['POST'])
def offline_payment():
    data = request.json
    # Admin approves offline payment manually
    return jsonify({
        'message': f"Offline payment recorded for booking {data['booking_id']}"
    })