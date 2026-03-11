'''---------------------------------------------
main.py
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
from gui_tkinter import gui_Hearing_test

gui_Hearing_test()

    
