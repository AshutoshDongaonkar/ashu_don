from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GetApi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    param1 = db.Column(db.String(100), nullable=False)
    param2 = db.Column(db.String(100), nullable=False)
    param3 = db.Column(db.String(100), nullable=False)
    param4 = db.Column(db.String(100))
    param5 = db.Column(db.String(100))
    

    def __repr__(self):
        return f'<GetApi {self.param1} {self.param2} {self.param3}>'
        
class ReportException(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    param1 = db.Column(db.String(100))
    param2 = db.Column(db.String(100))
    param3 = db.Column(db.String(100))
    param4 = db.Column(db.String(100))
    param5 = db.Column(db.String(100))
    param6 = db.Column(db.String(100))
    

    def __repr__(self):
        return f'<GetApi {self.param1} {self.param2} {self.param3}>'

class ClientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    param1 = db.Column(db.String(100))
    param2 = db.Column(db.String(100))
    param3 = db.Column(db.String(100))
    param4 = db.Column(db.String(100))
    param5 = db.Column(db.String(100))
    param6 = db.Column(db.String(100))   # for date-time stamp
    param7 = db.Column(db.String(100))  # for additional comments
    
    def __repr__(self):
        return f'<ClientRecord {self.param1} {self.param2} {self.param3}>'
