from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ApiReturn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    param1 = db.Column(db.String(100), nullable=False)
    param2 = db.Column(db.String(100), nullable=False)
    param3 = db.Column(db.String(100), nullable=False)
    param4 = db.Column(db.String(100))
    param5 = db.Column(db.String(100))

    def __repr__(self):
        return f'<ApiReturn {self.param1} {self.param2} {self.param3}>'

class ClientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    param1 = db.Column(db.String(100), nullable=False)
    param2 = db.Column(db.String(100), nullable=False)
    param3 = db.Column(db.String(100), nullable=False)
    param4 = db.Column(db.String(100))
    param5 = db.Column(db.String(100))

    def __repr__(self):
        return f'<ClientRecord {self.param1} {self.param2} {self.param3}>'
