from json import load
from keras.preprocessing.image import load_img
import numpy
from numpy.core.fromnumeric import size
from keras.applications.mobilenet import MobileNet
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, Flatten
from keras.preprocessing import image
from keras.models import Sequential, model_from_json
from keras.applications.mobilenet import preprocess_input
import numpy as np
import matplotlib.image as mpimg
from PIL import Image
import cv2

#import matplotlib.pyplot as plt
import json



class DiseaseClassifier:
    
    labels = ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion',
            'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'Nodule',
            'Pleural_Thickening', 'Pneumonia', 'Pneumothorax']
    #graph = tf.get_default_graph()

    def __init__(self):
        pass

    
    def build_model(self):
        with open('model_results/multi_disease_model.json', 'r') as json_file:
            architecture = json.load(json_file)
            model = model_from_json(json.dumps(architecture))

        model.load_weights('model_results/multi_disease_model_weight.h5')
        model.make_predict_function()
        return model

    
    def load_image(self,img_path):
        size = 128,128
        #img = image.load_img(img_path, target_size=(128, 128, 3))
        img = Image.open(img_path).convert("RGB")
        img = img.resize(size=(128,128))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img /= 255.
        return img


    def predict_image(self,model, img_path, biggest_result=False, show_result=False):
        
        new_image = self.load_image(img_path)
        pred = model.predict(new_image)
        if show_result:
            #img = mpimg.imread(img_path)
            #imgplot = plt.imshow(img, cmap='bone')
            #plt.title(pred)
            #plt.show()
            pass

        return (np.argmax(pred), np.max(pred)) if biggest_result else pred


