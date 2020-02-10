import tkinter as tk


class VKeyboard(tk.Toplevel):
    INSTANCE = None
    
    def __init__(self, parent):
        super().__init__(parent)
        # Don't show the 'Toplevel' at instantiation
        super().withdraw()
        
        self.configure(background="cornflowerblue")
        self.geometry("+0+283")
        self.wm_attributes("-alpha", 0.7)
        self.wm_attributes("-type", 'toolwindow')
        self.wm_overrideredirect(boolean=True)
        
        self.create()
        self.uppercase = False
        self.entry = None
        
        # Process all application == parent events
        parent.bind_all('<FocusIn>', self.on_event, add='+')
        parent.bind_all('<Button-1>', self.on_event, add='+')
    
    def on_event(self, event):
        w = event.widget
        
        # Don't process the own Button
        if w.master is not self:
            w_class_name = w.winfo_class()
            print('on_focus_in:{}'.format((w_class_name, self.state())))
            
            if w_class_name in ('Entry',):
                if self.state() == 'withdrawn':
                    self.deiconify()
                
                self.entry = w
            
            elif w_class_name in ('Button',):
                super().withdraw()
                w.focus_force()
    
    def create(self):
        alphabets = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', "\\"],
            ['Caps Lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Enter'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
            ['Space']
        ]
        
        for y, row in enumerate(alphabets):
            x = 0
            for text in row:
                if text in ('Enter', 'Shift'):
                    width = 18
                    columnspan = 2
                elif text == 'Space':
                    width = 124
                    columnspan = 16
                elif text in ('Backspace', '\\', 'Tab', '`', 'Caps Lock'):
                    width = 10
                    columnspan = 1
                else:
                    width = 4
                    columnspan = 1
                
                _btn = tk.Button(self, text=text, width=width, padx=3, pady=3, bd=12, bg="black", fg="white")
                _btn.grid(row=y, column=x, columnspan=columnspan)
                _btn.bind('<Button-1>', self.select)
                
                x += columnspan
    
    def select(self, event):
        value = event.widget['text']
        
        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = '\n'
        elif value == 'Tab':
            value = '\t'
        
        if value == "Backspace":
            if isinstance(self.entry, tk.Entry):
                self.entry.delete(len(self.entry.get()) - 1, 'end')
            # elif isinstance(entry, tk.Text):
            else:  # tk.Text
                self.entry.delete('end - 2c', 'end')
        
        elif value in ('Caps Lock', 'Shift'):
            self.uppercase = not self.uppercase  # change True to False, or False to True
        else:
            if self.uppercase:
                value = value.upper()
            
            self.entry.insert('end', value)


if __name__ == "__main__":
    root = tk.Tk()
    entry = tk.Entry(root).grid()
    btn = tk.Button(root, text='withdraw').grid()
    VKeyboard(root)
    root.mainloop()
