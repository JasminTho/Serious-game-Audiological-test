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
Last modified: 2025-02-19
---------------------------------------------'''

# Included modules
import threading
import keyboard
import numpy as np
import sounddevice as sd
import time

# global variables
frequencies = [125, 250, 500, 750, 1000, 2000, 3000, 4000, 6000, 8000]      #Typical frequencies for hearing test
program_active = True
tone_heard = False

# Functions
def keyboard_input_thread():
    ''' 
    Separate thread that checks whether the patient has heard the tone.
    If ENTER is pressed, the global variable 'tone_heard' is set to True.
    '''	          
    while program_active:
        global tone_heard
        if keyboard.is_pressed('enter'):
            tone_heard = True
            time.sleep(0.3)         #debounce to avoid multiple triggers
        time.sleep(0.05)
    

def play_tones(time_vector, duration, reference_amplitude, sampling_rate):
    '''
    Plays tones at all test frequencies and 
    increases sound level until tone is heard
    '''
    print('Ton abspielen')              # Message to user, so they could see that the program is working
    global tone_heard
    hearing_threshold = {}
    for freq in frequencies:                              
        base_tone = np.sin(2 * np.pi * freq * time_vector)                       
        for sound_level in range(-5, 110, 5):           
            hearing_threshold[freq] = 'nicht gehört'                               # Default result if tone not heard
            amplitude = reference_amplitude * 10 ** (sound_level/20)               
            audio_signal = (amplitude * base_tone).astype(np.float32)               
            
            sd.play(audio_signal, sampling_rate)                            
            sd.wait()       
            time.sleep(0.5)                                                             
            
            if tone_heard:
                hearing_threshold[freq] = sound_level                                 
                break 
        tone_heard = False                                                 
    return hearing_threshold                                                       
           

def run_hearing_test():
    '''
    Initializes all hearing test parameters and starts the test. 
    All Variables are chosen, that represent a typical hearing test.
    Returns a dictionary with hearing thresholds per frequency.
    '''
    sampling_rate = 44100       
    duration = 1                       
    time_vector = np.linspace(0, duration, int(sampling_rate * duration))                  
    reference_amplitude = 0.01
    return play_tones(time_vector, duration, reference_amplitude, sampling_rate)           
    
    
# Main
print('Willkommen zum Hörtest. \nSobald Sie einen Ton hören, drücken sie bitte Enter.')              # Welcome Text and User Informations
input('Zum Starten drücke bitte Enter: ')                                              

keyboard_thread = threading.Thread(
    target=keyboard_input_thread,
    daemon=True
    )
keyboard_thread.start()

hearing_threshold=run_hearing_test()
program_active = False
print('\n')                                                                                         # Output of the Measurement
print('Hörergebnis:')
for freq in hearing_threshold:
    print(freq, 'Hz :',hearing_threshold[freq], 'dbHL')


    
