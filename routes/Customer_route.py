import json
from flask import jsonify, request, Response
from flask_restx import Namespace, Resource, fields
from databaseSet import db
from models.Customer import Customer

api = Namespace('customers', description="Opérations sur les clients")

# Define Swagger Model for Customer
customer_model = api.model('Customer', {
    'idCustomer': fields.Integer(description='ID du client'),
    'customer_name': fields.String(required=True, description='Nom du client'),
    'mail_address': fields.String(required=True, description='Adresse mail'),
    'password': fields.String(required=True, description='Mot de passe')  # Can be hashed in production
})

# Route: Get All Customers & Create a Customer
@api.route('/')
class CustomerList(Resource):
    @api.doc('get_customers')
    def get(self):
        """Récupère la liste de tous les clients"""
        customers = Customer.query.all()
        return jsonify([
            {'idCustomer': c.idCustomer, 'customer_name': c.customer_name, 'mail_address': c.mail_address}
            for c in customers
        ])

    @api.expect(customer_model)
    @api.doc('create_customer')
    def post(self):
        """Ajoute un nouveau client"""
        data = request.get_json()
        customer = Customer(
            customer_name=data['customer_name'],
            mail_address=data['mail_address'],
            password=data['password']
        )
        db.session.add(customer)
        db.session.commit()
        response_data = {'message': 'Client crée', 'id': customer.idCustomer}
        response = Response(response=json.dumps(response_data), status=201, mimetype='application/json')
        return response


# Route: Get, Update, Delete a Specific Customer
@api.route('/<int:customer_id>')
@api.param('customer_id', 'L\'ID du client')
class CustomerResource(Resource):
    @api.doc('get_customer')
    def get(self, customer_id):
        """Récupère un client par ID"""
        customer = Customer.query.get_or_404(customer_id)
        response_data = {'idCustomer': customer.idCustomer, 'customer_name': customer.customer_name, 'mail_address': customer.mail_address}
        response = Response(response=json.dumps(response_data), mimetype='application/json')
        return response

    @api.expect(customer_model)
    @api.doc('update_customer')
    def put(self, customer_id):
        """Met à jour un client"""
        data = request.get_json()
        customer = Customer.query.get_or_404(customer_id)

        customer.customer_name = data.get('customer_name', customer.customer_name)
        customer.mail_address = data.get('mail_address', customer.mail_address)
        if 'password' in data and data['password']:
            customer.password = data['password']

        db.session.commit()
        response_data = {'message': 'Customer updated'}
        response = Response(response=json.dumps(response_data), mimetype='application/json')
        return response

    @api.doc('delete_customer')
    def delete(self, customer_id):
        """Supprime un client"""
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        response_data = {'message': 'Client supprimé'}
        response = Response(response=json.dumps(response_data), mimetype='application/json')
        return response


# Route: Authenticate a Customer
@api.route('/authenticate')
class CustomerAuth(Resource):
    @api.expect(customer_model)
    @api.doc('authenticate_customer')
    def post(self):
        """Authentifie un client"""
        data = request.get_json()
        customer = Customer.query.filter_by(customer_name=data['customer_name'], password=data['password']).first()
        if customer:
            response_data = {'message': 'Client authentifié', 'idCustomer': customer.idCustomer, 'customer_name': customer.customer_name}
            response = Response(response=json.dumps(response_data), mimetype='application/json')
            return response
        else:
            response_data = {'message': 'Client non trouvé'}
            response = Response(response=json.dumps(response_data), status=404, mimetype='application/json')
            return response
