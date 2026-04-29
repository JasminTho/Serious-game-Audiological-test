'''---------------------------------------------
main.py
Controller program for the Serious Game. 
Console control of the machine learning workflow.

Author: JT
Last modified: 2026-04-28
---------------------------------------------'''

# Inclusion
# Included modules
from json import load
import pandas as pd

# Other programm files
from gui_tkinter import HearingTestGUI
from synthetic_dataset import SyntheticData
from ml_model_selection import MLModel
from train_predict_ml import TestPredictModel

class MainController():
    def __init__(self):
        '''
        Set initial program parameters
        '''
        self.file_dataset = 'data/Synthetic_audiology_data.csv'
        self.file_model_params = 'config/ML_selection.json'
        self.default_size_dataset = 5000

        
    def run_program(self):
        '''
        Control panel that allows the user to manage different stages of the workflow
        Generate Data -> Choose best ML Setup -> Train the model of entire dataset -> run Hearing Test
        '''
        self.handle_dataset()
        self.handle_model_selection()
        self.handle_training_model()
        self.start_hearing_test()
    
    def handle_dataset(self):
        '''
        Handles whether a dataset should be generated

        '''
        self.user_choice = self.asc_question('Should a synthetic dataset be generated (y/n): ')

        # If yes, the user is ask, of the size of the dataset and if a integer is given the dataset is generated
        # otherwise the default data size is used (with error message on console)
        if self.user_choice == 'y':
            number_of_samples = input('How many samples should be generated: ')
            try: 
                self.data = SyntheticData(self.file_dataset, int(number_of_samples))
            except ValueError:
                print(f'Invalid input! Dataset will be generated with {self.default_size_dataset} samples.')
                self.data = SyntheticData(self.file_dataset, self.default_size_dataset).dataset   
        # If no, try to open an existing dataset, if not possible generated a dataset with default data size
        elif self.user_choice == 'n':
            try:
                self.data = pd.read_csv(self.file_dataset)
            except FileNotFoundError:
                print(f'No dataset saved in {self.file_dataset}. Dataset will be generated with {self.default_size_dataset} samples.')
                self.data = SyntheticData(self.file_dataset, self.default_size_dataset).dataset
        
    def handle_model_selection(self):
        '''
        Handles whether a model selection should be performed
        '''
        self.user_choice = self.asc_question('Should the most suitable ml - method estimate again (y/n): ')
        
        # If yes, model selection is started
        if self.user_choice == 'y':
            self.selected_ml_parameters = MLModel(self.data, self.file_model_params).model_choosen
        
        # If no, try to open an existing model_params, if not possible starting model selection
        elif self.user_choice == 'n':
            try:
                with open(self.file_model_params, 'r', encoding = 'utf-8') as stream:
                    self.selected_ml_parameters = load(stream)
            except FileNotFoundError:
                print(f'No model parameters saved in {self.file_model_params}. Model evaluation started')
                # Model selection is done and saved in self.file_model_params
                self.selected_ml_parameters = MLModel(self.data, self.file_model_params).model_choosen
          
    def handle_training_model(self):
        '''
        Handles whether the model should be trained on the full dataset
        '''
        self.user_choice = self.asc_question('Should the model be trained for the hearing test (y/n): ')
        
        # If yes train the model on the chosen parameters
        if self.user_choice == 'y':
            tpm= TestPredictModel()
            tpm_model = tpm.train_model(self.data, self.selected_ml_parameters)
            self.trained_model = tpm_model

        # If no, try to load an existing model, if not possible train the model
        elif self.user_choice == 'n':
            try:
                with open(self.file_model_params, 'r', encoding = 'utf-8') as stream:
                    self.selected_ml_parameters = load(stream)
            except FileNotFoundError:
                print(f'No trained model saved in {self.file_model_params}. Model evaluation started')
                tpm= TestPredictModel()
                tpm_model = tpm.train_model(self.data, self.selected_ml_parameters)
                self.trained_model = tpm_model['Model']
                
    def start_hearing_test(self):
        ''' 
        Starts the Hearing Test GUI
        '''
        app = HearingTestGUI()
        print('Starting Hearing Test')
        app.run()  
        
    def asc_question(self, question):
        '''
        Checks if the user input is 'y' or 'n'

        '''
        while True:
            answer = input(question).strip().lower()
            if answer in ['y', 'n']:
                return answer
            print('Invalid input')

# Main execution
if __name__ == '__main__':
    app = MainController()
    app.run_program()
    
