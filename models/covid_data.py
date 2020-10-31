from db import db

class CoivdModel(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    label = db.Column(db.String(100))
    accuracy = db.Column(db.String(100))


    def __init__(self,label,accuracy):
        self.label = label
        self.accuracy = accuracy
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'label':self.label,'accuracy':self.accuracy}

    