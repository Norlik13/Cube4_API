from flask import Blueprint, request, jsonify
from databaseSet import db
from models.Color import Color
from models.Cepage import Cepage
from models.Appellation import Appellation
from models.Provider import Provider
from models.Wine import Wine
from models.Customer import Customer
from models.Orders import Orders
from models.OrdersDetail import OrdersDetail

api_bp = Blueprint('api', __name__)

# Create Color
@api_bp.route('/colors', methods=['POST'])
def create_color():
    data = request.get_json()
    color = Color(color=data['color'])
    db.session.add(color)
    db.session.commit()
    return jsonify({'message': 'Color created', 'id': color.idColor}), 201

# Create Cepage
@api_bp.route('/cepages', methods=['POST'])
def create_cepage():
    data = request.get_json()
    cepage = Cepage(cepage=data['cepage'])
    db.session.add(cepage)
    db.session.commit()
    return jsonify({'message': 'Cepage created', 'id': cepage.idCepage}), 201

# Create Appellation
@api_bp.route('/appellations', methods=['POST'])
def create_appellation():
    data = request.get_json()
    appellation = Appellation(appellation=data['appellation'])
    db.session.add(appellation)
    db.session.commit()
    return jsonify({'message': 'Appellation created', 'id': appellation.idAppellation}), 201

# Create Provider
@api_bp.route('/providers', methods=['POST'])
def create_provider():
    data = request.get_json()
    provider = Provider(phone_number=data['phone_number'], domain_name=data['domain_name'])
    db.session.add(provider)
    db.session.commit()
    return jsonify({'message': 'Provider created', 'id': provider.idProvider}), 201

# Create Wine
@api_bp.route('/wines', methods=['POST'])
def create_wine():
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
    return jsonify({'message': 'Wine created', 'id': wine.idWine}), 201

# Create Customer
@api_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(
        customer_name=data['customer_name'],
        username=data['username'],
        mail_adress=data['mail_adress'],
        password=data['password']
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Customer created', 'id': customer.idcustomer}), 201

# Create Order along with Order Details
@api_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    # Expecting: customer_idcustomer, status, and an optional list "order_details" with each detail's:
    # quantity, status, and Wine_idWine.
    order = Orders(
        customer_idcustomer=data['customer_idcustomer'],
        status=data['status']
    )
    db.session.add(order)
    db.session.flush()  # get order id for details

    for d in data.get('order_details', []):
        order_detail = OrdersDetail(
            quantity=d['quantity'],
            status=d['status'],
            Wine_idWine=d['Wine_idWine'],
            Orders_idOrders=order.idOrders
        )
        db.session.add(order_detail)
    db.session.commit()
    return jsonify({'message': 'Order created', 'id': order.idorder}), 201

# Update Order Status
@api_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    order = Orders.query.get_or_404(order_id)
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Order status updated'}), 200
