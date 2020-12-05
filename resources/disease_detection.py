from io import BytesIO
from os import name
from flask.globals import request
from flask import jsonify, send_file
from h5py._hl.files import File
from machine.covid19 import COVID
from machine.disease_classifier import DiseaseClassifier
from flask_restful import Resource,reqparse
import io
from PIL import Image
import numpy as np
from models.covid_data import CoivdModel
import tensorflow as tf

graph = tf.compat.v1.get_default_graph() # Get the default graph from tensorflow

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

        return {'result': label,'accuracy': accuracy}

    
    #detect various types of lung diseases
    def post(self):
        file = request.files['file']
        if not file:
            return "Please add image"
        
        disease = DiseaseClassifier()
        model = disease.build_model()
        
        preds = disease.predict_image(model, file)
        
        preds = np.array(preds).ravel().tolist()
        accuracy_map = {'Atelectasis':preds[0], 'Cardiomegaly':preds[1], 'Consolidation':preds[2], 'Edema':preds[3], 'Effusion':preds[4],
                'Emphysema':preds[5], 'Fibrosis':preds[6], 'Hernia':preds[7], 'Infiltration':preds[8], 'Mass':preds[9], 'Nodule':preds[10],
                'Pleural_Thickening':preds[11], 'Pneumonia':preds[12], 'Pneumothorax':preds[13]}
        #print(accuracy_map)
        #print(max(accuracy_map,key=accuracy_map.get))

        return {'predictions':accuracy_map,'Higest Value':max(accuracy_map,key=accuracy_map.get)}


        

