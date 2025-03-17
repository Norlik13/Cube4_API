# from .api_routes import api_bp, api
# from flask import jsonify, request
# from models import Appellation
# from databaseSet import db
# from flask_restx import fields
#
# appellation_model = api.model('Appellation', {
#     'idAppellation': fields.Integer(description="ID de l'appelation"),
#     'appellation': fields.String(required=True, description="Nom de l'appellation")
# })
#
#
# @api_bp.route('/appellations', methods=['GET'])
# def get_appellations():
#     appellations = Appellation.query.all()
#     result = [{'idAppellation': appellation.idAppellation, 'appellation': appellation.appellation} for appellation in
#               appellations]
#     return jsonify(result), 200
#
#
# @api_bp.route('/appellations', methods=['POST'])
# def create_appellation():
#     data = request.get_json()
#     appellation = Appellation(appellation=data['appellation'])
#     db.session.add(appellation)
#     db.session.commit()
#     return jsonify({'message': 'Appellation created', 'id': appellation.idAppellation}), 201
import json

from flask import request, jsonify, Response
from flask_restx import Namespace, Resource, fields
from databaseSet import db
from models.Appellation import Appellation

api = Namespace('appellations', description="Opérations liées aux appellations")

appellation_model = api.model('Appellation', {
    'idAppellation': fields.Integer(description="ID de l'appellation"),
    'appellation': fields.String(required=True, description="Nom de l'appellation")
})

@api.route('/')
class AppellationList(Resource):
    @api.doc('get_appellations')
    def get(self):
        """Récupère la liste des appellations"""
        appellations = Appellation.query.all()
        return jsonify([{'idAppellation': a.idAppellation, 'appellation': a.appellation} for a in appellations])

    @api.expect(appellation_model)
    @api.doc('create_appellation')
    def post(self):
        """Ajoute une nouvelle appellation"""
        data = request.get_json()
        appellation = Appellation(appellation=data['appellation'])
        db.session.add(appellation)
        db.session.commit()
        response_data = {'message': 'Appellation crée', 'id': appellation.idAppellation}
        response = Response(response=json.dumps(response_data), status=201, mimetype='application/json')
        return response

@api.route('/<int:appellation_id>')
@api.param('appellation_id', 'L\'ID de l\'appellation')
class AppellationResource(Resource):
    @api.doc('delete_appellation')
    def delete(self, appellation_id):
        """Supprime une appellation"""
        appellation = Appellation.query.get_or_404(appellation_id)
        db.session.delete(appellation)
        db.session.commit()
        return jsonify({'message': 'Appellation supprimé'})
