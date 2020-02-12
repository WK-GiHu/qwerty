from VKeyboard import VKeyboard
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class Registration_User(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Thesis")
        
        self.main_frame = Frame(self)
        self.main_frame.pack(fill = BOTH, expand = 1)
        
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
                
        
        first_name = StringVar()
        middle_name = StringVar()
        last_name = StringVar()
        sex = StringVar()
        birth_day = StringVar()
        civil_status = StringVar()
        year_of_residency = StringVar()
        place_of_birth = StringVar()
        security_question = StringVar()
        answer = StringVar()
        
        self.label_head = Label(self.main_frame, text = "Fill up all informations below",bg = "white", font = ("Times New Roman", 25))
        self.label_head.grid(row = 0, column = 1, columnspan = 2)
        
        self.space_label= Label (self.main_frame, text = "\t\t", bg = "white")
        self.space_label.grid(row = 1, column = 0)

        self.label_first_name = Label(self.main_frame, text = "First Name\t:", relief = "ridge",bg = "white")
        self.label_first_name.grid(row = 1, column = 1, padx = 5, pady = 15)
        self.entry_first_name = Entry(self.main_frame, textvariable = first_name,bg = "white", width = "45")
        self.entry_first_name.grid(row = 1, column = 2, pady = 15)
        #self.entry_first_name.bind('<FocusIn>', self.first_name_keyboard_resident)
        

        self.label_middle_name = Label(self.main_frame, text = "Middle Name\t:",bg = "white", relief = "ridge")
        self.label_middle_name.grid(row = 2, column = 1)
        self.entry_middle_name = Entry(self.main_frame, textvariable = middle_name,bg = "white", width = "45")
        self.entry_middle_name.grid(row = 2, column = 2, pady = 15)
        #self.entry_middle_name.bind('<FocusIn>', self.middle_name_keyboard_resident)
        
        self.label_last_name = Label(self.main_frame, text = "Last Name\t:",bg = "white", relief = "ridge")
        self.label_last_name.grid(row = 3, column = 1)
        self.entry_last_name = Entry(self.main_frame, textvariable = last_name,bg = "white", width = "45")
        self.entry_last_name.grid(row = 3, column = 2, pady = 15)
        #self.entry_last_name.bind('<FocusIn>', self.last_name_keyboard_resident)
        
        self.label_sex = Label(self.main_frame, text = "Sex\t\t:",bg = "white", relief = "ridge")
        self.label_sex.grid(row = 4, column = 1)
        
        self.option_list_sex = ["Male", "Female"]
        self.option = ttk.Combobox(self.main_frame, state = "readonly", textvariable = sex, width = "43", values = self.option_list_sex)
        self.option.grid(row = 4, column = 2, pady = 15)
            
        self.label_birth_day = Label(self.main_frame, text = "Birth Day\t\t:",bg = "white", relief = "ridge")
        self.label_birth_day.grid(row = 5, column = 1)
        self.entry_birth_day = Entry(self.main_frame, textvariable = birth_day,bg = "white", width = "45")
        self.entry_birth_day.grid(row = 5, column = 2, pady = 15)
 
        #self.entry_birth_day.bind('<FocusIn>',self.birth_day_keyboard_resident)
        
        self.label_civil_status = Label(self.main_frame, text = "Civil Status\t:",bg = "white", relief = "ridge")
        self.label_civil_status.grid(row = 6, column = 1)
        
        self.option_list_cs = ["Single", "Married", "Widdow", "Separated", "Live-in", "Unkown"]
        self.option_cs = ttk.Combobox(self.main_frame, state="readonly", textvariable = civil_status, width = "43", values = self.option_list_cs)
        self.option_cs.grid(row = 6, column = 2, pady = 15)
        
        self.label_year_of_residency = Label(self.main_frame, text = "Date of Residency\t:",bg = "white", relief = "ridge")
        self.label_year_of_residency.grid(row = 7, column = 1, pady = 15)
        self.entry_year_of_residency = Entry(self.main_frame, textvariable = year_of_residency,bg = "white", width = "45")
        self.entry_year_of_residency.grid(row = 7, column = 2)
        
        self.label_place_of_birth = Label(self.main_frame, text = "Place of Birth\t:",bg = "white", relief = "ridge")
        self.label_place_of_birth.grid(row = 8, column = 1)
        self.entry_place_of_birth = Entry(self.main_frame, textvariable = place_of_birth,bg = "white", width = "45")
        self.entry_place_of_birth.grid(row = 8, column = 2, pady = 15)
        #self.entry_place_of_birth.bind('<FocusIn>',self.place_of_birth_keyboard_resident)
        

        self.button_submit = Button(self.main_frame, text = "Proceed to Step 2",bg = "white")
        self.button_submit.grid(row = 11, column = 2, pady = 5)
        
        Label(self.main_frame, text = "\t \t \t   ",bg = "white").grid(row = 3, column = 3)

       # self.label_place_of_birth = Label(self.main_frame, text = "Upload Excel File",bg = "white", font = ("Times New Roman" , 15))
       # self.label_place_of_birth.place(x= 780, y = 80)
       # self.excel_upload = Button(self.main_frame, text = "Upload Excel File",bg = "white", command = self.Upload_Button)
        
       # self.excel_upload.grid(row = 2, column = 4)
       # self.excel_submit = Button(self.main_frame, text = "Submit Excel File",bg = "white", command = self.Submit_Button)
       # self.excel_submit.grid(self.main_frame = 3, column = 4, pady = 5)
        self.back_button = Button(self.main_frame, text = "Back",bg = "white", command = self.destroy)
        self.back_button.grid(row = 12, column = 2)


if __name__ == "__main__":
    Registration_User().mainloop()
