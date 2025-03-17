# from flask import request, jsonify
# from databaseSet import db
# from models.Cepage import Cepage
# from .api_routes import api_bp, api
# from flask_restx import fields
#
# cepage_model = api.model('Cepage', {
#     'idCepage': fields.Integer(description="ID du cepage"),
#     'cepage': fields.String(required=True, description="Nom du cepage")
# })
#
#
# @api_bp.route('/cepages', methods=['POST'])
# def create_cepage():
#     data = request.get_json()
#     cepage = Cepage(cepage=data['cepage'])
#     db.session.add(cepage)
#     db.session.commit()
#     return jsonify({'message': 'Cepage created', 'id': cepage.idCepage}), 201
#
#
# @api_bp.route('/cepages', methods=['GET'])
# def get_cepages():
#     cepages = Cepage.query.all()
#     result = [{'idCepage': cepage.idCepage, 'cepage': cepage.cepage} for cepage in cepages]
#     return jsonify(result), 200
import json

from flask import request, jsonify, Response
from flask_restx import Namespace, Resource, fields
from databaseSet import db
from models.Cepage import Cepage

api = Namespace('cepages', description="Oprérations liées aux cépages")

cepage_model = api.model('Cepage', {
    'idCepage': fields.Integer(description="ID du cépage"),
    'cepage': fields.String(required=True, description="Nom du cépage")
})

@api.route('/')
class CepageList(Resource):
    @api.doc('get_cepages')
    def get(self):
        """Récupère la liste des cépages"""
        cepages = Cepage.query.all()
        return jsonify([{'idCepage': c.idCepage, 'cepage': c.cepage} for c in cepages])

    @api.expect(cepage_model)
    @api.doc('create_cepage')
    def post(self):
        """Ajoute un nouveau cépage"""
        data = request.get_json()
        cepage = Cepage(cepage=data['cepage'])
        db.session.add(cepage)
        db.session.commit()
        response_data = {'message': 'Cepage created', 'id': cepage.idCepage}
        response = Response(response=json.dumps(response_data), status=201, mimetype='application/json')
        return response

@api.route('/<int:cepage_id>')
@api.param('cepage_id', 'L\'ID du cépage')
class CepageResource(Resource):
    @api.doc('delete_cepage')
    def delete(self, cepage_id):
        """Supprime un cépage"""
        cepage = Cepage.query.get_or_404(cepage_id)
        db.session.delete(cepage)
        db.session.commit()
        return jsonify({'message': 'Cepage deleted'})
