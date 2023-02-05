from index import db

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Restaurant %r>' % self.name
