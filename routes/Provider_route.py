import json

from flask import jsonify, request, Response
from flask_restx import Namespace, Resource, fields
from databaseSet import db
from models.Provider import Provider

api = Namespace('providers', description="Opérations liées aux fournisseurs de vin")

provider_model = api.model('Provider', {
    'idProvider': fields.Integer(description='ID du fournisseur'),
    'domain_name': fields.String(required=True, description='Nom de domaine'),
    'phone_number': fields.Integer(required=True, description='Numéro de téléphone')
})

@api.route('/')
class ProviderList(Resource):
    @api.doc('get_providers')
    def get(self):
        """Récupère la liste des fournisseurs"""
        providers = Provider.query.all()
        return jsonify([
            {'idProvider': provider.idProvider, 'phone_number': provider.phone_number, 'domain_name': provider.domain_name}
            for provider in providers
        ])

    @api.expect(provider_model)
    @api.doc('create_provider')
    def post(self):
        """Ajoute un nouveau fournisseur"""
        data = request.get_json()
        provider = Provider(phone_number=data['phone_number'], domain_name=data['domain_name'])
        db.session.add(provider)
        db.session.commit()
        response_data = {'message': 'Fournisseur crée', 'id': provider.idProvider}
        response = Response(response=json.dumps(response_data), status=201, mimetype='application/json')
        return response

@api.route('/<int:provider_id>')
@api.param('provider_id', 'L\'ID du fournisseur')
class WineResource(Resource):
    @api.doc('delete_provider')
    def delete(self, wine_id):
        wine = Provider.query.get(wine_id)
        db.session.delete(wine)
        db.session.commit()
        return jsonify({'message': 'Fournisseur supprimé'})

    @api.expect(provider_model)
    @api.doc('update_provider')
    def put(self, provider_id):
        data = request.get_json()
        provider = Provider.query.get(provider_id)
        provider.phone_number = data['phone_number']
        provider.domain_name = data['domain_name']
        db.session.commit()
        return jsonify({'message': 'Fournisseur modifié'})

    @api.doc('get_provider')
    def get(self, provider_id):
        provider = Provider.query.get_or_404(provider_id)
        return jsonify({'idProvider': provider.idProvider, 'phone_number': provider.phone_number, 'domain_name': provider.domain_name})
