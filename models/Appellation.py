from databaseSet import db


class Appellation(db.Model):
    __tablename__ = 'Appellation'
    idAppellation = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appellation = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Appellation {self.appellation}>"
