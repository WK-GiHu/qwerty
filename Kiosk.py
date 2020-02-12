from tkinter import *
from VKeyboard import VKeyboard
import pymysql
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import register_user


class Kiosk(Tk):
    def __init__(self):
        super().__init__()
        VKeyboard(self)
        
        self.login_rfid_button = Button(self, text = "Login",width = 20,command = self.choose_user, bg= "white")
        self.login_rfid_button.pack(pady = 10)
        
        self.close_button = Button(self, text="Close", bg = "white",width = 20, command=self.destroy)
        self.close_button.pack(pady = 10)
                       
    #Main window after login#           
    def choose_user(self):
        messagebox.showinfo("Successful Login!","Welcome")
            
        self.master_choose_form_user = Toplevel()
        self.master_choose_form_user.attributes("-fullscreen", True)
        
        self.brgy_clearance = Button(self.master_choose_form_user, text = "Barangay Clearance", width = 30, height = 5,bg = "white")
        self.brgy_clearance .grid(row = 0 , column = 0, padx = 70, pady = 15)
        
        self.brgy_certification = Button(self.master_choose_form_user, text = "Barangay Certification", width = 30, height = 5, bg = "white")
        self.brgy_certification.grid(row = 0 , column = 1, padx = 70, pady = 15)
        
        self.certificate_of_residency = Button(self.master_choose_form_user, text = "Certificate of Residency", width = 30, height = 5, bg = "white")
        self.certificate_of_residency.grid(row = 1 , column = 0, padx = 70, pady = 15)
        
        self.certificate_of_cohabitation = Button(self.master_choose_form_user, text = "Certificate of Residency for Student", width = 30, height = 5,bg = "white")
        self.certificate_of_cohabitation.grid(row = 1 , column = 1, padx = 70, pady = 15)
        
        self.certificate_of_indigency = Button(self.master_choose_form_user, text = "Certificate of Indigency", width = 30, height = 5, bg = "white")
        self.certificate_of_indigency.grid(row = 2 , column = 0, padx = 70, pady = 15)
        
        self.certificate_of_late_registry =Button(self.master_choose_form_user, text = "Certificate of Late Registry", width = 30, height = 5,bg = "white")
        self.certificate_of_late_registry.grid(row = 2 , column = 1, padx = 70, pady = 15)
        
        self.business_permit = Button(self.master_choose_form_user, text = "Barangay Business Permit", width = 30, height = 5,bg = "white")
        self.business_permit.grid(row = 3 , column = 0, padx = 70, pady = 15)
        
        self.business_permit = Button(self.master_choose_form_user, text = "Back to LOGIN", width = 30, height = 5,bg = "white", command = self.master_choose_form_user.destroy)
        self.business_permit.grid(row = 3 , column = 1, padx = 70, pady = 15)
    
        self.register_user_button = Button(self.master_choose_form_user, text = "Register User", width = 20, height = 3, bg = "white", command = self.register)
        self.register_user_button.place(x = 850, y = 250)
        
        
#=============================update module for residents===========================#    
    
    def register(self):
        register_user.Registration_User()

if __name__ == "__main__":
    Kiosk().mainloop()

