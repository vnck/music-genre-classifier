import joblib
import numpy as np

class Classifier():
    """Loads the classification model based on specifications provided during initialization of class.
    Parameters
    ----------
    configs: dict
        The specifications that describe the classifier to be used, refer to the yaml file under /configs.
    
    Attributes
    ----------
    configs : dict
        The complete set of configs provided during initialization.
    model_path : str
        The path to the model
    model_type : type
        The type of the model
    labels : list
        A list of label names where the index maps the model predictions output.
    model : object
        The loaded model
    """
    
    def __init__(self, configs:dict) -> None:
        """load model configs and model"""
        self.configs = configs
        # model configs
        self.model_path = configs['path']
        self.model_type = configs['type']
        self.labels = configs['labels']
        # load model
        self.model = self.load_model(self.model_path, self.model_type)

    def predict(self, features, labels:bool = False):
        """Return prediction output frm the model
        
        Paramaters
        ----------
        features: array-like of shape (n, num_features)
            The array of feature inputs to predict on.

        labels: bool
            If True, the label names are returned.
            If False, the numerical predicted outputs are returned.

        Returns
        -------
        preds : array-like of shape (n,)
            The predicted outputs of the model.
        """
        preds = self.model.predict(features)
        if labels:
            preds = [self.labels[i] for i in preds]
        return preds

    def predict_proba(self, features:list):
        """Returns prediction probabilities output from the model

        Paramaters
        ----------
        features: array-like of shape (n, num_features)
            The array of feature inputs to predict on.

        Returns
        -------
        pred_probs : array-like of shape (n, num_features)
            The predicted probabilities of the input features to the model.
        """
        pred_probs = self.model.predict_proba(features)
        return pred_probs

    def load_model(self, model_path:str, model_type:str):
        """load the model based on the model_path and model_type."""
        if model_type == 'random forest classifier':
            model = joblib.load(model_path)
        return model