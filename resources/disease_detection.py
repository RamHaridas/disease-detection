from flask.globals import request
from flask import jsonify
from h5py._hl.files import File
from machine.inference import get_disease_name
from machine.covid19 import COVID
from flask_restful import Resource,reqparse
import io
from PIL import Image
import numpy as np



class DiseaseResource(Resource):
    parser = reqparse.RequestParser()

    #not working (model not available)
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


    #detects covid 19 postitive or not
    def put(self):
        file = request.files['file']
        if not file:
            return {'message':'please add image'}
        
        c = COVID() #creating obj of COVID class

        dataBytesIO = io.BytesIO(file.read())
        dataBytesIO.seek(0)
        image = Image.open(file)

        test_image = c.preprocess(image)
        
        prediction = c.model.predict(test_image)
        result = np.argmax(prediction,axis=1)[0]
        accuracy = float(np.max(prediction,axis=1)[0])

        label = c.label_dict[result]

        #print(prediction,result,accuracy)

        response = {'prediction': {'result': label,'accuracy': accuracy}}

        return jsonify(response)

