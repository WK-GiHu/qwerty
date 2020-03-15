from tkinter import *
import threading
import pymysql
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from PIL import Image, ImageTk
import datetime
from FingerprintDevice import FingerprintThread
from VKeyboard import VKeyboard

import update_residents
import update_admins

class RFIDThread(threading.Thread):
    def __init__(self, app, callback):
        super().__init__(daemon = True)
        result = None
        self.app = app
        self.app.bind('<<GRANT_ACCESS>>', callback)
        self.start()
    
    def run(self):
        self.db = pymysql.connect(host = "192.168.1.9",port = 3306, user = "root",passwd = "justin",db= "thesis_main")
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        self.reader = SimpleMFRC522()
        while True:
            self.id, text = self.reader.read()
            self.cursor.execute("SELECT * FROM residents_admin WHERE RFID = %s",str(self.id))
            RFIDThread.result = self.cursor.fetchone()
            print(RFIDThread.result)
            if RFIDThread.result: 
                messagebox.showinfo("Success!", "Welcome")
                self.app.event_generate('<<GRANT_ACCESS>>', state = 11, when='tail')
            else:
                self.cursor.execute("SELECT * FROM residents_db WHERE RFID = %s", str(self.id))
                RFIDThread.result = self.cursor.fetchone()
                print(RFIDThread.result)
                if RFIDThread.result: 
                    messagebox.showinfo("Success!", "Welcome")
                    self.app.event_generate('<<GRANT_ACCESS>>', state = 12, when='tail')
                else:
                    messagebox.showerror("Warning!","Your RFID card is not yet registered!")


class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.attributes("-fullscreen", True)
        self.funcid = self.bind('<Button-1>', self.on_button_clicked)
        
        label = Label(self, text = "NO ANNOUNCEMENT YET!!!", bg = "white")
        label.pack(fill = "both", expand =1)
        
    def on_button_clicked(self, event):
        print('SplashScreen.on_button_click')
        self.unbind('<Button-1>', funcid=self.funcid)
        self.master.event_generate('<<IDLE>>', state = 1, when='tail')
        self.destroy()
         
        
class IdleCounter(threading.Thread):
    label = 'idle'

    def __init__(self, app):
        super().__init__(daemon=True)
        self.app = app

        self.timeout = 20
        self._counter = self.timeout

        self.start()
        self.app.bind('<<IDLE>>', self.on_idle)

    def run(self):
        print('run()'.format())
        
        while True:
            if self._counter > 0:
                self._counter -= 1
                
                if self._counter == 0:
                    self.app.event_generate('<<TIMEOUT>>', when='tail')
                    
            time.sleep(1)
                    
        print('IdleCounter terminated'.format())
        
    def on_idle(self, event):
        if event.state == 1:
            self._counter = self.timeout
        elif self._counter > 0 and event.state == 0:
            self._counter = self.timeout

class Kiosk(tk.Tk):
    def __init__(self):
        super().__init__()
        VKeyboard(self)
        self.camb25 = font.Font(family='Cambria', size=25)
        font.families()
        
        self.db = pymysql.connect(host = "192.168.1.9",port = 3306, user = "root",passwd = "justin",db= "thesis_main")
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
        
        self.attributes("-fullscreen", True)
        self.img = (Image.open("login_bg.jpg"))
        self.image = self.img.resize((self.ws,self.hs))
        self.img_background = ImageTk.PhotoImage(self.image)
        self.imglabel = Label(self, image = self.img_background).place(x=0,y=0)
        self.img2 = ImageTk.PhotoImage(Image.open("rosario_logo.png"))
        
        self.fp = FingerprintThread(self)
        self.bind('<<FINGERPRINT>>', self.on_fingerprint)
        
        RFIDThread(self, callback = self.on_grant_access)
        IdleCounter(self)
        self.bind('<<TIMEOUT>>', self.on_timeout)
        
        GPIO.setwarnings(False)
        self.configure(bg="white")
        self.geometry("{}x{}".format(self.ws, self.hs))
        #self.T_printer = Usb(0x0fe6, 0x811e, 98, 0x82, 0x02)
    
    def on_fingerprint(self, event):
        print('on_fingerprint()  template_id={}'.format(event.state)) 
        if event.state >= 0:
            template_id = event.state
            self.cursor.execute("SELECT * FROM residents_admin WHERE FINGER_TEMPLATE = %s", template_id)
            event.result = self.cursor.fetchone()
            print (event.result) 
            if event.result: 
                event.state = 1
                return self.on_grant_access(event)
            else: 
                self.cursor.execute("SELECT * FROM residents_db WHERE FINGER_TEMPLATE = %s", template_id) 
                event.result = self.cursor.fetchone() 
                print (event.result) 
                if event.result:
                    event.state = 2
                    return self.on_grant_access(event)
               
        messagebox.showerror("Warning!","Your fingerprint is not yet registered!") 

    def on_timeout(self, event):
        SplashScreen(self)
                  
    def on_grant_access(self, event):
        print('Kiosk.on_grant_access()')
        if event.state <10:
            self.details = event.result
            self.firstn = self.details[3]
            self.middlen = self.details[2]
            self.lastn = self.details[1]
            self.SEX = self.details[4]
            self.dob = self.details[5]
            self.civils = self.details[6]
            self.year_resides = self.details[7]
            self.address = self.details[8]
            self.pob = self.details[9]
            self.cn = self.details[10]
            self.sq1 = self.details[11]
            self.ans = self.details[12]
            self.image = self.details[13]
            self.rf = self.details [16]
            self.age = self.calculate_age(self.dob)
            print(self.age)
            print ("Finger Thread")
            print (self.details)
            if event.state == 1:
                self.choose_admin()
            elif event.state == 2:
                self.choose_user()            
        else:
            self.details = RFIDThread.result
            self.firstn = self.details[3]
            self.middlen = self.details[2]
            self.lastn = self.details[1]
            self.SEX = self.details[4]
            self.dob = self.details[5]
            self.civils = self.details[6]
            self.year_resides = self.details[7]
            self.address = self.details[8]
            self.pob = self.details[9]
            self.cn = self.details[10]
            self.sq1 = self.details[11]
            self.ans = self.details[12]
            self.image = self.details[13]
            self.rf = self.details [16]
            self.age = self.calculate_age(self.dob)
            print(self.age)
            print ("RFID Thread")
            if event.state == 11:
                if self.sq1 == "":
                    messagebox.showinfo("Notice!", "Please register your security question first before proceeding")
                else:
                    self.security_question()
            elif event.state == 12:
                if self.sq1 == "":
                    messagebox.showinfo("Notice!", "Please register your security question first before proceeding")
                else:
                    self.security_question()
        
        self.deiconify()
            
#=============================update module for residents===========================#    
    def Update_Residents(self):
        update_residents.Update_residents()
#=============================update module for admin===========================#    
    def Update_Admins(self):
        update_admins.Update_admins()
