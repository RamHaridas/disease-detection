from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
import psycopg2
import os

from resources.disease_detection import DiseaseResource

normal = os.environ.get('DATABASE_URL','sqlite:///data.db')
postgres_url = ""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = normal
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


#add api endpoints here
api.add_resource(DiseaseResource,'/detect')  



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    #migrate = Migrate(app,db)
    #manager = Manager(app)
    #manager.add_command('db', MigrateCommand)
    #manager.run()
    app.run(port=5000, debug=True)