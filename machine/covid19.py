from keras.models import load_model
import cv2
import numpy as np
from numpy.lib.function_base import select



class COVID:
    model = load_model('/var/www/html/disease-rest/models_ml/model-015.model')
    label_dict = {0:'Covid19 Negative', 1:'Covid19 Positive'}
    img_size = 100

    def __init__(self):
        pass

    
    def preprocess(self,img):

        img = np.array(img)

        if(img.ndim == 3):
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        gray = gray/255
        
        resized = cv2.resize(gray,(self.img_size,self.img_size))
        reshaped = resized.reshape(1,self.img_size,self.img_size)
        return reshaped