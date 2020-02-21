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
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    def run(self):
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
                print(self.cursor.fetchone())
                
                if self.cursor.fetchone() is not None:
                    self.cursor.execute("SELECT FIRST_NAME FROM residents_admin WHERE FINGER_TEMPLATE = %s", positionNumber)
                    self.get_Firstn = self.cursor.fetchone()
                    self.get_Firstn1 = str(self.get_Firstn[0])
                    self.cursor.execute("SELECT MIDDLE_NAME FROM residents_admin WHERE FINGER_TEMPLATE = %s", positionNumber)
                    self.get_Middlen = self.cursor.fetchone()
                    self.get_Middlen1 = str(self.get_Middlen[0])
                    self.cursor.execute("SELECT LAST_NAME FROM residents_admin WHERE FINGER_TEMPLATE = %s", positionNumber)
                    self.get_Lastn = self.cursor.fetchone()
                    self.get_Lastn1 = str(self.get_Lastn[0])
                    self.cursor.execute("SELECT BIRTH_DATE FROM residents_admin WHERE FINGER_TEMPLATE = %s", positionNumber)
                    self.get_Birthd = self.cursor.fetchone()
                    self.get_Birthd1 = str(self.get_Birthd[0])
                    self.dob = datetime.strptime(self.get_Birthd1, "%Y-%m-%d")
                    self.get_dob = self.calculate_age(self.dob)
                    self.cursor.execute("SELECT PLACE_OF_BIRTH FROM residents_admin WHERE FINGER_TEMPLATE = %s", positionNumber)
                    self.get_Placeb = self.cursor.fetchone()
                    self.get_Placeb1 = str(self.get_Placeb[0])
                    self.cursor.execute("SELECT CIVIL_STATUS FROM residents_admin WHERE FINGER_TEMPLATE = %s", positionNumber)
                    self.get_Civils = self.cursor.fetchone()
                    self.get_Civils1 = str(self.get_Civils[0])
                    self.cursor.execute("SELECT SEX FROM residents_admin WHERE FINGER_TEMPLATE = %s", positionNumber)
                    self.get_Sex = self.cursor.fetchone()
                    self.get_Sex1 = str(self.get_Sex[0])
                    self.cursor.execute("SELECT YEAR_OF_RESIDENCY FROM residents_admin WHERE FINGER_TEMPLATE = %s", positionNumber)
                    self.get_dateOfResidency = self.cursor.fetchone()
                    self.get_dateOfResidency1 = str(self.get_dateOfResidency[0])
                    self.cursor.execute("SELECT ADDRESS FROM residents_admin WHERE FINGER_TEMPLATE = %s", positionNumber)
                    self.get_Address = self.cursor.fetchone()
                    self.get_Address = str(self.get_Address[0])
                    self.app.event_generate('<<GRANT_ACCESS>>', when='tail')
                else:
                    self.cursor.execute("SELECT * FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                    if self.cursor.fetchone() is not None: 
                        self.cursor.execute("SELECT FIRST_NAME FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                        self.get_Firstn = self.cursor.fetchone()
                        self.get_Firstn1 = str(self.get_Firstn[0])
                        self.cursor.execute("SELECT MIDDLE_NAME FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                        self.get_Middlen = self.cursor.fetchone()
                        self.get_Middlen1 = str(self.get_Middlen[0])
                        self.cursor.execute("SELECT LAST_NAME FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                        self.get_Lastn = self.cursor.fetchone()
                        self.get_Lastn1 = str(self.get_Lastn[0])
                        self.cursor.execute("SELECT BIRTH_DATE FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                        self.get_Birthd = self.cursor.fetchone()
                        self.get_Birthd1 = str(self.get_Birthd[0])
                        self.dob = datetime.strptime(self.get_Birthd1, "%Y-%m-%d")
                        self.get_dob = self.calculate_age(self.dob)
                        self.cursor.execute("SELECT PLACE_OF_BIRTH FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                        self.get_Placeb = self.cursor.fetchone()
                        self.get_Placeb1 = str(self.get_Placeb[0])
                        self.cursor.execute("SELECT CIVIL_STATUS FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                        self.get_Civils = self.cursor.fetchone()
                        self.get_Civils1 = str(self.get_Civils[0])
                        self.cursor.execute("SELECT SEX FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                        self.get_Sex = self.cursor.fetchone()
                        self.get_Sex1 = str(self.get_Sex[0])
                        self.cursor.execute("SELECT YEAR_OF_RESIDENCY FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                        self.get_dateOfResidency = self.cursor.fetchone()
                        self.get_dateOfResidency1 = str(self.get_dateOfResidency[0])
                        self.cursor.execute("SELECT ADDRESS FROM residents_db WHERE FINGER_TEMPLATE = %s", positionNumber)
                        self.get_Address = self.cursor.fetchone()
                        self.get_Address = str(self.get_dateOfResidency[0])
                        self.app.event_generate('<<GRANT_ACCESS>>', when='tail')
                    else:
                        messagebox.showerror("Warning!","Your fingerprint is not yet registered!")


            
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
        
        GPIO.setwarnings(False)
        self.configure(bg="white")    
        self.geometry("{}x{}".format(self.ws, self.hs))
        self.T_printer = Usb(0x0fe6, 0x811e, 98, 0x82, 0x02)
        
    def on_grant_access(self, *event):
        print(Kiosk.on_grant_access())
        
        self.deiconiy