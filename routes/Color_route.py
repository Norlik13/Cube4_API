import json

from flask import request, jsonify, Response
from flask_restx import Namespace, Resource, fields
from databaseSet import db
from models.Color import Color

api = Namespace('colors', description="Opérations liées aux couleurs de vin")

color_model = api.model('Color', {
    'idColor': fields.Integer(description="ID de la couleur"),
    'color': fields.String(required=True, description="Couleur du vin")
})

@api.route('/')
class ColorList(Resource):
    @api.doc('get_colors')
    def get(self):
        """Récupère la liste des couleurs"""
        colors = Color.query.all()
        return jsonify([{'idColor': c.idColor, 'color': c.color} for c in colors])

    @api.expect(color_model)
    @api.doc('create_color')
    def post(self):
        """Ajoute une nouvelle couleur"""
        data = request.get_json()
        color = Color(color=data['color'])
        db.session.add(color)
        db.session.commit()
        response_data = {'message': 'Couleur Crée', 'id': color.idColor}
        response = Response(response=json.dumps(response_data), status=201, mimetype='application/json')
        return response

@api.route('/<int:color_id>')
@api.param('color_id', 'L\'ID de la couleur')
class ColorResource(Resource):
    @api.doc('delete_color')
    def delete(self, color_id):
        """Supprime une couleur"""
        color = Color.query.get_or_404(color_id)
        db.session.delete(color)
        db.session.commit()
        return jsonify({'message': 'Couleur supprimé'})
