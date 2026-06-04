'''---------------------------------------------
ml_model.py
This program evaluates the following baseline ML methods for the synthetic dataset.
- Decision tree
- Random Forest
- Knn
- logistic regression
Inclusion of stratisfieldKFold

Author: JT
Last modified: 2026-05-12
---------------------------------------------'''
# Import modules
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier 

# Imported modules for main excecution
from json import dump

class MLModel:
    def __init__(self, dataset, file_name):
        self.dataset = dataset
        self.file_name = file_name
        self.select_features_targets()
        self.ml_model = {'Tree':DecisionTreeClassifier(),
                         'RandomForest':RandomForestClassifier(),
                         'LogisticRegression':LogisticRegression(max_iter = 1000),
                         'KNN':KNeighborsClassifier()}
        self.cross_validation()
        self.evaluate_model()
        # self.save_model()
      
    def select_features_targets(self):
        '''
        Selection of the features and target for the machine learning methods
        '''
        self.features = self.dataset.drop(columns = ['Hearing_Loss', 'PTA4'])
        self.target = self.dataset['Hearing_Loss']
    
    def cross_validation(self):
        '''
        The dataset is splitted 5 times to evaluate the machine learning models.
        Using the StratifiedKFold to ensure, that in classification of hearing loss
        is in the train dataset
        '''
        self.skf = StratifiedKFold(n_splits = 5, shuffle = True, random_state = 42)
        print(self.skf)
    
    def evaluate_model(self):
        '''
        Training and evaluation of the models. Save model name and accuracy in the dictionary ml_results
        '''
        self.ml_results = pd.DataFrame(columns = ['Model', 'Accuracy'])
        for model_name in self.ml_model:
            accuracy_per_fold = []
            for n, (train_index, test_index) in enumerate(self.skf.split(self.features, self.target)):
                model = self.ml_model[model_name]
                
                if model_name == 'Tree' or model_name == 'RandomForest':
                    feature_train, feature_test = self.features.iloc[train_index], self.features.iloc[test_index]
                    target_train, target_test = self.target.iloc[train_index], self.target.iloc[test_index]
                    model.fit(feature_train, target_train)
                    prediction = model.predict(feature_test)
                else:
                    self.feature_train, self.feature_test = self.features.iloc[train_index], self.features.iloc[test_index]
                    target_train, target_test = self.target.iloc[train_index], self.target.iloc[test_index]
                    self.scaling_features()   
                    model.fit(self.features_scaled_train, target_train)
                    prediction = model.predict(self.features_scaled_test)
                accuracy = accuracy_score(target_test, prediction)
                accuracy_per_fold.append(accuracy)
                print(f'{model_name} Fold {n+1}: {accuracy:.4f}')
            mean_accuracy = np.mean(accuracy_per_fold)
            print(f'{model_name} Mean Accuracy: {mean_accuracy:.4f}')
            self.ml_results.loc[len(self.ml_results)] = [model_name, mean_accuracy]
        print(self.ml_results)
        print(dataset.head())
        print(dataset.columns)
                
    def scaling_features(self):
        '''
        For the machine learning algorithms KNN and logistic regression feature scaling 
        are more suitable.
        Method: Standardisation
        Train and test features are scaled using the mean and standard deviation of the 
        train features.
        '''
        self.features_scaled_train = pd.DataFrame()
        self.features_scaled_test = pd.DataFrame()
        for feature in self.feature_train:
            # Flag parameters are not scaled because they are not measurement values
            if not feature.endswith('_flag'):           
                mean_train = self.feature_train[feature].mean()
                std_train = self.feature_train[feature].std()
                # Avoid division by zero
                if std_train == 0:
                    scal_train = self.feature_train[feature] - mean_train
                    scal_test = self.feature_test[feature] - mean_train
                else:
                    scal_train = (self.feature_train[feature] - mean_train) / std_train
                    scal_test = (self.feature_test[feature] - mean_train) / std_train
                self.features_scaled_train[feature] = scal_train
                self.features_scaled_test[feature] = scal_test
            else:
                self.features_scaled_train[feature] = self.feature_train[feature]
                self.features_scaled_test[feature] = self.feature_test[feature]

    def save_model(self):
        '''
        Saving the model name and accuracy of the  best performing model in a json file.
        '''
        best_performance = self.ml_results['Accuracy'].max()
        self.model_choosen = {}
        for idx in range(len(self.ml_results)):
            if best_performance == self.ml_results.loc[idx, 'Accuracy']:
                self.model_choosen['Model'] = self.ml_results.loc[idx, 'Model']
                self.model_choosen['Accuracy'] = self.ml_results.loc[idx, 'Accuracy']
        with open(self.file_name, 'w', encoding = 'utf-8') as stream:
            dump(self.model_choosen, stream)
        print('Best model saved.')

# Main execution
if __name__ == '__main__':
    file_dataset = 'data/Synthetic_audiology_data.csv'
    file_model_params = 'config/ML_selection.json'
    try:
        dataset = pd.read_csv(file_dataset)
        print('Dataset loaded')
        MLModel(dataset, file_model_params)
    except FileNotFoundError:
        print('No File in directory')
    
        