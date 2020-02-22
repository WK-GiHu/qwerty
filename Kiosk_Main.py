from tkinter import *
import pymysql
import threading
from pyfingerprint.pyfingerprint import PyFingerprint
from PIL import Image, ImageTk
import time
from mfrc522 import SimpleMFRC522

class FingerprintThread(threading.Thread):
    def __init__(self, app, callback):
        super().__init__()
        self.app = app
        self.app.bind('<<GRANT_ACCESS>>', callback)
        self.start()

    def run(self):        
        self.db = pymysql.connect(host = "192.168.1.19",port = 3306, user = "root",passwd = "justin",db= "thesis_db")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
        
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        while True:
        
            print('Waiting for finger...')

            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass

                ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(0x01)

                ## Searchs template
            result = f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            self.cursor.execute("SELECT * FROM residents_admin WHERE FINGER_TEMPLATE = %s",positionNumber)
            sekf.result = self.cursor.fetchone()
            print (self.result)
            if self.result:
                self.app.event_generate('<<GRANT_ACCESS>>', when='tail')
            else:
                self.cursor.execute("SELECT * FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                self.result = self.cursor.fetchone()
                print (self.result)
                if self.result: 
                    self.app.event_generate('<<GRANT_ACCESS>>', when='tail')
                else:
                    messagebox.showerror("Warning!","Your fingerprint is not yet registered!")

    
class RFIDThread(threading.Thread):
    def __init__(self, app, callback):
        super().__init__()
        self.app = app
        self.app.bind('<<GRANT_ACCESS>>', callback)
        self.start()
    
    def run(self):
        self.db = pymysql.connect(host = "192.168.1.19",port = 3306, user = "root",passwd = "justin",db= "thesis_db")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        self.reader = SimpleMFRC522()
        self.id, text = self.reader.read()
        while True:
            self.cursor.execute("SELECT * FROM residents_admin WHERE RFID = %s",str(self.id))
            self.result = self.cursor.fetchone()
            print(self.result)
            if self.result: 
                self.app.event_generate('<<GRANT_ACCESS>>', when='tail')
            else:
                self.cursor.execute("SELECT * FROM residents_db WHERE RFID = %s", str(self.id))
                self.result = self.cursor.fetchone()
                print(self.result)
                if self.result: 
                    self.app.event_generate('<<GRANT_ACCESS>>', when='tail')
                else:
                    messagebox.showerror("Warning!","Your RFID card is not yet registered!")
                    
class Kiosk(tk.Tk):
    def __init__(self):
        super().__init__()
        VKeyboard(self)
        
        self.db = pymysql.connect(host = "192.168.1.19",port = 3306, user = "root",passwd = "justin",db= "thesis_db")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)

        #create table
        """self.QueryResident = "CREATE TABLE IF NOT EXISTS residents_db (ID INT(11) not null AUTO_INCREMENT, FIRST_NAME varchar(255) not null, MIDDLE_NAME varchar(255) not null, LAST_NAME varchar(255) not null,SEX varchar(255) not null, BIRTH_DATE date, CIVIL_STATUS varchar(255) not null, YEAR_OF_RESIDENCY int, PLACE_OF_BIRTH varchar(255) not null, SECURITY_QUESTION varchar(255), ANSWER varchar(255), RFID varchar(255) not null, FINGER_TEMPLATE varchar(255), PRIMARY KEY (ID))"
        self.cursor.execute(self.QueryResident)
        self.QueryResident_admin = "CREATE TABLE IF NOT EXISTS residents_admin (ID INT(11) not null AUTO_INCREMENT, FIRST_NAME varchar(255) not null, MIDDLE_NAME varchar(255) not null, LAST_NAME varchar(255) not null,SEX varchar(255) not null, BIRTH_DATE date, CIVIL_STATUS varchar(255) not null, YEAR_OF_RESIDENCY int, PLACE_OF_BIRTH varchar(255) not null, SECURITY_QUESTION varchar(255), ANSWER varchar(255), RFID varchar(255) not null,FINGER_TEMPLATE varchar(255), PRIMARY KEY(ID))"
        self.cursor.execute(self.QueryResident_admin)
        """
        self.title("Thesis")
        self.style = Style()
        self.style.theme_use('alt')
        self.style.map('TCombobox', fieldbackground=[('readonly','white')])
        
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        print(self.ws, self.hs)
        
        self.img = (Image.open("background_kiosk.png"))
        self.image = self.img.resize((self.ws,self.hs))
        self.img_background = ImageTk.PhotoImage(self.image)
        self.imglabel = Label(self, image = self.img_background).place(x=0,y=0)

        self.img2 = ImageTk.PhotoImage(Image.open("rosario_logo.png"))
        
        FingerprintThread(self, callback = self.on_grant_access)
        RFIDThread(self, callback = self.on_grant_access)
        GPIO.setwarnings(False)
        self.configure(bg="white")    
        self.geometry("{}x{}".format(self.ws, self.hs))
        self.T_printer = Usb(0x0fe6, 0x811e, 98, 0x82, 0x02)
       
    def on_grant_access(self, *event):
        print('Kiosk.on_grant_access()')
        
        self.deiconify()

    
    #if there's RFID on db this security_question method will be called        
    def security_question(self):
        messagebox.showinfo("Success", "Proceed to security question")

        self.sqa_frame = Frame(self.master_login)
        self.sqa_frame.pack(fill = "both", expand = 1)
        self.img_sq = (Image.open("background_kiosk.png"))
        self.image_sq = self.img_sq.resize((self.ws,self.hs))
        self.img_background_sq = ImageTk.PhotoImage(self.image_sq)
        
        
        self.or_label = Label(self.sqa_frame, image = self.img_background_sq)
        self.or_label.pack(fill= "both", expand = 1)
        
        answer = StringVar()
        self.input = 0
        self.label_question = Label(self.sqa_frame, text = self.get_sq1, bg = "white")
        self.label_question.place(x = 780, y = 250)
        
                    
        self.label_head_sq = Label(self.sqa_frame, text = "Security_Question",bg = "white", font = ("Times New Roman", 25))
        self.label_head_sq.pack()

        self.entry_answer = Entry(self.sqa_frame, textvariable = answer)
        self.entry_answer.place(x = 780, y = 300)
        self.label_answer = Label(self.sqa_frame, text = "Answer :", bg = "white")
        self.label_answer.place(x = 780, y = 275)
        self.submit_button_sq = Button(self.sqa_frame, text = "Submit", bg = "white", command = lambda: self.submit_answer(answer.get()))
        self.submit_button_sq.place(x = 780, y = 325)
        self.back_button_sq = Button(self.sqa_frame, text = "Back", bg = "white",command = self.master_login.destroy)
        self.back_button_sq.place(x = 890, y = 325)
        
    def submit_answer(self, answer):
        answerLimit = 2
        if self.input < answerLimit:
            self.cursor.execute("SELECT * FROM residents_admin WHERE ANSWER = %s AND RFID = %s",(answer, str(self.id)))
            if self.cursor.fetchone() is not None:
                self.master_login.destroy()
                self.choose_admin()
            else:
                self.cursor.execute("SELECT * FROM residents_db WHERE ANSWER = %s AND RFID = %s",(answer, str(self.id)))
                if self.cursor.fetchone() is not None:
                    self.master_login.destroy()
                    self.choose_user()
                else:
                    messagebox.showerror("Warning!","Wrong Security Question or Answer", parent= master_login)
                    self.input+=1
        else:
            messagebox.showerror("Warning!","Wrong input 3 times", parent= master_login)
            self.master_login.destroy()
    # if fingerprint exists in residents_admin database this page will appear       
    
    def choose_admin(self):
        messagebox.showinfo("Success", "Welcome!")
        self.get_Firstn1 = str(self.get_Firstn[0])
        self.get_Middlen1 = str(self.get_Middlen[0])
        self.get_Lastn1 = str(self.get_Lastn[0])
        self.get_full_name = (self.get_Lastn1 + ","+" "+ self.get_Firstn1 + " " + self. get_Middlen1)
        
        self.master_choose_admin = Toplevel()
        self.master_choose_admin.attributes("-fullscreen", True)
        
        self.main_frame_admin = Frame(self.master_choose_admin)
        self.main_frame_admin.pack(fill = "both", expand = 1)
        self.img_choose_form_admin = (Image.open("background_kiosk.png"))
        
        self.image_choose_form_admin = self.img_choose_form_admin.resize((self.ws,self.hs))
        self.img_background_choose_form_admin = ImageTk.PhotoImage(self.image_choose_form_admin)
        self.imglabel_choose_form_admin = Label(self.main_frame_admin, image = self.img_background_choose_form_admin)
        self.imglabel_choose_form_admin.place(x=0,y=0)
        self.img_choose_logo = (Image.open("rosario_logo.png"))
        self.img_background_choose_logo_admin = ImageTk.PhotoImage(self.img_choose_logo)
        self.imglabel_choose_logo_admin = Label(self.main_frame_admin, image = self.img_background_choose_logo_admin)
        self.imglabel_choose_logo_admin.place(x=1300,y=70)
        
        self.extra_spaces1 = Label(self.main_frame_admin, text = "\t\t\t\t",bg = "white")
        self.extra_spaces1.grid(row = 0, column = 0)
        
        self.extra_spaces2 = Label(self.main_frame_admin, text = "\t\t\t",bg = "white")
        self.extra_spaces2.grid(row = 0, column = 1)

        self.extra_spaces3 = Label(self.main_frame_admin, text = "\t\t\t",bg = "white")
        self.extra_spaces3.grid(row = 0, column = 2)
        
        self.extra_spaces3 = Label(self.main_frame_admin, text = "\t\t\t",bg = "white")
        self.extra_spaces3.grid(row = 0, column = 3)
        
        self.extra_spaces4 = Label(self.main_frame_admin, text = "\t\t\t",bg = "white")
        self.extra_spaces4.grid(row = 0, column = 4)
        
        self.extra_spaces5 = Label(self.main_frame_admin, text = "\t\t\t",bg = "white")
        self.extra_spaces5.grid(row = 0, column = 5)
        
        self.extra_spaces6 = Label(self.main_frame_admin, text = "\t\t\t",bg = "white")
        self.extra_spaces6.grid(row = 0, column = 6)
        
        self.extra_spaces7 = Label(self.main_frame_admin, text = "\t\t\t",bg = "white")
        self.extra_spaces7.grid(row = 0, column = 7)
        
        self.extra_spaces8 = Label(self.main_frame_admin, text = "\t\t\t",bg = "white")
        self.extra_spaces8.grid(row = 0, column = 8)
        
        self.label_name = Label(self.main_frame_admin, text = "Welcome, " + self.get_full_name, bg = "white", font = ("Times New Roman", 20))
        self.label_name.grid(row = 1, column = 0)
        
        self.label_head_admin = Label(self.main_frame_admin, text = "Admin Main Page",bg = "white", font = ("Times New Roman", 25))
        self.label_head_admin.grid(row = 1, column = 3, columnspan = 2, sticky= "nesw")

        self.choose_form_button = Button(self.main_frame_admin, text = "Choose/Print Forms", width = 30, height = 5,bg = "white", command = self.choose_form_admin)
        self.choose_form_button.grid(row = 4, column = 3, padx = 20, pady = 5, columnspan = 2)
        
        self.back_login = Button(self.main_frame_admin, text = "Back", width = 20, height = 3,bg = "white", command = self.master_choose_admin.destroy)
        self.back_login.grid(row = 5, column = 3, padx = 20, pady = 15, columnspan = 2)
    
        self.register_admin_button = Button(self.main_frame_admin, text = "Register Admin", width = 30, height = 5, bg = "white", command = self.register_admin)
        self.register_admin_button.grid(row = 2, column = 3, pady = 5, )
        
        self.register_user_button = Button(self.main_frame_admin, text = "Register User", width = 30, height = 5, bg = "white", command = self.register)
        self.register_user_button.grid(row = 2, column = 4)
        
        self.update_admin_button = Button(self.main_frame_admin, text = "Update Admin", width = 30, height = 5, bg = "white", command = self.Update_Admins)
        self.update_admin_button.grid(row = 3, column = 3)
        
        self.update_user_button = Button(self.main_frame_admin, text = "Update User", width = 30, height = 5, bg = "white", command = self.Update_Residents)
        self.update_user_button.grid(row = 3, column = 4)

    def choose_form_admin(self):
        self.main_frame_admin.pack_forget()
        self.choose_form_frame = Frame(self.master_choose_admin)
        self.choose_form_frame.pack(expand = 1, fill = "both")
        
        self.img_choose_form = (Image.open("background_kiosk.png"))
        self.image_choose_form = self.img_choose_form.resize((self.ws,self.hs))
        self.img_background_choose_form = ImageTk.PhotoImage(self.image_choose_form)
        self.imglabel_choose_form = Label(self.choose_form_frame, image = self.img_background_choose_form).place(x=0,y=0)
        self.img_choose_logo = (Image.open("rosario_logo.png"))
        self.img_background_choose_logo = ImageTk.PhotoImage(self.img_choose_logo)
        self.imglabel_choose_logo = Label(self.choose_form_frame, image = self.img_background_choose_logo).place(x=1300,y=70)
       
        extra_spaces1 = Label(self.choose_form_frame, text = "\t\t\t\t",bg = "white")
        extra_spaces1.grid(row = 0, column = 0)
        
        extra_spaces2 = Label(self.choose_form_frame, text = "\t\t\t",bg = "white")
        extra_spaces2.grid(row = 0, column = 1)

        extra_spaces3 = Label(self.choose_form_frame, text = "\t\t\t",bg = "white")
        extra_spaces3.grid(row = 0, column = 2)
        
        extra_spaces3 = Label(self.choose_form_frame, text = "\t\t\t",bg = "white")
        extra_spaces3.grid(row = 0, column = 3)
        
        extra_spaces4 = Label(self.choose_form_frame, text = "\t\t\t",bg = "white")
        extra_spaces4.grid(row = 0, column = 4)
        
        extra_spaces5 = Label(self.choose_form_frame, text = "\t\t\t",bg = "white")
        extra_spaces5.grid(row = 0, column = 5)
        
        extra_spaces6 = Label(self.choose_form_frame, text = "\t\t\t",bg = "white")
        extra_spaces6.grid(row = 0, column = 6)
        
        extra_spaces7 = Label(self.choose_form_frame, text = "\t\t\t",bg = "white")
        extra_spaces7.grid(row = 0, column = 7)
        
        extra_spaces8 = Label(self.choose_form_frame, text = "\t\t\t",bg = "white")
        extra_spaces8.grid(row = 0, column = 8)
        
        
        self.label_name_choose = Label(self.choose_form_frame, text = "Welcome, " + self.get_full_name, bg = "white", font = ("Times New Roman", 20))
        self.label_name_choose.grid(row = 1, column = 0)
        
        self.label_head_choose_form_admin = Label(self.choose_form_frame, text = "Available Printable Forms",bg = "white", font = ("Times New Roman", 25))
        self.label_head_choose_form_admin.grid(row = 1, column = 3, columnspan = 2, sticky= "nesw")
       
        self.brgy_certification = Button(self.choose_form_frame, text = "Barangay Certification", width = 30, height = 5, bg = "white",command = self.brgy_purpose)
        self.brgy_certification.grid(row = 2 , column = 3, pady = 15)
                
        self.certificate_of_indigency_button = Button(self.choose_form_frame, text = "Certificate of Indigency", width = 30, height = 5, bg = "white",command = self.print_ar_cert_of_indigency)
        self.certificate_of_indigency_button.grid(row = 2 , column = 4, pady = 15, padx = 5)
        
        self.certificate_of_residency_button = Button(self.choose_form_frame, text = "Certificate of Residency", width = 30, height = 5, bg = "white",command = self.brgy_purpose_residency)
        self.certificate_of_residency_button.grid(row = 3 , column = 3, padx = 5)
        
        self.certificate_of__residency_student_button = Button(self.choose_form_frame, text = "Certificate of Residency for Student", width = 30, height = 5,bg = "white", command = self.brgy_purpose_residency_student)
        self.certificate_of__residency_student_button.grid(row = 3 , column = 4, pady = 15)
        
        self.back_button2 = Button(self.choose_form_frame, text = "Back", width = 20, height = 3,bg = "white", command = self.back)
        self.back_button2.grid(row = 6 , column = 3, columnspan = 2)
    
    def back(self):
        self.choose_form_frame.pack_forget()
        self.main_frame_admin.pack(fill="both", expand = 1)
        

    #if fingerprint exists in residents_db database this will appear 
#================================choose forms for residents==============================#
    def choose_user(self):
        messagebox.showinfo("Success", "Welcome!")

        self.master_choose_form_user = Toplevel()
        self.master_choose_form_user.attributes("-fullscreen", True)
        
        self.ws = self.winfo_screenwidth()
        
        self.hs = self.winfo_screenheight()
        
        # I erased the fetchone() so these variables must change        
        self.get_Firstn1 = str(self.get_Firstn[0])
        self.get_Middlen1 = str(self.get_Middlen[0])
        self.get_Lastn1 = str(self.get_Lastn[0])
        self.get_full_name = (self.get_Lastn1 + ","+" "+ self.get_Firstn1 + " " + self. get_Middlen1)
        
        self.img_choose_form_user = (Image.open("background_kiosk.png"))
        self.image_choose_form_user = self.img_choose_form_user.resize((self.ws,self.hs))
        self.img_background_choose_form_user = ImageTk.PhotoImage(self.image_choose_form_user)
        self.imglabel_choose_form_user = Label(self.master_choose_form_user, image = self.img_background_choose_form_user).place(x=0,y=0)
        self.img_choose_logo_user = (Image.open("rosario_logo.png"))
        self.img_background_choose_logo_user = ImageTk.PhotoImage(self.img_choose_logo_user)
        self.imglabel_choose_logo_user = Label(self.master_choose_form_user, image = self.img_background_choose_logo_user).place(x=1300,y=70)
        
        
        extra_spaces1 = Label(self.master_choose_form_user, text = "\t\t\t\t",bg = "white")
        extra_spaces1.grid(row = 0, column = 0)
        
        extra_spaces2 = Label(self.master_choose_form_user, text = "\t\t\t",bg = "white")
        extra_spaces2.grid(row = 0, column = 1)

        extra_spaces3 = Label(self.master_choose_form_user, text = "\t\t\t",bg = "white")
        extra_spaces3.grid(row = 0, column = 2)
        
        extra_spaces3 = Label(self.master_choose_form_user, text = "\t\t\t",bg = "white")
        extra_spaces3.grid(row = 0, column = 3)
        
        extra_spaces4 = Label(self.master_choose_form_user, text = "\t\t\t",bg = "white")
        extra_spaces4.grid(row = 0, column = 4)
        
        extra_spaces5 = Label(self.master_choose_form_user, text = "\t\t\t",bg = "white")
        extra_spaces5.grid(row = 0, column = 5)
        
        extra_spaces6 = Label(self.master_choose_form_user, text = "\t\t\t",bg = "white")
        extra_spaces6.grid(row = 0, column = 6)
        
        extra_spaces7 = Label(self.master_choose_form_user, text = "\t\t\t",bg = "white")
        extra_spaces7.grid(row = 0, column = 7)
        
        extra_spaces8 = Label(self.master_choose_form_user, text = "\t\t\t",bg = "white")
        extra_spaces8.grid(row = 0, column = 8)
        
        self.label_name_user = Label(self.master_choose_form_user, text = "Welcome, " + self.get_full_name, bg = "white", font = ("Times New Roman", 20))
        self.label_name_user.grid(row = 1, column = 0)
        
        self.label_head_choose_form_user = Label(self.master_choose_form_user, text = "Available Printable Forms",bg = "white", font = ("Times New Roman", 25))
        self.label_head_choose_form_user.grid(row = 1, column = 3, columnspan = 2, sticky= "nesw")

        self.brgy_certification_user = Button(self.master_choose_form_user, text = "Barangay Certification", width = 30, height = 5, bg = "white",command = self.brgy_purpose)
        self.brgy_certification_user.grid(row = 2, column = 3, pady = 15, padx = 5)
        
        self.certificate_of_indigency_button_user = Button(self.master_choose_form_user, text = "Certificate of Indigency", width = 30, height = 5, bg = "white",command = self.print_ar_cert_of_indigency)
        self.certificate_of_indigency_button_user.grid(row = 2 , column = 4, pady = 15, padx = 5)
        
        self.certificate_of_residency_button_user = Button(self.master_choose_form_user, text = "Certificate of Residency", width = 30, height = 5, bg = "white",command = self.brgy_purpose_residency)
        self.certificate_of_residency_button_user.grid(row = 3 , column = 3, padx = 5)
        
        self.certificate_of_residency_student_button_user = Button(self.master_choose_form_user, text = "Certificate of Residency for Student", width = 30, height = 5,bg = "white", command = self.brgy_purpose_residency_student)
        self.certificate_of_residency_student_button_user.grid(row = 3 , column = 4, pady = 15)
        
        self.back_login_user = Button(self.master_choose_form_user, text = "Back to LOGIN", width = 20, height = 3, bg = "white", command = self.master_choose_form_user.destroy)
        self.back_login_user.grid(row = 6, column = 3,columnspan =2, pady = 15, padx = 5)
