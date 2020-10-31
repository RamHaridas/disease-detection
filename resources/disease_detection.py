from io import BytesIO
from os import name
from flask.globals import request
from flask import jsonify, send_file
from h5py._hl.files import File
from machine.covid19 import COVID
from flask_restful import Resource,reqparse
import io
from PIL import Image
import numpy as np
from models.covid_data import CoivdModel



class DiseaseResource(Resource):
    parser = reqparse.RequestParser()

    #not working (model not available)
    def get(self):
        return {'results':[c.josn() for c in CoivdModel.query.all()]}


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

        covid = CoivdModel(label,accuracy)
        covid.save()
        #print(prediction,result,accuracy)

        #response = {'prediction': {'result': label,'accuracy': accuracy}}

        return {'saved':'image saved successfully'}

    
    def post(self):
        file = request.files['file']
        
        return send_file(BytesIO(file.read()),as_attachment=False,attachment_filename=file.filename)


        

