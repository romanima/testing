import datetime

from flask import Blueprint, jsonify, request
from app import db
from app.models import Client, Parking, ClientParking

bp = Blueprint('api', __name__)

def register_routes(app):
    @bp.route('/clients', methods=['GET'])
    def get_clients():
        clients = Client.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'surname': c.surname,
            'credit_card': c.credit_card,
            'car_number': c.car_number
        } for c in clients])

    @bp.route('/parkings', methods=['GET'])
    def get_parkings():
        parkings = Parking.query.all()
        return jsonify([{
            'id': p.id,
            'address': p.address,
            'opened': p.opened,
            'count_places': p.count_places,
            'count_available_places': p.count_available_places
        } for p in parkings])

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        client = Client.query.get_or_404(client_id)
        return jsonify({
            'id': client.id,
            'name': client.name,
            'surname': client.surname,
            'credit_card': client.credit_card,
            'car_number': client.car_number
        })

    @app.route('/clients', methods=['POST'])
    def create_client():
        data = request.get_json()
        client = Client(
            name=data['name'],
            surname=data['surname'],
            credit_card=data.get('credit_card'),
            car_number=data['car_number']
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({'id': client.id}), 201

    @app.route('/parkings', methods=['POST'])
    def create_parking():
        data = request.get_json()
        parking = Parking(
            address=data['address'],
            opened=data.get('opened', True),
            count_places=data['count_places'],
            count_available_places=data['count_places']
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify({'id': parking.id}), 201

    @app.route('/client_parkings', methods=['POST'])
    def enter_parking():
        data = request.get_json()
        client_id, parking_id = data['client_id'], data['parking_id']

        client = Client.query.get_or_404(client_id)
        parking = Parking.query.get_or_404(parking_id)

        if not parking.opened:
            return jsonify({'error': 'Parking is closed'}), 400
        if parking.count_available_places <= 0:
            return jsonify({'error': 'No available places'}), 400

        existing = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id
        ).first()
        if existing:
            return jsonify({'error': 'Client already in parking'}), 400

        log = ClientParking(client_id=client_id, parking_id=parking_id)
        parking.count_available_places -= 1
        db.session.add_all([log, parking])
        db.session.commit()
        return jsonify({'id': log.id}), 201

    @app.route('/client_parkings', methods=['DELETE'])
    def exit_parking():
        data = request.get_json()
        client_id, parking_id = data['client_id'], data['parking_id']

        log = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id
        ).first_or_404()
        client = Client.query.get_or_404(client_id)

        if not client.credit_card:
            return jsonify({'error': 'No credit card for payment'}), 400

        parking = Parking.query.get_or_404(parking_id)
        log.time_out = datetime.utcnow()
        parking.count_available_places += 1
        db.session.add_all([log, parking])
        db.session.commit()
        return jsonify({'message': 'Exit successful'}), 200
