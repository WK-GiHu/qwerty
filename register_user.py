import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from datetime import datetime, date
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from pyfingerprint.pyfingerprint import PyFingerprint
import pymysql

class Registration_User(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Thesis")
        self.attributes("-fullscreen", True)
       
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill = "both", expand = 1)
        
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        print(self.ws, self.hs)        
        self.db = pymysql.connect(host = "192.168.1.11",port = 3306, user = "root",passwd = "justin",db= "thesis_db")
        self.cursor = self.db.cursor()
        GPIO.setwarnings(False)
        self.reader = SimpleMFRC522()
        
        self.attributes('-fullscreen', True)
        #self.wm_attributes('-type', 'splash')
        
        
        self.img_register_info = (Image.open("background_kiosk.png"))
        self.image_register_info = self.img_register_info.resize((self.ws,self.hs))
        self.img_background_register_info = ImageTk.PhotoImage(self.image_register_info)
        self.imglabel_register_info = tk.Label(self.main_frame, image = self.img_background_register_info).place(x=0,y=0)
        
        
        first_name = tk.StringVar()
        middle_name = tk.StringVar()
        last_name = tk.StringVar()
        sex = tk.StringVar()
        birth_day = tk.StringVar()
        civil_status = tk.StringVar()
        year_of_residency = tk.StringVar()
        place_of_birth = tk.StringVar()
        security_question = tk.StringVar()
        answer = tk.StringVar()
        
        self.label_head = tk.Label(self.main_frame, text = "Fill up all informations below",bg = "white", font = ("Times New Roman", 25))
        self.label_head.grid(row = 0, column = 1, columnspan = 2)
        
        self.space_label= tk.Label (self.main_frame, text = "\t\t", bg = "white")
        self.space_label.grid(row = 1, column = 0)

        self.label_first_name = tk.Label(self.main_frame, text = "First Name\t:", relief = "ridge",bg = "white")
        self.label_first_name.grid(row = 1, column = 1, padx = 5, pady = 15)
        self.entry_first_name = tk.Entry(self.main_frame, textvariable = first_name,bg = "white", width = "45")
        self.entry_first_name.grid(row = 1, column = 2, pady = 15)
        #self.entry_first_name.bind('<FocusIn>', self.first_name_keyboard_resident)
        

        self.label_middle_name = tk.Label(self.main_frame, text = "Middle Name\t:",bg = "white", relief = "ridge")
        self.label_middle_name.grid(row = 2, column = 1)
        self.entry_middle_name = tk.Entry(self.main_frame, textvariable = middle_name,bg = "white", width = "45")
        self.entry_middle_name.grid(row = 2, column = 2, pady = 15)
        #self.entry_middle_name.bind('<FocusIn>', self.middle_name_keyboard_resident)
        
        self.label_last_name = tk.Label(self.main_frame, text = "Last Name\t:",bg = "white", relief = "ridge")
        self.label_last_name.grid(row = 3, column = 1)
        self.entry_last_name = tk.Entry(self.main_frame, textvariable = last_name,bg = "white", width = "45")
        self.entry_last_name.grid(row = 3, column = 2, pady = 15)
        #self.entry_last_name.bind('<FocusIn>', self.last_name_keyboard_resident)
        
        self.label_sex = tk.Label(self.main_frame, text = "Sex\t\t:",bg = "white", relief = "ridge")
        self.label_sex.grid(row = 4, column = 1)
        
        self.option_list_sex = ["Male", "Female"]
        self.option = ttk.Combobox(self.main_frame, state = "readonly", textvariable = sex, width = "43", values = self.option_list_sex)
        self.option.grid(row = 4, column = 2, pady = 15)
            
        self.label_birth_day = tk.Label(self.main_frame, text = "Birth Day\t\t:",bg = "white", relief = "ridge")
        self.label_birth_day.grid(row = 5, column = 1)
        self.entry_birth_day = tk.Entry(self.main_frame, textvariable = birth_day,bg = "white", width = "45")
        self.entry_birth_day.grid(row = 5, column = 2, pady = 15)
 
        #self.entry_birth_day.bind('<FocusIn>',self.birth_day_keyboard_resident)
        
        self.label_civil_status = tk.Label(self.main_frame, text = "Civil Status\t:",bg = "white", relief = "ridge")
        self.label_civil_status.grid(row = 6, column = 1)
        
        self.option_list_cs = ["Single", "Married", "Widdow", "Separated", "Live-in", "Unkown"]
        self.option_cs = ttk.Combobox(self.main_frame, state="readonly", textvariable = civil_status, width = "43", values = self.option_list_cs)
        self.option_cs.grid(row = 6, column = 2, pady = 15)
        
        self.label_year_of_residency = tk.Label(self.main_frame, text = "Date of Residency\t:",bg = "white", relief = "ridge")
        self.label_year_of_residency.grid(row = 7, column = 1, pady = 15)
        self.entry_year_of_residency = tk.Entry(self.main_frame, textvariable = year_of_residency,bg = "white", width = "45")
        self.entry_year_of_residency.grid(row = 7, column = 2)
        
        self.label_place_of_birth = tk.Label(self.main_frame, text = "Place of Birth\t:",bg = "white", relief = "ridge")
        self.label_place_of_birth.grid(row = 8, column = 1)
        self.entry_place_of_birth = tk.Entry(self.main_frame, textvariable = place_of_birth,bg = "white", width = "45")
        self.entry_place_of_birth.grid(row = 8, column = 2, pady = 15)
        #self.entry_place_of_birth.bind('<FocusIn>',self.place_of_birth_keyboard_resident)
        
        self.label_question = tk.Label(self.main_frame, text = "Security Question\t:",bg = "white", relief = "ridge")
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
        
        self.question_list= ttk.Combobox(self.main_frame, state = "readonly", width = "43", textvariable = security_question, values = self.question_list)
        self.question_list.grid(row = 9, column = 2, pady = 15)
        
        self.answer_label = tk.Label(self.main_frame, text = "Answer\t\t:", bg ="white", relief = "ridge")
        self.answer_label.grid(row = 10, column = 1)
        self.answer_entry = tk.Entry(self.main_frame, textvariable = answer, width = "45")
        self.answer_entry.grid(row = 10, column = 2, pady = 15)
        #self.answer_entry.bind('<FocusIn>',self.answer_keyboard_resident)
        

        self.button_submit = tk.Button(self.main_frame, text = "Proceed to Step 2",bg = "white", command = lambda: self.registered(first_name.get(),
                                                                                                                     middle_name.get(),
                                                                                                                     last_name.get(), sex.get(),
                                                                                                                     birth_day.get(),
                                                                                                                     civil_status.get(),
                                                                                                                     year_of_residency.get(),
                                                                                                                     place_of_birth.get(),
                                                                                                                     security_question.get(), answer.get()))
        self.button_submit.grid(row = 11, column = 2, pady = 5)
        
        tk.Label(self.main_frame, text = "\t \t \t   ",bg = "white").grid(row = 3, column = 3)

       # self.label_place_of_birth = tk.Label(self.main_frame, text = "Upload Excel File",bg = "white", font = ("Times New Roman" , 15))
       # self.label_place_of_birth.place(x= 780, y = 80)
       # self.excel_upload = Button(self.main_frame, text = "Upload Excel File",bg = "white", command = self.Upload_Button)
        
       # self.excel_upload.grid(row = 2, column = 4)
       # self.excel_submit = Button(self.main_frame, text = "Submit Excel File",bg = "white", command = self.Submit_Button)
       # self.excel_submit.grid(self.main_frame = 3, column = 4, pady = 5)
        self.back_button = tk.Button(self.main_frame, text = "Back",bg = "white", command = self.destroy)
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
        
        print(self.get_first_name)
        print(self.get_middle_name)
        print(self.get_last_name)
        print(self.get_sex)
        print(self.get_birth_day)
        print(self.get_civil_status)
        print(self.get_year_of_residency)
        print(self.get_place_of_birth)
        print(self.get_security_question)
        print(self.get_answer)
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
            self.step2_register()
    
    def step2_register(self):
        self.main_frame.pack_forget()
        self.rfid_frame = tk.Frame(self)
        self.rfid_frame.pack(fill = BOTH, expand = 1)
        
        self.img_register = (Image.open("RFID_register.png"))
        self.img_background_register = ImageTk.PhotoImage(self.img_register)
        tk.Label_register = tk.Label(self.rfid_frame, image = self.img_background_register)
        tk.Label_register.grid(row = 0, column = 0)
        tk.Label_register.bind('<Enter>', self.RFID_registered)
        

    def RFID_registered(self, event):
        self.update()
        try:
            self.id, self.text = self.reader.read()
            self.cursor.execute("SELECT * FROM residents_db WHERE RFID = %s", str(self.id))
            if (self.cursor.fetchone() is not None):
                messagebox.showerror("Notice!", "RFID card is already registered", parent = self)
            else:
                self.cursor.execute("SELECT * FROM residents_admin WHERE RFID = %s", str(self.id))
                if (self.cursor.fetchone() is not None):
                    messagebox.showerror("Notice!", "RFID card is already registered", parent = self)                   
                else:
                    messagebox.showinfo("Success", "Proceeding to step 3", parent = self)
                    self.register_fingerprint()
                    
        except:
            GPIO.cleanup()
            
    def register_fingerprint(self):
        self.rfid_frame.pack_forget()        
        self.img_register_finger = (Image.open("finger_register.png"))
        self.img_background_register_finger = ImageTk.PhotoImage(self.img_register_finger)
        
        self.finger_frame = tk.Frame(self)
        self.finger_frame.pack(fill = BOTH, expand = True)
        
        tk.Label_register = tk.Label(self.finger_frame, image = self.img_background_register_finger)
        tk.Label_register.grid(row = 0, column = 0)
        
        tk.Label_register.bind('<Enter>', self.registered_fingerprint)
    
    def registered_fingerprint(self,event):
        self.update()
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')
        
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))

        ## Gets some sensor information
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

        ## Tries to enroll new finger
        tk.Label(self, text = "Waiting for finger...", width = 20).place(x = 450, y = 680)
        self.update()

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

            ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

            ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0] 

        if ( positionNumber >= 0 ):
            messagebox.showinfo("Notice", "Fingerprint is already registered\n please try again", parent = self)
                
        tk.Label(self, text = "Remove finger...", width = 20).place(x = 450, y = 680)
        self.update()

        time.sleep(2)

        tk.Label(self, text = "Waiting for the same finger again...", width = 28).place(x = 410, y = 680)
        self.update()


        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

            ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            tk.Label(self.finger_frame, text = "Finger do not match",width = 30).place(x = 430, y = 680)
            tk.Label(self.finger_frame, text = "Scan your finger again").place(x = 436, y = 700)
            self.update()
            
            ## Creates a template
        else:
            f.createTemplate()
            characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
            ## Saves template at new position number
            positionNumber = f.storeTemplate()
            self.cursor.execute("INSERT INTO residents_db (FIRST_NAME, MIDDLE_NAME, LAST_NAME, SEX, BIRTH_DATE, CIVIL_STATUS, YEAR_OF_RESIDENCY, PLACE_OF_BIRTH, SECURITY_QUESTION, ANSWER, RFID, FINGER_TEMPLATE) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(self.get_first_name,
                                                                                                                                                                                                                                                                            self.get_middle_name,
                                                                                                                                                                                                                                                                            self.get_last_name,
                                                                                                                                                                                                                                                                            self.get_sex,
                                                                                                                                                                                                                                                                            self.get_birth_day,
                                                                                                                                                                                                                                                                            self.get_civil_status,
                                                                                                                                                                                                                                                                            self.get_year_of_residency,
                                                                                                                                                                                                                                                                            self.get_place_of_birth,
                                                                                                                                                                                                                                                                            self.get_security_question,
                                                                                                                                                                                                                                                                            self.get_answer,
                                                                                                                                                                                                                                                                            str(self.id),positionNumber))
            self.db.commit()
            messagebox.showinfo("Success", "Fingerprint successfully registered", parent = self)
            self.destroy()

    
    

if __name__ == "__main__":
    Registration_User().mainloop()


