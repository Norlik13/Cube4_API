import json

from flask import jsonify, request, Response
from models import Wine
from databaseSet import db
from flask_restx import fields, Resource, Namespace

api = Namespace('wines', description="Opérations liées aux fournisseurs de vin")

wine_model = api.model('Wine', {
    'idWine': fields.Integer(description='ID du vin'),
    'cuvee_name': fields.String(required=True, description='Nom de la cuvée'),
    'Vintage': fields.Integer(required=True, description='Année'),
    'provider_price': fields.Float(required=True, description='Prix fournisseur'),
    'selling_price': fields.Float(required=True, description='Prix de vente'),
    'stock_quantity': fields.Integer(required=True, description='Quantité en stock'),
    'Color_idColor': fields.Integer(description='ID Couleur'),
    'Cepage_idCepage': fields.Integer(description='ID Cépage'),
    'Appellation_idAppellation': fields.Integer(description='ID Appellation'),
    'Provider_idProvider': fields.Integer(description='ID Fournisseur')
})

wine_patch_model = api.model('WinePatch', {
    'stock_quantity': fields.Integer(description='Quantité en stock')
})

@api.route('/')
class WineList(Resource):
    @api.doc('get_wines')
    def get(self):
        wines = Wine.query.all()
        result = []
        for wine in wines:
            result.append({
                'idWine': wine.idWine,
                'provider_price': wine.provider_price,
                'selling_price': wine.selling_price,
                'stock_quantity': wine.stock_quantity,
                'Vintage': wine.Vintage,
                'Sparkling': wine.Sparkling,
                'cuvee_name': wine.cuvee_name,
                'Color': {'Color_color': wine.color.color, 'Color_id': wine.color.idColor} if wine.color else None,
                'Cepage': {'Cepage_cepage': wine.cepage.cepage, 'Cepage_id': wine.cepage.idCepage} if wine.cepage else None,
                'Appellation': {'Appellation_name': wine.appellation.appellation, 'Appellation_id': wine.appellation.idAppellation} if wine.appellation else None,
                'Provider': {'Provider_domain_name': wine.provider.domain_name, 'Provider_id': wine.provider.idProvider, 'Provider_phone_number': wine.provider.phone_number} if wine.provider else None
            })
        return jsonify(result)

    @api.expect(wine_model)
    @api.doc('create_wine')
    def post(self):
        data = request.get_json()
        wine = Wine(
            provider_price=data['provider_price'],
            selling_price=data['selling_price'],
            stock_quantity=data['stock_quantity'],
            Vintage=data['Vintage'],
            Sparkling=data['Sparkling'],
            cuvee_name=data['cuvee_name'],
            Color_idColor=data['Color_idColor'],
            Cepage_idCepage=data['Cepage_idCepage'],
            Appellation_idAppellation=data['Appellation_idAppellation'],
            Provider_idProvider=data['Provider_idProvider']
        )
        db.session.add(wine)
        db.session.commit()
        response_data = {'message': 'Vin crée', 'id': wine.idWine}
        response = Response(response=json.dumps(response_data), status=201, mimetype='application/json')
        return response


@api.route('/<int:wine_id>')
@api.param('wine_id', 'L\'ID du vin')
class WineResource(Resource):
    @api.doc('get_wine')
    def get(self, wine_id):
        wine = Wine.query.get_or_404(wine_id)
        result = {
            'idWine': wine.idWine,
            'provider_price': wine.provider_price,
            'selling_price': wine.selling_price,
            'stock_quantity': wine.stock_quantity,
            'Vintage': wine.Vintage,
            'Sparkling': wine.Sparkling,
            'cuvee_name': wine.cuvee_name,
            'Color': {'Color_color': wine.color.color, 'Color_id': wine.color.idColor} if wine.color else None,
            'Cepage': {'Cepage_cepage': wine.cepage.cepage, 'Cepage_id': wine.cepage.idCepage} if wine.cepage else None,
            'Appellation': {'Appellation_name': wine.appellation.appellation, 'Appellation_id': wine.appellation.idAppellation} if wine.appellation else None,
            'Provider': {'Provider_domain_name': wine.provider.domain_name, 'Provider_id': wine.provider.idProvider, 'Provider_phone_number': wine.provider.phone_number} if wine.provider else None
        }
        return jsonify(result)

    @api.doc('delete_wine')
    def delete(self, wine_id):
        wine = Wine.query.get(wine_id)
        db.session.delete(wine)
        db.session.commit()
        return jsonify({'message': 'Vin Supprimé'})

    @api.expect(wine_model)
    @api.doc('update_wine')
    def put(self, wine_id):
        data = request.get_json()
        wine = Wine.query.get(wine_id)
        wine.provider_price = data['provider_price']
        wine.selling_price = data['selling_price']
        wine.stock_quantity = data['stock_quantity']
        wine.Vintage = data['Vintage']
        wine.Sparkling = data['Sparkling']
        wine.cuvee_name = data['cuvee_name']
        wine.Color_idColor = data['Color_idColor']
        wine.Cepage_idCepage = data['Cepage_idCepage']
        wine.Appellation_idAppellation = data['Appellation_idAppellation']
        wine.Provider_idProvider = data['Provider_idProvider']
        db.session.commit()
        return jsonify({'message': 'Vin Modifié'})


@api.route('/inventory/<int:wine_id>')
@api.param('wine_id', 'L\'ID du vin')
class WineInventory(Resource):
    @api.expect(wine_patch_model)
    @api.doc('update_stock')
    def put(self, wine_id):
        data = request.get_json()
        wine = Wine.query.get(wine_id)
        wine.stock_quantity = data['stock_quantity']
        db.session.commit()
        return jsonify({'message': 'Stock Mis à jour'})
