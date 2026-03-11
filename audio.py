'''---------------------------------------------
audiology.py
This program performs a basic hearing test by 
playing pure tones from 125 
to 8000 Hz. For each frequency the sound level is increased 
until the tone is heard by the patient. 
If a frequency is not heard, the program marks the tone 
as 'nicht gehört'.

User interaction and output messages are in German.
Code and comments are written in English. 

Author: JT
Last modified: 2026-02-19
---------------------------------------------'''

# Included modules
import threading
import numpy as np
import sounddevice as sd
import time

class Hearing_test:
    def __init__(self):
        #Typical frequencies for hearing test
        self.frequencies = [125, 250, 500, 750, 1000, 2000, 3000, 4000, 6000, 8000]
        self.soundlevel = list(range(-5,110,5))
        self.program_active = True
        self.tone_heard = False
        self.sampling_rate = 44100
        self.duration = 1  
        self.reference_amplitude = 0.01
        self.status_test = 'ongoing'
        
    def control_console(self):                  # Set for testing the script, will be replace later
        press_button_thread = threading.Thread(target=self.press_button_thread,
                                           daemon=True)
        press_button_thread.start()
        while not self.program_active:
            time.sleep(0.01)
        self.program_active = False
        print('\n')                                                                                         # Output of the Measurement
        print('Hörergebnis:')
        
        for freq in self.hearing_threshold:
            print(freq, 'Hz :', self.hearing_threshold[freq], 'dbHL')    
    
    def press_button_thread(self):
        '''
        Separate thread that checks whether the patient has heard the tone.
        If ENTER is pressed, the global variable 'tone_heard' is set to True.
        '''
        self.tone_heard = True
        time.sleep(0.3)         #debounce to avoid multiple triggers
        time.sleep(0.05)
    
    def run_hearing_test(self):
       '''
       Initializes all hearing test parameters and starts the test.
       All Variables are chosen, that represent a typical hearing test.
       Returns a dictionary with hearing thresholds per frequency.
       '''
       
       time_vector = np.linspace(0, self.duration, int(self.sampling_rate * self.duration))                  
       self.play_tones(time_vector)
       self.status_test = 'finish'

    def play_tones(self, time_vector):
        '''
        Plays tones at all test frequencies and 
        increases sound level until tone is heard
        '''
        self.hearing_threshold = {}
        for self.freq in self.frequencies:                         
            base_tone = np.sin(2 * np.pi * self.freq * time_vector)                       
            for sound_level in self.soundlevel:          
                self.hearing_threshold[self.freq] = 'nicht gehört'                               # Default result if tone not heard
                amplitude = self.reference_amplitude * 10 ** (sound_level/20)               
                audio_signal = (amplitude * base_tone).astype(np.float32)               
                
                sd.play(audio_signal, self.sampling_rate)                            
                sd.wait()       
                time.sleep(0.5)                                                             
                
                if self.tone_heard:
                    self.hearing_threshold[self.freq] = sound_level                                 
                    break 
            self.tone_heard = False                                                                                               

# Main
if __name__ == '__main__':
    Hearing_test()


    
