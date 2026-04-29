'''---------------------------------------------
audiogram.py
This program plots an audiogram based on the test result of the hearing test.
Further the pta4 level is evaluated if possible

Code and comments are written in English. 

Author: JT
Last modified: 2026-04-28
---------------------------------------------'''

# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from json import load
from time import localtime
from train_predict_ml import TestPredictModel


class Audiogram:
    def __init__(self, hearing_threshold = None,  setup_text= None, language = 'English'): 
        self.pdm = TestPredictModel()
        self.hearing_threshold = hearing_threshold
        self.language = language
        self.setup_text =  setup_text
        self.x_ticks = [0.125, 0.250, 0.500, 0.750, 1, 1.5, 2, 3, 4, 6, 8]
        self.hearing_outcome = list(self.hearing_threshold.iloc[0, 0:len(self.x_ticks)])

        self.init_figure()
    
    def init_figure(self):
        self.graphical_result = plt.subplots(
                nrows=3,        # 3 suplots among themselves for header, pure tone measurement and results
                ncols=1,        # one column for unique width
                gridspec_kw={'height_ratios':[0.5, 10, 0.5]},  # Relation between the subplots
                constrained_layout=True  # automatic distance between title and text
        )
        
        # Creation of several plots
        self.plot_header()
        self.plot_pure_tone()
        self.plot_result()
        plt.show()
    
    def plot_header(self):
        '''
        Header of the Audiogram for test information, current date of measurement
        '''
        ax = plt.subplot(3,1,1)
        ax.axis('off')          # no 'plot' is shown here, so no axis are seen
        plt.title(self.setup_text[self.language]['audiogram']['title'], pad =10)
        # Date of the measurement
        date= localtime()
        date_str = self.setup_text[self.language]['audiogram']['date']
        plt.text(0,-1,
                 f'{date_str}:\n{date.tm_mday:02d}.{date.tm_mon:02d}.{date.tm_year};{date.tm_hour:02d}:{date.tm_min:02d}')
    
    def plot_pure_tone(self):
        '''
        Pure tone measurement plot
        '''
        plt.subplot(3,1,2)
        # Handling of not heard frequencies
        for tone in range(11):
            if self.hearing_outcome[tone] == 110 and self.hearing_threshold.iloc[0,tone+len(self.x_ticks)] == 1:
                self.hearing_outcome[tone] = None                  
                plt.text(self.x_ticks[tone],110,'\u2198', c='b')
        
        # Layout of the plot
        plt.grid()
        plt.xscale('log')
        plt.xlim(0.125,8)
        plt.ylim(110,-5)
        plt.minorticks_off()
        plt.tick_params(axis='both',
                        which = 'both',
                        top = True, 
                        bottom = False, 
                        labeltop=True, 
                        labelbottom = False,
                        direction = 'in')
        plt.xticks(self.x_ticks, self.x_ticks)
        plt.yticks(range(-10, 120, 10))
        plt.gca().xaxis.set_label_position('top')
        plt.xlabel(self.setup_text[self.language]['audiogram']['x_label'])
        plt.ylabel(self.setup_text[self.language]['audiogram']['y_label'])
        
        # plot of the measurement
        self.graphical_result = plt.plot(self.x_ticks, self.hearing_outcome, 'x-', c = 'b')
    
    def plot_result(self):
        '''
        Plot of the result, current mean pta4
        Planned to give the user a advice, if had a hearing loss
        '''
        ax = plt.subplot(3,1,3)
        ax.axis('off')
        rel_freq = (0.5, 1, 2, 4)         # relevant tones for the pta4
        '''
        Try to evaluate the mean, only possible, when all relevant frequencies were heard 
        by the user. Otherwise output is not calculatable
        '''

        try:
            pure_tone_average = [self.hearing_threshold[str(freq) + '_khz'] for freq in rel_freq]
            pta = np.mean(pure_tone_average)
            self.hearing_threshold['PTA4'] = pta
            str_pta = str(pta) + ' dB'
        except KeyError:
            str_pta = self.setup_text[self.language]['audiogram']['pta4_unavailable']
            self.hearing_threshold['PTA4'] = np.nan
            
        self.pdm.predict_hearing_loss(self.hearing_threshold)
        prediction = str(self.pdm.prediction[0])    
        str_hearing_loss = self.setup_text[self.language]['prediction_hearing_loss']['hearing_loss']
        str_prediction = self.setup_text[self.language]['prediction_hearing_loss'][prediction]
        ax.text(0, 0.5, f'PTA4 (0.5, 1, 2, 4 kHz): {str_pta}\
                \n{str_hearing_loss}: {str_prediction}')
# Main
if __name__ == '__main__':
    hearing_threshold = pd.DataFrame([{'0.125_khz' : 0, 
                                     '0.25_khz' : 0, 
                                     '0.5_khz' : 5, 
                                     '0.75_khz' : 0, 
                                     '1_khz' : 0, 
                                     '1.5_khz' : 0, 
                                     '2_khz' : 0, 
                                     '3_khz' : 0, 
                                     '4_khz' : 0, 
                                     '6_khz' : 0, 
                                     '8_khz' : 0,
                                     '0.125_flag' : 0, 
                                     '0.25_flag' : 0, 
                                     '0.5_flag' : 0, 
                                     '0.75_flag' : 0, 
                                     '1_flag' : 0, 
                                     '1.5_flag' : 0, 
                                     '2_flag' : 0, 
                                     '3_flag' : 0, 
                                     '4_flag' : 0, 
                                     '6_flag' : 0, 
                                     '8_flag' : 0}])
    with open('config\Menu_text_gui.json', 'r', encoding = 'utf-8') as file:
        setup_text = load(file)
    Audiogram(hearing_threshold, setup_text)
    


    
