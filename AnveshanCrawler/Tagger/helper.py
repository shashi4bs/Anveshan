import joblib

def load_cv_n_tf():
    try: 
        cv = joblib.load('./Tagger/countvectorier.sav')
        tf = joblib.load('./Tagger/tfidftransformer.sav')
        return cv, tf
    except Exception as E:
        raise Exception('Anveshan Crawler failed to load Tag Generator')
    
def load_model():
    try:
        return joblib.load('./Tagger/model.sav')
    except Exception as E:
        raise Exception('Anveshan Crawler failed to load Tag Generator')
    

def load_labels():
    #load labels from label.names file
    labels = []
    try:
        with open('./Tagger/label.names') as f:
            for label in f.readlines():
                labels.append(label)
        return labels
    except Exception as E:
        raise Exception('Anveshan Crawler failed to load Tag Generator')
    

