import tkinter as tk
class VKeyboard(tk.Toplevel):
    INSTANCE = None
    def __init__(self):
     # here goes the settings for the Toplevel

        alphabets = [
            ['`','1','2','3','4','5','6','7','8','9','0','-','=','Backspace'],
            ['Tab','q','w','e','r','t','y','u','i','o','p','[',']',"\\"],
            ['Caps Lock','a','s','d','f','g','h','j','k','l',';',"'",'Enter'],
            ['Shift','z','x','c','v','b','n','m',',','.','/','Shift'],
            ['Space']
        ]    

        uppercase = False  # use uppercase chars. 

    def select(entry, value):
        global uppercase

        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = '\n'
        elif value == 'Tab':
            value = '\t'

        if value == "Backspace":
            if isinstance(entry, tk.Entry):
                entry.delete(len(entry.get())-1, 'end')
            #elif isinstance(entry, tk.Text):
            else: # tk.Text
                entry.delete('end - 2c', 'end')
        elif value in ('Caps Lock', 'Shift'):
            uppercase = not uppercase # change True to False, or False to True
        else:
            if uppercase:
                value = value.upper()
            entry.insert('end', value)

    def create(root, entry):

        window = tk.Toplevel(root)
        window.configure(background="cornflowerblue")
        window.wm_attributes("-alpha", 0.7)

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

                tk.Button(window, text=text, width=width, 
                          command=lambda value=text: select(entry, value),
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
    main = VKeyboard(root)
    root.mainloop()
