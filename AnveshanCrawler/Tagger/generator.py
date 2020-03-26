#from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from Tagger.helper import load_cv_n_tf, load_model, load_labels
import numpy as np

class TagGenerator(object):
    
    def __init__(self):
        self.cv, self.tf = load_cv_n_tf()
        self.model = load_model()
        self.labels = load_labels()
    
    def generate_tag(self, text):
        #print('text test: ', np.array([text]).reshape(1, -1)[0])
        count_vector = self.cv.transform(np.array(text).reshape(1, -1)[0])
        tfidf_vector = self.tf.transform(count_vector)
        prediction = self.model.predict(tfidf_vector.toarray())
        return self.labels[int(prediction)]

    def __str__(self):
        return " ".join(self.labels)
    
    
