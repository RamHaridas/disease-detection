from flask import Flask 
from flask_restful import Api
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
import psycopg2
import os
from db import db


from resources.disease_detection import DiseaseResource


normal = os.environ.get('DATABASE_URL')
postgres_url = {
 'user': 'ram',
 'pw': 'ram',
 'db': 'ram',
 'host': 'localhost',
 'port': '5432',
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % postgres_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


#add api endpoints here
api.add_resource(DiseaseResource,'/detect')  

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/lol')
def check():
    return "WORKING 786"



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    #migrate = Migrate(app,db)
    #manager = Manager(app)
    #manager.add_command('db', MigrateCommand)
    #manager.run()
    app.run()