from tkinter import *
import threading
import pymysql
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from PIL import Image, ImageTk
import datetime
from pyfingerprint.pyfingerprint import PyFingerprint
from VKeyboard import VKeyboard
class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.attributes("-fullscreen", True)

        self.funcid = self.bind('<Button-1>', self.on_button_clicked)

        label = Label(self, text = "NO ANNOUNCEMENT YET!!!")
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

        self.timeout = 5
        self._counter = self.timeout

        self.start()
        self.app.bind('<<IDLE>>', self.on_idle)

    def run(self):
        print('run()'.format())
        
        while True:
            if self._counter > 0:
                self._counter -= 1
                
                # For testing only
                print('\t{}'.format(self._counter))
                IdleCounter.label = 'timeout in {} sec.'.format(self._counter)
                
                if self._counter == 0:
                    # For testing only
                    IdleCounter.label = 'idle, click to reset'
                    
                    self.app.event_generate('<<TIMEOUT>>', when='tail')
                    
            time.sleep(1)
                    
        print('IdleCounter terminated'.format())
        
    def on_idle(self, event):
        print('IdleCounter.on_idle(state={})'.format(event.state))
        if event.state == 1:
            event.state = 0
            if self._counter > 0 and event.state == 0:
                self._counter = self.timeout

    
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
        
        self.attributes("-fullscreen", True)
        self.img = (Image.open("background_kiosk.png"))
        self.image = self.img.resize((self.ws,self.hs))
        self.img_background = ImageTk.PhotoImage(self.image)
        self.imglabel = Label(self, image = self.img_background).place(x=0,y=0)

        self.img2 = ImageTk.PhotoImage(Image.open("rosario_logo.png"))
        
        FingerprintThread(self, callback = self.on_grant_access)
        RFIDThread(self, callback = self.on_grant_access)
        IdleCounter(self)
        self.bind('<<TIMEOUT>>', self.on_timeout)
        GPIO.setwarnings(False)
        self.configure(bg="white")    
        self.geometry("{}x{}".format(self.ws, self.hs))
        self.T_printer = Usb(0x0fe6, 0x811e, 98, 0x82, 0x02)
        
    def on_timeout(self, event):
        SplashScreen(self)
     
