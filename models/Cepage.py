from databaseSet import db


class Cepage(db.Model):
    __tablename__ = 'Cepage'
    idCepage = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cepage = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Cepage {self.cepage}>"
