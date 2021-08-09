import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder

class FeatureTransformer():
    """Loads the specifications for feature engineering based on specifications provided during initialization of class.

    Parameters
    ----------
    configs: dict
        The specifications that describe the classifier to be used, refer to the yaml file under /configs.
    
    Attributes
    ----------
    configs: dict
        The complete set of configs provided during initialization.
    binary_features: list
        The list of names of binary features.
    categorical_features: list
        The list of names of categorical features.
    numerical_features: list
        The list of names of numerical features.
    all_features: list
        The list of all features to be used for prediction.
    one_hot_encoding: boolean
        Indicates whether to perform one hot encoding on categorical features.
    onehot_categories: list
        List of category names for one hot encoding
    numerical_normalization: str
        Specifies the method for normalizing numerical values.
    numerical_impute: str
        Specifies the strategy for imputing missing numerical values.


    """
    def __init__(self, configs: dict):
        """load feature engineering configurations."""
        self.configs = configs
        # feature configs
        self.binary_features = configs['binary']['columns']
        self.categorical_features = configs['categorical']['columns']
        self.numerical_features = configs['numerical']['columns']
        self.all_features = self.binary_features + self.categorical_features + self.numerical_features
        self.one_hot_encoding = configs['categorical']['one_hot_encode']
        self.onehot_categories = configs['categorical']['one_hot_categories']
        self.numerical_normalization = configs['numerical']['normalization']
        self.numerical_impute = configs['numerical']['impute_missing']

    
    def transform(self,df):
        """feature engineering based on the configurations specified.
        
        Parameters
        ----------
        df: dataframe
            The dataframe of raw features to be processed.
        
        Returns
        -------
        features : array-like of size (n, num_features)
            The array of processed features.
        """
        df = df[self.all_features]
        if self.categorical_features and self.one_hot_encoding:
            # one hot encoding
            df = encode_onehot(df, self.categorical_features, categories=self.onehot_categories)
        if self.numerical_normalization:
            # normalisation strategy
            if self.numerical_normalization == 'standard':
                df = normalize_standard(df, self.numerical_features)
            elif self.numerical_normalization == 'minmax':
                df = normalize_minmax(df, self.numerical_features)
        if self.numerical_impute:
            # impute missing values using specified strategy
            df = impute_missing(df, self.numerical_features, self.numerical_impute)
        
        features = df.values
        return features


def impute_missing(df, features: list, strategy: str = 'median'):
    """Imputes missing values based on the strategy specified."""
    imp = SimpleImputer(missing_values=np.nan, strategy=strategy)
    for f in features:
        df[f] = imp.fit_transform(df[f].values.reshape(-1,1)).reshape(-1)
    return df

def normalize_standard(df, features: list):
    """Normalize features using standard scaler."""
    scaler = StandardScaler()
    for f in features:
        df[f] = scaler.fit_transform(df[f].values.reshape(-1,1)).reshape(-1)
    return df

def normalize_minmax(df, features: list):
    """Normalize features using min max."""
    scaler = MinMaxScaler()
    for f in features:
        df[f] = scaler.fit_transform(df[f].values.reshape(-1,1)).reshape(-1)
    return df

def encode_onehot(df, features: list, categories= 'auto', drop_original=True):
    """Encodes features using one hot encoding."""
    enc = OneHotEncoder(handle_unknown='ignore', categories=[categories])
    for f in features:
        onehot = enc.fit_transform(df[f].values.reshape(-1,1)).toarray()
        feature_names = enc.categories_[0]
        df[feature_names] = onehot
        if drop_original:
            df = df.drop(f,axis=1)
    return df

def encode_numerical(df, features: list, drop_original: bool = True):
    """Encodes non-numerical features into numerical features."""
    labels = []
    for f in features:
        df[f] = pd.Categorical(df[f])
        df[f+'_idx'] = df[f].cat.codes
        if drop_original:
            df = df.drop(f,axis=1)
        labels.append(dict(enumerate(df[f].cat.categories)))
    return df, labels