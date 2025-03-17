from databaseSet import db


class Provider(db.Model):
    __tablename__ = 'Provider'
    idProvider = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.Integer, nullable=False)
    domain_name = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Provider {self.domain_name}>"
