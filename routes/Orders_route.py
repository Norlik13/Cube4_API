import json

from flask import jsonify, request, Response
from flask_restx import Namespace, Resource, fields
from databaseSet import db
from models.Orders import Orders
from models.OrdersDetail import OrdersDetail

api = Namespace('orders', description="Operations related to orders and order details")

# Swagger Models for Orders and Order Details
order_model = api.model('Order', {
    'idOrders': fields.Integer(description='ID de la commande'),
    'customer_idcustomer': fields.Integer(required=False, description='ID du client'),
    'provider_idprovider': fields.Integer(required=False, description='ID du fournisseur'),
    'status': fields.String(description='Statut de la commande', required=True)
})

order_detail_model = api.model('OrderDetail', {
    'idOrdersDetail': fields.Integer(description='ID du détail de commande'),
    'quantity': fields.Integer(required=True, description='Quantité'),
    'Wine_idWine': fields.Integer(required=True, description='ID du vin associé'),
    'order_idOrders': fields.Integer(description='ID de la commande associée')
})

order_create_model = api.model('OrderCreate', {
    'customer_idcustomer': fields.Integer(description='ID du client', required=False),
    'provider_idprovider': fields.Integer(description='ID du fournisseur', required=False),
    'status': fields.String(description='Statut de la commande', required=True),
    'order_details': fields.List(fields.Nested(order_detail_model), description="Liste des détails de la commande")
})

# Route: Get All Orders & Create an Order
@api.route('/')
class OrderList(Resource):
    @api.doc('get_orders')
    def get(self):
        """Récupère la liste de toutes les commandes"""
        orders = Orders.query.all()
        result = [
            {
                'idOrders': order.idOrders,
                'customer_idcustomer': order.Customer_idCustomer,
                'provider_idprovider': order.Provider_idProvider,
                'status': order.status
            } for order in orders
        ]
        return jsonify(result)

    @api.expect(order_create_model)
    @api.doc('create_order')
    def post(self):
        """Ajoute une nouvelle commande avec plusieurs détails"""
        data = request.get_json()
        order = Orders(
            Customer_idCustomer=data.get('customer_idcustomer'),
            Provider_idProvider=data.get('provider_idprovider'),
            status=data['status']
        )
        db.session.add(order)
        db.session.flush()  # Get the generated ID

        # Add multiple order details if provided
        for d in data.get('order_details', []):
            order_detail = OrdersDetail(
                quantity=d['quantity'],
                Wine_idWine=d['Wine_idWine'],
                order_idOrders=order.idOrders
            )
            db.session.add(order_detail)

        db.session.commit()
        response_data = {'message': 'Commande crée', 'id': order.idOrders}
        response = Response(response=json.dumps(response_data), status=201, mimetype='application/json')
        return response


# Route: Get, Update, Delete an Order
@api.route('/<int:order_id>')
@api.param('order_id', 'L\'ID de la commande')
class OrderResource(Resource):
    @api.doc('get_order')
    def get(self, order_id):
        """Récupère une commande par ID"""
        order = Orders.query.get_or_404(order_id)
        return jsonify({
            'idOrders': order.idOrders,
            'customer_idcustomer': order.Customer_idCustomer,
            'provider_idprovider': order.Provider_idProvider,
            'status': order.status
        })

    @api.expect(order_model)
    @api.doc('update_order_status')
    def put(self, order_id):
        """Met à jour le statut d'une commande"""
        data = request.get_json()
        order = Orders.query.get_or_404(order_id)
        order.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Order status updated'})

    @api.doc('delete_order')
    def delete(self, order_id):
        """Supprime une commande"""
        order = Orders.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted'})


# Route: Get/Add Order Details
@api.route('/<int:order_id>/details')
@api.param('order_id', 'L\'ID de la commande')
class OrderDetailList(Resource):
    @api.doc('get_order_details')
    def get(self, order_id):
        """Récupère tous les détails d'une commande"""
        order_details = OrdersDetail.query.filter_by(order_idOrders=order_id).all()
        result = [
            {
                'idOrdersDetail': od.idOrdersDetail,
                'quantity': od.quantity,
                'Wine_idWine': od.Wine_idWine,
                'order_idOrders': od.order_idOrders
            } for od in order_details
        ]
        return jsonify(result)

    @api.expect(order_detail_model)
    @api.doc('add_order_detail')
    def post(self, order_id):
        """Ajoute un détail de commande"""
        data = request.get_json()
        order_detail = OrdersDetail(
            quantity=data['quantity'],
            Wine_idWine=data['Wine_idWine'],
            order_idOrders=order_id
        )
        db.session.add(order_detail)
        db.session.commit()
        response_data = {'message': 'Article ajouté à la commande', 'id': order_detail.idOrdersDetail}
        response = Response(response=json.dumps(response_data), status=201, mimetype='application/json')
        return response


# Route: Update/Delete an Order Detail
@api.route('/<int:order_id>/details/<int:detail_id>')
@api.param('order_id', 'L\'ID de la commande')
@api.param('detail_id', 'L\'ID du détail de commande')
class OrderDetailResource(Resource):
    @api.doc('update_order_detail')
    def put(self, order_id, detail_id):
        """Met à jour un détail de commande"""
        data = request.get_json()
        order_detail = OrdersDetail.query.filter_by(order_idOrders=order_id, idOrdersDetail=detail_id).first_or_404()
        order_detail.quantity = data.get('quantity', order_detail.quantity)
        order_detail.Wine_idWine = data.get('Wine_idWine', order_detail.Wine_idWine)
        db.session.commit()
        return jsonify({'message': 'Order detail updated'})

    @api.doc('delete_order_detail')
    def delete(self, order_id, detail_id):
        """Supprime un détail de commande"""
        order_detail = OrdersDetail.query.filter_by(order_idOrders=order_id, idOrdersDetail=detail_id).first_or_404()
        db.session.delete(order_detail)
        db.session.commit()
        return jsonify({'message': 'Order detail deleted'})
