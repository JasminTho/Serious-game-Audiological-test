'''---------------------------------------------
audiology.py
This program plots a audiogram based on the test result of the hearing test.
Further the pta4 level is evaluated if possible

Code and comments are written in English. 

Author: JT
Last modified: 2026-03-25
---------------------------------------------'''

# Imports
import matplotlib.pyplot as plt
import numpy as np
from time import localtime

class Audiogram:
    def __init__(self, hearing_threshold = None, language = 'English', setup_text= None): 
        self.hearing_threshold = hearing_threshold
        self.language = language
        self.setup_text =  setup_text
        self.hearing_outcome = list(self.hearing_threshold.values())
        self.x_ticks = [0.125, 0.250, 0.500, 0.750, 1, 1.5, 2, 3, 4, 6, 8]
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
            if self.hearing_outcome[tone] == 'not heard':
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
        rel_freq = (500, 1000, 2000, 4000)         # relevant tones for the pta4
        '''
        Try to evaluate the mean, only possible, when all relevant frequencies were heard 
        by the user. Otherwise output is not calculatable
        '''
        try:
            pure_tone_average = [self.hearing_threshold[k] for k in rel_freq]
            pta = np.mean(pure_tone_average)
            ax.text(0, 0.5, 'PTA4 (0.5, 1, 2, 4 kHz): ' + str(pta) + ' dB')
        except KeyError:
            pta = self.setup_text[self.language]['audiogram']['pta4_unavailable']
            ax.text(0, 0.5, 'PTA4 (0.5, 1, 2, 4 kHz): ' + str(pta))
                                                                             
# Main
if __name__ == '__main__':
    Audiogram()


    
