'''---------------------------------------------
train_predict_ml.py
This script train the selected machine learning algorithm on the full dataset.
The type of hearing loss is predicted based on the measured hearing threshold.

Author: JT
Last modified: 2026-04-28
---------------------------------------------'''
# Imports
# Imported modules
import joblib
import pandas as pd

# All tested sklearn are imported, so that during hyperparameter fitting 
# each method can be used to train the entire dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier 

# Imported modul for main execution
from json import load
class TestPredictModel:
    def __init__(self):
        self.ml_model = {'Tree':DecisionTreeClassifier(),
                         'RandomForest':RandomForestClassifier(),
                         'LogisticRegression':LogisticRegression(max_iter = 1000),
                         'KNN':KNeighborsClassifier()}
        self.model_file = 'models/model_hearing_test.pkl'
        
    def train_model(self, dataset, ml_parameters):
        '''
        Training the entire dataset on the evaluated model.
        '''
        self.dataset = dataset
        model_name = str(ml_parameters['Model'])
        self.select_features_targets()
        print(f'Machine Learning model: {model_name}')
        self.scaling_features_train()
        self.model = self.ml_model[model_name]
        if model_name == 'Tree' or model_name == 'RandomForest':
            self.model.fit(self.features, self.target)
        else:
            self.model.fit(self.features_scal_data, self.target)
        self.save_model()

      
    def select_features_targets(self):
        '''
        Select features and target
        '''
        self.features = self.dataset.drop(columns = 'Hearing_Loss')
        self.target = self.dataset['Hearing_Loss']
        
    def scaling_features_train(self):
        '''
        For the machine learning algorithms KNN and logistic regression feature scaling 
        are more suitable.
        Method: Standardisation
        Mean and standard deviation of each features are saved for later prediction.
        '''
        self.features_scal_data = pd.DataFrame()
        self.mean = []
        self.std = []
        for feature in self.features:
            if not feature.endswith('_flag'):
                mean = self.features[feature].mean()
                std = self.features[feature].std()
                if std == 0:
                    scal_data = self.features[feature] - mean
                else:
                    scal_data = (self.features[feature] - mean) / std
                self.mean.append(mean)
                self.std.append(std)
                self.features_scal_data[feature] = scal_data
            else:
                self.features_scal_data[feature] = self.features[feature]
        
    def save_model(self):
        '''
        Saving the trained model, mean and standardivation, trained features in a pkl file
        '''
        save_nn = {'Model' : self.model,
                   'Mean': self.mean,
                   'std' : self.std,
                   'Features_train' : self.features.columns}
        joblib.dump(save_nn, self.model_file)
                       
    def predict_hearing_loss(self, hearing_threshold):
        '''
        Predict the kind of hearing loss based on the measures of the hearing threshold
        '''
        self.hearing_threshold = hearing_threshold
        # Loading the trained model
        file = joblib.load(self.model_file)
        model = file['Model']
        self.mean_train = file['Mean']
        self.std_train = file['std']
        self.features_train = file['Features_train']
        if isinstance(model, (DecisionTreeClassifier, RandomForestClassifier)):
            self.prediction = model.predict(self.hearing_threshold)
        else:
            self.scaling_hearing_threshold()
            self.prediction = model.predict(self.hearing_threshold_scal)


    
    def scaling_hearing_threshold(self):
        'Scalling of the hearing threshold'
        self.hearing_threshold_scal = pd.DataFrame()
        n = 0
        for feature in self.hearing_threshold:
            if feature == self.features_train[n]  and not feature.endswith('_flag'):
                if self.std_train[n] == 0:
                    scal_data = self.hearing_threshold[feature] - self.mean_train[n]
                else:
                    scal_data = (self.hearing_threshold[feature] - self.mean_train[n]) / self.std_train[n]
                self.hearing_threshold_scal[feature] = scal_data
                n += 1
            else:
                self.hearing_threshold_scal[feature] = self.hearing_threshold[feature]
                    
# Main execution
if __name__ == '__main__':
    file_name = 'data/Synthetic_audiology_data.csv'
    dataset = pd.read_csv(file_name)
    with open('config/ML_selection.json', 'r', encoding = 'utf-8') as stream:
        ml_parameters = load(stream)
    model = TestPredictModel()
    model.train_model(dataset, ml_parameters)