from tkinter import *
from VKeyboard import VKeyboard
import pymysql
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk

class Registration_User(Tk):
    def __init__(self):
        super().__init__()
        self.title("Thesis")
        self.attributes("-fullscreen", True)
        VKeyboard(self)
        
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
        self.option = Combobox(self.main_frame, state = "readonly", textvariable = sex, width = "43", values = self.option_list_sex)
        self.option.grid(row = 4, column = 2, pady = 15)
            
        self.label_birth_day = Label(self.main_frame, text = "Birth Day\t\t:",bg = "white", relief = "ridge")
        self.label_birth_day.grid(row = 5, column = 1)
        self.entry_birth_day = Entry(self.main_frame, textvariable = birth_day,bg = "white", width = "45")
        self.entry_birth_day.grid(row = 5, column = 2, pady = 15)
 
        #self.entry_birth_day.bind('<FocusIn>',self.birth_day_keyboard_resident)
        
        self.label_civil_status = Label(self.main_frame, text = "Civil Status\t:",bg = "white", relief = "ridge")
        self.label_civil_status.grid(row = 6, column = 1)
        
        self.option_list_cs = ["Single", "Married", "Widdow", "Separated", "Live-in", "Unkown"]
        self.option_cs = Combobox(self.main_frame, state="readonly", textvariable = civil_status, width = "43", values = self.option_list_cs)
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
        
        self.label_question = Label(self.main_frame, text = "Security Question\t:",bg = "white", relief = "ridge")
        self.label_question.grid(row= 9, column = 1)
        self.question_list = ["What was your childhood nickname?",
                                      "In what city did you meet your spouse/significant other?",
                                      "What is the name of your favorite childhood friend?",
                                      "What street did you live on in third grade?",
                                      "What is the middle name of your youngest child?",
                                      "What is your oldest sibling's middle name?",
                                      "What school did you attend for sixth grade?",
                                      "What is your oldest cousin's first and last name?",
                                      "What was the name of your first stuffed animal?",
                                      "In what city or town did your mother and father meet?",
                                      "Where were you when you had your first kiss?",
                                      "What is the first name of the boy or girl that you first kissed?",
                                      "What was the last name of your third grade teacher?",
                                      "In what city does your nearest sibling live?",
                                      "What is your maternal grandmother's maiden name?",
                                      "In what city or town was your first job?",
                                      "What is the name of the place your wedding reception was held?",
                                      "What is the name of a college you applied to but didn't attend?",
                                      "What was the name of your elementary / primary school?",
                                      "What is the name of the company of your first job?",
                                      "What was your favorite place to visit as a child?",
                                      "What is your spouse's mother's maiden name?",
                                      "What is the country of your ultimate dream vacation?",
                                      "What is the name of your favorite childhood teacher?",
                                      "To what city did you go on your honeymoon?",
                                      "What was your dream job as a child?",
                                      "Who was your childhood hero?"]
        
        self.question_list= Combobox(self.main_frame, state = "readonly", width = "43", textvariable = security_question, values = self.question_list)
        self.question_list.grid(row = 9, column = 2, pady = 15)
        
        self.answer_label = Label(self.main_frame, text = "Answer\t\t:", bg ="white", relief = "ridge")
        self.answer_label.grid(row = 10, column = 1)
        self.answer_entry = Entry(self.main_frame, textvariable = answer, width = "45")
        self.answer_entry.grid(row = 10, column = 2, pady = 15)
        #self.answer_entry.bind('<FocusIn>',self.answer_keyboard_resident)
        

        self.button_submit = Button(self.main_frame, text = "Proceed to Step 2",bg = "white", command = lambda: self.registered(first_name.get(),
                                                                                                                     middle_name.get(),
                                                                                                                     last_name.get(), sex.get(),
                                                                                                                     birth_day.get(),
                                                                                                                     civil_status.get(),
                                                                                                                     year_of_residency.get(),
                                                                                                                     place_of_birth.get(),
                                                                                                                     security_question.get(), answer.get()))
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

    def registered(self,get_first_name,
                   get_middle_name,
                   get_last_name,
                   get_sex,
                   get_birth_day,
                   get_civil_status,
                   get_year_of_residency,
                   get_place_of_birth,
                   get_security_question,
                   get_answer):
        self.get_first_name = get_first_name
        self.get_middle_name = get_middle_name
        self.get_last_name = get_last_name
        self.get_sex = get_sex
        self.get_birth_day = get_birth_day 
        self.get_civil_status = get_civil_status
        self.get_year_of_residency = get_year_of_residency 
        self.get_place_of_birth = get_place_of_birth
        self.get_security_question = get_security_question
        self.get_answer = get_answer
        try: 
            _year = int(self.get_birth_day[0:4])
            _month = int(self.get_birth_day[4:6])
            _day = int(self.get_birth_day[6:8])
               
            self.get_birth_day = datetime.datetime(_year, _month, _day)
        except Exception as e:
            self.get_birth_day = ""
            
        if (self.get_first_name == "" or self.get_middle_name == "" or
            self.get_last_name == "" or self.get_sex == "" or self.get_birth_day == "" or
            self.get_civil_status == "" or self.get_place_of_birth == "" or
            self.get_security_question =="" or self.get_answer == "" or
            self.get_year_of_residency ==""):
                messagebox.showerror("Error!","Please complete the required field", parent = self)
        else:
            #register to db
            pass
        
if __name__ == "__main__":
    Registration_User().mainloop()

