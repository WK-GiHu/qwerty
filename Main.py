from tkinter import *
from tkinter import ttk
from tkinter import font  as tkfont
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
import pymysql
import cv2 
import io

class Admin_System(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.db = pymysql.connect(host = "localhost", user = "root",passwd = "",db= "thesis_main")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        self.QueryResident = "CREATE TABLE IF NOT EXISTS residents_admin (ID INT(11) not null AUTO_INCREMENT, LAST_NAME varchar(255) not null, FIRST_NAME varchar(255) not null, MIDDLE_NAME varchar(255) not null, SEX varchar(255) not null, BIRTH_DATE date, CIVIL_STATUS varchar(255) not null, YEAR_OF_RESIDENCY int, ADDRESS varchar(255) not null, PLACE_OF_BIRTH varchar(255) not null, IMAGE BLOB, USERNAME varchar(255) not null, PASSWORD varchar(255) not null, PRIMARY KEY (ID))"
        self.cursor.execute(self.QueryResident)
        self.QueryResident_admin = "CREATE TABLE IF NOT EXISTS residents_db (ID INT(11) not null AUTO_INCREMENT, LAST_NAME varchar(255) not null, FIRST_NAME varchar(255) not null, MIDDLE_NAME varchar(255) not null, SEX varchar(255) not null, BIRTH_DATE date, CIVIL_STATUS varchar(255) not null, YEAR_OF_RESIDENCY int, ADDRESS varchar(255) not null, PLACE_OF_BIRTH varchar(255) not null, SECURITY_QUESTION varchar(255), ANSWER varchar(255), IMAGE BLOB, RFID varchar(255) not null, FINGER_TEMPLATE varchar(255) not null, PRIMARY KEY (ID))"
        self.cursor.execute(self.QueryResident_admin)
        self.shared_data = {"username": StringVar(),
                            "password": StringVar()
                           }
        
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.frames = {}
        for F in (Login_Page, Main_Page, User_Registration, Admin_Registration, User_Update, Admin_Update):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login_Page")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    

class Login_Page(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.db = pymysql.connect(host = "localhost", user = "root",passwd = "",db= "thesis_main")
        self.cursor = self.db.cursor()

        label = Label(self, text="Login", font=controller.title_font)
        label.grid(row = 0, column = 0, columnspan = 2, sticky = "nesw")

        label_username = Label(self, text = "Username: ", bg = "white")
        label_username.grid(row = 1, column = 0)
        label_password = Label(self, text = "Password: ", bg = "white")
        label_password.grid(row = 2, column = 0)
        
        self.entry_username = Entry(self, textvariable = self.controller.shared_data["username"], bg = "white")
        self.entry_username.grid(row = 1, column = 1)
        self.entry_password = Entry(self, textvariable = self.controller.shared_data["password"], show = "*",bg = "white")
        self.entry_password.grid(row = 2, column = 1)
        button_submit = Button(self, text="Login",
                            command=lambda: self.submit_login(self.controller.shared_data["username"].get(), self.controller.shared_data["password"].get()))
        button_submit.grid(row = 3, column = 0, columnspan = 2)
        
    def submit_login(self, username, password):
        print (username)
        print(password)
        self.cursor.execute("SELECT * FROM residents_admin WHERE USERNAME = %s AND PASSWORD = %s", (username, password))
        if self.cursor.fetchone() is not None:
            messagebox.showinfo("Success", "Welcome")
            self.controller.show_frame("Main_Page")
        elif username =="" or password =="":
            messagebox.showerror("Notice!", "Please input password and username")
        else:
            messagebox.showerror("Notice!", "username or password is incorrect")
            
       
        
class Main_Page(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.db = pymysql.connect(host = "localhost", user = "root",passwd = "",db= "thesis_main")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
    
        label = Label(self, text="Main Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = Button(self, text="register user",
                           command=lambda: controller.show_frame("User_Registration"))
        button1.pack()
        button2= Button(self, text="register_admin",
                           command=lambda: controller.show_frame("Admin_Registration"))
        button2.pack()
        button3= Button(self, text="update_user",
                           command=lambda: controller.show_frame("User_Update"))
        button3.pack()
        button4= Button(self, text="update_admin",
                           command=lambda: controller.show_frame("Admin_Update"))
        button4.pack()
        button5 = Button (self, text = "show profile", command = self.profile)
        button5.pack()
      
    def profile(self): 
        self.cursor.execute("SELECT IMAGE FROM residents_admin WHERE USERNAME = %s AND PASSWORD = %s",(self.controller.shared_data["username"].get(), self.controller.shared_data["password"].get()))
        self.picture=self.cursor.fetchall()
        byte_image = io.BytesIO(self.picture[0][0])
        print(byte_image)
        img = Image.open(byte_image)
        img.show()
        image = img.resize((250,250))
        phimg = ImageTk.PhotoImage(image)

        panel = Label(self, image = phimg)
        panel.place(x = 50, y = 50)
      

class User_Registration(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.db = pymysql.connect(host = "localhost", user = "root",passwd = "",db= "thesis_main")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        
        first_name = StringVar()
        middle_name = StringVar()
        last_name = StringVar()
        sex = StringVar()
        birth_year= StringVar()
        birth_month = StringVar()
        birth_day = StringVar()
        civil_status = StringVar()
        year_of_residency = StringVar()
        address = StringVar()
        place_of_birth = StringVar()
        security_question = StringVar()
        answer = StringVar()

        self.label_head = Label(self, text = "Fill up all informations below",bg = "white", font = ("Times New Roman", 25))
        self.label_head.grid(row = 0, column = 1, columnspan = 2)

        self.space_label= Label (self, text = "\t\t", bg = "white")
        self.space_label.grid(row = 1, column = 0)

        self.label_first_name = Label(self, text = "First Name\t:", relief = "ridge",bg = "white")
        self.label_first_name.grid(row = 1, column = 1, padx = 5, pady = 15)
        self.entry_first_name = Entry(self, textvariable = first_name,bg = "white", width = "45")
        self.entry_first_name.grid(row = 1, column = 2, pady = 15)        

        self.label_middle_name = Label(self, text = "Middle Name\t:",bg = "white", relief = "ridge")
        self.label_middle_name.grid(row = 2, column = 1)
        self.entry_middle_name = Entry(self, textvariable = middle_name,bg = "white", width = "45")
        self.entry_middle_name.grid(row = 2, column = 2, pady = 15)
        
        self.label_last_name = Label(self, text = "Last Name\t:",bg = "white", relief = "ridge")
        self.label_last_name.grid(row = 3, column = 1)
        self.entry_last_name = Entry(self, textvariable = last_name,bg = "white", width = "45")
        self.entry_last_name.grid(row = 3, column = 2, pady = 15)
        
        self.label_sex = Label(self, text = "Sex\t\t:",bg = "white", relief = "ridge")
        self.label_sex.grid(row = 4, column = 1)

        self.option_list_sex = ["Male", "Female"]
        self.option = ttk.Combobox(self, state = "readonly", textvariable = sex, width = "43", values = self.option_list_sex)
        self.option.grid(row = 4, column = 2, pady = 15)
        
        self.label_birth_day = Label(self, text = "Birth Day\t",bg = "white", relief = "ridge")
        self.label_birth_day.grid(row = 5, column = 1)

        self.date_frame = Frame(self)
        self.date_frame.grid(row = 5, column = 2)
        year_now = datetime.date.today().year
        year_choices = list(range(year_now-50, year_now+1))
        self.option_birth_yr = ttk.Combobox(self.date_frame, state = "readonly", textvariable = birth_year, width= "6", values = year_choices)
        self.option_birth_yr.grid(row = 0, column = 0, padx = 5)

        month_choices = ['1','2','3','4','5','6','7','8','9','10','11','12']
        
        self.option_birth_mm = ttk.Combobox(self.date_frame, state = "readonly", textvariable = birth_month, width = "3", values = month_choices)
        self.option_birth_mm.grid(row = 0, column =1)

        day_choices = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        
        self.option_birth_mm = ttk.Combobox(self.date_frame, state = "readonly", textvariable = birth_day, width = "3", values = day_choices)
        self.option_birth_mm.grid(row = 0, column =2, padx = 5)
        
        self.label_civil_status = Label(self, text = "Civil Status\t:",bg = "white", relief = "ridge")
        self.label_civil_status.grid(row = 6, column = 1)

        self.option_list_cs = ["Single", "Married", "Widow", "Separated", "Live-in", "Unkown"]
        self.option_cs = ttk.Combobox(self, state="readonly", textvariable = civil_status, width = "43", values = self.option_list_cs)
        self.option_cs.grid(row = 6, column = 2, pady = 15)

        self.label_year_of_residency = Label(self, text = "Year of Residency\t:",bg = "white", relief = "ridge")
        self.label_year_of_residency.grid(row = 7, column = 1, pady = 15)

        self.option_year_of_residency = ttk.Combobox(self, state = "readonly", textvariable = year_of_residency, width= "6", values = year_choices)
        self.option_year_of_residency.grid(row = 7, column = 2)

        self.label_address = Label(self, text = "Address\t:",bg = "white", relief = "ridge")
        self.label_address.grid(row = 8, column = 1, pady = 15)
        self.entry_address = Entry(self, textvariable = address,bg = "white", width = "45")
        self.entry_address.grid(row = 8, column = 2)

        self.label_place_of_birth = Label(self, text = "Place of Birth\t:",bg = "white", relief = "ridge")
        self.label_place_of_birth.grid(row = 9, column = 1)
        self.entry_place_of_birth = Entry(self, textvariable = place_of_birth,bg = "white", width = "45")
        self.entry_place_of_birth.grid(row = 9, column = 2, pady = 15)
        
        self.label_question = Label(self, text = "Security Question\t:",bg = "white", relief = "ridge")
        self.label_question.grid(row= 10, column = 1)
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

        self.question_list= ttk.Combobox(self, state = "readonly", textvariable = security_question, values = self.question_list)
        self.question_list.grid(row = 10, column = 2, pady = 15)

        self.answer_label = Label(self, text = "Answer\t\t:", bg ="white", relief = "ridge")
        self.answer_label.grid(row = 11, column = 1)
        self.answer_entry = Entry(self, textvariable = answer, width = "45")
        self.answer_entry.grid(row = 11, column = 2, pady = 15)
        
        self.button_submit = Button(self, text = "Proceed to Step 2",bg = "white", command = lambda: self.registered(first_name.get(),
                                                                                                                     middle_name.get(),
                                                                                                                     last_name.get(), sex.get(),
                                                                                                                     birth_year.get(),
                                                                                                                     birth_month.get(),
                                                                                                                     birth_day.get(),
                                                                                                                     civil_status.get(),
                                                                                                                     year_of_residency.get(),
                                                                                                                     address.get(),
                                                                                                                     place_of_birth.get(),
                                                                                                                     security_question.get(), answer.get()))
        self.button_submit.grid(row = 12, column = 2, pady = 5)

        self.back_button = Button(self, text = "Back",bg = "white", command = lambda: controller.show_frame("Main_Page"))
        self.back_button.grid(row = 13, column = 2)

        blank_space = Label(self, text = "\t\t\t\t")
        blank_space.grid(row = 0, column =3)
        self.take_photo_button = Button(self, text = "Take a Photo", bg ="white", command = self.take_photo)
        self.take_photo_button.grid(row = 3, column = 4)
        
    def take_photo(self):
        key = cv2. waitKey(1)
        webcam = cv2.VideoCapture(0)
        while True:
            try:
                check, frame = webcam.read()
                print(check) #prints true as long as the webcam is running
                print(frame) #prints matrix values of each framecd
                cv2.imshow("Capturing", frame)
                key = cv2.waitKey(1)
                if key == ord('s'): 
                    cv2.imwrite(filename='saved_img.jpg', img=frame)
                    webcam.release()
                    img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
                    img_new = cv2.imshow("Captured Image", img_new)
                    cv2.waitKey(5)
                    cv2.destroyAllWindows()
                    self.picture_label = Label(self, text = "Photo Taken")
                    self.picture_label.grid(row =3, column = 3)
                    self.upload_photo_button.grid_forget()
                    break
                elif key == ord('q'):
                    print("Turning off camera.")
                    webcam.release()
                    print("Camera off.")
                    print("Program ended.")
                    cv2.destroyAllWindows()
                    break
            except(KeyboardInterrupt):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break


    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def registered(self, first_name, middle_name, last_name, sex, birth_year, birth_month, birth_day, civil_status, year_of_residency, address, place_of_birth, security_question, answer):
        print (first_name)
        print (middle_name)
        print (last_name)
        print (sex)
        print (birth_year)
        print (birth_month)
        print (birth_day)
        print (civil_status)
        print (year_of_residency)
        print (address)
        print (place_of_birth)
        print (security_question)
        print (answer)
        try :
            if self.picture_label.cget("text") == "":
                messagebox.showerror("Notice!", "Please take a picture")
            else:
                    
                photo = 'saved_img.jpg'
                user_picture = self.convertToBinaryData(photo)

                #birth_day
                _year = int(birth_year)
                _month = int(birth_month)
                _day = int(birth_day)

                birth_day = datetime.date(_year, _month, _day)
                print (birth_day)
                if (first_name =="" or middle_name == "" or last_name == "" or sex =="" or birth_day == "" or civil_status =="" or
                    year_of_residency == "" or address =="" or place_of_birth == "" or security_question == "" or answer == ""):
                    messagebox.showerror("Error!","Please complete the required field")
                else:
                    self.cursor.execute ("INSERT INTO residents_db (LAST_NAME, FIRST_NAME, MIDDLE_NAME, SEX, BIRTH_DATE, CIVIL_STATUS, YEAR_OF_RESIDENCY, ADDRESS, PLACE_OF_BIRTH, SECURITY_QUESTION, ANSWER, IMAGE) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(last_name,middle_name,
                                                                                                                                                                                                                                                                   first_name,
                                                                                                                                                                                                                                                                   sex,
                                                                                                                                                                                                                                                                   birth_day,
                                                                                                                                                                                                                                                                   civil_status,
                                                                                                                                                                                                                                                                   year_of_residency,
                                                                                                                                                                                                                                                                   address,
                                                                                                                                                                                                                                                                   place_of_birth,
                                                                                                                                                                                                                                                                   security_question,
                                                                                                                                                                                                                                                                   answer, user_picture))
                    self.db.commit()
                    messagebox.showinfo("Success", "Registration Complete")
        except Exception as e:
            messagebox.showerror("Notice!", "Please take a picture")
            
class Admin_Registration(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.db = pymysql.connect(host = "localhost", user = "root",passwd = "",db= "thesis_main")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        
        first_name = StringVar()
        middle_name = StringVar()
        last_name = StringVar()
        sex = StringVar()
        birth_year= StringVar()
        birth_month = StringVar()
        birth_day = StringVar()
        civil_status = StringVar()
        year_of_residency = StringVar()
        address = StringVar()
        place_of_birth = StringVar()
        username = StringVar()
        password= StringVar()
        self.confirm_password = StringVar()
        

        self.label_head = Label(self, text = "Fill up all informations below",bg = "white", font = ("Times New Roman", 25))
        self.label_head.grid(row = 0, column = 1, columnspan = 2)

        self.space_label= Label (self, text = "\t\t", bg = "white")
        self.space_label.grid(row = 1, column = 0)

        self.label_first_name = Label(self, text = "First Name\t:", relief = "ridge",bg = "white")
        self.label_first_name.grid(row = 1, column = 1, padx = 5, pady = 15)
        self.entry_first_name = Entry(self, textvariable = first_name,bg = "white", width = "45")
        self.entry_first_name.grid(row = 1, column = 2, pady = 15)        

        self.label_middle_name = Label(self, text = "Middle Name\t:",bg = "white", relief = "ridge")
        self.label_middle_name.grid(row = 2, column = 1)
        self.entry_middle_name = Entry(self, textvariable = middle_name,bg = "white", width = "45")
        self.entry_middle_name.grid(row = 2, column = 2, pady = 15)
        
        self.label_last_name = Label(self, text = "Last Name\t:",bg = "white", relief = "ridge")
        self.label_last_name.grid(row = 3, column = 1)
        self.entry_last_name = Entry(self, textvariable = last_name,bg = "white", width = "45")
        self.entry_last_name.grid(row = 3, column = 2, pady = 15)
        
        self.label_sex = Label(self, text = "Sex\t\t:",bg = "white", relief = "ridge")
        self.label_sex.grid(row = 4, column = 1)

        self.option_list_sex = ["Male", "Female"]
        self.option = ttk.Combobox(self, state = "readonly", textvariable = sex, width = "43", values = self.option_list_sex)
        self.option.grid(row = 4, column = 2, pady = 15)
        
        self.label_birth_day = Label(self, text = "Birth Day\t",bg = "white", relief = "ridge")
        self.label_birth_day.grid(row = 5, column = 1)

        self.date_frame = Frame(self)
        self.date_frame.grid(row = 5, column = 2)
        year_now = datetime.date.today().year
        year_choices = list(range(year_now-50, year_now+1))
        self.option_birth_yr = ttk.Combobox(self.date_frame, state = "readonly", textvariable = birth_year, width= "6", values = year_choices)
        self.option_birth_yr.grid(row = 0, column = 0, padx = 5)

        month_choices = ['1','2','3','4','5','6','7','8','9','10','11','12']
        
        self.option_birth_mm = ttk.Combobox(self.date_frame, state = "readonly", textvariable = birth_month, width = "3", values = month_choices)
        self.option_birth_mm.grid(row = 0, column =1)

        day_choices = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        
        self.option_birth_mm = ttk.Combobox(self.date_frame, state = "readonly", textvariable = birth_day, width = "3", values = day_choices)
        self.option_birth_mm.grid(row = 0, column =2, padx = 5)
        
        self.label_civil_status = Label(self, text = "Civil Status\t:",bg = "white", relief = "ridge")
        self.label_civil_status.grid(row = 6, column = 1)

        self.option_list_cs = ["Single", "Married", "Widow", "Separated", "Live-in", "Unkown"]
        self.option_cs = ttk.Combobox(self, state="readonly", textvariable = civil_status, width = "43", values = self.option_list_cs)
        self.option_cs.grid(row = 6, column = 2, pady = 15)

        self.label_year_of_residency = Label(self, text = "Year of Residency\t:",bg = "white", relief = "ridge")
        self.label_year_of_residency.grid(row = 7, column = 1, pady = 15)

        self.option_year_of_residency = ttk.Combobox(self, state = "readonly", textvariable = year_of_residency, width= "6", values = year_choices)
        self.option_year_of_residency.grid(row = 7, column = 2)

        self.label_address = Label(self, text = "Address\t:",bg = "white", relief = "ridge")
        self.label_address.grid(row = 8, column = 1, pady = 15)
        self.entry_address = Entry(self, textvariable = address,bg = "white", width = "45")
        self.entry_address.grid(row = 8, column = 2)

        self.label_address = Label(self, text = "Place of Birth \t:",bg = "white", relief = "ridge")
        self.label_address.grid(row = 9, column = 1, pady = 15)
        self.entry_address = Entry(self, textvariable = place_of_birth,bg = "white", width = "45")
        self.entry_address.grid(row = 9, column = 2)

        self.label_place_of_birth = Label(self, text = "Username\t:",bg = "white", relief = "ridge")
        self.label_place_of_birth.grid(row = 10, column = 1)
        self.entry_place_of_birth = Entry(self, textvariable = username,bg = "white", width = "45")
        self.entry_place_of_birth.grid(row = 10, column = 2, pady = 15)
        
        self.label_place_of_birth = Label(self, text = "Password\t:",bg = "white", relief = "ridge")
        self.label_place_of_birth.grid(row = 11, column = 1)
        self.entry_place_of_birth = Entry(self, textvariable = password,show = "*", bg = "white", width = "45")
        self.entry_place_of_birth.grid(row = 11, column = 2, pady = 15)
        
        self.label_place_of_birth = Label(self, text = "Confirm Password\t:",bg = "white", relief = "ridge")
        self.label_place_of_birth.grid(row = 12, column = 1)
        self.entry_place_of_birth = Entry(self, textvariable = self.confirm_password,show = "*",bg = "white", width = "45")
        self.entry_place_of_birth.grid(row = 12, column = 2, pady = 15)
        
        self.button_submit = Button(self, text = "Proceed to Step 2",bg = "white", command = lambda: self.registered(first_name.get(),
                                                                                                                     middle_name.get(),
                                                                                                                     last_name.get(), sex.get(),
                                                                                                                     birth_year.get(),
                                                                                                                     birth_month.get(),
                                                                                                                     birth_day.get(),
                                                                                                                     civil_status.get(),
                                                                                                                     year_of_residency.get(),
                                                                                                                     address.get(),
                                                                                                                     place_of_birth.get(),
                                                                                                                     username.get(), password.get()))
        self.button_submit.grid(row = 13, column = 2, pady = 5)

        self.back_button = Button(self, text = "Back",bg = "white", command = lambda: controller.show_frame("Main_Page"))
        self.back_button.grid(row = 14, column = 2)

        blank_space = Label(self, text = "\t\t\t\t")
        blank_space.grid(row = 0, column =3)
        self.take_photo_button = Button(self, text = "Take a Photo", bg ="white", command = self.take_photo_admin)
        self.take_photo_button.grid(row = 3, column = 4)
        
    def take_photo_admin(self):
        key = cv2. waitKey(1)
        webcam = cv2.VideoCapture(0)
        while True:
            try:
                check, frame = webcam.read()
                print(check) #prints true as long as the webcam is running
                print(frame) #prints matrix values of each framecd
                cv2.imshow("Capturing", frame)
                key = cv2.waitKey(1)
                if key == ord('s'): 
                    cv2.imwrite(filename='saved_img.jpg', img=frame)
                    webcam.release()
                    img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
                    img_new = cv2.imshow("Captured Image", img_new)
                    cv2.waitKey(5)
                    cv2.destroyAllWindows()
                    self.picture_label = Label(self, text = "Photo Taken")
                    self.picture_label.grid(row =3, column = 3)
                    self.upload_photo_button.grid_forget()
                    break
                elif key == ord('q'):
                    print("Turning off camera.")
                    webcam.release()
                    print("Camera off.")
                    print("Program ended.")
                    cv2.destroyAllWindows()
                    break
            except(KeyboardInterrupt):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break


    def convertToBinaryData_admin(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData


    def registered(self, first_name, middle_name, last_name, sex, birth_year, birth_month, birth_day, civil_status, year_of_residency, address, place_of_birth, username, password):
        print (first_name)
        print (middle_name)
        print (last_name)
        print (sex)
        print (birth_year)
        print (birth_month)
        print (birth_day)
        print (civil_status)
        print (year_of_residency)
        print (address)
        print (place_of_birth)
        print (username)
        print (password)
        try:
            if self.picture_label.cget("text") == "":
                messagebox.showerror("Notice!", "Please take a picture")
            else:
                
                photo = 'saved_img.jpg'                        
                user_photo = self.convertToBinaryData_admin(photo)
                
                #birth_day
                _year = int(birth_year)
                _month = int(birth_month)
                _day = int(birth_day)

                birth_day = datetime.date(_year, _month, _day)
                print (birth_day)
                if (first_name =="" or middle_name == "" or last_name == "" or sex =="" or birth_day == "" or civil_status =="" or
                    year_of_residency == "" or address =="" or place_of_birth == "" or username == "" or password == "" or self.confirm_password.get() ==""):
                    messagebox.showerror("Error!","Please complete the required field")
                elif password !=self.confirm_password.get():
                    messagebox.showerror("Notice","Password does not match")
                    
                else:
                    
                    self.cursor.execute ("INSERT INTO residents_admin (LAST_NAME, FIRST_NAME, MIDDLE_NAME, SEX, BIRTH_DATE, CIVIL_STATUS, YEAR_OF_RESIDENCY, ADDRESS, PLACE_OF_BIRTH, IMAGE, USERNAME, PASSWORD) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(last_name,middle_name,
                                                                                                                                                                                                                                                                   first_name,
                                                                                                                                                                                                                                                                   sex,
                                                                                                                                                                                                                                                                   birth_day,
                                                                                                                                                                                                                                                                   civil_status,
                                                                                                                                                                                                                                                                   year_of_residency,
                                                                                                                                                                                                                                                                   address,
                                                                                                                                                                                                                                                                   place_of_birth, user_photo,
                                                                                                                                                                                                                                                                   username,
                                                                                                                                                                                                                                                                   password))
                    self.db.commit()
                    messagebox.showinfo("Success", "Registration Complete")
        except Exception as e:
            messagebox.showerror("Notice!", "Please take a picture")
            

class User_Update(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        self.db = pymysql.connect(host = "localhost", user = "root",passwd = "",db= "thesis_main")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        
        self.top = Frame(self, bg = "white")
        self.top.grid(row = 0, column = 0, pady = 5)

        self.bottom = Frame(self, bg = "white")
        self.bottom.grid(row = 3, column = 0, pady = 5)

        self.search_bar = StringVar()
        self.search_entry = Entry(self.top, width = 80, bg = "white", textvariable = self.search_bar)
        self.search_entry.grid(row = 0, column = 1)
        self.search_bar.trace("w", self.search_data)
        self.reset_button = Button(self.top, text = "refresh", bg = "white", command = self.reset_data)
        self.reset_button.grid(row = 0, column = 3)

        self.tree = ttk.Treeview(self, selectmode="browse", columns = (1,2,3,4,5,6,7,8,9,10), height = 35, show = "headings")
        self.tree.grid(row = 1, column = 0)

        self.update_button = Button(self.bottom, text = "Update Details", bg = "white")
        self.update_button.grid(row = 0, column = 0, padx=5)
        
        self.update_RFID = Button(self.bottom, text = "Update RFID", bg = "white")
        self.update_RFID.grid(row = 0, column = 1)

        self.update_finger_button = Button(self.bottom, text = "Update Fingerprint", bg = "white")
        self.update_finger_button.grid(row = 0, column = 2, padx=5)
        
        self.back_button = Button(self.bottom, text = "Back", bg = "white", command = lambda: controller.show_frame("Main_Page"))
        self.back_button.grid(row = 0, column = 3)
                
        self.tree.heading(1, text="ID")
        self.tree.heading(2, text="Last Name")
        self.tree.heading(3, text="First Name")
        self.tree.heading(4, text="Middle Name")
        self.tree.heading(5, text="Sex")
        self.tree.heading(6, text="Birth Date")
        self.tree.heading(7, text="Civil Status")
        self.tree.heading(8, text="Year of Residency")
        self.tree.heading(9, text="Address")
        self.tree.heading(10, text="Place of Birth")
        
        self.tree.column(1, width = 100)
        self.tree.column(2, width = 115)
        self.tree.column(3, width = 115)
        self.tree.column(4, width = 115)
        self.tree.column(5, width = 90)
        self.tree.column(6, width = 100)
        self.tree.column(7, width = 115)
        self.tree.column(8, width = 150)
        self.tree.column(9, width = 200)
        self.tree.column(10, width = 300)
        
        self.scrolly = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrolly.grid(row = 1, column = 1, sticky = "nesw")
        
        self.tree.configure(yscrollcommand=self.scrolly.set)

        self.cursor.execute("SELECT * FROM residents_db")
        self.fetch = self.cursor.fetchall()
        for data in self.fetch:
            self.tree.insert('', 'end', values=(data))

    def reset_data(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM residents_db")
        self.fetch = self.cursor.fetchall()
        for data in self.fetch:
            self.tree.insert('', 'end', values=(data))

    def search_data(self, *args):
        searching = str(self.search_bar.get())
        
        if (self.search_bar.get() != ""):
            self.tree.delete(*self.tree.get_children())
            self.cursor.execute("SELECT * FROM residents_db WHERE LAST_NAME LIKE %s OR MIDDLE_NAME LIKE %s OR FIRST_NAME LIKE %s",('%'+searching+'%','%'+searching+'%','%'+searching+'%'))
            self.fetch = self.cursor.fetchall()

            for data in self.fetch:
                self.tree.insert('', 'end', values=(data))


class Admin_Update(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.db = pymysql.connect(host = "localhost", user = "root",passwd = "",db= "thesis_main")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        
        self.top = Frame(self, bg = "white")
        self.top.grid(row = 0, column = 0, pady = 5)

        self.bottom = Frame(self, bg = "white")
        self.bottom.grid(row = 3, column = 0, pady = 5)

        self.search_bar = StringVar()
        self.search_entry = Entry(self.top, width = 80, bg = "white", textvariable = self.search_bar)
        self.search_entry.grid(row = 0, column = 1)
        self.search_bar.trace("w", self.search_data)
        self.reset_button = Button(self.top, text = "refresh", bg = "white", command = self.reset_data)
        self.reset_button.grid(row = 0, column = 3)

        self.tree = ttk.Treeview(self, selectmode="browse", columns = (1,2,3,4,5,6,7,8,9,10), height = 35, show = "headings")
        self.tree.grid(row = 1, column = 0)

        self.update_button = Button(self.bottom, text = "Update Details", bg = "white")
        self.update_button.grid(row = 0, column = 0, padx=5)
        
        self.update_RFID = Button(self.bottom, text = "Update RFID", bg = "white")
        self.update_RFID.grid(row = 0, column = 1)

        self.update_finger_button = Button(self.bottom, text = "Update Fingerprint", bg = "white")
        self.update_finger_button.grid(row = 0, column = 2, padx=5)
        
        self.back_button = Button(self.bottom, text = "Back", bg = "white", command = lambda: controller.show_frame("Main_Page"))
        self.back_button.grid(row = 0, column = 3)
                
        self.tree.heading(1, text="ID")
        self.tree.heading(2, text="Last Name")
        self.tree.heading(3, text="First Name")
        self.tree.heading(4, text="Middle Name")
        self.tree.heading(5, text="Sex")
        self.tree.heading(6, text="Birth Date")
        self.tree.heading(7, text="Civil Status")
        self.tree.heading(8, text="Year of Residency")
        self.tree.heading(9, text="Address")
        self.tree.heading(10, text="Place of Birth")
        
        self.tree.column(1, width = 100)
        self.tree.column(2, width = 115)
        self.tree.column(3, width = 115)
        self.tree.column(4, width = 115)
        self.tree.column(5, width = 90)
        self.tree.column(6, width = 100)
        self.tree.column(7, width = 115)
        self.tree.column(8, width = 150)
        self.tree.column(9, width = 200)
        self.tree.column(10, width = 300)
        
        self.scrolly = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrolly.grid(row = 1, column = 1, sticky = "nesw")
        
        self.tree.configure(yscrollcommand=self.scrolly.set)

        self.cursor.execute("SELECT * FROM residents_admin")
        self.fetch = self.cursor.fetchall()
        for data in self.fetch:
            self.tree.insert('', 'end', values=(data))

    def reset_data(self):
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        print(list_values)

        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM residents_admin")
        self.fetch = self.cursor.fetchall()
        for data in self.fetch:
            self.tree.insert('', 'end', values=(data))

    def search_data(self, *args):
        searching = str(self.search_bar.get())
        
        if (self.search_bar.get() != ""):
            self.tree.delete(*self.tree.get_children())
            self.cursor.execute("SELECT * FROM residents_admin WHERE LAST_NAME LIKE %s OR MIDDLE_NAME LIKE %s OR FIRST_NAME LIKE %s",('%'+searching+'%','%'+searching+'%','%'+searching+'%'))
            self.fetch = self.cursor.fetchall()

            for data in self.fetch:
                self.tree.insert('', 'end', values=(data))




if __name__ == "__main__":
    main = Admin_System()
    main.mainloop()
