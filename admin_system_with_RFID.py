from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
import pymysql
import io
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

class admin_system(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.db = pymysql.connect(host = "192.168.1.9", port = 3306, user = "root",passwd = "justin",db= "thesis_main")
        self.cursor = self.db.cursor()
        GPIO.setwarnings(False)
        
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        
        self.geometry("{}x{}".format(self.ws, self.hs))
        
        self.reader = SimpleMFRC522()

        self.db.autocommit(True)
        self.QueryResident = "CREATE TABLE IF NOT EXISTS residents_admin (ID INT(11) not null AUTO_INCREMENT, LAST_NAME varchar(255) not null, FIRST_NAME varchar(255) not null, MIDDLE_NAME varchar(255) not null, SEX varchar(255) not null, BIRTH_DATE date, CIVIL_STATUS varchar(255) not null, YEAR_OF_RESIDENCY int, ADDRESS varchar(255) not null, PLACE_OF_BIRTH varchar(255) not null, Contact_No varchar(255), IMAGE LONGBLOB, USERNAME varchar(255) not null, PASSWORD varchar(255) not null, PRIMARY KEY (ID))"
        self.cursor.execute(self.QueryResident)
        self.QueryResident_admin = "CREATE TABLE IF NOT EXISTS residents_db (ID INT(11) not null AUTO_INCREMENT, LAST_NAME varchar(255) not null, FIRST_NAME varchar(255) not null, MIDDLE_NAME varchar(255) not null, SEX varchar(255) not null, BIRTH_DATE date, CIVIL_STATUS varchar(255) not null, YEAR_OF_RESIDENCY int, ADDRESS varchar(255) not null, PLACE_OF_BIRTH varchar(255) not null, SECURITY_QUESTION varchar(255), ANSWER varchar(255), Contact_No varchar(255) not null, IMAGE LONGBLOB, RFID varchar(255) not null, FINGER_TEMPLATE varchar(255) DEFAULT '' not null, PRIMARY KEY (ID))"
        self.cursor.execute(self.QueryResident_admin)
        self.QueryResident_announcement = "CREATE TABLE IF NOT EXISTS residents_announcement (IMAGE LONGBLOB not null)"
        self.cursor.execute(self.QueryResident_announcement)
        self.QueryResident_edit_form = "CREATE TABLE IF NOT EXISTS edit_form_db (`X-Position` varchar(255) not null, `Y-Position` varchar(255) not null, Form_Details varchar(255) not null)"
        self.cursor.execute(self.QueryResident_edit_form)
        self.QueryResident_report = "CREATE TABLE IF NOT EXISTS residents_transaction_db (NAME varchar(255) not null, CONTACT_NO varchar(255) not null, TIME_AND_DATE date, FORM_PRINTED varchar(255) not null, OR_NUMBER varchar(255) not null)"
        self.cursor.execute(self.QueryResident_report)
        
        self.login_frame = Frame(self)
        self.login_frame.pack(fill = "both", expand = 1)
        self.admin_log_img = (Image.open("admin_bg.jpg"))
        self.admin_log_image = self.admin_log_img.resize((self.ws, self.hs))
        self.img_background_log = ImageTk.PhotoImage(self.admin_log_image)
        self.label_log = Label(self.login_frame, image = self.img_background_log) 
        self.label_log.place(x=0, y = 0)
        
        self.input_field_frame = Frame(self.login_frame, bg = "white")
        self.input_field_frame.grid(row = 0, column = 0)
        
        self.label_username = Label(self.input_field_frame, text = "Username: ", bg = "white")
        self.label_username.grid(row = 1, column = 0)
        self.label_password = Label(self.input_field_frame, text = "Password: ", bg = "white")
        self.label_password.grid(row = 2, column = 0)
        
        self.username = StringVar()
        self.password = StringVar()
        
        self.entry_username = Entry(self.input_field_frame, textvariable = self.username, bg = "white")
        self.entry_username.grid(row = 1, column = 1)
        self.entry_password = Entry(self.input_field_frame, textvariable = self.password, show = "*",bg = "white")
        self.entry_password.grid(row = 2, column = 1)
        button_submit = Button(self.input_field_frame, text="Login", command=lambda: self.submit_login(self.username.get(), self.password.get()))
        button_submit.grid(row = 3, column = 0, columnspan = 2)
        self.login_frame.columnconfigure(0, weight = 1)
        self.login_frame.rowconfigure(0, weight = 1)


    def submit_login(self, username, password):
        self.cursor.execute("SELECT * FROM residents_admin WHERE USERNAME = %s AND PASSWORD = %s", (username, password))
        if self.cursor.fetchone() is not None:
            messagebox.showinfo("Success", "Welcome")
            self.main_page()
        elif username =="" or password =="":
            messagebox.showerror("Notice!", "Please input password and username")
        else:
            messagebox.showerror("Notice!", "username or password is incorrect")

    def main_page(self):
            
        self.login_frame.pack_forget()
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()

        self.geometry("{}x{}".format(self.ws, self.hs))
        
        self.Main_Frame = Frame(self)
        self.Main_Frame.pack(fill = "both", expand = 1)
        
        self.admin_main_img = (Image.open("admin_bg.jpg"))
        self.admin_main_image = self.admin_main_img.resize((self.ws, self.hs))
        self.img_background_login = ImageTk.PhotoImage(self.admin_main_image)
        self.label_login = Label(self.Main_Frame, image = self.img_background_login) 
        self.label_login.place(x=0, y = 0)
                
        self.profile_frame = Frame(self.Main_Frame)
        self.profile_frame.grid(row = 0, column = 1, sticky = "nsew", padx = 30, pady = 100)
            
        self.cursor.execute("SELECT * FROM residents_admin WHERE USERNAME = %s AND PASSWORD = %s",(self.username.get(), self.password.get()))
        self.data = self.cursor.fetchone()
        
        print(self.data[0],self.data[1],self.data[2],self.data[3],self.data[4],
              self.data[5],self.data[6],self.data[7],self.data[8],self.data[9],
              self.data[10],self.data[11],self.data[12],self.data[13],)
        
        self.picture=self.data[13]
        print(self.picture)
        
        self.img_detail = Image.open("member_details.jpg")
        self.img_copy= self.img_detail.copy()
        
        self.detail_img = ImageTk.PhotoImage(self.img_detail)

        self.detail_bg = Label(self.profile_frame, image = self.detail_img)
        self.detail_bg.place(x = 0, y = 0, relwidth=1, relheight=1)
        self.detail_bg.bind('<Configure>', self._resize_image)
        
        self.byte_image = io.BytesIO(self.picture)
        self.img = Image.open(self.byte_image)
        self.img2 = self.img.resize((100,100))
        self.phimg = ImageTk.PhotoImage(self.img2)
        self.profile_image = Label(self.profile_frame, image = self.phimg)
        self.profile_image.grid(row = 0, column = 1, sticky = "e", padx = 30, pady = 10)

        self.lbl_name = Label(self.profile_frame, text = "Name:", bg = "white")
        self.lbl_name.grid(row = 1, column = 0, sticky = "w", padx = 10, pady = 10)
        self.lbl_bday = Label(self.profile_frame, text = "Birthday:", bg = "white")
        self.lbl_bday.grid(row = 2, column = 0, sticky = "w", padx = 10, pady = 10)
        self.lbl_name = Label(self.profile_frame, text = "Address:", bg = "white")
        self.lbl_name.grid(row = 3, column = 0, sticky = "w", padx = 10, pady = 10)
        self.lbl_name = Label(self.profile_frame, text = "Contact No.:", bg = "white")
        self.lbl_name.grid(row = 5, column = 0, sticky = "w", padx = 10, pady = 10)
        self.add_frame = Frame(self.profile_frame,bg = "white")
        self.add_frame.grid(row = 3, column = 1, sticky = "w", padx = 10, pady = 10)
        
        self.full_name = (self.data[1] + "," + " " + self.data[2] + " " + self.data[3])
        self.profile_name = Label(self.profile_frame, text = self.full_name.title(), bg = "white")
        self.profile_name.grid(row = 1, column = 1, sticky = "W", padx = 10, pady = 10)
        
        self.profile_bday = Label(self.profile_frame, text = self.data[5], bg = "white")
        self.profile_bday.grid(row = 2, column = 1, sticky = "W", padx = 10, pady = 10)
        self.full_address = "Brgy. Wawa III, Rosario, Cavite"
        
        self.profile_address= Label(self.add_frame, text = self.data[8].title(), bg = "white")
        self.profile_address.grid(row = 0, column = 0, sticky = "w")
        self.profile_address2= Label(self.add_frame, text = self.full_address.title(), bg = "white")
        self.profile_address2.grid(row = 1, column = 0, sticky = "w")
             
        self.profile_contact= Label(self.profile_frame, text = self.data[10], bg = "white")
        self.profile_contact.grid(row = 5, column = 1, sticky = "w", padx = 10)
        
        self.main_button_frame = Frame(self.Main_Frame, bg = "white")
        self.main_button_frame.grid(row = 0, column = 2)
        
        self.register_user_btn = Button(self.main_button_frame,bg ="white", height = 3, width = 20, text="register user", command = self.register_user)
        self.register_user_btn.grid(row = 0, column = 0)
        
        self.register_admin_btn= Button(self.main_button_frame,bg ="white", height = 3, width = 20, text="register_admin", command = self.register_admin)
        self.register_admin_btn.grid(row = 1, column = 0, pady = 15)
        
        self.update_user_btn= Button(self.main_button_frame,bg ="white", height = 3, width = 20, text="update_user", command = self. update_user)
        self.update_user_btn.grid(row = 2, column = 0)
        
        self.update_admin_btn= Button(self.main_button_frame,bg ="white", height = 3, width = 20, text="update_admin", command = self.update_admin)
        self.update_admin_btn.grid(row = 3, column = 0, pady = 15)
        
        self.upload_announcement_btn= Button(self.main_button_frame,bg ="white", height = 3, width = 20, text="Upload Announcement", command = self.upload_announcement)
        self.upload_announcement_btn.grid(row = 0, column = 1, padx = 15)
        
        self.btn_update_brgy_form= Button(self.main_button_frame,bg ="white", height = 3, width = 20, text="View transaction history", command = self.view_report)
        self.btn_update_brgy_form.grid(row = 1, column = 1, padx = 15)
        
        self.btn_view_report_history= Button(self.main_button_frame,bg ="white", height = 3, width = 20, text="Update Form", command = self.revise_form)
        self.btn_view_report_history.grid(row = 2, column = 1, padx = 15)
        
        self.logout_btn= Button(self.main_button_frame,bg ="white", height = 3, width = 20, text="Logout", command = self.logout)
        self.logout_btn.grid(row = 3, column = 1, padx = 15)
    
    def upload_image_announcement(self):
        
        self.filename_announcement = askopenfilename(title = "Open File", filetypes = (("png files", "*.png"), ("jpeg files", "*.jpeg")))
        self.upload_img_announcement = (Image.open(self.filename_announcement))
        self.upload_image_announcement2= self.upload_img_announcement.resize((122, 121))
        self.img_upload_announcement = ImageTk.PhotoImage(self.upload_image_announcement2)
        self.label_upload_announcement = Label(self.up_announcement_frame, image = self.img_upload_announcement) 
        self.label_upload_announcement.grid(row = 0, column = 0, sticky = "w", padx = 40, pady = 20)

    def upload_announcement(self):
        self.Main_Frame.pack_forget()
        self.announcement_frame = Frame(self)
        self.announcement_frame.pack(fill = "both", expand = 1)
  
        self.announcement_main_img = (Image.open("admin_bg.jpg"))
        self.announcement_main_image = self.announcement_main_img.resize((self.ws, self.hs))
        self.img_background_announcement = ImageTk.PhotoImage(self.announcement_main_image)
        self.label_announcement = Label(self.announcement_frame, image = self.img_background_announcement) 
        self.label_announcement.place(x=0, y = 0)
              
        self.up_announcement_frame = Frame(self.announcement_frame, bg = "white")
        self.up_announcement_frame.grid(row = 0, column = 0, sticky = "s")
        
        self.sub_announcement_frame = Frame(self.announcement_frame, bg = "white")
        self.sub_announcement_frame.grid(row = 1, column = 0, sticky = "n")
        
        self.empty_space_announcement=Label(self.up_announcement_frame, width = 15, height = 7, bg = "white")
        self.empty_space_announcement.grid(row = 0, column = 0, sticky = "w", padx = 40, pady = 20)
        
        self.btn_upload_announcement = Button(self.up_announcement_frame, bg = "white", text = "Upload an Image", command = self.upload_image_announcement)
        self.btn_upload_announcement.grid(row = 0, column = 1)
        self.btn_submit_announcement = Button(self.sub_announcement_frame, bg = "white", text = "Submit", command = self.submit_announcement)
        self.btn_submit_announcement.grid(row = 0, column = 1)
        self.btn_back_announcement = Button(self.sub_announcement_frame, bg = "white", text = "Back", command = self.back_to_mp_again)
        self.btn_back_announcement.grid(row = 0, column = 0, padx = 10)
        
        self.announcement_frame.columnconfigure(0, weight = 1)
        self.announcement_frame.rowconfigure(0, weight = 1)
        self.announcement_frame.rowconfigure(1, weight = 1)

    def back_to_mp_again(self):
        self.announcement_frame.pack_forget()
        self.Main_Frame.pack(fill = "both", expand =1)
        
    def submit_announcement(self):
        self.cursor.execute("SELECT * FROM residents_announcement")
        result = self.cursor.fetchone()
        if result:
            print(result)
            photo_announcement = self.filename_announcement
            user_photo_announcement = self.convertToBinaryData_announcement(photo_announcement)
            self.cursor.execute("UPDATE residents_announcement SET IMAGE = %s WHERE IMAGE IS NOT NULL OR IMAGE = %s", (user_photo_announcement, result))
            messagebox.showinfo("Success!","Announcement has been updated")
            self.announcement_frame.pack_forget()
            self.Main_Frame.pack(fill = "both", expand = 1)
        else:
            photo_announcement = self.filename_announcement                        
            user_photo_announcement = self.convertToBinaryData_announcement(photo_announcement)
            self.announcement_query = "INSERT INTO residents_announcement (IMAGE) VALUES(%s)"
            self.cursor.execute(self.announcement_query, user_photo_announcement)
            messagebox.showinfo("Success!","Announcement has been updated")
            self.announcement_frame.pack_forget()
            self.Main_Frame.pack(fill = "both", expand = 1)
    
    def convertToBinaryData_announcement(self, filename):
        # Convert digital data tobinary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    
    def view_report(self):
        pass
    
    def revise_form(self):
        self.Main_Frame.pack_forget()
        self.revise_form_frame = Frame(self)
        self.revise_form_frame.pack(fill = "both", expand = 1)
        
        
        self.revise_main_img = (Image.open("admin_bg.jpg"))
        self.revise_main_image = self.revise_main_img.resize((self.ws, self.hs))
        self.img_background_revise = ImageTk.PhotoImage(self.revise_main_image)
        self.label_revise = Label(self.revise_form_frame, image = self.img_background_revise) 
        self.label_revise.place(x=0, y = 0)
        self.revise_btn_frame = Frame(self.revise_form_frame, bg = "white")
        self.revise_btn_frame.grid(row = 0, column = 0, sticky = "s")
        
        self.back_frame = Frame(self.revise_form_frame, bg = "white")
        self.back_frame.grid(row = 1, column = 0, sticky = "n")
        
        self.brgy_btn1 = Button(self.revise_btn_frame, text = "Barangay Certification",width = "25", height = "5", bg = "white", command = self.revise_brgy_clearance)
        self.brgy_btn1.grid(row = 0, column = 0, sticky = "es", padx = 10, pady = 10)
        
        self.brgy_btn2 = Button(self.revise_btn_frame, text = "Certificate of Residency",width = "25", height = "5", bg = "white", command = self.revise_cert_residency)
        self.brgy_btn2.grid(row = 0, column = 1, sticky = "ws", padx = 10, pady = 10)
        
        self.brgy_btn3 = Button(self.revise_btn_frame, text = "Certificate of Residency\nfor Student",width = "25", height = "5", bg = "white",command = self.revise_cert_residency_student)
        self.brgy_btn3.grid(row = 1, column = 0, sticky = "en", padx = 10, pady = 10)
        
        self.brgy_btn4 = Button(self.revise_btn_frame, text = "Certificate of Indigency",width = "25", height = "5", bg = "white", command = self.revise_cert_indigency)
        self.brgy_btn4.grid(row = 1, column = 1, sticky = "wn", padx = 10, pady = 10)
        
        self.back_btn = Button(self.back_frame, text = "back", bg = "white", height = "4", width = "15",command = self.back_from_revise_form)
        self.back_btn.grid(row =0,column = 0)
        
        self.revise_form_frame.columnconfigure(0, weight = 1)
        self.revise_form_frame.rowconfigure(0, weight = 1)
        self.revise_form_frame.rowconfigure(1, weight = 1)

    def revise_brgy_clearance(self):
        self.revise_form_frame.pack_forget()
        self.revise_clear_frame = Frame(self)
        self.revise_clear_frame.pack(fill = "both", expand = 1)
        self.revise_clear_main_img = (Image.open("admin_bg.jpg"))
        self.revise_clear_main_image = self.revise_clear_main_img.resize((self.ws, self.hs))
        self.img_background_revise_clear = ImageTk.PhotoImage(self.revise_clear_main_image)
        self.label_revise_clear = Label(self.revise_clear_frame, image = self.img_background_revise_clear) 
        self.label_revise_clear.place(x=0, y = 0)
        
        self.clear_frame = Frame(self.revise_clear_frame, bg = "white")
        self.clear_frame.grid(row = 0, column = 0)
        
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Full_Name"))
        self.res_BC_Full_Name = self.cursor.fetchone()
        print(self.res_BC_Full_Name)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Age"))
        self.res_BC_Age = self.cursor.fetchone()
        print(self.res_BC_Age)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Year_Resides"))
        self.res_BC_Year_Resides = self.cursor.fetchone()
        print(self.res_BC_Year_Resides)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Address"))
        self.res_BC_Address = self.cursor.fetchone()
        print(self.res_BC_Address)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_DOB"))
        self.res_BC_DOB = self.cursor.fetchone()
        print(self.res_BC_DOB)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_POB"))
        self.res_BC_POB = self.cursor.fetchone()
        print(self.res_BC_POB)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Civil_Status"))
        self.res_BC_Civil_Status = self.cursor.fetchone()
        print(self.res_BC_Civil_Status)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Sex"))
        self.res_BC_Sex = self.cursor.fetchone()
        print(self.res_BC_Sex)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_BRGY_residence"))
        self.res_BC_BRGY_residence = self.cursor.fetchone()
        print(self.res_BC_BRGY_residence)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Today"))
        self.res_BC_Today = self.cursor.fetchone()
        print(self.res_BC_Today)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Purpose"))
        self.res_BC_Purpose = self.cursor.fetchone()
        print(self.res_BC_Purpose)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Issued_Day"))
        self.res_BC_Issued_Day = self.cursor.fetchone()
        print(self.res_BC_Issued_Day)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BC_Issued_Month"))
        self.res_BC_Issued_Month = self.cursor.fetchone()
        print(self.res_BC_Issued_Month)
        
        BC_Full_Namex = StringVar()
        BC_Agex = StringVar()
        BC_Year_Residesx = StringVar()
        BC_Addressx = StringVar()
        BC_DOBx = StringVar()
        BC_POBx = StringVar()
        BC_Civil_Statusx = StringVar()
        BC_Sexx = StringVar()
        BC_BRGY_residencex = StringVar()
        BC_Todayx = StringVar()
        BC_Purposex = StringVar()
        BC_Issued_Dayx = StringVar()
        BC_Issued_Monthx = StringVar()

        BC_Full_Namey = StringVar()
        BC_Agey = StringVar()
        BC_Year_Residesy = StringVar()
        BC_Addressy = StringVar()
        BC_DOBy = StringVar()
        BC_POBy = StringVar()
        BC_Civil_Statusy = StringVar()
        BC_Sexy = StringVar()
        BC_BRGY_residencey = StringVar()
        BC_Todayy = StringVar()
        BC_Purposey = StringVar()
        BC_Issued_Dayy = StringVar()
        BC_Issued_Monthy = StringVar()
        
        
        
        self.clearance_entryx1 = Entry (self.clear_frame, textvariable = BC_Full_Namex)
        self.clearance_entryx2 = Entry (self.clear_frame, textvariable = BC_Agex)
        self.clearance_entryx3 = Entry (self.clear_frame, textvariable = BC_Year_Residesx)
        self.clearance_entryx4 = Entry (self.clear_frame, textvariable = BC_Addressx)
        self.clearance_entryx5 = Entry (self.clear_frame, textvariable = BC_DOBx)
        self.clearance_entryx6 = Entry (self.clear_frame, textvariable = BC_POBx)
        self.clearance_entryx7 = Entry (self.clear_frame, textvariable = BC_Civil_Statusx)
        self.clearance_entryx8 = Entry (self.clear_frame, textvariable = BC_Sexx)
        self.clearance_entryx9 = Entry (self.clear_frame, textvariable = BC_BRGY_residencex)
        self.clearance_entryx10 = Entry (self.clear_frame, textvariable = BC_Todayx)
        self.clearance_entryx11 = Entry (self.clear_frame, textvariable = BC_Purposex)
        self.clearance_entryx12 = Entry (self.clear_frame, textvariable = BC_Issued_Dayx)
        self.clearance_entryx13 = Entry (self.clear_frame, textvariable = BC_Issued_Monthx)
        
        self.clearance_entryy1 = Entry (self.clear_frame, textvariable = BC_Full_Namey)
        self.clearance_entryy2 = Entry (self.clear_frame, textvariable = BC_Agey)
        self.clearance_entryy3 = Entry (self.clear_frame, textvariable = BC_Year_Residesy)
        self.clearance_entryy4 = Entry (self.clear_frame, textvariable = BC_Addressy)
        self.clearance_entryy5 = Entry (self.clear_frame, textvariable = BC_DOBy)
        self.clearance_entryy6 = Entry (self.clear_frame, textvariable = BC_POBy)
        self.clearance_entryy7 = Entry (self.clear_frame, textvariable = BC_Civil_Statusy)
        self.clearance_entryy8 = Entry (self.clear_frame, textvariable = BC_Sexy)
        self.clearance_entryy9 = Entry (self.clear_frame, textvariable = BC_BRGY_residencey)
        self.clearance_entryy10 = Entry (self.clear_frame, textvariable = BC_Todayy)
        self.clearance_entryy11 = Entry (self.clear_frame, textvariable = BC_Purposey)
        self.clearance_entryy12 = Entry (self.clear_frame, textvariable = BC_Issued_Dayy)
        self.clearance_entryy13 = Entry (self.clear_frame, textvariable = BC_Issued_Monthy)
        
        
        self.clearance_labelx = Label(self.clear_frame, text = "X-Position", bg = "white")
        self.clearance_labely = Label(self.clear_frame, text = "Y-Position", bg = "white")
        self.clearance_labelx.grid(row = 0, column = 1)
        self.clearance_labely.grid(row = 0, column = 2)
        
        self.clearance_label1 = Label(self.clear_frame, text = "Name:", bg = "white")
        self.clearance_label2 = Label(self.clear_frame, text = "Age:", bg = "white")
        self.clearance_label3 = Label(self.clear_frame, text = "Year of Residency:", bg = "white")
        self.clearance_label4 = Label(self.clear_frame, text = "Address:", bg = "white")
        self.clearance_label5 = Label(self.clear_frame, text = "Date of Birth:", bg = "white")
        self.clearance_label6 = Label(self.clear_frame, text = "Place of Birth:", bg = "white")
        self.clearance_label7 = Label(self.clear_frame, text = "Civil Status:", bg = "white")
        self.clearance_label8 = Label(self.clear_frame, text = "Sex:", bg = "white")
        self.clearance_label9 = Label(self.clear_frame, text = "Issued at:", bg = "white")
        self.clearance_label10 = Label(self.clear_frame, text = "Issued on:", bg = "white")
        self.clearance_label11 = Label(self.clear_frame, text = "Purpose:", bg = "white")
        self.clearance_label12 = Label(self.clear_frame, text = "Issued Day:", bg = "white")
        self.clearance_label13 = Label(self.clear_frame, text = "Issued Month:", bg = "white")
        
        self.clearance_label1.grid(row = 1, column = 0, sticky = "w")
        self.clearance_label2.grid(row = 2, column = 0, sticky = "w")
        self.clearance_label3.grid(row = 3, column = 0, sticky = "w")
        self.clearance_label4.grid(row = 4, column = 0, sticky = "w")
        self.clearance_label5.grid(row = 5, column = 0, sticky = "w")
        self.clearance_label6.grid(row = 6, column = 0, sticky = "w")
        self.clearance_label7.grid(row = 7, column = 0, sticky = "w")
        self.clearance_label8.grid(row = 8, column = 0, sticky = "w")
        self.clearance_label9.grid(row = 9, column = 0, sticky = "w")
        self.clearance_label10.grid(row = 10, column = 0, sticky = "w")
        self.clearance_label11.grid(row = 11, column = 0, sticky = "w")
        self.clearance_label12.grid(row = 12, column = 0, sticky = "w")
        self.clearance_label13.grid(row = 13, column = 0, sticky = "w")
        
        self.clearance_entryx1.grid(row = 1, column = 1, padx = 5)
        self.clearance_entryx2.grid(row = 2, column = 1, pady =5)
        self.clearance_entryx3.grid(row = 3, column = 1)
        self.clearance_entryx4.grid(row = 4, column = 1, pady =5)
        self.clearance_entryx5.grid(row = 5, column = 1)
        self.clearance_entryx6.grid(row = 6, column = 1, pady =5)
        self.clearance_entryx7.grid(row = 7, column = 1)
        self.clearance_entryx8.grid(row = 8, column = 1, pady =5)
        self.clearance_entryx9.grid(row = 9, column = 1)
        self.clearance_entryx10.grid(row = 10, column = 1, pady =5)
        self.clearance_entryx11.grid(row = 11, column = 1)
        self.clearance_entryx12.grid(row = 12, column = 1, pady =5)
        self.clearance_entryx13.grid(row = 13, column = 1)
        
        self.clearance_entryy1.grid(row = 1, column = 2)
        self.clearance_entryy2.grid(row = 2, column = 2)
        self.clearance_entryy3.grid(row = 3, column = 2)
        self.clearance_entryy4.grid(row = 4, column = 2)
        self.clearance_entryy5.grid(row = 5, column = 2)
        self.clearance_entryy6.grid(row = 6, column = 2)
        self.clearance_entryy7.grid(row = 7, column = 2)
        self.clearance_entryy8.grid(row = 8, column = 2)
        self.clearance_entryy9.grid(row = 9, column = 2)
        self.clearance_entryy10.grid(row = 10, column = 2)
        self.clearance_entryy11.grid(row = 11, column = 2)
        self.clearance_entryy12.grid(row = 12, column = 2)
        self.clearance_entryy13.grid(row = 13, column = 2)
        
        self.clearance_entryx1.insert(0, self.res_BC_Full_Name[0])
        self.clearance_entryx2.insert(0, self.res_BC_Age[0])
        self.clearance_entryx3.insert(0, self.res_BC_Year_Resides[0])
        self.clearance_entryx4.insert(0, self.res_BC_Address[0])
        self.clearance_entryx5.insert(0, self.res_BC_DOB[0])
        self.clearance_entryx6.insert(0, self.res_BC_POB[0])
        self.clearance_entryx7.insert(0, self.res_BC_Civil_Status[0])
        self.clearance_entryx8.insert(0, self.res_BC_Sex[0])
        self.clearance_entryx9.insert(0, self.res_BC_BRGY_residence[0])
        self.clearance_entryx10.insert(0, self.res_BC_Today[0])
        self.clearance_entryx11.insert(0, self.res_BC_Purpose[0])
        self.clearance_entryx12.insert(0, self.res_BC_Issued_Day[0])
        self.clearance_entryx13.insert(0, self.res_BC_Issued_Month[0])
        
        self.clearance_entryy1.insert(0, self.res_BC_Full_Name[1])
        self.clearance_entryy2.insert(0, self.res_BC_Age[1])
        self.clearance_entryy3.insert(0, self.res_BC_Year_Resides[1])
        self.clearance_entryy4.insert(0, self.res_BC_Address[1])
        self.clearance_entryy5.insert(0, self.res_BC_DOB[1])
        self.clearance_entryy6.insert(0, self.res_BC_POB[1])
        self.clearance_entryy7.insert(0, self.res_BC_Civil_Status[1])
        self.clearance_entryy8.insert(0, self.res_BC_Sex[1])
        self.clearance_entryy9.insert(0, self.res_BC_BRGY_residence[1])
        self.clearance_entryy10.insert(0, self.res_BC_Today[1])
        self.clearance_entryy11.insert(0, self.res_BC_Purpose[1])
        self.clearance_entryy12.insert(0, self.res_BC_Issued_Day[1])
        self.clearance_entryy13.insert(0, self.res_BC_Issued_Month[1])
        
        self.button_back = Button(self.clear_frame, text = "back", command = self.back_from_clear)
        self.button_back.grid(row = 14, column = 0, pady = 10, columnspan = 2)
        
        self.button_submit_clear = Button(self.clear_frame, text = "Submit", command = lambda: self.update_revise_form(BC_Full_Namex.get(),
                                                                                                                              BC_Agex.get(),
                                                                                                                              BC_Year_Residesx.get(),
                                                                                                                              BC_Addressx.get(),
                                                                                                                              BC_DOBx.get(),
                                                                                                                              BC_POBx.get(),
                                                                                                                              BC_Civil_Statusx.get(),
                                                                                                                              BC_Sexx.get(),
                                                                                                                              BC_BRGY_residencex.get(),
                                                                                                                              BC_Todayx.get(),
                                                                                                                              BC_Purposex.get(),
                                                                                                                              BC_Issued_Dayx.get(),
                                                                                                                              BC_Issued_Monthx.get(),
                                                                                                                              BC_Full_Namey.get(),
                                                                                                                              BC_Agey.get(),
                                                                                                                              BC_Year_Residesy.get(),
                                                                                                                              BC_Addressy.get(),
                                                                                                                              BC_DOBy.get(),
                                                                                                                              BC_POBy.get(),
                                                                                                                              BC_Civil_Statusy.get(),
                                                                                                                              BC_Sexy.get(),
                                                                                                                              BC_BRGY_residencey.get(),
                                                                                                                              BC_Todayy.get(),
                                                                                                                              BC_Purposey.get(),
                                                                                                                              BC_Issued_Dayy.get(),
                                                                                                                              BC_Issued_Monthy.get()))
        self.button_submit_clear.grid(row = 14, column = 1, columnspan = 2)
        
        self.revise_clear_frame.columnconfigure(0, weight = 1)
        self.revise_clear_frame.rowconfigure(0, weight = 1)
        
    def back_from_clear(self):
        self.revise_clear_frame.pack_forget()
        self.revise_form_frame.pack(fill = "both", expand = 1)
        
    def update_revise_form(self, BC_full_namex, BC_agex, BC_year_residesx, BC_addressx,
                           BC_dobx, BC_pobx, BC_civil_statusx, BC_sexx, BC_brgy_residencex,
                           BC_todayx, BC_purposex, BC_issued_dayx, BC_issued_monthx, BC_full_namey,
                           BC_agey, BC_year_residesy, BC_addressy, BC_doby, BC_poby,
                           BC_civil_statusy, BC_sexy, BC_brgy_residencey, BC_todayy,
                           BC_purposey, BC_issued_dayy, BC_issued_monthy):
        
        self.BC_full_namex = BC_full_namex
        self.BC_agex = BC_agex
        self.BC_year_residesx = BC_year_residesx
        self.BC_addressx = BC_addressx
        self.BC_dobx = BC_dobx
        self.BC_pobx = BC_pobx
        self.BC_civil_statusx = BC_civil_statusx
        self.BC_sexx = BC_sexx
        self.BC_brgy_residencex = BC_brgy_residencex
        self.BC_todayx = BC_todayx
        self.BC_purposex = BC_purposex
        self.BC_issued_dayx = BC_issued_dayx
        self.BC_issued_monthx = BC_issued_monthx
        self.BC_full_namey = BC_full_namey
        self.BC_agey = BC_agey
        self.BC_year_residesy = BC_year_residesy
        self.BC_addressy = BC_addressy
        self.BC_doby = BC_doby
        self.BC_poby = BC_poby
        self.BC_civil_statusy = BC_civil_statusy
        self.BC_sexy = BC_sexy
        self.BC_brgy_residencey = BC_brgy_residencey
        self.BC_todayy = BC_todayy
        self.BC_purposey = BC_purposey
        self.BC_issued_dayy = BC_issued_dayy
        self.BC_issued_monthy = BC_issued_monthy
        
        print (self.BC_full_namex,
                self.BC_agex,
                self.BC_year_residesx,
                self.BC_addressx,
                self.BC_dobx,
                self.BC_pobx,
                self.BC_civil_statusx,
                self.BC_sexx,
                self.BC_brgy_residencex,
                self.BC_todayx,
                self.BC_purposex,
                self.BC_issued_dayx,
                self.BC_issued_monthx,
                self.BC_full_namey,
                self.BC_agey,
                self.BC_year_residesy,
                self.BC_addressy,
                self.BC_doby,
                self.BC_poby,
                self.BC_civil_statusy,
                self.BC_sexy,
                self.BC_brgy_residencey,
                self.BC_todayy,
                self.BC_purposey,
                self.BC_issued_dayy,
                self.BC_issued_monthy)
        
        if (self.BC_full_namex == "" or self.BC_agex == "" or self.BC_year_residesx == "" or
            self.BC_addressx == "" or self.BC_dobx == "" or self.BC_pobx == "" or self.BC_civil_statusx == "" or
            self.BC_sexx == "" or self.BC_brgy_residencex == "" or self.BC_todayx == "" or
            self.BC_purposex == "" or self.BC_issued_dayx == "" or self.BC_issued_monthx == "" or
            self.BC_full_namey == "" or self.BC_agey == "" or self.BC_year_residesy == "" or
            self.BC_addressy == "" or self.BC_doby == "" or self.BC_poby == "" or
            self.BC_civil_statusy == "" or self.BC_sexy == "" or self.BC_brgy_residencey == "" or
            self.BC_todayy == "" or self.BC_purposey == "" or self.BC_issued_dayy == "" or
            self.BC_issued_monthy == ""):
            messagebox.showerror("NotIce!", "the input field must not left blank")
        else:
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_full_namex, self.BC_full_namey, "BC_Full_Name" ))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_agex, self.BC_agey,"BC_Age"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_year_residesx, self.BC_year_residesy,"BC_Year_Resides"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_addressx, self.BC_addressy,"BC_Address"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_dobx, self.BC_doby,"BC_DOB"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_pobx, self.BC_poby,"BC_POB"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_civil_statusx, self.BC_civil_statusy,"BC_Civil_Status"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_sexx, self.BC_sexy,"BC_Sex"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_brgy_residencex, self.BC_brgy_residencey,"BC_BRGY_residence"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_todayx, self.BC_todayy,"BC_Today"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_purposex, self.BC_purposey,"BC_Purpose"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_issued_dayx, self.BC_issued_dayy,"BC_Issued_Day"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BC_issued_monthx, self.BC_issued_monthy,"BC_Issued_Month"))

            messagebox.showinfo("Success!", "Text position has been updated")
        

            
    def revise_cert_residency(self):
        self.revise_form_frame.pack_forget()
        self.revise_residency_frame = Frame(self)
        self.revise_residency_frame.pack(fill = "both", expand = 1)
        
        self.revise_residency_main_img = (Image.open("admin_bg.jpg"))
        self.revise_residency_main_image = self.revise_residency_main_img.resize((self.ws, self.hs))
        self.img_background_revise_residency = ImageTk.PhotoImage(self.revise_residency_main_image)
        self.label_revise_residency = Label(self.revise_residency_frame, image = self.img_background_revise_residency) 
        self.label_revise_residency.place(x=0, y = 0)
        
        self.residency_frame = Frame(self.revise_residency_frame, bg = "white")
        self.residency_frame.grid(row = 0, column = 0)
        
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BR_Full_Name"))
        self.res_BR_Full_Name = self.cursor.fetchone()
        print(self.res_BR_Full_Name)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BR_Year_Resides"))
        self.res_BR_Year_Resides = self.cursor.fetchone()                                         
        print(self.res_BR_Year_Resides)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BR_Address"))
        self.res_BR_Address = self.cursor.fetchone()
        print(self.res_BR_Address)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BR_Purpose"))
        self.res_BR_Purpose = self.cursor.fetchone()
        print(self.res_BR_Purpose)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BR_Issued_Day"))
        self.res_BR_Issued_Day = self.cursor.fetchone()
        print(self.res_BR_Issued_Day)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BR_Issued_Month"))
        self.res_BR_Issued_Month = self.cursor.fetchone()                                        
        print(self.res_BR_Issued_Month)
        
        BR_Full_Namex = StringVar()
        BR_Year_Residesx = StringVar()
        BR_Addressx = StringVar()
        BR_Purposex = StringVar()
        BR_Issued_Dayx = StringVar()
        BR_Issued_Monthx = StringVar()
        
        BR_Full_Namey = StringVar()
        BR_Year_Residesy = StringVar()
        BR_Addressy = StringVar()
        BR_Purposey = StringVar()
        BR_Issued_Dayy = StringVar()
        BR_Issued_Monthy = StringVar()
        
        self.residency_entryx1 = Entry (self.residency_frame, textvariable = BR_Full_Namex)
        self.residency_entryx2 = Entry (self.residency_frame, textvariable = BR_Year_Residesx)
        self.residency_entryx3 = Entry (self.residency_frame, textvariable = BR_Addressx)
        self.residency_entryx4 = Entry (self.residency_frame, textvariable = BR_Purposex)
        self.residency_entryx5 = Entry (self.residency_frame, textvariable = BR_Issued_Dayx)
        self.residency_entryx6 = Entry (self.residency_frame, textvariable = BR_Issued_Monthx)
        
        self.residency_entryy1 = Entry (self.residency_frame, textvariable = BR_Full_Namey)
        self.residency_entryy2 = Entry (self.residency_frame, textvariable = BR_Year_Residesy)
        self.residency_entryy3 = Entry (self.residency_frame, textvariable = BR_Addressy)
        self.residency_entryy4 = Entry (self.residency_frame, textvariable = BR_Purposey)
        self.residency_entryy5 = Entry (self.residency_frame, textvariable = BR_Issued_Dayy)
        self.residency_entryy6 = Entry (self.residency_frame, textvariable = BR_Issued_Monthy)
        
        self.residency_labelx = Label(self.residency_frame, text = "X-Position", bg = "white")
        self.residency_labely = Label(self.residency_frame, text = "Y-Position", bg = "white")
        self.residency_labelx.grid(row = 0, column = 1)
        self.residency_labely.grid(row = 0, column = 2)
        
        self.residency_label1 = Label(self.residency_frame, text = "Name:", bg = "white")
        self.residency_label2 = Label(self.residency_frame, text = "Year of residency:", bg = "white")
        self.residency_label3 = Label(self.residency_frame, text = "Address:", bg = "white")
        self.residency_label4 = Label(self.residency_frame, text = "Purpose:", bg = "white")
        self.residency_label5 = Label(self.residency_frame, text = "Issued Day:", bg = "white")
        self.residency_label6 = Label(self.residency_frame, text = "Issued Month:", bg = "white")
        
        self.residency_label1.grid(row = 1, column = 0, sticky = "w")
        self.residency_label2.grid(row = 2, column = 0, sticky = "w")
        self.residency_label3.grid(row = 3, column = 0, sticky = "w")
        self.residency_label4.grid(row = 4, column = 0, sticky = "w")
        self.residency_label5.grid(row = 5, column = 0, sticky = "w")
        self.residency_label6.grid(row = 6, column = 0, sticky = "w")
        
        self.residency_entryx1.grid(row = 1, column = 1, padx = 5) 
        self.residency_entryx2.grid(row = 2, column = 1, pady =5)
        self.residency_entryx3.grid(row = 3, column = 1)
        self.residency_entryx4.grid(row = 4, column = 1, pady =5)
        self.residency_entryx5.grid(row = 5, column = 1)
        self.residency_entryx6.grid(row = 6, column = 1, pady =5)
        
        self.residency_entryy1.grid(row = 1, column = 2) 
        self.residency_entryy2.grid(row = 2, column = 2)
        self.residency_entryy3.grid(row = 3, column = 2)
        self.residency_entryy4.grid(row = 4, column = 2)
        self.residency_entryy5.grid(row = 5, column = 2)
        self.residency_entryy6.grid(row = 6, column = 2)
        
        self.residency_entryx1.insert(0, self.res_BR_Full_Name[0])
        self.residency_entryx2.insert(0, self.res_BR_Year_Resides[0] )
        self.residency_entryx3.insert(0, self.res_BR_Address[0])
        self.residency_entryx4.insert(0, self.res_BR_Purpose[0])
        self.residency_entryx5.insert(0, self.res_BR_Issued_Day[0])
        self.residency_entryx6.insert(0, self.res_BR_Issued_Month[0])
        
        self.residency_entryy1.insert(0,self.res_BR_Full_Name[1])
        self.residency_entryy2.insert(0,self.res_BR_Year_Resides[1]  )
        self.residency_entryy3.insert(0,self.res_BR_Address[1])
        self.residency_entryy4.insert(0,self.res_BR_Purpose[1])
        self.residency_entryy5.insert(0,self.res_BR_Issued_Day[1])
        self.residency_entryy6.insert(0,self.res_BR_Issued_Month[1])
        
        self.button_back2 = Button(self.residency_frame, text = "back", command = self.back_from_residency)
        self.button_back2.grid(row = 7, column = 0, pady = 10, columnspan = 2)
        
        self.button_submit_residency = Button(self.residency_frame, text = "Submit", command = lambda: self.update_residency_form(BR_Full_Namex.get(),
                                                                                                                                         BR_Year_Residesx.get(),
                                                                                                                                         BR_Addressx.get(),
                                                                                                                                         BR_Purposex.get(),
                                                                                                                                         BR_Issued_Dayx.get(),
                                                                                                                                         BR_Issued_Monthx.get(),
                                                                                                                                         BR_Full_Namey.get(),
                                                                                                                                         BR_Year_Residesy.get(),
                                                                                                                                         BR_Addressy.get(),
                                                                                                                                         BR_Purposey.get(),
                                                                                                                                         BR_Issued_Dayy.get(),
                                                                                                                                         BR_Issued_Monthy.get()))
        self.button_submit_residency.grid(row = 7, column = 1, columnspan = 2)
    
        self.revise_residency_frame.columnconfigure(0, weight = 1)
        self.revise_residency_frame.rowconfigure(0, weight = 1)
        
    def update_residency_form(self,BR_full_namex,
                              BR_year_residesx,
                              BR_addressx,
                              BR_purposex,
                              BR_issued_dayx,
                              BR_issued_monthx,
                              BR_full_namey,
                              BR_year_residesy,
                              BR_addressy,
                              BR_purposey,
                              BR_issued_dayy,
                              BR_issued_monthy):
        
        self.BR_full_namex = BR_full_namex
        self.BR_year_residesx = BR_year_residesx
        self.BR_addressx = BR_addressx
        self.BR_purposex = BR_purposex
        self.BR_issued_dayx = BR_issued_dayx
        self.BR_issued_monthx = BR_issued_monthx
        self.BR_full_namey = BR_full_namey
        self.BR_year_residesy = BR_year_residesy
        self.BR_addressy = BR_addressy
        self.BR_purposey = BR_purposey
        self.BR_issued_dayy = BR_issued_dayy
        self.BR_issued_monthy = BR_issued_monthy
        
        print(self.BR_full_namex,
              self.BR_year_residesx,
              self.BR_addressx,
              self.BR_purposex,
              self.BR_issued_dayx,
              self.BR_issued_monthx,
              self.BR_full_namey,
              self.BR_year_residesy,
              self.BR_addressy,
              self.BR_purposey,
              self.BR_issued_dayy,
              self.BR_issued_monthy)
        
        if (BR_full_namex == "" or
            BR_year_residesx == "" or
            BR_addressx == "" or
            BR_purposex == "" or
            BR_issued_dayx == "" or
            BR_issued_monthx == "" or
            BR_full_namey == "" or
            BR_year_residesy == "" or
            BR_addressy == "" or
            BR_purposey == "" or
            BR_issued_dayy == "" or
            BR_issued_monthy == ""):
            messagebox.showerror("Notice!", "The input filled must not left blank")
        else:
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BR_full_namex, self.BR_full_namey, "BR_Full_Name" ))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BR_year_residesx, self.BR_year_residesy,"BR_Year_Resides"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BR_addressx, self.BR_addressy,"BR_Address"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BR_purposex, self.BR_purposey,"BR_Purpose"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BR_issued_dayx, self.BR_issued_dayy,"BR_Issued_Day"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BR_issued_monthx, self.BR_issued_monthy,"BR_Issued_Month"))
            self.db.commit()
            messagebox.showinfo("Success", "The Form text position has been updated")
           
        

    def back_from_residency(self):
        self.revise_residency_frame.pack_forget()
        self.revise_form_frame.pack(fill = "both", expand = 1)
        
    def revise_cert_residency_student(self):
        self.revise_form_frame.pack_forget()
        self.revise_residency_student_frame = Frame(self)
        self.revise_residency_student_frame.pack(fill = "both", expand = 1)
        
        self.revise_residency_student_main_img = (Image.open("admin_bg.jpg"))
        self.revise_residency_student_main_image = self.revise_residency_student_main_img.resize((self.ws, self.hs))
        self.img_background_revise_residency_student = ImageTk.PhotoImage(self.revise_residency_student_main_image)
        self.label_revise_residency_student = Label(self.revise_residency_student_frame, image = self.img_background_revise_residency_student) 
        self.label_revise_residency_student.place(x=0, y = 0)
        
        self.residency_student_frame = Frame(self.revise_residency_student_frame, bg = "white")
        self.residency_student_frame.grid(row = 0, column = 0)
        
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_Full_Name"))
        self.res_BRS_Full_Name = self.cursor.fetchone()
        print(self.res_BRS_Full_Name)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_Age"))
        self.res_BRS_Age = self.cursor.fetchone()
        print(self.res_BRS_Age)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_Nationality"))
        self.res_BRS_Nationality = self.cursor.fetchone()
        print(self.res_BRS_Nationality)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_Year_Resides"))
        self.res_BRS_Year_Resides= self.cursor.fetchone()
        print(self.res_BRS_Year_Resides)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_DOB"))
        self.res_BRS_DOB = self.cursor.fetchone()
        print(self.res_BRS_DOB)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_POB"))
        self.res_BRS_POB = self.cursor.fetchone()
        print(self.res_BRS_POB)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_Address"))
        self.res_BRS_Address = self.cursor.fetchone()
        print(self.res_BRS_Address)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_Purpose"))
        self.res_BRS_Purpose = self.cursor.fetchone()
        print(self.res_BRS_Purpose)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_Issued_Day"))
        self.res_BRS_Issued_Day = self.cursor.fetchone()
        print(self.res_BRS_Issued_Day)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BRS_Issued_Month"))
        self.res_BRS_Issued_Month = self.cursor.fetchone()
        print(self.res_BRS_Issued_Month)
        
        BRS_full_namex = StringVar()
        BRS_agex = StringVar()
        BRS_nationalityx = StringVar()
        BRS_year_residesx = StringVar()
        BRS_dobx = StringVar()
        BRS_pobx = StringVar()
        BRS_addressx = StringVar()
        BRS_purposex = StringVar()
        BRS_issued_dayx = StringVar() 
        BRS_issued_monthx = StringVar()
        
        BRS_full_namey = StringVar()
        BRS_agey = StringVar()
        BRS_nationalityy = StringVar()
        BRS_year_residesy = StringVar()
        BRS_doby = StringVar()
        BRS_poby = StringVar()
        BRS_addressy = StringVar()
        BRS_purposey = StringVar()
        BRS_issued_dayy = StringVar() 
        BRS_issued_monthy = StringVar()
        
        self.residency_student_entryx1 = Entry (self.residency_student_frame, textvariable = BRS_full_namex)
        self.residency_student_entryx2 = Entry (self.residency_student_frame, textvariable = BRS_agex)
        self.residency_student_entryx3 = Entry (self.residency_student_frame, textvariable = BRS_nationalityx)
        self.residency_student_entryx4 = Entry (self.residency_student_frame, textvariable = BRS_year_residesx)
        self.residency_student_entryx5 = Entry (self.residency_student_frame, textvariable = BRS_dobx)
        self.residency_student_entryx6 = Entry (self.residency_student_frame, textvariable = BRS_pobx)
        self.residency_student_entryx7 = Entry (self.residency_student_frame, textvariable = BRS_addressx)
        self.residency_student_entryx8 = Entry (self.residency_student_frame, textvariable = BRS_purposex)
        self.residency_student_entryx9 = Entry (self.residency_student_frame, textvariable = BRS_issued_dayx)
        self.residency_student_entryx10 = Entry (self.residency_student_frame, textvariable = BRS_issued_monthx)
        
        self.residency_student_entryy1 = Entry (self.residency_student_frame, textvariable = BRS_full_namey)
        self.residency_student_entryy2 = Entry (self.residency_student_frame, textvariable = BRS_agey)
        self.residency_student_entryy3 = Entry (self.residency_student_frame, textvariable = BRS_nationalityy)
        self.residency_student_entryy4 = Entry (self.residency_student_frame, textvariable = BRS_year_residesy)
        self.residency_student_entryy5 = Entry (self.residency_student_frame, textvariable = BRS_doby)
        self.residency_student_entryy6 = Entry (self.residency_student_frame, textvariable = BRS_poby)
        self.residency_student_entryy7 = Entry (self.residency_student_frame, textvariable = BRS_addressy)
        self.residency_student_entryy8 = Entry (self.residency_student_frame, textvariable = BRS_purposey)
        self.residency_student_entryy9 = Entry (self.residency_student_frame, textvariable = BRS_issued_dayy)
        self.residency_student_entryy10 = Entry (self.residency_student_frame, textvariable = BRS_issued_monthy)

        self.residency_student_labelx = Label(self.residency_student_frame, text = "X-Position", bg = "white")
        self.residency_student_labely = Label(self.residency_student_frame, text = "Y-Position", bg = "white")
        self.residency_student_labelx.grid(row = 0, column = 1)
        self.residency_student_labely.grid(row = 0, column = 2)
        
        self.residency_student_label1 = Label(self.residency_student_frame, text = "Name:", bg = "white")
        self.residency_student_label2 = Label(self.residency_student_frame, text = "Age:", bg = "white")
        self.residency_student_label3 = Label(self.residency_student_frame, text = "Nationality:", bg = "white")
        self.residency_student_label4 = Label(self.residency_student_frame, text = "Year of Residency:", bg = "white")
        self.residency_student_label5 = Label(self.residency_student_frame, text = "Date of Birth:", bg = "white")
        self.residency_student_label6 = Label(self.residency_student_frame, text = "Place of Birth:", bg = "white")
        self.residency_student_label7 = Label(self.residency_student_frame, text = "Address:", bg = "white")
        self.residency_student_label8 = Label(self.residency_student_frame, text = "Purpose:", bg = "white")
        self.residency_student_label9 = Label(self.residency_student_frame, text = "Issued Day:", bg = "white")
        self.residency_student_label10 = Label(self.residency_student_frame, text = "Issued Month:", bg = "white")
        
        self.residency_student_label1.grid(row = 1, column = 0, sticky = "w")
        self.residency_student_label2.grid(row = 2, column = 0, sticky = "w")
        self.residency_student_label3.grid(row = 3, column = 0, sticky = "w")
        self.residency_student_label4.grid(row = 4, column = 0, sticky = "w")
        self.residency_student_label5.grid(row = 5, column = 0, sticky = "w")
        self.residency_student_label6.grid(row = 6, column = 0, sticky = "w")
        self.residency_student_label7.grid(row = 7, column = 0, sticky = "w")
        self.residency_student_label8.grid(row = 8, column = 0, sticky = "w")
        self.residency_student_label9.grid(row = 9, column = 0, sticky = "w")
        self.residency_student_label10.grid(row = 10, column = 0, sticky = "w")
        
        self.residency_student_entryx1.grid(row = 1, column = 1, padx = 5) 
        self.residency_student_entryx2.grid(row = 2, column = 1, pady =5)
        self.residency_student_entryx3.grid(row = 3, column = 1)
        self.residency_student_entryx4.grid(row = 4, column = 1, pady =5)
        self.residency_student_entryx5.grid(row = 5, column = 1)
        self.residency_student_entryx6.grid(row = 6, column = 1, pady =5)
        self.residency_student_entryx7.grid(row = 7, column = 1)
        self.residency_student_entryx8.grid(row = 8, column = 1, pady =5)
        self.residency_student_entryx9.grid(row = 9, column = 1)
        self.residency_student_entryx10.grid(row = 10, column = 1, pady =5)
        
        self.residency_student_entryy1.grid(row = 1, column = 2) 
        self.residency_student_entryy2.grid(row = 2, column = 2)
        self.residency_student_entryy3.grid(row = 3, column = 2)
        self.residency_student_entryy4.grid(row = 4, column = 2)
        self.residency_student_entryy5.grid(row = 5, column = 2)
        self.residency_student_entryy6.grid(row = 6, column = 2)
        self.residency_student_entryy7.grid(row = 7, column = 2)
        self.residency_student_entryy8.grid(row = 8, column = 2)
        self.residency_student_entryy9.grid(row = 9, column = 2)
        self.residency_student_entryy10.grid(row = 10, column = 2)
        
        self.residency_student_entryx1.insert(0, self.res_BRS_Full_Name[0])
        self.residency_student_entryx2.insert(0, self.res_BRS_Age[0])
        self.residency_student_entryx3.insert(0, self.res_BRS_Nationality[0])
        self.residency_student_entryx4.insert(0, self.res_BRS_Year_Resides[0])
        self.residency_student_entryx5.insert(0, self.res_BRS_DOB[0])
        self.residency_student_entryx6.insert(0, self.res_BRS_POB[0])
        self.residency_student_entryx7.insert(0, self.res_BRS_Address[0])
        self.residency_student_entryx8.insert(0, self.res_BRS_Purpose[0])
        self.residency_student_entryx9.insert(0, self.res_BRS_Issued_Day[0])
        self.residency_student_entryx10.insert(0, self.res_BRS_Issued_Month[0])
        
        self.residency_student_entryy1.insert(0, self.res_BRS_Full_Name[1])
        self.residency_student_entryy2.insert(0, self.res_BRS_Age[1])
        self.residency_student_entryy3.insert(0, self.res_BRS_Nationality[1])
        self.residency_student_entryy4.insert(0, self.res_BRS_Year_Resides[1])
        self.residency_student_entryy5.insert(0, self.res_BRS_DOB[1])
        self.residency_student_entryy6.insert(0, self.res_BRS_POB[1])
        self.residency_student_entryy7.insert(0, self.res_BRS_Address[1])
        self.residency_student_entryy8.insert(0, self.res_BRS_Purpose[1])
        self.residency_student_entryy9.insert(0, self.res_BRS_Issued_Day[1])
        self.residency_student_entryy10.insert(0, self.res_BRS_Issued_Month[1])
        
        self.button_back3 = Button(self.residency_student_frame, text = "back", command = self.back_from_residency_student)
        self.button_back3.grid(row = 11, column = 0, pady = 10, columnspan = 2)
        
        self.button_submit_residency_student = Button(self.residency_student_frame, text = "Submit", command = lambda: self.update_residency_student_form(BRS_full_namex.get(),
                                                                                                                                                                 BRS_agex.get(),
                                                                                                                                                                 BRS_nationalityx.get(),
                                                                                                                                                                 BRS_year_residesx.get(),
                                                                                                                                                                 BRS_dobx.get(),
                                                                                                                                                                 BRS_pobx.get(),
                                                                                                                                                                 BRS_addressx.get(),
                                                                                                                                                                 BRS_purposex.get(),
                                                                                                                                                                 BRS_issued_dayx.get(),
                                                                                                                                                                 BRS_issued_monthx.get(),
                                                                                                                                                                 BRS_full_namey.get(),
                                                                                                                                                                 BRS_agey.get(),
                                                                                                                                                                 BRS_nationalityy.get(),
                                                                                                                                                                 BRS_year_residesy.get(),
                                                                                                                                                                 BRS_doby.get(),
                                                                                                                                                                 BRS_poby.get(),
                                                                                                                                                                 BRS_addressy.get(),
                                                                                                                                                                 BRS_purposey.get(),
                                                                                                                                                                 BRS_issued_dayy.get(),
                                                                                                                                                                 BRS_issued_monthy.get()))
        self.button_submit_residency_student.grid(row = 11, column = 1, columnspan = 2)
        self.revise_residency_student_frame.columnconfigure(0, weight = 1)
        self.revise_residency_student_frame.rowconfigure(0, weight = 1)
        
    def update_residency_student_form(self,BRS_Full_namex,BRS_Agex, BRS_Nationalityx,
                                      BRS_Year_Residesx, BRS_Dobx, BRS_Pobx, BRS_Addressx,
                                      BRS_Purposex, BRS_Issued_dayx, BRS_Issued_monthx,
                                      BRS_Full_namey, BRS_Agey, BRS_Nationalityy,
                                      BRS_Year_Residesy, BRS_Doby, BRS_Poby,
                                      BRS_Addressy, BRS_purposey, BRS_Issued_dayy,
                                      BRS_Issued_monthy):
        self.BRS_Full_namex = BRS_Full_namex
        self.BRS_Agex = BRS_Agex
        self.BRS_Nationalityx = BRS_Nationalityx
        self.BRS_Year_Residesx = BRS_Year_Residesx
        self.BRS_Dobx = BRS_Dobx
        self.BRS_Pobx = BRS_Pobx
        self.BRS_Addressx = BRS_Addressx
        self.BRS_Purposex = BRS_Purposex
        self.BRS_Issued_dayx = BRS_Issued_dayx
        self.BRS_Issued_monthx = BRS_Issued_monthx
        self.BRS_Full_namey = BRS_Full_namey
        self.BRS_Agey = BRS_Agey
        self.BRS_Nationalityy = BRS_Nationalityy
        self.BRS_Year_Residesy = BRS_Year_Residesy
        self.BRS_Doby = BRS_Doby
        self.BRS_Poby = BRS_Poby
        self.BRS_Addressy = BRS_Addressy
        self.BRS_purposey = BRS_purposey
        self.BRS_Issued_dayy = BRS_Issued_dayy
        self.BRS_Issued_monthy = BRS_Issued_monthy

        print(self.BRS_Full_namex,
              self.BRS_Agex,
              self.BRS_Nationalityx,
              self.BRS_Year_Residesx,
              self.BRS_Dobx,
              self.BRS_Pobx,
              self.BRS_Addressx,
              self.BRS_Purposex,
              self.BRS_Issued_dayx,
              self.BRS_Issued_monthx,
              self.BRS_Full_namey,
              self.BRS_Agey,
              self.BRS_Nationalityy,
              self.BRS_Year_Residesy,
              self.BRS_Doby,
              self.BRS_Poby,
              self.BRS_Addressy,
              self.BRS_purposey,
              self.BRS_Issued_dayy,
              self.BRS_Issued_monthy)
        
        if (self.BRS_Full_namex == "" or self.BRS_Agex == "" or self.BRS_Nationalityx == "" or
            self.BRS_Year_Residesx == "" or self.BRS_Dobx == "" or self.BRS_Pobx == "" or
            self.BRS_Addressx == "" or self.BRS_Purposex == "" or self.BRS_Issued_dayx == "" or
            self.BRS_Issued_monthx == "" or self.BRS_Full_namey == "" or self.BRS_Agey == "" or
            self.BRS_Nationalityy == "" or self.BRS_Year_Residesy == "" or self.BRS_Addressy == "" or
            self.BRS_purposey == "" or self.BRS_Issued_dayy == "" or
            self.BRS_Issued_monthy == "" or self.BRS_Doby == "" or self.BRS_Poby == ""):
            messagebox.showerror("Notice!", "The input filled must not left blank")
        else:
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Full_namex, self.BRS_Full_namey, "BRS_Full_Name" ))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Agex, self.BRS_Agey,"BRS_Age"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Nationalityx, self.BRS_Nationalityy,"BRS_Nationality"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Year_Residesx, self.BRS_Year_Residesy,"BRS_Year_Resides"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Dobx, self.BRS_Doby,"BRS_DOB"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Pobx, self.BRS_Poby,"BRS_POB"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Addressx, self.BRS_Addressy,"BRS_Address"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Purposex, self.BRS_purposey,"BRS_Purpose"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Issued_dayx, self.BRS_Issued_dayy,"BRS_Issued_Day"))
            self.cursor.execute("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s", (self.BRS_Issued_monthx, self.BRS_Issued_monthy,"BRS_Issued_Month"))

            self.db.commit()
            messagebox.showinfo("Success", "The Form text position has been updated")
        
    def back_from_residency_student(self):
        self.revise_residency_student_frame.pack_forget()
        self.revise_form_frame.pack(fill = "both", expand = 1)
    
    def revise_cert_indigency(self):
        self.revise_form_frame.pack_forget()
        self.revise_indigency_frame = Frame(self)
        self.revise_indigency_frame.pack(fill = "both", expand = 1)
        
        self.revise_indigency_main_img = (Image.open("admin_bg.jpg"))
        self.revise_indigency_main_image = self.revise_indigency_main_img.resize((self.ws, self.hs))
        self.img_background_revise_indigency = ImageTk.PhotoImage(self.revise_indigency_main_image)
        self.label_revise_indigency = Label(self.revise_indigency_frame, image = self.img_background_revise_indigency) 
        self.label_revise_indigency.place(x=0, y = 0)
        self.indigency_frame = Frame(self.revise_indigency_frame, bg = "white")
        self.indigency_frame.grid(row = 0, column = 0)
        
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BI_Full_Name"))
        self.res_BI_Full_Name= self.cursor.fetchone()
        print(self.res_BI_Full_Name)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BI_Address"))
        self.res_BI_Address = self.cursor.fetchone()
        print(self.res_BI_Address)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BI_Issued_Day"))
        self.res_BI_Issued_Day = self.cursor.fetchone()
        print(self.res_BI_Issued_Day)
        self.cursor.execute("SELECT * FROM edit_form_db WHERE Form_Details = %s" , ("BI_Issued_Month"))
        self.res_BI_Issued_Month = self.cursor.fetchone()
        print(self.res_BI_Issued_Month)
        
        bi_full_namex = StringVar()
        bi_addressx = StringVar()
        bi_issued_dayx = StringVar()
        bi_issued_monthx = StringVar()
        
        bi_full_namey = StringVar()
        bi_addressy = StringVar()
        bi_issued_dayy = StringVar()
        bi_issued_monthy = StringVar()
        
        self.indigency_entryx1 = Entry (self.indigency_frame, textvariable = bi_full_namex)
        self.indigency_entryx2 = Entry (self.indigency_frame, textvariable = bi_addressx)
        self.indigency_entryx3 = Entry (self.indigency_frame, textvariable = bi_issued_dayx)
        self.indigency_entryx4 = Entry (self.indigency_frame, textvariable = bi_issued_monthx)
        
        self.indigency_entryy1 = Entry (self.indigency_frame, textvariable = bi_full_namey)
        self.indigency_entryy2 = Entry (self.indigency_frame, textvariable = bi_addressy)
        self.indigency_entryy3 = Entry (self.indigency_frame, textvariable = bi_issued_dayy)
        self.indigency_entryy4 = Entry (self.indigency_frame, textvariable = bi_issued_monthy)
        
        self.indigency_labelx = Label(self.indigency_frame, text = "X-Position", bg = "white")
        self.indigency_labely = Label(self.indigency_frame, text = "Y-Position", bg = "white")
        self.indigency_labelx.grid(row = 0, column = 1)
        self.indigency_labely.grid(row = 0, column = 2)
        
        self.indigency_label1 = Label(self.indigency_frame, text = "Name:", bg = "white")
        self.indigency_label2 = Label(self.indigency_frame, text = "Address:", bg = "white")
        self.indigency_label3 = Label(self.indigency_frame, text = "Issued Day:", bg = "white")
        self.indigency_label4 = Label(self.indigency_frame, text = "Issued Month:", bg = "white")
        
        self.indigency_label1.grid(row = 1, column = 0, sticky = "w")
        self.indigency_label2.grid(row = 2, column = 0, sticky = "w")
        self.indigency_label3.grid(row = 3, column = 0, sticky = "w")
        self.indigency_label4.grid(row = 4, column = 0, sticky = "w")
        
        self.indigency_entryx1.grid(row = 1, column = 1, padx = 5)
        self.indigency_entryx2.grid(row = 2, column = 1, pady =5)
        self.indigency_entryx3.grid(row = 3, column = 1)
        self.indigency_entryx4.grid(row = 4, column = 1, pady =5)
         
        self.indigency_entryy1.grid(row = 1, column = 2) 
        self.indigency_entryy2.grid(row = 2, column = 2)
        self.indigency_entryy3.grid(row = 3, column = 2)
        self.indigency_entryy4.grid(row = 4, column = 2)

        self.indigency_entryx1.insert(0, str(self.res_BI_Full_Name[0]))
        self.indigency_entryx2.insert(0, str(self.res_BI_Address[0]))
        self.indigency_entryx3.insert(0, str(self.res_BI_Issued_Day[0]))
        self.indigency_entryx4.insert(0, str(self.res_BI_Issued_Month[0]))

        self.indigency_entryy1.insert(0, str(self.res_BI_Full_Name[1]))
        self.indigency_entryy2.insert(0, str(self.res_BI_Address[1]))
        self.indigency_entryy3.insert(0, str(self.res_BI_Issued_Day[1]))
        self.indigency_entryy4.insert(0, str(self.res_BI_Issued_Month[1]))
        
        self.button_back2 = Button(self.indigency_frame, text = "back", command = self.back_from_indigency)
        self.button_back2.grid(row = 5, column = 0, pady = 10, columnspan = 2)
        
        self.button_submit_indigency = Button(self.indigency_frame, text = "Submit", command = lambda: self.update_indigency_form(bi_full_namex.get(),
                                                                                                                                         bi_addressx.get(),
                                                                                                                                         bi_issued_dayx.get(),
                                                                                                                                         bi_issued_monthx.get(),
                                                                                                                                         bi_full_namey.get(),
                                                                                                                                         bi_addressy.get(),
                                                                                                                                         bi_issued_dayy.get(),
                                                                                                                                         bi_issued_monthy.get()))
        self.button_submit_indigency.grid(row = 5, column = 1, columnspan = 2)
        
        self.revise_indigency_frame.columnconfigure(0, weight = 1)
        self.revise_indigency_frame.rowconfigure(0, weight = 1)
        
    def update_indigency_form(self, bi_Full_namex, bi_Addressx, bi_Issued_dayx,
                              bi_Issued_monthx, bi_Full_namey, bi_Addressy,
                              bi_Issued_dayy, bi_Issued_monthy):
        
        self.bi_Full_namex = bi_Full_namex
        self.bi_Addressx = bi_Addressx
        self.bi_Issued_dayx = bi_Issued_dayx
        self.bi_Issued_monthx =bi_Issued_monthx
        self.bi_Full_namey = bi_Full_namey
        self.bi_Addressy = bi_Addressy
        self.bi_Issued_dayy = bi_Issued_dayy
        self.bi_Issued_monthy = bi_Issued_monthy
        
        if (self.bi_Full_namex == "" or self.bi_Addressx == "" or
            self.bi_Issued_dayx == "" or self.bi_Issued_monthx == "" or
            self.bi_Full_namey == "" or self.bi_Addressy == "" or
            self.bi_Issued_dayy == "" or self.bi_Issued_monthy == ""):
            messagebox.showerror("Notice!", "The input filled must not left blank")
            print(self.bi_Full_namex, self.bi_Addressx, self.bi_Issued_dayx,
                  self.bi_Issued_monthx, self.bi_Full_namey, self.bi_Addressy,
                  self.bi_Issued_dayy, self.bi_Issued_monthy)
        else:
            self.cursor.execute ("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s" ,(self.bi_Full_namex, self.bi_Full_namey, "BI_Full_Name"))
            self.cursor.execute ("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s" ,(self.bi_Addressx, self.bi_Addressy, "BI_Address"))
            self.cursor.execute ("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s" ,(self.bi_Issued_dayx, self.bi_Issued_dayy, "BI_Issued_Day"))
            self.cursor.execute ("UPDATE edit_form_db SET `X-Position` = %s, `Y-Position` = %s WHERE Form_Details = %s" ,(self.bi_Issued_monthx, self.bi_Issued_monthy, "BI_Issued_Month"))
            self.db.commit()
            messagebox.showinfo("Success", "The Form text position has been updated")
        
    def back_from_indigency(self):
        self.revise_indigency_frame.pack_forget()
        self.revise_form_frame.pack(fill = "both", expand = 1)

    def back_from_revise_form(self):
        self.revise_form_frame.pack_forget()
        self.Main_Frame.pack(fill = "both", expand =1)

    def _resize_image(self,event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.detail_bg.configure(image =  self.background_image)
        
    def logout(self):
        self.Main_Frame.pack_forget()
        self.login_frame.pack(fill = "both", expand = 1)
        
    def register_user(self):
        self.Main_Frame.pack_forget()
        
        self.register_user_frame = Frame(self)
        self.register_user_frame.pack(fill = "both", expand = 1)
        self.user_name_frame = Frame(self.register_user_frame)
        self.user_name_frame.grid(row = 0, column = 0)
                
        self.user_register_img = (Image.open("admin_bg.jpg"))
        self.user_register_image= self.user_register_img.resize((self.ws, self.hs))
        self.img_user_register = ImageTk.PhotoImage(self.user_register_image)
        self.label_register_user = Label(self.register_user_frame, image = self.img_user_register) 
        self.label_register_user.place(x=0, y = 0)
        
        self.header_frame_user = Frame(self.register_user_frame, bg = "white")
        self.header_frame_user.grid(row = 0, column = 0, sticky = "w", pady = 10)
        
        self.name_frame_user = Frame(self.register_user_frame, bg = "white")
        self.name_frame_user.grid(row = 1, column = 0, sticky = "w", pady = 10, padx = 25)
        
        self.frame_add_user = Frame(self.register_user_frame, bg = "white")
        self.frame_add_user.grid(row = 3, column = 0, sticky = "w", pady = 10, padx = 25)
        
        self.birth_frame_user = Frame(self.register_user_frame, bg = "white")
        self.birth_frame_user.grid(row = 4, column = 0, sticky = "w", pady = 10, padx = 25)
        
        self.year_frame_user = Frame(self.register_user_frame, bg = "White")
        self.year_frame_user.grid(row = 5, column = 0, sticky = "w", pady = 10, padx = 25)
        
        self.log_frame_user = Frame(self.register_user_frame, bg = "white")
        self.log_frame_user.grid(row = 6, column = 0, sticky = "w", padx = 25)
        
        first_name_user = StringVar()
        middle_name_user = StringVar()
        last_name_user = StringVar()
        sex_user = StringVar()
        birth_year_user= StringVar()
        birth_month_user = StringVar()
        birth_day_user = StringVar()
        civil_status_user = StringVar()
        year_of_residency_user = StringVar()
        address_user = StringVar()
        contact_no_user = StringVar()
        place_of_birth_user = StringVar()
        security_question_user = StringVar()
        answer_user = StringVar()
        self.p_user = StringVar()

        self.label_head = Label(self.header_frame_user, text = "Personal Data Sheet",bg = "white", font = ("Times New Roman", 25))
        self.label_head.grid(row = 0, column = 0, sticky = "w")

        self.label_first_name = Label(self.name_frame_user, text = "First Name",bg = "white")
        self.label_first_name.grid(row = 0, column = 0, sticky = "w")
        self.entry_first_name = Entry(self.name_frame_user, textvariable = first_name_user,bg = "white")
        self.entry_first_name.grid(row = 1, column = 0)        

        self.label_middle_name = Label(self.name_frame_user, text = "Middle Name",bg = "white")
        self.label_middle_name.grid(row = 0, column = 1, sticky = "w", padx = 20)
        self.entry_middle_name = Entry(self.name_frame_user, textvariable = middle_name_user,bg = "white")
        self.entry_middle_name.grid(row = 1, column = 1, padx = 20)
        
        self.label_last_name = Label(self.name_frame_user, text = "Last Name",bg = "white")
        self.label_last_name.grid(row = 0, column = 2)
        self.entry_last_name = Entry(self.name_frame_user, textvariable = last_name_user,bg = "white")
        self.entry_last_name.grid(row = 1, column = 2)
        
        
        self.address_user = "Brgy. Wawa III, Rosario, Cavite"
        self.label_address = Label(self.frame_add_user, text = "Address",bg = "white")
        self.label_address.grid(row = 0, column = 0, sticky = "w")
        self.entry_address = Entry(self.frame_add_user, width = "40", textvariable = address_user,bg = "white")
        self.entry_address.grid(row = 1, column = 0)
        
        self.default_add = Label(self.frame_add_user, text = self.address_user,bg = "white")
        self.default_add.grid(row = 1, column = 1)
        
        self.label_birth_day = Label(self.birth_frame_user, text = "Birth Day",bg = "white")
        self.label_birth_day.grid(row = 0, column = 0, sticky = "w")

        self.date_frame_user = Frame(self.birth_frame_user)
        self.date_frame_user.grid(row = 1, column = 0)
        
        year_now = datetime.date.today().year
        year_choices = list(range(year_now-50, year_now+1))
        self.option_birth_yr = ttk.Combobox(self.date_frame_user, state = "readonly", textvariable = birth_year_user, width= "6", values = year_choices)
        self.option_birth_yr.grid(row = 0, column = 0)

        month_choices = ['1','2','3','4','5','6','7','8','9','10','11','12']
        
        self.option_birth_mm = ttk.Combobox(self.date_frame_user, state = "readonly", textvariable = birth_month_user, width = "3", values = month_choices)
        self.option_birth_mm.grid(row = 0, column =1)

        day_choices = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        
        self.option_birth_mm = ttk.Combobox(self.date_frame_user, state = "readonly", textvariable = birth_day_user, width = "3", values = day_choices)
        self.option_birth_mm.grid(row = 0, column =2, padx = 5)


        self.label_place_of_birth = Label(self.birth_frame_user, text = "Place of Birth",bg = "white")
        self.label_place_of_birth.grid(row = 0, column = 1, sticky = "w", padx = 20)
        self.entry_place_of_birth = Entry(self.birth_frame_user, textvariable = place_of_birth_user, bg = "white",width = "44")
        self.entry_place_of_birth.grid(row = 1, column = 1, sticky = "w", padx = 20)
             
        self.label_year_of_residency = Label(self.year_frame_user, text = "Year of Residency",bg = "white")
        self.label_year_of_residency.grid(row = 0, column = 0, sticky = "w")
            
        self.option_year_of_residency = ttk.Combobox(self.year_frame_user, state = "readonly", textvariable = year_of_residency_user, width= "6", values = year_choices)
        self.option_year_of_residency.grid(row = 1, column = 0, sticky = "w")
        
        self.label_sex = Label(self.year_frame_user, text = "Sex", bg = "white")
        self.label_sex.grid(row = 0, column = 1, sticky = "w", padx = 15)

        self.option_list_sex = ["Male", "Female"]
        self.option = ttk.Combobox(self.year_frame_user, state = "readonly", width = "7", textvariable = sex_user, values = self.option_list_sex)
        self.option.grid(row = 1, column = 1, padx = 15)
                
        self.label_civil_status = Label(self.year_frame_user, text = "Civil Status",bg = "white")
        self.label_civil_status.grid(row = 0, column = 2, padx = 12)

        self.option_list_cs = ["Single", "Married", "Widow", "Separated", "Live-in", "Unkown"]
        self.option_cs = ttk.Combobox(self.year_frame_user, state = "readonly", width = "12", textvariable = civil_status_user, values = self.option_list_cs)
        self.option_cs.grid(row = 1, column = 2, padx = 12)

        self.contact_no_lbl = Label(self.year_frame_user, text = "Contact No.",bg = "white")
        self.contact_no_lbl.grid(row = 0, column = 3, sticky = "w", padx = 10)
        self.entry_contact_no = Entry(self.year_frame_user, textvariable = contact_no_user,bg = "white")
        self.entry_contact_no.grid(row = 1, column = 3, padx = 10)        
        
        self.sec_qa_frame =Frame(self.register_user_frame, bg = "white")
        self.sec_qa_frame.grid(row = 7, column = 0, sticky = "w", pady = 10, padx = 25)
         
        self.label_question = Label(self.sec_qa_frame, text = "Security Question",bg = "white")
        self.label_question.grid(row= 0, column = 0, sticky = "w")
        
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
        
        self.question_list= ttk.Combobox(self.sec_qa_frame, state = "readonly",width = "43", textvariable = security_question_user, values = self.question_list)

        self.question_list.grid(row = 1, column = 0)

        self.answer_label = Label(self.sec_qa_frame, text = "Answer", bg ="white")
        self.answer_label.grid(row = 0, column = 1, sticky = "w")
        self.answer_entry = Entry(self.sec_qa_frame, textvariable = answer_user)
        self.answer_entry.grid(row = 1, column = 1, padx = 10)
        
        self.button_frame_user = Frame(self.register_user_frame, bg = "white")
        self.button_frame_user.grid(row = 8, column = 0 , sticky = "w")
        
        
        self.upload_img_frame = Frame(self.button_frame_user, bg = "white")
        self.upload_img_frame.grid(row = 0, column = 0, sticky = "w")
        
        self.submit_frame_user = Frame(self.button_frame_user, bg = "white")
        self.submit_frame_user.grid(row = 0, column = 1, sticky = "w")
        
        self.empty_space=Label(self.upload_img_frame, width = 15, height = 7, bg = "white")
        self.empty_space.grid(row = 0, column = 0, sticky = "w", padx = 40, pady = 20)
        
        self.upload_photo_button_user = Button(self.upload_img_frame, text = "Upload a Photo", bg ="white", command = self.upload_image_user)
        self.upload_photo_button_user.grid(row = 0, column = 1)
       
        
        
        
        self.button_submit_user = Button(self.submit_frame_user, text = "Proceed to Step 2",bg = "white", command = lambda: self.step2_registration(first_name_user.get(),
                                                                                                                                              middle_name_user.get(),
                                                                                                                                              last_name_user.get(), sex_user.get(),
                                                                                                                                              birth_year_user.get(),
                                                                                                                                              birth_month_user.get(),
                                                                                                                                              birth_day_user.get(),
                                                                                                                                              civil_status_user.get(),
                                                                                                                                              year_of_residency_user.get(),
                                                                                                                                              address_user.get(),
                                                                                                                                              place_of_birth_user.get(),
                                                                                                                                              contact_no_user.get(),
                                                                                                                                              security_question_user.get(),
                                                                                                                                              answer_user.get()))
        self.button_submit_user.grid(row = 0, column = 2, sticky = "w", padx = 40)

        self.back_button = Button(self.submit_frame_user, text = "Back",bg = "white", command = self.back_to_main_page_fuser)
        self.back_button.grid(row = 1, column = 2, pady = 10, padx = 40)
    
    def step2_registration(self, first_name, middle_name, last_name, sex, birth_year, birth_month, birth_day, civil_status, year_of_residency, address, place_of_birth, contact_no, security_question, answer):
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
        print (contact_no)
        print (security_question)
        print (answer)
        
        self.first_name  = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.sex = sex
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.civil_status = civil_status
        self.year_of_residency = year_of_residency
        self.address = address
        self.place_of_birth = place_of_birth
        self.contact_no = contact_no
        self.security_question = security_question
        self.answer = answer

        if self.p_user == "":
            messagebox.showerror("please upload an image")
        else:
            try:
                        
                self.photo = self.filename_user                      
                self.user_photo = self.convertToBinaryData_admin(self.photo)
                
                #birth_day
                _year = int(birth_year)
                _month = int(birth_month)
                _day = int(birth_day)

                self.birth_day = datetime.date(_year, _month, _day)
                print (self.birth_day)
                if (first_name =="" or middle_name == "" or last_name == "" or sex =="" or birth_day == "" or civil_status =="" or
                    year_of_residency == "" or address =="" or place_of_birth == "" or answer == "" or self.security_question==""
                      or contact_no ==""):
                    messagebox.showerror("Error!","Please complete the information above")
                else:
                    self.register_rfid_window = Toplevel()
                
                    self.register_rfid_window.geometry("{}x{}".format(self.ws, self.hs))

                    self.rfid_register_img = (Image.open("scan_rfid.png"))
                    self.rfid_register_image= self.rfid_register_img.resize((self.ws, self.hs))
                    self.rfid_register_user = ImageTk.PhotoImage(self.rfid_register_image)
                    self.label_register_rfid = Label(self.register_rfid_window, image = self.rfid_register_user) 
                    self.label_register_rfid.place(x=0, y = 0)
                    

                    self.label_register_rfid.bind("<Enter>", self.registered_user)

            except AttributeError:
                messagebox.showerror("Error", "Please Upload an Image")
                
            except ValueError:
                messagebox.showerror("Error", "Invalid Date Input")
                
            except FileNotFoundError:
                messagebox.showerror("Error", "Please Upload an Image")
                    
    
    def registered_user(self, event):
        print (self.first_name)
        print (self.middle_name)
        print (self.last_name) 
        print (self.sex)
        print (self.birth_year)
        print (self.birth_month) 
        print (self.birth_day) 
        print (self.civil_status)
        print (self.year_of_residency)
        print (self.address)
        print (self.place_of_birth)
        print (self.contact_no)
        print (self.security_question)
        print (self.answer)
        self.register_rfid_window.update()
        id, self.text = self.reader.read()
        
        self.cursor.execute("SELECT * FROM residents_db WHERE RFID = %s", (id))
        if (self.cursor.fetchone() is not None):
            messagebox.showerror("Notice!", "RFID card is already registered, try again!", parent = self.register_rfid_window)
        else:
            self.cursor.execute ("INSERT INTO residents_db (LAST_NAME, FIRST_NAME, MIDDLE_NAME, SEX, BIRTH_DATE, CIVIL_STATUS, YEAR_OF_RESIDENCY, ADDRESS, PLACE_OF_BIRTH, SECURITY_QUESTION, ANSWER, Contact_No, IMAGE, RFID) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(self.last_name,
                                                                                                                                                                                                                                                                                                self.first_name,
                                                                                                                                                                                                                                                                                                self.middle_name,
                                                                                                                                                                                                                                                                                                self.sex,
                                                                                                                                                                                                                                                                                                self.birth_day,
                                                                                                                                                                                                                                                                                                self.civil_status,
                                                                                                                                                                                                                                                                                                self.year_of_residency,
                                                                                                                                                                                                                                                                                                self.address,
                                                                                                                                                                                                                                                                                                self.place_of_birth,
                                                                                                                                                                                                                                                                                                self.security_question,
                                                                                                                                                                                                                                                                                                self.answer,
                                                                                                                                                                                                                                                                                                self.contact_no,
                                                                                                                                                                                                                                                                                                self.user_photo,
                                                                                                                                                                                                                                                                                                id))
            messagebox.showinfo("Success", "Registration Complete", parent = self.register_rfid_window)
            self.register_rfid_window.destroy()
            self.register_user_frame.pack_forget()
            self.Main_Frame.pack(fill = "both", expand = 1)
            
    def back_to_main_page_fuser(self):
        self.register_user_frame.pack_forget()
        self.Main_Frame.pack(fill = "both", expand = 1)

    def upload_image_user(self): 
        self.filename_user = askopenfilename(title = "Open File", filetypes = (("png files", "*.png"), ("jpeg files", "*.jpeg")))
        self.upload_img_user = (Image.open(self.filename_user))
        self.upload_image_user_bg= self.upload_img_user.resize((122, 121))
        self.img_upload_user = ImageTk.PhotoImage(self.upload_image_user_bg)
        self.label_upload_user = Label(self.upload_img_frame, image = self.img_upload_user) 
        self.label_upload_user.grid(row=0, column = 0)
        self.p_user=self.filename_user
    
    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

 
        
    def register_admin(self):
        
        self.Main_Frame.pack_forget()
        self.register_admin_frame = Frame(self)
        self.register_admin_frame.pack(fill = "both", expand = 1)
        
        self.admin_register_img = (Image.open("admin_bg.jpg"))
        self.admin_register_image= self.admin_register_img.resize((self.ws, self.hs))
        self.img_admin_register = ImageTk.PhotoImage(self.admin_register_image)
        self.label_register_admin = Label(self.register_admin_frame, image = self.img_admin_register)
        self.label_register_admin.place(x=0, y = 0)
        
        self.header_frame = Frame(self.register_admin_frame, bg = "white")
        self.header_frame.grid(row = 0, column = 0, sticky = "w", pady = 10)
        
        self.name_frame = Frame(self.register_admin_frame, bg = "white")
        self.name_frame.grid(row = 1, column = 0, sticky = "w", pady = 10, padx = 25)
        
        self.frame_add = Frame(self.register_admin_frame, bg = "white")
        self.frame_add.grid(row = 3, column = 0, sticky = "w", pady = 10, padx = 25)
        
        self.year_frame = Frame(self.register_admin_frame, bg = "White")
        self.year_frame.grid(row = 5, column = 0, sticky = "w", pady = 10, padx = 25)
        
        self.birth_frame = Frame(self.register_admin_frame, bg = "white")
        self.birth_frame.grid(row = 4, column = 0, sticky = "w", pady = 10, padx = 25)
        
        self.log_frame = Frame(self.register_admin_frame, bg = "white")
        self.log_frame.grid(row = 7, column = 0, sticky = "w", pady = 10, padx = 25)
        
        self.p = StringVar()

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
        contact_no = StringVar()
        security_question_admin = StringVar()
        answer_admin = StringVar()
        username = StringVar()
        password= StringVar()
        self.confirm_password = StringVar()
        
        self.label_head = Label(self.header_frame, text = "Personal Data Sheet",bg = "white", font = ("Times New Roman", 25))
        self.label_head.grid(row = 0, column = 0, sticky = "w", padx = 10)
        
        '''
        self.space_label= Label (self.register_admin_frame, text = "\t\t", bg = "White")
        self.space_label.grid(row = 1, column = 0)
        '''
        
        self.label_first_name = Label(self.name_frame, text = "First Name", bg= "white")
        self.label_first_name.grid(row = 1, column = 0, sticky = "w")
        self.entry_first_name = Entry(self.name_frame, textvariable = first_name,bg = "white")
        self.entry_first_name.grid(row = 2, column = 0)        

        self.label_middle_name = Label(self.name_frame, text = "Middle Name",bg = "white")
        self.label_middle_name.grid(row = 1, column = 1, sticky = "w", padx = 20)
        self.entry_middle_name = Entry(self.name_frame, textvariable = middle_name,bg = "white")
        self.entry_middle_name.grid(row = 2, column = 1, padx = 20)
        
        self.label_last_name = Label(self.name_frame, text = "Last Name",bg = "white")
        self.label_last_name.grid(row = 1, column = 2, sticky = "w")
        self.entry_last_name = Entry(self.name_frame, textvariable = last_name,bg = "white")
        self.entry_last_name.grid(row = 2, column = 2)
        
        self.label_address = Label(self.frame_add, text = "Address",bg = "white")
        self.label_address.grid(row = 1, column = 0, sticky = "w")
        self.entry_address = Entry(self.frame_add, textvariable = address,bg = "white", width = "40")
        self.entry_address.grid(row = 2, column = 0, sticky = "w")
        self.lbl_address = Label(self.frame_add, text = "Brgy. Wawa III, Rosario, Cavite", bg = "white")
        self.lbl_address.grid(row = 2, column =1, sticky = "w")
        
        year_now = datetime.date.today().year
        year_choices = list(range(year_now-50, year_now+1))
        
        self.label_year_of_residency = Label(self.year_frame, text = "Year of Residency",bg = "white")
        self.label_year_of_residency.grid(row = 0, column = 0, sticky = "w")

        self.option_year_of_residency = ttk.Combobox(self.year_frame, state = "readonly", textvariable = year_of_residency, width= "8", values = year_choices)
        self.option_year_of_residency.grid(row = 1, column = 0, sticky = "w")
        
        self.label_birth_day = Label(self.birth_frame, text = "Birth Day",bg = "white")
        self.label_birth_day.grid(row = 0, column = 0, sticky = "w")
        
        self.date_frame = Frame(self.birth_frame, bg = "white")
        self.date_frame.grid(row = 1, column = 0)
                
        self.option_birth_yr = ttk.Combobox(self.date_frame, state = "readonly", textvariable = birth_year, width= "6", values = year_choices)
        self.option_birth_yr.grid(row = 1, column = 0, padx = 10, sticky = "w")
        self.option_birth_yr.set("year")
        month_choices = ['1','2','3','4','5','6','7','8','9','10','11','12']
        
        self.option_birth_mm = ttk.Combobox(self.date_frame, state = "readonly", textvariable = birth_month, width = "3", values = month_choices)
        self.option_birth_mm.grid(row = 1, column =1, sticky = "w")
        self.option_birth_mm.set("mm")
        day_choices = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
        
        self.option_birth_dd = ttk.Combobox(self.date_frame, state = "readonly", textvariable = birth_day, width = "3", values = day_choices)
        self.option_birth_dd.grid(row = 1, column =2, padx = 10, sticky = "w")
        self.option_birth_dd.set("dd")
        
        self.label_pob = Label(self.birth_frame, text = "Place of Birth",bg = "white")
        self.label_pob.grid(row = 0, column = 1, sticky = "w", padx = 20)
        self.entry_pob = Entry(self.birth_frame, textvariable = place_of_birth,bg = "white", width = "43")
        self.entry_pob.grid(row = 1, column = 1)
        
        self.label_sex = Label(self.year_frame, text = "Sex",bg = "white")
        self.label_sex.grid(row = 0, column = 2, sticky = "w", padx = 15)

        self.option_list_sex = ["Male", "Female"]
        self.option = ttk.Combobox(self.year_frame, state = "readonly", textvariable = sex, width = "7", values = self.option_list_sex)
        self.option.grid(row = 1, column = 2, padx = 15)
        
        self.label_civil_status = Label(self.year_frame, text = "Civil Status",bg = "white")
        self.label_civil_status.grid(row = 0, column = 3, sticky = "w", padx = 12)

        self.option_list_cs = ["Single", "Married", "Widow", "Separated", "Live-in", "Unkown"]
        self.option_cs = ttk.Combobox(self.year_frame, state="readonly", textvariable = civil_status, width = "12", values = self.option_list_cs)
        self.option_cs.grid(row = 1, column = 3, padx = 12, sticky = "w")

        self.lbl_contact_no = Label(self.year_frame, text = "Contact_No", bg = "white")
        self.lbl_contact_no.grid(row = 0, column = 4, sticky = "w", padx = 10)

        self.entry_contact_no = Entry(self.year_frame, textvariable = contact_no, bg = "white")
        self.entry_contact_no.grid(row = 1, column = 4, sticky = "w", padx = 10)

        self.label_usrname = Label(self.log_frame, text = "Username",bg = "white")
        self.label_usrname.grid(row = 0, column = 0, sticky = "w")
        self.entry_usrname = Entry(self.log_frame, textvariable = username,bg = "white", width = "20")
        self.entry_usrname.grid(row = 1, column = 0)
        
        self.frame_sqa_admin = Frame(self.register_admin_frame, bg = "white")
        self.frame_sqa_admin.grid(row = 6, column = 0, sticky = "w", pady = 10, padx = 25)
        
        
        self.label_question = Label(self.frame_sqa_admin, text = "Security Question",bg = "white")
        self.label_question.grid(row= 0, column = 0, sticky = "w")
        
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
        
        self.question_list= ttk.Combobox(self.frame_sqa_admin, state = "readonly",width = "43", textvariable = security_question_admin, values = self.question_list)

        self.question_list.grid(row = 1, column = 0)

        self.answer_label_admin = Label(self.frame_sqa_admin, text = "Answer", bg ="white")
        self.answer_label_admin.grid(row = 0, column = 1, sticky = "w")
        self.answer_entry_admin = Entry(self.frame_sqa_admin, textvariable = answer_admin)
        self.answer_entry_admin.grid(row = 1, column = 1, padx = 10)
        
        self.label_password = Label(self.log_frame, text = "Password",bg = "white")
        self.label_password.grid(row = 0, column = 1, padx = 20, sticky = "w")
        self.entry_password = Entry(self.log_frame, textvariable = password,show = "*", bg = "white", width = "20")
        self.entry_password.grid(row = 1, column = 1, padx = 20)
        
        self.label_confirm_pass = Label(self.log_frame, text = "Confirm Password",bg = "white")
        self.label_confirm_pass.grid(row = 0, column = 2, sticky = "w")
        self.entry_confirm_pass = Entry(self.log_frame, textvariable = self.confirm_password,show = "*",bg = "white", width = "20")
        self.entry_confirm_pass.grid(row = 1, column = 2)
        
        self.button_frame = Frame(self.register_admin_frame, bg = "white")
        self.button_frame.grid(row = 8, column = 0 , sticky = "w")
        
        self.upload_img_frame = Frame(self.button_frame, bg = "white")
        self.upload_img_frame.grid(row = 0, column = 0, sticky = "w")
        self.submit_frame = Frame(self.button_frame, bg = "white")
        self.submit_frame.grid(row = 0, column = 1, sticky = "w")
        
        self.empty_space=Label(self.upload_img_frame, width = 15, height = 7, bg = "white")
        self.empty_space.grid(row = 0, column = 0, sticky = "w", padx = 40, pady = 20)
        
        self.upload_photo_button = Button(self.upload_img_frame, text = "Upload a Photo", bg ="white", command = self.upload_image)
        self.upload_photo_button.grid(row = 0, column = 1)
        
        self.button_submit = Button(self.submit_frame, text = "Proceed to Step 2",bg = "white", command = lambda: self.registered(first_name.get(),
                                                                                                                                  middle_name.get(),
                                                                                                                                  last_name.get(), sex.get(),
                                                                                                                                  birth_year.get(),
                                                                                                                                  birth_month.get(),
                                                                                                                                  birth_day.get(),
                                                                                                                                  civil_status.get(),
                                                                                                                                  year_of_residency.get(),
                                                                                                                                  address.get(),
                                                                                                                                  place_of_birth.get(),
                                                                                                                                  contact_no.get(),
                                                                                                                                  username.get(),
                                                                                                                                  password.get(),
                                                                                                                                  security_question_admin.get(),
                                                                                                                                  answer_admin.get()))
        self.button_submit.grid(row = 0, column = 2, padx = 40)

        self.back_button = Button(self.submit_frame, text = "Back",bg = "white", command = self.back_to_main_page_fadmin)
        self.back_button.grid(row = 1, column = 2, padx = 40, pady = 10)
    

    def upload_image(self):
        
        self.filename = askopenfilename(title = "Open File", filetypes = (("png files", "*.png"), ("jpeg files", "*.jpeg"))) # show an "Open" dialog box and return the path to the selected file  
        self.admin_upload_img = (Image.open(self.filename))
        self.admin_upload_image= self.admin_upload_img.resize((122, 121))
        self.img_admin_upload = ImageTk.PhotoImage(self.admin_upload_image)
        self.label_upload_admin = Label(self.upload_img_frame, image = self.img_admin_upload)
        self.label_upload_admin.grid(row=0, column = 0)
        self.p=self.filename
        
    def back_to_main_page(self):
        self.register_user_frame.pack_forget()
        self.Main_Frame.pack(fill = "both", expand = 1)

    def convertToBinaryData_admin(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    
    def registered(self, first_name, middle_name, last_name, sex, birth_year, birth_month, birth_day, civil_status, year_of_residency, address, place_of_birth, contact_no, username, password, security_question_admin, answer_admin):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.sex = sex
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.civil_status = civil_status
        self.year_of_residency = year_of_residency
        self.address = address
        self.place_of_birth = place_of_birth
        self.contact_no = contact_no
        self.username = username
        self.password = password
        self.security_question_admin = security_question_admin
        self.answer_admin = answer_admin
        
        self.cursor.execute("SELECT * FROM residents_admin WHERE USERNAME = %s", (username))
        print("Nagawa to")
        if (self.cursor.fetchone() is not None):
            messagebox.showerror("Notice!", "Username already taken")
        elif (self.first_name =="" or self.middle_name == "" or self.last_name == "" or self.sex =="" or self.birth_day == "" or self.civil_status =="" or
            self.year_of_residency == "" or self.address =="" or self.place_of_birth == "" or self.username == "" or self.password == "" or self.confirm_password ==""
              or self.contact_no =="" or self.security_question_admin == "" or self.answer_admin == ""):
            messagebox.showerror("Error!","Please complete the information above")
        elif password !=self.confirm_password.get():
            messagebox.showerror("Notice","Password does not match")    
        else:
            try:
                self.photo = self.filename                        
                self.user_photo = self.convertToBinaryData_admin(self.photo)
                
                #birth_day
                _year = int(self.birth_year)
                _month = int(self.birth_month)
                _day = int(self.birth_day)
                
                self.birth_day = datetime.date(_year, _month, _day)
                print (self.birth_day)
                
                self.admin_register = Toplevel(self)
                self.admin_register.geometry("{}x{}".format(self.ws, self.hs))
                
                self.admin_rfid_img = (Image.open("scan_rfid.png"))
                self.admin_rfid_image = self.admin_rfid_img.resize((self.ws, self.hs))
                self.img_admin_rfid = ImageTk.PhotoImage(self.admin_rfid_image)
                self.label_rfid_admin = Label(self.admin_register, image = self.img_admin_rfid)
                self.label_rfid_admin.pack(fill="both", expand = 1)
                self.label_rfid_admin.bind("<Enter>", self.registered_data)
               
            
            except AttributeError:
                messagebox.showerror("Error", "Please upload an Image")
   
            except ValueError:
                messagebox.showerror("Error", "Invalid Date Input")
 
            except FileNotFoundError:
                messagebox.showerror("Error", "Please upload an Image")
                
    def registered_data(self, event):
        print (self.first_name)
        print (self.middle_name)
        print (self.last_name)
        print (self.sex)
        print (self.birth_year)
        print (self.birth_month)
        print (self.birth_day)
        print (self.civil_status)
        print (self.year_of_residency)
        print (self.address)
        print (self.place_of_birth)
        print (self.contact_no)
        print (self.username)
        print (self.password)
               
        if self.p == "":
            messagebox.showerror("please upload an image")
        else:
            self.id, self.text = self.reader.read()
            self.cursor.execute("SELECT * FROM residents_admin WHERE RFID = %s", (self.id))
            self.res_id = self.cursor.fetchone()
            if self.res_id:
                messagebox.showerror("Notice!", "RFID already registered")
            else:
                self.cursor.execute ("INSERT INTO residents_admin (LAST_NAME, FIRST_NAME, MIDDLE_NAME, SEX, BIRTH_DATE, CIVIL_STATUS, YEAR_OF_RESIDENCY, ADDRESS, PLACE_OF_BIRTH, Contact_No, SECURITY_QUESTION, ANSWER, IMAGE, USERNAME, PASSWORD, RFID) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(self.last_name,
                                                                                                                                                                                                                                                                                                                                   self.middle_name,
                                                                                                                                                                                                                                                                                                                                   self.first_name,
                                                                                                                                                                                                                                                                                                                                   self.sex,
                                                                                                                                                                                                                                                                                                                                   self.birth_day,
                                                                                                                                                                                                                                                                                                                                   self.civil_status,
                                                                                                                                                                                                                                                                                                                                   self.year_of_residency,
                                                                                                                                                                                                                                                                                                                                   self.address,
                                                                                                                                                                                                                                                                                                                                   self.place_of_birth,
                                                                                                                                                                                                                                                                                                                                   self.contact_no,
                                                                                                                                                                                                                                                                                                                                   self.security_question_admin,
                                                                                                                                                                                                                                                                                                                                   self.answer_admin,
                                                                                                                                                                                                                                                                                                                                   self.user_photo,
                                                                                                                                                                                                                                                                                                                                   self.username,
                                                                                                                                                                                                                                                                                                                                   self.password,
                                                                                                                                                                                                                                                                                                                                   self.id))
                self.db.commit()
                messagebox.showinfo("Success", "Registration Complete", parent = self.admin_register)
                self.admin_register.destroy()
                self.register_admin_frame.pack_forget()
                self.Main_Frame.pack(fill = "both", expand = 1)
            

    def back_to_main_page_fadmin(self):
        self.register_admin_frame.pack_forget()
        self.Main_Frame.pack(fill = "both", expand = 1)

    def update_user(self):
        self.Main_Frame.pack_forget()
        self.update_frame = Frame(self)
        self.update_frame.pack(fill = "both", expand = 1)
        
        self.top = Frame(self.update_frame, bg = "white")
        self.top.grid(row = 0, column = 0, pady = 5)

        self.bottom = Frame(self.update_frame, bg = "white")
        self.bottom.grid(row = 3, column = 0, pady = 5)

        self.search_bar = StringVar()
        self.search_entry = Entry(self.top, width = 80, bg = "white", textvariable = self.search_bar)
        self.search_entry.grid(row = 0, column = 1)
        self.search_bar.trace("w", self.search_data)
        self.reset_button = Button(self.top, text = "refresh", bg = "white", command = self.reset_data)
        self.reset_button.grid(row = 0, column = 3)
        
        
        self.tree = ttk.Treeview(self.update_frame, selectmode="browse", columns = (1,2,3,4,5,6,7,8,9,10), height = 27, show = "headings")
        self.tree.grid(row = 1, column = 0)

        self.update_button = Button(self.bottom, text = "Update Details", bg = "white", command = self.update_data)
        self.update_button.grid(row = 0, column = 0, padx=5)
        
        self.update_RFID = Button(self.bottom, text = "Update RFID", bg = "white", command = self.update_RFID_user)
        self.update_RFID.grid(row = 0, column = 1)

        self.update_finger_button = Button(self.bottom, text = "Update Image", bg = "white", command = self.update_image_user)
        self.update_finger_button.grid(row = 0, column = 2, padx=5)
        
        self.back_button = Button(self.bottom, text = "Back", bg = "white", command = self.back_to_main_page_fupdateu)
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
        
        self.tree.column(1,stretch=True, width = 50)
        self.tree.column(2,stretch=True, width = 100)
        self.tree.column(3,stretch=True, width = 100)
        self.tree.column(4,stretch=True, width = 100)
        self.tree.column(5,stretch=True, width = 100)
        self.tree.column(6,stretch=True, width = 100)
        self.tree.column(7,stretch=True, width = 100)
        self.tree.column(8,stretch=True, width = 100)
        self.tree.column(9,stretch=True, width = 150)
        self.tree.column(10,stretch=True, width = 100)
        
        self.scrolly = Scrollbar(self.update_frame, orient="vertical", command=self.tree.yview)
        self.scrolly.grid(row = 1, column = 1, sticky = "nesw")
        
        self.scrollx = Scrollbar(self.update_frame, orient="horizontal", command=self.tree.xview)
        self.scrollx.grid(row = 2, column = 0, sticky = "nesw")
        
        self.tree.configure(yscrollcommand=self.scrolly.set)
        self.tree.configure(xscrollcommand=self.scrollx.set)
        
        self.cursor.execute("SELECT * FROM residents_db")
        self.fetch = self.cursor.fetchall()
        
        for data in self.fetch:
            self.tree.insert('', 'end', values=(data))
            
    def back_to_main_page_fupdateu(self):
        self.update_frame.destroy()
        self.Main_Frame.pack(fill = "both", expand = 1)
        
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
                
                
    def update_image_user(self):
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        if (list_values == ""):
            messagebox.showerror('Notice!', "Please Select a row")
        else:
            
            self.update_frame.pack_forget()
            self.update_image_frame = Frame(self)
            self.update_image_frame.pack(fill = "both", expand = 1)
            
            self.img_update_info_user = (Image.open("admin_bg.jpg"))
            self.image_update_info_user = self.img_update_info_user.resize((self.ws,self.hs))
            self.img_background_update_info_user = ImageTk.PhotoImage(self.image_update_info_user)
            self.imglabel_update_info_user = Label(self.update_image_frame, image = self.img_background_update_info_user)
            self.imglabel_update_info_user.place(x=0,y=0)
            
            self.update_image_frame2 = Frame(self.update_image_frame)
            self.update_image_frame2.grid(row =0, column = 0)
            
            self.up_update_image_frame2 = Frame(self.update_image_frame2)
            self.up_update_image_frame2.grid(row = 0, column = 0)
            
            self.down_update_image_frame2 = Frame(self.update_image_frame2)
            self.down_update_image_frame2.grid(row = 1, column = 0)
            
            self.empty_space=Label(self.up_update_image_frame2, width = 15, height = 7, bg = "white")
            self.empty_space.grid(row = 0, column = 0, sticky = "w", padx = 40, pady = 20)
            
            self.upload_photo_button = Button(self.up_update_image_frame2, text = "Upload a Photo", bg ="white", command = self.upload_updated_image_user)
            self.upload_photo_button.grid(row = 0, column = 1)
            
            self.button_submit = Button(self.down_update_image_frame2, text = "Submit",bg = "white", command=self.updated_image_user)
            self.button_submit.grid(row = 0, column = 1, padx = 10)

            self.back_button = Button(self.down_update_image_frame2, text = "Back",bg = "white", command = self.back_update_page_fuser)
            self.back_button.grid(row = 0, column = 0)        
            
            self.update_image_frame.columnconfigure(0, weight = 1)
            self.update_image_frame.rowconfigure(0, weight = 1)
            
            
    def convertToBinaryData_user_update(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    
    def upload_updated_image_user(self):
        self.filename_update = askopenfilename(title = "Open File", filetypes = (("png files", "*.png"), ("jpeg files", "*.jpeg"))) # show an "Open" dialog box and return the path to the selected file  
        self.user_upload_img_update = (Image.open(self.filename_update))
        self.user_upload_image_update = self.user_upload_img_update.resize((122, 121))
        self.img_user_upload_update = ImageTk.PhotoImage(self.user_upload_image_update)
        self.label_upload_user_update = Label(self.up_update_image_frame2, image = self.img_user_upload_update)
        self.label_upload_user_update.grid(row=0, column = 0)
        
    def updated_image_user(self):
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        try:
            photo = self.filename_update                        
            user_photo = self.convertToBinaryData_user_update(photo)
            self.cursor.execute ("UPDATE residents_db SET IMAGE = %s WHERE ID = %s" ,(user_photo, str(list_values[0])))
            messagebox.showinfo("Success!","Your Image has been updated")
            self.update_image_frame.pack_forget()
            self.update_frame.pack(fill = "both", expand = 1)
        except:
            messagebox.showerror("Notice!", "Please upload an Image")
            
    def back_update_page_fuser(self):
        self.update_image_frame.pack_forget()
        self.update_frame.pack(fill = "both", expand = 1)
        
        
    def update_RFID_user(self):
        
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        if (list_values == ""):
            messagebox.showerror('Notice!', "Please Select a Row")
        else:   
            self.update_rfid_window = Toplevel()
                    
            self.update_rfid_window.geometry("{}x{}".format(self.ws, self.hs))

            self.rfid_update_img = (Image.open("scan_rfid.png"))
            self.rfid_update_image= self.rfid_update_img.resize((self.ws, self.hs))
            self.rfid_update_user = ImageTk.PhotoImage(self.rfid_update_image)
            self.label_update_rfid = Label(self.update_rfid_window, image = self.rfid_update_user) 
            self.label_update_rfid.place(x=0, y = 0)
                        

            self.label_update_rfid.bind("<Enter>", self.updated_RFID_user)
        
    def updated_RFID_user(self, event):
        self.update_rfid_window.update()
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        print(list_values)
        
        try:
            id, self.text = self.reader.read()
            self.cursor.execute("SELECT * FROM residents_db WHERE RFID = %s", str(id))
            if (self.cursor.fetchone() is not None):
                messagebox.showerror("Notice!", "RFID card is already registered\nPlease try again", parent = self.update_rfid_window)
                self.update_rfid_window.destroy()                
            else:
                self.cursor.execute("SELECT * FROM residents_db WHERE RFID = %s", str(id))
                if (self.cursor.fetchone() is not None):
                    messagebox.showerror("Notice!", "RFID card is already registered\nPlease try again", parent = self.update_rfid_window)
                    self.update_rfid_window.destroy()
                else:
                    self.cursor.execute ("UPDATE residents_db SET RFID = %s WHERE ID = %s" ,(str(id), str(list_values[0])))
                    messagebox.showinfo("Success!","Your RFID has been updated successfully", parent = self.update_rfid_window)
                    self.update_rfid_window.destroy()
        except:
            GPIO.cleanup()
        
    def update_data(self):
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        
        if (list_values == ""):
            messagebox.showerror('Error!', "Please Select a Row", parent = self)
        else:
            self.first_name_user_update = StringVar()
            self.middle_name_user_update = StringVar()
            self.last_name_user_update = StringVar()
            self.sex_user_update = StringVar()
            self.birth_year_user_update= StringVar()
            self.birth_month_user_update = StringVar()
            self.birth_day_user_update = StringVar()
            self.civil_status_user_update = StringVar()
            self.year_of_residency_user_update = StringVar()
            self.address_user_update = StringVar()
            self.contact_no_user_update = StringVar()
            self.place_of_birth_user_update = StringVar()
            self.security_question_user_update = StringVar()
            self.answer_user_update = StringVar()
            
            self.update_frame.pack_forget()
            self.update_data_frame = Frame(self)
            self.update_data_frame.pack(fill = "both", expand = 1)
            
            self.img_update_info = (Image.open("admin_bg.jpg"))
            self.image_update_info = self.img_update_info.resize((self.ws,self.hs))
            self.img_background_update_info = ImageTk.PhotoImage(self.image_update_info)
            self.imglabel_update_info = Label(self.update_data_frame, image = self.img_background_update_info)
            self.imglabel_update_info.place(x=0,y=0)
            
            self.header_frame_user_update = Frame(self.update_data_frame, bg = "white")
            self.header_frame_user_update.grid(row = 0, column = 0, sticky = "w", pady = 10)
            
            self.name_frame_user_update = Frame(self.update_data_frame, bg = "white")
            self.name_frame_user_update.grid(row = 1, column = 0, sticky = "w", pady = 10, padx = 25)
            
            self.frame_add_user_update = Frame(self.update_data_frame, bg = "white")
            self.frame_add_user_update.grid(row = 3, column = 0, sticky = "w", pady = 10, padx = 25)
            
            self.year_frame_user_update = Frame(self.update_data_frame, bg = "White")
            self.year_frame_user_update.grid(row = 5, column = 0, sticky = "w", pady = 10, padx = 25)
            
            self.birth_frame_user_update = Frame(self.update_data_frame, bg = "white")
            self.birth_frame_user_update.grid(row = 4, column = 0, sticky = "w", pady = 10, padx = 25)
            
            self.log_frame_user_update = Frame(self.update_data_frame, bg = "white")
            self.log_frame_user_update.grid(row = 6, column = 0, sticky = "w", pady = 10, padx = 25)
            
            self.label_head_update = Label(self.header_frame_user_update, text = "Update Personal Data Sheet",bg = "white", font = ("Times New Roman", 25))
            self.label_head_update.grid(row = 0, column = 0, sticky = "w")

            self.label_first_name_update = Label(self.name_frame_user_update, text = "First Name",bg = "white")
            self.label_first_name_update.grid(row = 0, column = 0, sticky = "w")
            self.entry_first_name_update = Entry(self.name_frame_user_update, textvariable = self.first_name_user_update,bg = "white")
            self.entry_first_name_update.grid(row = 1, column = 0)        
            
            if str(list_values[2]) != "":
                self.entry_first_name_update.insert(0,str(list_values[2]))
            
            self.label_middle_name_update = Label(self.name_frame_user_update, text = "Middle Name",bg = "white")
            self.label_middle_name_update.grid(row = 0, column = 1, sticky = "w", padx = 20)
            self.entry_middle_name_update = Entry(self.name_frame_user_update, textvariable = self.middle_name_user_update,bg = "white")
            self.entry_middle_name_update.grid(row = 1, column = 1, padx = 20)
            
            if str(list_values[3]) != "":
                self.entry_middle_name_update.insert(0,str(list_values[3]))
            
            self.label_last_name_update = Label(self.name_frame_user_update, text = "Last Name",bg = "white")
            self.label_last_name_update.grid(row = 0, column = 2)
            self.entry_last_name_update = Entry(self.name_frame_user_update, textvariable = self.last_name_user_update,bg = "white")
            self.entry_last_name_update.grid(row = 1, column = 2)
            
            if str(list_values[1]) != "":
                self.entry_last_name_update.insert(0,str(list_values[1]))
            
            
            self.label_address_user_update ="Brgy. Wawa III, Rosario, Cavite"
            self.label_address_update = Label(self.frame_add_user_update, text = "Address",bg = "white")
            self.label_address_update.grid(row = 0, column = 0, sticky = "w")
            self.entry_address_update = Entry(self.frame_add_user_update, width = "40", textvariable = self.address_user_update,bg = "white")
            self.entry_address_update.grid(row = 1, column = 0)
            
            if str(list_values[8]) != "":
                self.entry_address_update.insert(0,str(list_values[8]))
            
            self.default_add_update = Label(self.frame_add_user_update, text = self.label_address_user_update,bg = "white")
            self.default_add_update.grid(row = 1, column = 1)
            
            if str(list_values[5]) != "":
                year, month, day = list_values[5].split('-')
                self.label_birth_day_update = Label(self.birth_frame_user_update, text = "Birth Day",bg = "white")
                self.label_birth_day_update.grid(row = 0, column = 0, sticky = "w")

                self.date_frame_user_update = Frame(self.birth_frame_user_update)
                self.date_frame_user_update.grid(row = 1, column = 0)
                
                year_now_update = datetime.date.today().year
                year_choices_update = list(range(year_now_update-50, year_now_update+1))
                self.option_birth_yr_update = ttk.Combobox(self.date_frame_user_update, state = "readonly", textvariable = self.birth_year_user_update, width= "6", values = year_choices_update)
                self.option_birth_yr_update.grid(row = 0, column = 0)

                month_choices_update = ['1','2','3','4','5','6','7','8','9','10','11','12']
                
                self.option_birth_mm_update= ttk.Combobox(self.date_frame_user_update, state = "readonly", textvariable = self.birth_month_user_update, width = "3", values = month_choices_update)
                self.option_birth_mm_update.grid(row = 0, column =1)

                day_choices_update = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
                
                self.option_birth_dd_update = ttk.Combobox(self.date_frame_user_update, state = "readonly", textvariable = self.birth_day_user_update, width = "3", values = day_choices_update)
                self.option_birth_dd_update.grid(row = 0, column =2, padx = 5)
                self.option_birth_yr_update.set(year)
                self.option_birth_mm_update.set(month)
                self.option_birth_dd_update.set(day)
            
            self.label_place_of_birth_update = Label(self.birth_frame_user_update, text = "Place of Birth",bg = "white")
            self.label_place_of_birth_update.grid(row = 0, column = 1, sticky = "w", padx = 20)
            self.entry_place_of_birth_update = Entry(self.birth_frame_user_update, textvariable = self.place_of_birth_user_update, bg = "white",width = "44")
            self.entry_place_of_birth_update.grid(row = 1, column = 1, sticky = "w", padx = 20)
        
            if str(list_values[9]) != "":
                self.entry_place_of_birth_update.insert(0,str(list_values[9]))
             
            self.label_year_of_residency_update = Label(self.year_frame_user_update, text = "Year of Residency",bg = "white")
            self.label_year_of_residency_update.grid(row = 0, column = 0, sticky = "w")
            
            
            self.option_yor_update = ttk.Combobox(self.year_frame_user_update, state = "readonly", textvariable = self.year_of_residency_user_update, width= "6", values = year_choices_update)
            self.option_yor_update.grid(row = 1, column = 0, sticky = "w")
            if str(list_values[7]) != "":
                self.option_yor_update.set(str(list_values[7]))
             
            
            self.label_sex_update = Label(self.year_frame_user_update, text = "Sex", bg = "white")
            self.label_sex_update.grid(row = 0, column = 1, sticky = "w", padx = 15)

            self.option_list_sex_update = ["Male", "Female"]
            self.option_update = ttk.Combobox(self.year_frame_user_update, state = "readonly", width = "7", textvariable = self.sex_user_update, values = self.option_list_sex_update)
            self.option_update.grid(row = 1, column = 1, padx = 15)
            
            if str(list_values[4]) != "":
                self.option_update.set(str(list_values[4]))
                     
            self.label_civil_status_update = Label(self.year_frame_user_update, text = "Civil Status",bg = "white")
            self.label_civil_status_update.grid(row = 0, column = 2, padx = 12)
            
            
            self.option_list_cs_update = ["Single", "Married", "Widow", "Separated", "Live-in", "Unkown"]
            self.option_cs_update = ttk.Combobox(self.year_frame_user_update, state = "readonly", width = "12", textvariable = self.civil_status_user_update, values = self.option_list_cs_update)
            self.option_cs_update.grid(row = 1, column = 2, padx = 12)
            
            if str(list_values[6]) != "":
                self.option_cs_update.set(list_values[6])
             
            self.contact_no_lbl_update = Label(self.year_frame_user_update, text = "Contact No.",bg = "white")
            self.contact_no_lbl_update.grid(row = 0, column = 3, sticky = "w", padx = 10)
            self.entry_contact_no_update = Entry(self.year_frame_user_update, textvariable = self.contact_no_user_update,bg = "white")
            self.entry_contact_no_update.grid(row = 1, column = 3, padx = 10)        
            
            if str(list_values[12]) != "":
                self.entry_contact_no_update.insert(0, str(list_values[12]))
             
            self.sec_qa_frame_update =Frame(self.update_data_frame, bg = "white")
            self.sec_qa_frame_update.grid(row = 7, column = 0, sticky = "w", pady = 10, padx = 25)
             
            self.label_question_update = Label(self.sec_qa_frame_update, text = "Security Question",bg = "white")
            self.label_question_update.grid(row= 0, column = 0, sticky = "w")
            
            self.question_list_update = ["What was your childhood nickname?",
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
            
            self.question_list_update_dd= ttk.Combobox(self.sec_qa_frame_update, state = "readonly",width = "43", textvariable = self.security_question_user_update, values = self.question_list_update)
            self.question_list_update_dd.grid(row = 1, column = 0)
            if str(list_values[10]) != "":
                self.question_list_update_dd.set(str(list_values[10]))
             
            self.answer_label_update = Label(self.sec_qa_frame_update, text = "Answer", bg ="white")
            self.answer_label_update.grid(row = 0, column = 1, sticky = "w")
            self.answer_entry_update = Entry(self.sec_qa_frame_update, textvariable = self.answer_user_update)
            self.answer_entry_update.grid(row = 1, column = 1, padx = 10)
            if str(list_values[11]) != "":
                self.answer_entry_update.insert(0,str(list_values[11]))
             
            self.button_frame_user_update = Frame(self.update_data_frame, bg = "white")
            self.button_frame_user_update.grid(row = 8, column = 0 , sticky = "nsew")
            
            
            
            self.button_submit_user_update = Button(self.button_frame_user_update, text = "Proceed to Step 2",bg = "white", command = lambda: self.updated_user_data(self.first_name_user_update.get(),
                                                                                                                                                  self.middle_name_user_update.get(),
                                                                                                                                                  self.last_name_user_update.get(), self.sex_user_update.get(),
                                                                                                                                                  self.birth_year_user_update.get(),
                                                                                                                                                  self.birth_month_user_update.get(),
                                                                                                                                                  self.birth_day_user_update.get(),
                                                                                                                                                  self.civil_status_user_update.get(),
                                                                                                                                                  self.year_of_residency_user_update.get(),
                                                                                                                                                  self.address_user_update.get(),
                                                                                                                                                  self.place_of_birth_user_update.get(),
                                                                                                                                                  self.contact_no_user_update.get(),
                                                                                                                                                  self.security_question_user_update.get(),
                                                                                                                                                  self.answer_user_update.get()))
            self.button_submit_user_update.grid(row = 0, column = 2, sticky = "w", padx = 220)
            
            self.back_button_update = Button(self.button_frame_user_update, text = "Back",bg = "white", command = self.back_from_update_data)
            self.back_button_update.grid(row = 1, column = 2, pady = 10, padx = 220)
            

    def updated_user_data(self, update_first_name, update_middle_name, update_last_name, update_sex, update_birth_year, update_birth_month, update_birth_day, update_civil_status, update_year_of_residency, update_address, update_place_of_birth, update_contact_no, update_security_question, update_answer):
        
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        
        print (update_first_name)
        print (update_middle_name)
        print (update_last_name)
        print (update_sex)
        print (update_birth_year)
        print (update_birth_month)
        print (update_birth_day)
        print (update_civil_status)
        print (update_year_of_residency)
        print (update_address)
        print (update_place_of_birth)
        print (update_contact_no)
        print (update_security_question)
        print (update_answer)
        
        _year = int(update_birth_year)
        _month = int(update_birth_month)
        _day = int(update_birth_day)
        update_birth_day = datetime.date(_year, _month, _day)
        
        if (update_first_name == "" or update_middle_name == "" or
            update_last_name == "" or update_sex == "" or  update_birth_year == "" or
            update_birth_month == "" or update_birth_day == "" or  update_civil_status == "" or
            update_year_of_residency == "" or update_address == "" or
            update_place_of_birth == "" or update_contact_no == "" or update_security_question == "" or
            update_answer == ""):
            messagebox.showerror("Notice!", "Please Update all the required data")
        else:
            self.cursor.execute ("UPDATE residents_db SET LAST_NAME = %s, FIRST_NAME = %s, MIDDLE_NAME = %s, SEX = %s, BIRTH_DATE = %s, CIVIL_STATUS = %s, YEAR_OF_RESIDENCY = %s, ADDRESS = %s, PLACE_OF_BIRTH = %s, SECURITY_QUESTION = %s, ANSWER = %s, Contact_No = %s WHERE ID = %s",(update_last_name,
                                                                                                                                                                                                                                                                                         update_first_name,
                                                                                                                                                                                                                                                                                         update_middle_name,
                                                                                                                                                                                                                                                                                         update_sex,
                                                                                                                                                                                                                                                                                         update_birth_day,
                                                                                                                                                                                                                                                                                         update_civil_status,
                                                                                                                                                                                                                                                                                         update_year_of_residency,
                                                                                                                                                                                                                                                                                         update_address,
                                                                                                                                                                                                                                                                                         update_place_of_birth,
                                                                                                                                                                                                                                                                                         update_security_question,
                                                                                                                                                                                                                                                                                         update_answer,
                                                                                                                                                                                                                                                                                         update_contact_no,
                                                                                                                                                                                                                                                                                         str(list_values[0])))
            messagebox.showinfo("Success!","The details have been updated", parent = self)
            self.update_data_frame.destroy()
            self.update_frame.pack(fill = "both", expand = 1)
                        
            self.db.commit()


        
    def back_from_update_data(self):
        self.update_data_frame.destroy()
        self.update_frame.pack(fill = "both", expand =1)
    '''===================================================================='''
    
    def update_admin(self):
        
        self.Main_Frame.pack_forget()
        self.update_frame_admin = Frame(self)
        self.update_frame_admin.pack(fill = "both", expand = 1)
        
        self.top = Frame(self.update_frame_admin, bg = "white")
        self.top.grid(row = 0, column = 0, pady = 5)

        self.bottom = Frame(self.update_frame_admin, bg = "white")
        self.bottom.grid(row = 3, column = 0, pady = 5)

        self.search_bar = StringVar()
        self.search_entry = Entry(self.top, width = 80, bg = "white", textvariable = self.search_bar)
        self.search_entry.grid(row = 0, column = 1)
        self.search_bar.trace("w", self.search_data)
        self.reset_button = Button(self.top, text = "refresh", bg = "white", command = self.reset_data)
        self.reset_button.grid(row = 0, column = 3)
        
        
        self.tree = ttk.Treeview(self.update_frame_admin, selectmode="browse", columns = (1,2,3,4,5,6,7,8,9,10), height = 27, show = "headings")
        self.tree.grid(row = 1, column = 0)

        self.update_button = Button(self.bottom, text = "Update Details", bg = "white", command = self.update_data_admin)
        self.update_button.grid(row = 0, column = 0, padx=5)

        self.update_finger_button = Button(self.bottom, text = "Update Image", bg = "white", command = self.update_image_admin)
        self.update_finger_button.grid(row = 0, column = 1)
        
        self.back_button = Button(self.bottom, text = "Back", bg = "white", command = self.back_to_mp_update_ad)
        self.back_button.grid(row = 0, column = 2, padx = 5)
        
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
        
        self.tree.column(1,stretch=True, width = 50)
        self.tree.column(2,stretch=True, width = 100)
        self.tree.column(3,stretch=True, width = 100)
        self.tree.column(4,stretch=True, width = 100)
        self.tree.column(5,stretch=True, width = 100)
        self.tree.column(6,stretch=True, width = 100)
        self.tree.column(7,stretch=True, width = 100)
        self.tree.column(8,stretch=True, width = 100)
        self.tree.column(9,stretch=True, width = 150)
        self.tree.column(10,stretch=True, width = 100)
        
        self.scrolly = Scrollbar(self.update_frame_admin, orient="vertical", command=self.tree.yview)
        self.scrolly.grid(row = 1, column = 1, sticky = "nesw")
        
        self.scrollx = Scrollbar(self.update_frame_admin, orient="horizontal", command=self.tree.xview)
        self.scrollx.grid(row = 2, column = 0, sticky = "nesw")
        
        self.tree.configure(yscrollcommand=self.scrolly.set)
        self.tree.configure(xscrollcommand=self.scrollx.set)
        
        self.cursor.execute("SELECT * FROM residents_admin")
        self.fetch = self.cursor.fetchall()
        
        for data in self.fetch:
            self.tree.insert('', 'end', values=(data))
    
    def update_data_admin(self):
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        
        print(list_values[0])
        print(list_values[1])
        print(list_values[2])
        print(list_values[3])
        print(list_values[4])
        print(list_values[5])
        print(list_values[6])
        print(list_values[7])
        print(list_values[8])
        print(list_values[9])
        print(list_values[10])
        print(list_values[11])
        print(list_values[12])
        print(list_values[13])
        if (list_values == ""):
            messagebox.showerror('Error!', "Please Select a Row", parent = self)
        else:
            self.update_frame_admin.pack_forget()
            self.update_admin_frame = Frame(self)
            self.update_admin_frame.pack(fill = "both", expand = 1)
            
            self.admin_update_img = (Image.open("admin_bg.jpg"))
            self.admin_update_image= self.admin_update_img.resize((self.ws, self.hs))
            self.img_admin_update = ImageTk.PhotoImage(self.admin_update_image)
            self.label_update_admin = Label(self.update_admin_frame, image = self.img_admin_update) 
            self.label_update_admin.place(x=0, y = 0)
            
            self.header_frame_update_admin = Frame(self.update_admin_frame, bg = "white")
            self.header_frame_update_admin.grid(row = 0, column = 0, sticky = "w", pady = 10)
            
            self.name_frame_update_admin = Frame(self.update_admin_frame, bg = "white")
            self.name_frame_update_admin.grid(row = 1, column = 0, sticky = "w", pady = 10, padx = 25)
            
            self.frame_add_update_admin = Frame(self.update_admin_frame, bg = "white")
            self.frame_add_update_admin.grid(row = 3, column = 0, sticky = "w", pady = 10, padx = 25)
            
            self.year_frame_update_admin = Frame(self.update_admin_frame, bg = "White")
            self.year_frame_update_admin.grid(row = 5, column = 0, sticky = "w", pady = 10, padx = 25)
            
            self.birth_frame_update_admin = Frame(self.update_admin_frame, bg = "white")
            self.birth_frame_update_admin.grid(row = 4, column = 0, sticky = "w", pady = 10, padx = 25)
            
            self.log_frame_update_admin = Frame(self.update_admin_frame, bg = "white")
            self.log_frame_update_admin.grid(row = 6, column = 0, sticky = "w", pady = 10, padx = 25)
            

            self.first_name_update_admin = StringVar()
            self.middle_name_update_admin = StringVar()
            self.last_name_update_admin = StringVar()
            self.sex_update_admin = StringVar()
            self.birth_year_update_admin= StringVar()
            self.birth_month_update_admin = StringVar()
            self.birth_day_update_admin = StringVar()
            self.civil_status_update_admin = StringVar()
            self.year_of_residency_update_admin = StringVar()
            self.address_update_admin = StringVar()
            self.place_of_birth_update_admin = StringVar()
            self.contact_no_update_admin = StringVar()
            self.username_update_admin = StringVar()
            self.password_update_admin = StringVar()
            self.confirm_password_update_admin = StringVar()
            
            self.label_head_update_admin = Label(self.header_frame_update_admin, text = "Personal Data Sheet",bg = "white", font = ("Times New Roman", 25))
            self.label_head_update_admin.grid(row = 0, column = 0, sticky = "w", padx = 10)
            
            '''
            self.space_label= Label (self.update_admin_frame, text = "\t\t", bg = "White")
            self.space_label.grid(row = 1, column = 0)
            '''
            
            self.label_first_name_update_admin = Label(self.name_frame_update_admin, text = "First Name", bg= "white")
            self.label_first_name_update_admin.grid(row = 1, column = 0, sticky = "w")
            self.entry_first_name_update_admin = Entry(self.name_frame_update_admin, textvariable = self.first_name_update_admin,bg = "white")
            self.entry_first_name_update_admin.grid(row = 2, column = 0)        
            
            if str(list_values[2]) != "":
                self.entry_first_name_update_admin.insert(0, str(list_values[2]))
                
            self.label_middle_name_update_admin = Label(self.name_frame_update_admin, text = "Middle Name",bg = "white")
            self.label_middle_name_update_admin.grid(row = 1, column = 1, sticky = "w", padx = 20)
            self.entry_middle_name_update_admin = Entry(self.name_frame_update_admin, textvariable = self.middle_name_update_admin,bg = "white")
            self.entry_middle_name_update_admin.grid(row = 2, column = 1, padx = 20)
            
            if str(list_values[3]) != "":
                self.entry_middle_name_update_admin.insert(0, str(list_values[3]))
            
            self.label_last_name_update_admin = Label(self.name_frame_update_admin, text = "Last Name",bg = "white")
            self.label_last_name_update_admin.grid(row = 1, column = 2, sticky = "w")
            self.entry_last_name_update_admin = Entry(self.name_frame_update_admin, textvariable = self.last_name_update_admin,bg = "white")
            self.entry_last_name_update_admin.grid(row = 2, column = 2)
            if str(list_values[1]) != "":
                self.entry_last_name_update_admin.insert(0, str(list_values[1]))
            
            self.label_address_update_admin = Label(self.frame_add_update_admin, text = "Address",bg = "white")
            self.label_address_update_admin.grid(row = 1, column = 0, sticky = "w")
            self.entry_address_update_admin = Entry(self.frame_add_update_admin, textvariable = self.address_update_admin,bg = "white", width = "40")
            self.entry_address_update_admin.grid(row = 2, column = 0, sticky = "w")
            self.lbl_address_update_admin = Label(self.frame_add_update_admin, text = "Brgy. Wawa III, Rosario, Cavite", bg = "white")
            self.lbl_address_update_admin.grid(row = 2, column =1, sticky = "w")
            
            if str(list_values[8]) != "":
                self.entry_address_update_admin.insert(0, str(list_values[8]))
            
            year_now_update_admin = datetime.date.today().year
            year_choices_update_admin = list(range(year_now_update_admin-50, year_now_update_admin+1))
            
            self.label_year_of_residency_update_admin = Label(self.year_frame_update_admin, text = "Year of Residency",bg = "white")
            self.label_year_of_residency_update_admin.grid(row = 0, column = 0, sticky = "w")
            
            self.option_year_of_residency_update_admin = ttk.Combobox(self.year_frame_update_admin, state = "readonly", textvariable = self.year_of_residency_update_admin, width= "8", values = year_choices_update_admin)
            self.option_year_of_residency_update_admin.grid(row = 1, column = 0, sticky = "w")
            if str(list_values[7]) != "":
                self.option_year_of_residency_update_admin.set(list_values[7])

            self.label_birth_day_update_admin = Label(self.birth_frame_update_admin, text = "Birth Day",bg = "white")
            self.label_birth_day_update_admin.grid(row = 0, column = 0, sticky = "w")
            
            self.date_frame_update_admin = Frame(self.birth_frame_update_admin, bg = "white")
            self.date_frame_update_admin.grid(row = 1, column = 0)
            
            self.option_birth_yr_update_admin = ttk.Combobox(self.date_frame_update_admin, state = "readonly", textvariable = self.birth_year_update_admin, width= "6", values = year_choices_update_admin)
            self.option_birth_yr_update_admin.grid(row = 1, column = 0, padx = 10)
            month_choices_update_admin = ['1','2','3','4','5','6','7','8','9','10','11','12']
            
            self.option_birth_mm_update_admin = ttk.Combobox(self.date_frame_update_admin, state = "readonly", textvariable = self.birth_month_update_admin, width = "3", values = month_choices_update_admin)
            self.option_birth_mm_update_admin.grid(row = 1, column =1)
            day_choices_update_admin = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
            
            self.option_birth_dd_update_admin = ttk.Combobox(self.date_frame_update_admin, state = "readonly", textvariable = self.birth_day_update_admin, width = "3", values = day_choices_update_admin)
            self.option_birth_dd_update_admin.grid(row = 1, column =2, padx = 10)
            
            yr, mm, dd = list_values[5].split('-')
            if str(list_values[5]) != "":
                self.option_birth_yr_update_admin.set(yr)
            if str(list_values[5]) != "":
                self.option_birth_mm_update_admin.set(mm)
            if str(list_values[5]) != "":
                self.option_birth_dd_update_admin.set(dd)
                
            self.label_pob_update_admin = Label(self.birth_frame_update_admin, text = "Place of Birth",bg = "white")
            self.label_pob_update_admin.grid(row = 0, column = 1, sticky = "w")
            self.entry_pob_update_admin = Entry(self.birth_frame_update_admin, textvariable = self.place_of_birth_update_admin,bg = "white", width = "43")
            self.entry_pob_update_admin.grid(row = 1, column = 1)
            if str(list_values[9]) != "":
                self.entry_pob_update_admin.insert(0, str(list_values[9]))
            
            self.label_sex = Label(self.year_frame_update_admin, text = "Sex",bg = "white")
            self.label_sex.grid(row = 0, column = 2, sticky = "w", padx = 15)

            self.option_list_sex_update_admin = ["Male", "Female"]
            self.option_update_admin = ttk.Combobox(self.year_frame_update_admin, state = "readonly", textvariable = self.sex_update_admin, width = "7", values = self.option_list_sex_update_admin)
            self.option_update_admin.grid(row = 1, column = 2, padx = 15)
            if str(list_values[4]) != "":
                self.option_update_admin.set(list_values[4])
            
            self.label_civil_status_update_admin = Label(self.year_frame_update_admin, text = "Civil Status",bg = "white")
            self.label_civil_status_update_admin.grid(row = 0, column = 3, sticky = "w", padx = 12)

            self.option_list_cs_update_admin = ["Single", "Married", "Widow", "Separated", "Live-in", "Unkown"]
            self.option_cs_update_admin = ttk.Combobox(self.year_frame_update_admin, state="readonly", textvariable = self.civil_status_update_admin, width = "12", values = self.option_list_cs_update_admin)
            self.option_cs_update_admin.grid(row = 1, column = 3, padx = 12, sticky = "w")
            if str(list_values[6]) != "":
                self.option_cs_update_admin.set(list_values[6])
            
            self.lbl_contact_no_update_admin = Label(self.year_frame_update_admin, text = "Contact_No", bg = "white")
            self.lbl_contact_no_update_admin.grid(row = 0, column = 4, sticky = "w", padx = 10)

            self.entry_contact_no_update_admin = Entry(self.year_frame_update_admin, textvariable = self.contact_no_update_admin, bg = "white")
            self.entry_contact_no_update_admin.grid(row = 1, column = 4, sticky = "w", padx = 10)
            
            if str(list_values[10]) != "":
                self.entry_contact_no_update_admin.insert(0, list_values[10])
            
            self.label_usrname_update_admin = Label(self.log_frame_update_admin, text = "Username",bg = "white")
            self.label_usrname_update_admin.grid(row = 0, column = 0, padx = 80, sticky = "w")
            self.entry_usrname_update_admin = Entry(self.log_frame_update_admin, textvariable = self.username_update_admin,bg = "white", width = "20")
            self.entry_usrname_update_admin.grid(row = 1, column = 0, padx = 80)
            
            if str(list_values[12]) != "":
                self.entry_usrname_update_admin.insert(0, list_values[12])
            
            self.label_password_update_admin = Label(self.log_frame_update_admin, text = "Password",bg = "white")
            self.label_password_update_admin.grid(row = 0, column = 1, sticky = "w")
            self.entry_password_update_admin = Entry(self.log_frame_update_admin, textvariable = self.password_update_admin, show = "*", bg = "white", width = "20")
            self.entry_password_update_admin.grid(row = 1, column = 1)
            if str(list_values[13]) != "":
                self.entry_password_update_admin.insert(0, list_values[13])
            
            
            self.button_frame_update_admin = Frame(self.update_admin_frame, bg = "white")
            self.button_frame_update_admin.grid(row = 7, column = 0 , sticky = "w")
            
            self.submit_frame_update_admin = Frame(self.button_frame_update_admin, bg = "white")
            self.submit_frame_update_admin.grid(row = 0, column = 0, sticky = "w")
           
            self.button_submit_update_admin = Button(self.submit_frame_update_admin, text = "Submit",bg = "white", command = lambda: self.updated_admin(self.first_name_update_admin.get(),
                                                                                                                                                        self.middle_name_update_admin.get(),
                                                                                                                                                        self.last_name_update_admin.get(),
                                                                                                                                                        self.sex_update_admin.get(),
                                                                                                                                                        self.birth_year_update_admin.get(),
                                                                                                                                                        self.birth_month_update_admin.get(),
                                                                                                                                                        self.birth_day_update_admin.get(),
                                                                                                                                                        self.civil_status_update_admin.get(),
                                                                                                                                                        self.year_of_residency_update_admin.get(),
                                                                                                                                                        self.address_update_admin.get(),
                                                                                                                                                        self.place_of_birth_update_admin.get(),
                                                                                                                                                        self.contact_no_update_admin.get(),
                                                                                                                                                        self.username_update_admin.get(),
                                                                                                                                                        self.password_update_admin.get()))
            self.button_submit_update_admin.grid(row = 0, column = 2, padx = 230)

            self.back_button_update_admin = Button(self.submit_frame_update_admin, text = "Back",bg = "white", command = self.back_fupdate_tupdate)
            self.back_button_update_admin.grid(row = 1, column = 2, padx = 230, pady = 5)
    
    def back_fupdate_tupdate(self):
        self.update_admin_frame.pack_forget()
        self.update_frame_admin.pack(fill = "both", expand =1)
        
    def updated_admin(self, update_admin_first_name, update_admin_middle_name, update_admin_last_name, update_admin_sex, update_admin_birth_year, update_admin_birth_month, update_admin_birth_day, update_admin_civil_status, update_admin_year_of_residency, update_admin_address, update_admin_place_of_birth, update_admin_contact_no, update_admin_username, update_admin_password):
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        
        print (update_admin_last_name)
        print (update_admin_first_name)
        print (update_admin_middle_name)
        print (update_admin_sex)
        print (update_admin_birth_year)
        print (update_admin_birth_month)
        print (update_admin_birth_day)
        print (update_admin_civil_status)
        print (update_admin_year_of_residency)
        print (update_admin_address)
        print (update_admin_place_of_birth)
        print (update_admin_contact_no)
        print (update_admin_username)
        print (update_admin_password)
        
        _year_update_admin = int(update_admin_birth_year)
        _month_update_admin = int(update_admin_birth_month)
        _day_update_admin = int(update_admin_birth_day)
        update_admin_birth_day = datetime.date(_year_update_admin, _month_update_admin, _day_update_admin)
        
        if (update_admin_last_name == "" or update_admin_first_name == "" or
            update_admin_middle_name == "" or update_admin_sex == "" or  update_admin_birth_year == "" or
            update_admin_birth_month == "" or update_admin_birth_day == "" or  update_admin_civil_status == "" or
            update_admin_year_of_residency == "" or update_admin_address == "" or
            update_admin_place_of_birth == "" or update_admin_contact_no == "" or update_admin_username == "" or
            update_admin_password == ""):
            messagebox.showerror("Notice!", "Please Update all the required data")
        else:
            self.cursor.execute ("UPDATE residents_admin SET LAST_NAME = %s, FIRST_NAME = %s, MIDDLE_NAME = %s, SEX = %s, BIRTH_DATE = %s, CIVIL_STATUS = %s, YEAR_OF_RESIDENCY = %s, ADDRESS = %s, PLACE_OF_BIRTH = %s, Contact_No = %s, USERNAME = %s, PASSWORD = %s WHERE ID = %s",(update_admin_last_name,
                                                                                                                                                                                                                                                                                       update_admin_first_name,
                                                                                                                                                                                                                                                                                       update_admin_middle_name,
                                                                                                                                                                                                                                                                                       update_admin_sex,
                                                                                                                                                                                                                                                                                       update_admin_birth_day,
                                                                                                                                                                                                                                                                                       update_admin_civil_status,
                                                                                                                                                                                                                                                                                       update_admin_year_of_residency,
                                                                                                                                                                                                                                                                                       update_admin_address,
                                                                                                                                                                                                                                                                                       update_admin_place_of_birth,
                                                                                                                                                                                                                                                                                       update_admin_contact_no,
                                                                                                                                                                                                                                                                                       update_admin_username,
                                                                                                                                                                                                                                                                                       update_admin_password,
                                                                                                                                                                                                                                                                                       str(list_values[0])))
            messagebox.showinfo("Success!","The details have been updated", parent = self)
            self.update_admin_frame.destroy()
            self.update_frame_admin.pack(fill = "both", expand = 1)
                        
            self.db.commit()
    
    def convertToBinaryData_admin_update(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def update_image_admin(self):
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        if (list_values == ""):
            messagebox.showerror('Notice!', "Please Select a row")
        else:
            self.update_frame_admin.pack_forget()
            self.update_admin_image_frame = Frame(self)
            self.update_admin_image_frame.pack(fill = "both", expand = 1)
            
            self.img_update_info_admin = (Image.open("admin_bg.jpg"))
            self.image_update_info_admin = self.img_update_info_admin.resize((self.ws,self.hs))
            self.img_background_update_info_admin = ImageTk.PhotoImage(self.image_update_info_admin)
            self.imglabel_update_info_admin = Label(self.update_admin_image_frame, image = self.img_background_update_info_admin)
            self.imglabel_update_info_admin.place(x=0, y=0)
            
            self.update_admin_image_frame2 = Frame(self.update_admin_image_frame, bg = "white")
            self.update_admin_image_frame2.grid(row = 0, column = 0)
            self.up_update_admin_image_frame2 = Frame(self.update_admin_image_frame2, bg = "white")
            self.up_update_admin_image_frame2.grid(row = 0, column = 0)
            self.down_update_admin_image_frame2 = Frame(self.update_admin_image_frame2, bg = "white")
            self.down_update_admin_image_frame2.grid(row = 1, column = 0)
            
            self.empty_space_admin=Label(self.update_admin_image_frame2, width = 15, height = 7, bg = "white")
            self.empty_space_admin.grid(row = 0, column = 0, sticky = "w", padx = 40, pady = 20)
            
            self.upload_admin_photo_button = Button(self.update_admin_image_frame2, text = "Upload a Photo", bg ="white", command = self.upload_updated_image_admin)
            self.upload_admin_photo_button.grid(row = 0, column = 1)
            
            self.button_submit_admin = Button(self.down_update_admin_image_frame2, text = "Submit",bg = "white", command=self.updated_image_admin)
            self.button_submit_admin.grid(row = 0, column = 1)

            self.back_button_admin = Button(self.down_update_admin_image_frame2, text = "Back",bg = "white", command = self.back_update_page_fadmin)
            self.back_button_admin.grid(row = 0, column = 0, padx = 10)
            
            self.update_admin_image_frame.columnconfigure(0, weight = 1)
            self.update_admin_image_frame.rowconfigure(0, weight = 1)        
    
    def upload_updated_image_admin(self):
        self.filename_update_admin = askopenfilename(title = "Open File", filetypes = (("png files", "*.png"), ("jpeg files", "*.jpeg"))) # show an "Open" dialog box and return the path to the selected file  
        self.admin_upload_img_update = (Image.open(self.filename_update_admin))
        self.admin_upload_image_update = self.admin_upload_img_update.resize((122, 121))
        self.img_admin_upload_update = ImageTk.PhotoImage(self.admin_upload_image_update)
        self.label_upload_user_update = Label(self.update_admin_image_frame2, image = self.img_admin_upload_update)
        self.label_upload_user_update.grid(row=0, column = 0)
        
    def updated_image_admin(self):
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        
        try:
                
            photo_admin = self.filename_update_admin                        
            user_photo_admin = self.convertToBinaryData_admin_update(photo_admin)
            self.cursor.execute ("UPDATE residents_admin SET IMAGE = %s WHERE ID = %s" ,(user_photo_admin, str(list_values[0])))
            messagebox.showinfo("Success!","Your Image has been updated")
            self.update_admin_image_frame.pack_forget()
            self.update_frame_admin.pack(fill = "both", expand = 1)
            
        except:
            messagebox.showerror("Notice!", "Please upload an image")
            
    def back_update_page_fadmin(self):
        self.update_admin_image_frame.pack_forget()
        self.update_frame_admin.pack(fill = "both", expand = 1)
        
    def back_to_mp_update_ad(self):
        self.update_frame_admin.pack_forget()
        self.Main_Frame.pack(fill = "both", expand = 1)
    
if __name__ == "__main__":
    admin_system().mainloop()
