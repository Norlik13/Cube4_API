from databaseSet import db


class Customer(db.Model):
    __tablename__ = 'Customer'
    idCustomer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(45), nullable=False, unique=True)
    mail_address = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Customer {self.username}>"
