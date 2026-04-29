'''---------------------------------------------
audio.py
This program performs a basic hearing test by 
playing pure tones from 125 to 8000 Hz. For each frequency the sound level is increased 
until the tone is heard by the patient. 


Author: JT
Last modified: 2026-04-28
---------------------------------------------'''

# Imports
import numpy as np
import pandas as pd
import sounddevice as sd
import time

class HearingTest:
    def __init__(self):
        #Typical frequencies for a hearing test
        self.frequencies = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
        # Standard audiometric intensity levels in 5 dB steps (approx. hearing threshold range)
        # Range extends slightly below 0 dB HL for sensitivity testing and up to 110 dB for upper limit
        self.soundlevel = list(range(-5,115,5))
        self.tone_heard = False
        self.sampling_rate = 44100
        self.duration = 1  
        self.reference_amplitude = 0.01
        self.program_active = True
        
        # Flags for definition of hearing abibility
        self.heard = 0
        self.not_heard = 1
        self.not_measured = 2

    def run_hearing_test(self, callback):
       '''
       Initializes all hearing test parameters and starts the test.
       All variables are chosen to represent a typical hearing test.
       Returns a dictionary with hearing thresholds per frequency.
       '''
       self.callback = callback
       self.time_vector = np.linspace(0, self.duration, int(self.sampling_rate * self.duration), endpoint=False)                  
       self.play_tones()

    def play_tones(self):
        '''
        Plays tones at all test frequencies and 
        increases sound level until tone is heard
        '''
        self.hearing_threshold = pd.DataFrame(index = [0],
            columns=['0.125_khz', '0.25_khz', '0.5_khz', '0.75_khz', '1_khz', '1.5_khz', '2_khz', '3_khz', '4_khz', '6_khz', '8_khz',
                                             '0.125_flag', '0.25_flag', '0.5_flag', '0.75_flag', '1_flag', '1.5_flag', '2_flag', '3_flag', '4_flag', '6_flag', '8_flag'])
        for freq in self.frequencies:
            value = freq / 1000
            if value.is_integer():
                str_freq = f'{int(value)}_khz'
                str_flag = f'{int(value)}_flag'
            else:
                str_freq = f'{value}_khz'
                str_flag = f'{value}_flag'
            if not self.program_active:
                break                
            base_tone = np.sin(2 * np.pi * freq * self.time_vector)
            
            # Default result if tone not heard 
            self.hearing_threshold.loc[0, str_freq] = 110
            self.hearing_threshold.loc[0, str_flag] = self.not_heard
                      
            for sound_level in self.soundlevel:          
                amplitude = self.reference_amplitude * 10 ** (sound_level/20)               
                audio_signal = (amplitude * base_tone).astype(np.float32)               
                
                sd.play(audio_signal, self.sampling_rate)                            
                sd.wait()       
                time.sleep(0.5)                                                             
                
                if self.tone_heard:
                    self.hearing_threshold.loc[0, str_freq] = sound_level
                    self.hearing_threshold.loc[0, str_flag] = self.heard                               
                    break 
            
            self.tone_heard = False    
            if self.callback:
                self.callback()             # send claback to the gui, so that the processbar is updated                                                                                      

# Main
if __name__ == '__main__':
    HearingTest()


    
