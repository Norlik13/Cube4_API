# models/order_detail.py
from databaseSet import db


class OrdersDetail(db.Model):
    __tablename__ = 'OrdersDetail'
    idOrdersDetail = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('processing', 'done', name='order_detail_status'), nullable=False)
    Wine_idWine = db.Column(db.Integer, db.ForeignKey('Wine.idWine'), nullable=False)
    order_idOrders = db.Column(db.Integer, db.ForeignKey('Orders.idOrders'), nullable=False)

    def __repr__(self):
        return f"<OrderDetail {self.idorderDetail}>"
