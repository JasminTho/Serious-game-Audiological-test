'''---------------------------------------------
synthetic_dataset.py
This program generates a synthetic dataset for training a machine learning algorithm.

Author: JT
Last modified: 2026-04-28
---------------------------------------------'''
# Import modules
import numpy as np
from random import shuffle, randint, choice
import pandas as pd

class SyntheticData:
    def __init__(self,file_name, number_of_samples):
        self.number_of_samples = number_of_samples
        self.file_name = file_name
        self.frequencies = [0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8]
        
        # Flags for definition of hearing ability
        self.heard = 0
        self.not_heard = 1
        self.not_measured = 2
        
        self.distribution_hearing_profile()
        self.generate_hearing_profiles()
        self.calculate_pta4()
        
        # Save of the dataset as csv file
        self.save_dataset()
        
                
    def distribution_hearing_profile(self):
        '''
        Typical hearing profile distribution in the population for sample size > 50.
        '''
        self.size_dataset = self.number_of_samples
        hearing_distribution = {
            'normal' : int(0.65 * self.size_dataset),
            'mild' : int(0.15 * self.size_dataset),
            'moderate' : int(0.1 * self.size_dataset),
            'severe' : int(0.05 * self.size_dataset),
            'presbyakusis' : int(0.04 * self.size_dataset),
            'surditas' : int(0.01 * self.size_dataset)}
        self.list_hearing_loss = []
        for hearing_type in hearing_distribution:
            for anzahl in range(hearing_distribution[hearing_type]):
                self.list_hearing_loss.append(hearing_type)
        shuffle(self.list_hearing_loss)
        
    def generate_hearing_profiles(self):
        '''
        Generation of the synthetic dataset
        '''
        self.dataset = pd.DataFrame(columns=['0.125_khz', '0.25_khz', '0.5_khz', '0.75_khz', '1_khz', '1.5_khz', '2_khz', '3_khz', '4_khz', '6_khz', '8_khz',
                                             '0.125_flag', '0.25_flag', '0.5_flag', '0.75_flag', '1_flag', '1.5_flag', '2_flag', '3_flag', '4_flag', '6_flag', '8_flag',
                                             'PTA4',
                                             'Hearing_Loss',])
        self.number_data = 0
        for hearing_profile in self.list_hearing_loss:
            if self.number_data % 100 == 0:
                progress = self.number_data / self.size_dataset * 100
                print(f'\rGenerated Data: {progress:.2f}%', end = '')
            self.dataset.loc[self.number_data, 'Hearing_Loss'] = hearing_profile
            if hearing_profile == 'normal':
                self.center = choice(range(0,15,5))
                self.generate_flat_curve()
            elif hearing_profile == 'mild':
                self.center = choice(range(15,45,5))
                self.generate_flat_curve()
            elif hearing_profile == 'moderate':
                self.center = choice(range(45,75,5))
                self.generate_flat_curve()
            elif hearing_profile == 'severe':
                self.center = choice(range(65,95,5))
                self.generate_flat_curve()
            elif hearing_profile == 'presbyakusis': 
                self.generate_presbyakusis()
            elif hearing_profile == 'surditas':
                self.center = choice(range(100,120,5))
                self.generate_flat_curve()
            self.number_data += 1
        print('\nData generation completed')
              
    def generate_flat_curve(self):
        '''
        Generating a flat hearing loss curve
        '''
        for i in range(len(self.frequencies)):
            noise = randint(-3, 3)
            threshold = self.center + noise
            str_frequenz = str(self.frequencies[i]) + '_khz'
            str_flag = str(self.frequencies[i]) + '_flag'
        # If threshold > 110, the tone will be marked as not heard
            if threshold <= 110:
                self.dataset.loc[self.number_data, str_frequenz] = round(threshold/5)*5
                self.dataset.loc[self.number_data, str_flag] = self.heard
            else:
                self.dataset.loc[self.number_data, str_frequenz] = 110
                self.dataset.loc[self.number_data, str_flag] = self.not_heard
        
    def generate_presbyakusis(self):
        '''
        Flat hearing curve at low frequencies, with increasing loss above 2 kHz
        '''
        center = choice(range(0,15,5))
        last_threshold = center
        
        for i in range(len(self.frequencies)):
            str_frequenz = str(self.frequencies[i]) + '_khz'
            str_flag = str(self.frequencies[i]) + '_flag'
            if self.frequencies[i] < 2:
                noise = randint(-3, 3)
                threshold = round((center + noise)/5)*5
            else:
                loss = choice([5, 10, 10, 15])
                threshold = last_threshold + loss
            if threshold <= 110:
                last_threshold = threshold
                self.dataset.loc[self.number_data, str_frequenz] = threshold
                self.dataset.loc[self.number_data, str_flag] = self.heard
            else:
                last_threshold = 110
                self.dataset.loc[self.number_data, str_frequenz] = 110
                self.dataset.loc[self.number_data, str_flag] = self.not_heard
    
    def calculate_pta4(self):
        '''
        Calculation of the mean for 0.5, 1, 2 and 4 kHz frequencies
        '''
        for idx in range(len(self.dataset)):
            relevant_frequencies = ['0.5_khz', '1_khz', '2_khz', '4_khz']
            measurement = list(self.dataset.loc[idx, relevant_frequencies])
            if len(measurement) == 4 and all(pd.notna(wert) for wert in measurement):
                self.dataset.loc[idx, 'PTA4'] = np.mean(measurement)
            else:
                self.dataset.loc[idx, 'PTA4'] = np.nan
        print('PTA - 4 Threshold calculated')

    def save_dataset(self):
        '''
        Saving the dataset to a CSV file
        '''
        self.dataset.to_csv(self.file_name, index=False)
        print(f'Dataset saved in {self.file_name}')

# Main execution
if __name__ == '__main__':
    file_dataset = 'data/Synthetic_audiology_data.csv'
    default_size_dataset = 5000
    SyntheticData(file_dataset, default_size_dataset)