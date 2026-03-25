'''---------------------------------------------
audio.py
This program performs a basic hearing test by 
playing pure tones from 125 to 8000 Hz. For each frequency the sound level is increased 
until the tone is heard by the patient. 
If a frequency is not heard, the program marks the tone 
as 'not heared'.

Code and comments are written in English. 

Author: JT
Last modified: 2026-03-25
---------------------------------------------'''

# Imports
import numpy as np
import sounddevice as sd
import time

class HearingTest:
    def __init__(self):
        #Typical frequencies for a hearing test
        self.frequencies = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
        self.soundlevel = list(range(-5,110,5))
        self.tone_heard = False
        self.sampling_rate = 44100
        self.duration = 1  
        self.reference_amplitude = 0.01
        self.program_active = True

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
        self.hearing_threshold = {}
        for freq in self.frequencies:
            if not self.program_active:
                break                
            base_tone = np.sin(2 * np.pi * freq * self.time_vector)
            self.hearing_threshold[freq] = 'not heard'   # Default result if tone not heard                       
            for sound_level in self.soundlevel:          
                amplitude = self.reference_amplitude * 10 ** (sound_level/20)               
                audio_signal = (amplitude * base_tone).astype(np.float32)               
                
                sd.play(audio_signal, self.sampling_rate)                            
                sd.wait()       
                time.sleep(0.5)                                                             
                
                if self.tone_heard:
                    self.hearing_threshold[freq] = sound_level                                 
                    break 
            self.tone_heard = False    
            if self.callback:
                self.callback()             # send claback to the gui, so that the processbar is updated                                                                                      

# Main
if __name__ == '__main__':
    HearingTest()


    
