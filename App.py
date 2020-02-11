import tkinter as tk
from VKeyboard import VKeyboard


class LabelEntry(tk.Frame):
    def __init__(self, parent, **kwargs):
        text = kwargs.pop('text', 'Unknown')
        super().__init__(parent, **kwargs)

        self.variable = tk.StringVar(self)
        pady = 5
        tk.Label(self, text='{}\t:'.format(text), relief="ridge", bg="white").grid(row=0, column=0, padx=5, pady=pady)
        self.entry = tk.Entry(self, textvariable=self.variable, bg="white", width="45")
        self.entry.grid(row=0, column=1, pady=pady)
class Form1(tk.Frame):
    def __init__(self, parent, fields, **kwargs):
        super().__init__(parent, **kwargs)


        self.fields = dict.fromkeys(fields, None)

        for row, text in enumerate(fields, 1):
            self.fields[text] = LabelEntry(self, text=text)
            self.fields[text].grid(row=row, column=0, pady=0)

    def get(self):
        return {key: item.entry.get() for key, item in self.fields.items()}


class Kiosk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Thesis")

        VKeyboard(self)

        form1 = Form1(self, ("First Name", "Middle Name", "Last Name"))
        form1.grid(row=1, column=0)

        vbtn = tk.Button(self, text="Proceed to Step 2", bg="white", command=lambda: self.registered(form1.get()))
        vbtn.grid(row=2, column=0, pady=5)

    def registered(self, data):
        print('registered:{}'.format(data))


if __name__ == "__main__":
    Kiosk().mainloop()
