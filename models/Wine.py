from databaseSet import db
from models.Color import Color
from models.Cepage import Cepage
from models.Appellation import Appellation
from models.Provider import Provider


class Wine(db.Model):
    __tablename__ = 'Wine'
    idWine = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    Vintage = db.Column(db.Integer, nullable=False)
    Sparkling = db.Column(db.Boolean, nullable=False)
    cuvee_name = db.Column(db.String(45), nullable=False)

    Color_idColor = db.Column(db.Integer, db.ForeignKey('Color.idColor'), nullable=False)
    Cepage_idCepage = db.Column(db.Integer, db.ForeignKey('Cepage.idCepage'), nullable=False)
    Appellation_idAppellation = db.Column(db.Integer, db.ForeignKey('Appellation.idAppellation'), nullable=False)
    Provider_idProvider = db.Column(db.Integer, db.ForeignKey('Provider.idProvider'), nullable=False)

    color = db.relationship('Color', backref=db.backref('wines', lazy=True))
    cepage = db.relationship('Cepage', backref=db.backref('wines', lazy=True))
    appellation = db.relationship('Appellation', backref=db.backref('wines', lazy=True))
    provider = db.relationship('Provider', backref=db.backref('wines', lazy=True))

    def __repr__(self):
        return f"<Wine {self.cuvee_name}>"
