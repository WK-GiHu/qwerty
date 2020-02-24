#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import tkinter as tk
# from modules.tkinter import Application
import threading, time


class IdleCounter(threading.Thread):
    label = 'idle'
    
    def __init__(self, app):
        super().__init__(daemon=True)
        self.app = app

        self.timeout = 5
        self._counter = self.timeout

        self.start()
        self.app.bind('<<IDLE>>', self.on_idle)

    def run(self):
        print('run()'.format())
        
        while True:
            if self._counter > 0:
                self._counter -= 1
                print('\t{}'.format(self._counter))
                IdleCounter.label = 'timeout in {} sec.'.format(self._counter)
                
                if self._counter == 0:
                    IdleCounter.label = 'idle, click to reset'
                    self.app.event_generate('<<TIMEOUT>>', when='tail')
                    
            time.sleep(1)
                    
        print('IdleCount terminated'.format())
        
    def on_idle(self, event):
        print('on_idle(state={})'.format(event.state))
        if event.state == 0:  # reset the counter
            self._counter = self.timeout
            # print('\t_counter:{}, _is_alive:{}'.format(self._counter, self._is_alive.is_set()))


class App(tk.Tk):
    def __init__(self):
        super().__init__()  # options=(tk.Menu,))  # geometry="200x200+0+0")
        self.menubar = tk.Menu()
        self.menubar.add_command(label='', command=self.on_click)
        self.config(menu=self.menubar)

        IdleCounter(self)
        self.bind('<<TIMEOUT>>', self.on_timeout)
        
        self.after(1000, self.update_label)
        
    def update_label(self):
        self.menubar.entryconfig(1, label=IdleCounter.label)
        self.after(500, self.update_label)
        
    def on_click(self):
        self.event_generate('<<IDLE>>', when='tail')

    def on_timeout(self, event):
        print('on_timeout()'.format())


if __name__ == "__main__":
    App().mainloop()
