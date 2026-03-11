'''---------------------------------------------
audiology.py
This program generate a tkinter graphical user interface for the Hearing Test

User interaction and output messages are in English and German.
Code and comments are written in English. 

Author: JT
Last modified: 2026-02-26
---------------------------------------------'''

# Included modules
from tkinter import Tk, Text, Label, WORD, Frame
from tkinter import ttk
from json import load
from audio import Hearing_test
import threading

class gui_Hearing_test:
    def __init__(self):
        # Load of the menu text 
        self.load_text_settup()
        self.ht = Hearing_test()
        
        self.window = Tk()
        
        # Settings window
        self.window.title(self.setup_text['English']['start_menu']['title'])
        self.window.resizable(False, False)
        
        # size and position of the window
        self.window_width  = 350 
        window_height = 200
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - self.window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        self.window.geometry(f'{self.window_width}x{window_height}+{center_x}+{center_y}')
        
        self.window.config(bg = '#FAEBD7')
        # Change to start window
        self.start_window()
        
        # start GUI
        self.window.mainloop()
        
    def load_text_settup(self): 
        with open('Menu_text_gui.json', 'r', encoding = 'utf-8') as file:
            self.setup_text = load(file)
    
    def start_window(self):
        initial_font =('Arial', 10)
        self.phase_programm = 'start'
        # Widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", 
                        font= initial_font,
                        justify = 'center')  
        self.bt_start_hearing_test = ttk.Button(self.window,
                                       text = self.setup_text['English']['start_menu']['button_text'],
                                       command = self.button_action)
        self.txt_user_information = Text(self.window,
                                    bg = '#FAEBD7',
                                    font = initial_font,
                                    height = 3,
                                    bd = 0,
                                    wrap = WORD)
        self.txt_user_information.tag_configure("center", justify="center")
        self.txt_user_information.insert('end', self.setup_text['English']['start_menu']['entry_text'], 'center')
        
        
        # Set cb_language and lb_language in a frame, to put it close together in the window
        self.frame = Frame(self.window,
                           bg = '#FAEBD7')
        self.cb_language = ttk.Combobox(self.frame,
                                        font = initial_font,
                                        width = 10)
        self.cb_language['values'] = ['English', 'German']
        self.cb_language.set('English')
        
        self.lb_language = Label(self.frame,
                                 text = 'Language:',
                                 font = initial_font,
                                 bg = '#FAEBD7',
                                 anchor = 'e')
        
        # Layout of widget
        self.bt_start_hearing_test.grid(column = 0, columnspan= 3, row =2, pady = 10)
        self.txt_user_information.grid(column = 0, columnspan = 3, row =1, padx = 10, sticky = 'ew')
        self.frame.grid(column = 2, row = 0, pady = 5, padx = 5, sticky = 'e')
        self.lb_language.grid(column = 0, row =0, padx = 5)
        self.cb_language.grid(column = 1, row =0)
        
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(1, weight=1) 
        self.window.rowconfigure(2, weight=0)
        # Change of the Language
        
        self.cb_language.bind("<<ComboboxSelected>>", self.language_change)
        
    # Eventhandling
    def button_action(self):
        if self.phase_programm == 'start':
            self.pure_tone_measurement()
        elif self.phase_programm == 'pure_tone_measurement':
            self.ht.tone_heard = True
            number_of_tones = len(self.ht.frequencies)
            self.progressbar.step(100/number_of_tones)
        elif self.phase_programm == 'result':
            self.start_window()
    
    
    def pure_tone_measurement(self):
        self.phase_programm = 'pure_tone_measurement'
        self.ht.program_active = True
        self.lb_language.destroy()
        self.cb_language.destroy()
        self.progressbar = ttk.Progressbar(self.window,
                                           length = self.window_width - 10)
        self.progressbar.grid(column = 0, columnspan= 3, row = 0)
        self.txt_user_information.delete(1.0,'end') 
        play_tone_thread = threading.Thread(target = self.play_tone, 
                                            daemon = True) 
        play_tone_thread.start()
 
    def language_change(self, event):
        language = self.cb_language.get()
        self.window.title(self.setup_text[language]['start_menu']['title'])
        self.txt_user_information.delete(1.0,'end')
        self.txt_user_information.insert('end', self.setup_text[language]['start_menu']['entry_text'], 'center')
        self.bt_start_hearing_test.config(text = self.setup_text[language]['start_menu']['button_text'])
    
    def play_tone(self):
        # Start Hearing Test
        self.ht.run_hearing_test()
        self.show_results()
    
    def show_results(self):
        self.phase_programm = 'result'
        print(self.ht.hearing_threshold)
        
        
# Main
if __name__ == '__main__':
    gui_Hearing_test()


    
