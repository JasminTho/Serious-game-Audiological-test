'''---------------------------------------------
ml_model.py
This program evaluates the following baseline ML methods for the synthetic dataset.
- Decision tree
- Random Forest
- Knn
- logistic regression

Author: JT
Last modified: 2026-04-28
---------------------------------------------'''
# Import modules
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
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
        self.split_dataset()
        self.scaling_features()
        self.evaluate_model()
        self.save_model()
      
    def select_features_targets(self):
        '''
        Selection of the features and target for the machine learning methods
        '''
        self.features = self.dataset.drop(columns = 'Hearing_Loss')
        self.target = self.dataset['Hearing_Loss']
        
    def split_dataset(self):
        '''
        Split the dataset in train and test to evaluate every model.
        Train set: 80 % of the dataset
        '''
        train_size = 0.8
        self.features_train, self.features_test,self.target_train, \
        self.target_test = train_test_split(self.features,
                                            self.target,
                                            train_size = train_size,
                                            random_state = 42) 
    
    def scaling_features(self):
        '''
        For the machine learning algorithms KNN and logistic regression feature scaling 
        are more suitable.
        Method: Standardisation
        Train and test features are scaled using the mean and standard deviation of the 
        train features.
        '''
        self.features_scaled_training = pd.DataFrame()
        self.features_scaled_test = pd.DataFrame()
        for feature in self.features_train:
            # Flag parameters are not scaled because they are not measurement values
            if not feature.endswith('_flag'):           
                mean_train = self.features_train[feature].mean()
                std_train = self.features_train[feature].std()
                # Avoid division by zero
                if std_train == 0:
                    scal_train = self.features_train[feature] - mean_train
                    scal_test = self.features_test[feature] - mean_train
                else:
                    scal_train = (self.features_train[feature] - mean_train) / std_train
                    scal_test = (self.features_test[feature] - mean_train) / std_train
                self.features_scaled_training[feature] = scal_train
                self.features_scaled_test[feature] = scal_test
            else:
                self.features_scaled_training[feature] = self.features_train[feature]
                self.features_scaled_test[feature] = self.features_test[feature]

              
    def evaluate_model(self):
        '''
        Training and evaluation of the models. Save model name and accuracy in the dictionary ml_results
        '''
        self.ml_results = pd.DataFrame({'Model':[],
                                        'Accuracy':[]})
        for model_name in self.ml_model:
            model = self.ml_model[model_name]
            if model_name == 'Tree' or model_name == 'RandomForest':
                model.fit(self.features_train, self.target_train)
                prediction = model.predict(self.features_test)
            else:
                model.fit(self.features_scaled_training, self.target_train)
                prediction = model.predict(self.features_scaled_test)
            correct_label = 0
            for i in range(len(prediction)):
                if prediction[i] == self.target_test.iloc[i]:
                    correct_label += 1
            accuracy = round(correct_label / len(prediction) * 100,2)
            result = [model_name, accuracy]
            self.ml_results.loc[len(self.ml_results)] = result
    
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