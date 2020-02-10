import tkinter as tk
class VKeyboard(tk.Toplevel):
    INSTANCE = None
    def __init__(self, parent):
     # here goes the settings for the Toplevel
        super().__init__(parent)
        self.configure(background="cornflowerblue")
        self.wm_attributes("-alpha", 0.7)
        self.create()
        self.uppercase = False
        self.entry = None

    def select(self, entry, value):

        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = '\n'
        elif value == 'Tab':
            value = '\t'

        if value == "Backspace":
            if isinstance(self.entry, tk.Entry):
                self.entry.delete(len(self.entry.get())-1, 'end')
            #elif isinstance(entry, tk.Text):
            else: # tk.Text
                self.entry.delete('end - 2c', 'end')
        elif value in ('Caps Lock', 'Shift'):
            self.uppercase = not self.uppercase # change True to False, or False to True
        else:
            if self.uppercase:
                value = value.upper()
            self.entry.insert('end', value)

    def create(self, root, entry):
        alphabets = [
            ['`','1','2','3','4','5','6','7','8','9','0','-','=','Backspace'],
            ['Tab','q','w','e','r','t','y','u','i','o','p','[',']',"\\"],
            ['Caps Lock','a','s','d','f','g','h','j','k','l',';',"'",'Enter'],
            ['Shift','z','x','c','v','b','n','m',',','.','/','Shift'],
            ['Space']
        ]    


        for y, row in enumerate(alphabets):

            x = 0

            #for x, text in enumerate(row):
            for text in row:

                if text in ('Enter', 'Shift'):
                    width = 15
                    columnspan = 2
                elif text == 'Space':
                    width = 130
                    columnspan = 16
                else:                
                    width = 5
                    columnspan = 1

                tk.Button(self, text=text, width=width, 
                          command=lambda value=text: self.select(value),
                          padx=3, pady=3, bd=12, bg="black", fg="white"
                         ).grid(row=y, column=x, columnspan=columnspan)

                x += columnspan

    @classmethod
    def entry(cls, master, entry):
        if cls.INSTANCE is None:
            cls.INSTANCE = cls(master)
        else:
            cls.INSTANCE.deiconify()
            cls.INSTANCE.entry = entry
    @classmethod
    def withdraw(cls):
        if cls.INSTANCE is not None:
            tk.Toplevel.withdraw(cls.INSTANCE)

if __name__ == '__main__':
    root = tk.Tk()
    entry = tk.Entry(root)
    entry.grid()
    VKeyboard.entry(root, entry)
    root.mainloop()
