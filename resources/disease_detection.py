from flask.globals import request
from machine.inference import get_disease_name
from flask_restful import Resource,reqparse


class DiseaseResource(Resource):
    parser = reqparse.RequestParser()
    

    def post(self):
        file = request.files['file']
        if file is None:
            return {'message':'please add an image file'}
        try:
            image = file.read()
            disease_name=get_disease_name(image_bytes=image)
            return {'message':disease_name}	
        except:
            return {'message':'failed'}

