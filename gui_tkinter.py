'''---------------------------------------------
gui_tkinter.py
This program generates a tkinter graphical user interface for the Hearing Test.
It starts a pure tone measurement and gives the results in a separated plot

User interaction and output messages are in English and German.
Code and comments are written in English. 

Author: JT
Last modified: 2026-03-25
---------------------------------------------'''

# Imports
from audio import HearingTest
from audiogram import Audiogram
from json import load
import threading
from tkinter import Tk, Text, Label, WORD, Frame, Button
from tkinter import ttk

class HearingTestGUI:
    def __init__(self):
        # Load all user interface texts from the JSON file
        self.load_text_setup()
        self.create_window()
    
    def create_window(self):
        '''
        Initialize core components
        '''
        self.ht = HearingTest()
        self.language = 'English'
        self.window = Tk()
        
        # Configure main window
        self.window.title(self.setup_text[self.language]['start_menu']['title'])
        self.window.resizable(False, False)                 # Prevent resizing of the window
        
        # Define window size and position
        self.window_width  = 350 
        window_height = 200
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - self.window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        self.window.geometry(f'{self.window_width}x{window_height}+{center_x}+{center_y}')      # Center the window on the screen
        self.window.config(bg = '#FAEBD7')
        
        # Initialize start window
        self.start_window()
        
        
    def load_text_setup(self): 
        '''
        Load the JSON File 'Menu_text_gui' to enable multi-language support
        '''
        with open('Menu_text_gui.json', 'r', encoding = 'utf-8') as file:
            self.setup_text = load(file)
    
    def start_window(self):
        '''
        Initialize the start screen of the GUI 
        '''
        initial_font = ('Arial', 10)
        self.phase_program = 'start'
        # Widgets
        style = ttk.Style()
        style.theme_use('clam') 
        self.bt_hearing_test = Button(self.window,
                                       text = self.setup_text[self.language]['start_menu']['button_text'],
                                       font= initial_font,
                                       justify = 'center',
                                       command = self.button_action)
        self.txt_user_information = Text(self.window,
                                    bg = '#FAEBD7',
                                    font = initial_font,
                                    height = 3,
                                    bd = 0,
                                    wrap = WORD)
        self.txt_user_information.tag_configure("center", justify="center")
        self.txt_user_information.insert('end', self.setup_text[self.language]['start_menu']['entry_text'], 'center')
        
        
        # Group language selection in a frame
        self.frame = Frame(self.window,
                           bg = '#FAEBD7')
        self.cb_language = ttk.Combobox(self.frame,
                                        font = initial_font,
                                        width = 10,
                                        state = 'readonly')
        self.cb_language['values'] = ['English', 'German']
        self.cb_language.set(self.language)
        
        self.lb_language = Label(self.frame,
                                 text = 'Language:',
                                 font = initial_font,
                                 bg = '#FAEBD7',
                                 anchor = 'e')
        
        # Layout of widget
        self.bt_hearing_test.grid(column = 0, columnspan= 3, row =2, pady = 10)
        self.txt_user_information.grid(column = 0, columnspan = 3, row =1, padx = 10, sticky = 'ew')
        self.frame.grid(column = 2, row = 0, pady = 5, padx = 5, sticky = 'e')
        self.lb_language.grid(column = 0, row =0, padx = 5)
        self.cb_language.grid(column = 1, row =0)
        
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(1, weight=1) 
        self.window.rowconfigure(2, weight=0)
        
        # Handle language change
        self.cb_language.bind("<<ComboboxSelected>>", self.language_change)
        
    def button_action(self):
        '''
        Managing of the event handling of the button.
        This is based on the phase of the program.
        '''
        if self.phase_program == 'start':
            self.pure_tone_measurement()
        elif self.phase_program == 'pure_tone_measurement':
            self.ht.tone_heard = True
            self.bt_hearing_test.config(state = 'disabled')         # After the button was clicked, it is disabled for a few seconds to avoid double mouse clicks
            self.window.after(500, lambda: self.bt_hearing_test.config(state = 'normal'))
        elif self.phase_program == 'result':
            self.new_start()

    def pure_tone_measurement(self):
        '''
        Measurement of the pure tone threshold using the standard tones.
        '''
        self.phase_program = 'pure_tone_measurement'
        self.ht.program_active = True
        self.frame.destroy()                            # The language frame is destroyed since the user can only change the language before starting the measurement
        self.progressbar = ttk.Progressbar(self.window,
                                           length = self.window_width - 10,
                                           mode='determinate')
        self.progressbar.grid(column = 0, columnspan= 3, row = 0)
        self.bt_hearing_test.config(text = self.setup_text[self.language][self.phase_program]['button_text'])
        self.txt_user_information.delete(1.0,'end')
        self.txt_user_information.insert('end', self.setup_text[self.language][self.phase_program]['entry_text'], 'center')
        play_tone_thread = threading.Thread(target = self.play_tone,                    # Run hearing test in a separate thread to keep the GUI responsive
                                            daemon = True) 
        play_tone_thread.start()
 
    def language_change(self, event):
        '''
        Update GUI text when the user changes the language
        '''
        self.language = self.cb_language.get()
        self.window.title(self.setup_text[self.language]['start_menu']['title'])
        self.txt_user_information.delete(1.0,'end')
        self.txt_user_information.insert('end', self.setup_text[self.language]['start_menu']['entry_text'], 'center')
        self.bt_hearing_test.config(text = self.setup_text[self.language]['start_menu']['button_text'])
    
    def play_tone(self):
        '''
        Run the Hearing Test
        '''
        self.ht.run_hearing_test(self.update_progressbar)
        self.window.after(0, self.show_results)
    
    def update_progressbar(self):
        '''
        Update the progress bar after each tested frequency
        '''
        progress_step = 100 / len(self.ht.frequencies)          # Calculate step size for each frequency
        self.window.after(0, lambda: self.progressbar.step(progress_step))
    
    def show_results(self):
        '''
        Show the result as a matplotlib plot file
        '''
        self.progressbar.destroy()
        self.phase_program = 'result'
        self.bt_hearing_test.config(text = self.setup_text[self.language][self.phase_program]['button_text'])
        self.txt_user_information.delete(1.0,'end')
        self.txt_user_information.insert('end', self.setup_text[self.language][self.phase_program]['entry_text'], 'center')
        Audiogram(self.ht.hearing_threshold, self.language, self.setup_text)
    
    def new_start(self):
        '''
        Reset the GUI for a new test
        '''
        self.bt_hearing_test.destroy()
        self.txt_user_information.destroy()
        self.start_window()
    
    def run(self):
        self.window.mainloop()
    
# Main
if __name__ == '__main__':
    app = HearingTestGUI()
    app.run()


    
