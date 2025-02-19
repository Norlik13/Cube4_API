from databaseSet import db


class Color(db.Model):
    __tablename__ = 'Color'
    idColor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"<Color {self.color}>"
