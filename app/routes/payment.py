from flask import Blueprint, request, jsonify, session
import stripe
from app.config import Config
from app.tasks import publish_message

payment_bp = Blueprint('payment', __name__)
stripe.api_key = Config.STRIPE_SECRET_KEY

@payment_bp.route('/payment/create', methods=['POST'])
def create_payment():
    data = request.json
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(data['amount']) * 100,
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
            publish_message('payment_notifications', {
                'booking_id': data['payment_intent_id'],
                'status': 'success'
            })
            return jsonify({'message': 'Payment successful'})
        return jsonify({'error': 'Payment not completed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/payment/offline', methods=['POST'])
def offline_payment():
    data = request.json
    publish_message('payment_notifications', {
        'booking_id': data['booking_id'],
        'status': 'offline_approved'
    })
    return jsonify({
        'message': f"Offline payment recorded for booking {data['booking_id']}"
    })