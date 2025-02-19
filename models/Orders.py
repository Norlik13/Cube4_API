from datetime import datetime
from databaseSet import db


class Orders(db.Model):
    __tablename__ = 'Orders'
    idOrders = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    Customer_idCustomer = db.Column(db.Integer, db.ForeignKey('Customer.idCustomer'), nullable=False)

    # Relationship to OrderDetail
    order_details = db.relationship('OrdersDetail', backref='Orders', lazy=True)

    def __repr__(self):
        return f"<Order {self.idorder}>"
