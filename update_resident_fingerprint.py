from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
import time
from PIL import Image, ImageTk
from datetime import datetime, date
from pyfingerprint.pyfingerprint import PyFingerprint
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import pymysql

class Update_residents(Toplevel):
    def __init__(self):
        super().__init__()
            
        self.attributes("-fullscreen", True)
        self.db = pymysql.connect(host = "192.168.1.9",port = 3306, user = "root",passwd = "justin",db= "thesis_db")

        self.db.autocommit(True)
        
        self.cursor = self.db.cursor()
                        
        self.treeview_frame_residents = Frame(self)
        self.treeview_frame_residents.pack(expand = 1, fill = "both")
                        
        self.reader=SimpleMFRC522()
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()

        self.img_tree_view = (Image.open("background_kiosk.png"))
        self.image_tree_view = self.img_tree_view.resize((self.ws,self.hs))
        self.img_background_tree_view = ImageTk.PhotoImage(self.image_tree_view)
        self.imglabel_tree_view = Label(self.treeview_frame_residents, image = self.img_background_tree_view)
        self.imglabel_tree_view.place(x=0,y=0)
        

        self.top = Frame(self.treeview_frame_residents, bg = "white")
        self.top.grid(row = 0, column = 0, pady = 5)
        
        self.bottom = Frame(self.treeview_frame_residents, bg = "white")
        self.bottom.grid(row = 3, column = 0, pady = 5)

        self.var = StringVar(self)
        self.search_bar = StringVar()
      
        self.OptionList = ["FIRST_NAME", "MIDDLE_NAME", "LAST_NAME"]
        self.option = Combobox(self.top, state = "readonly", textvariable = self.var, values = self.OptionList)
        self.option.grid(row = 0, column = 0)
        self.search_entry = Entry(self.top, width = 80, bg = "white", textvariable = self.search_bar)
        self.search_entry.grid(row = 0, column = 1)

        self.reset_button = Button(self.top, text = "refresh", bg = "white", command = self.reset_data)
        self.reset_button.grid(row = 0, column = 3)

        self.tree = Treeview(self.treeview_frame_residents,selectmode="browse", columns = (1,2,3,4,5,6,7,8,9,10,11,12,13,14), height = 48, show = "headings")
        self.tree.grid(row = 1, column = 0)

        self.update_finger_button = Button(self.bottom, text = "Update Fingerprint", bg = "white", command = self.Update_fingerprint)
        self.update_finger_button.grid(row = 0, column = 3)

        self.back_button = Button(self.bottom, text = "Back", bg = "white", command = self.destroy)
        self.back_button.grid(row = 0, column = 5)
                
        self.tree.heading(1, text="ID")
        self.tree.heading(2, text="First_Name")
        self.tree.heading(3, text="Middle_Name")
        self.tree.heading(4, text="Last_Name")
        self.tree.heading(5, text="Sex")
        self.tree.heading(6, text="Birth_Date")
        self.tree.heading(7, text="Civil_Status")
        self.tree.heading(8, text="Date_of_Residency")
        self.tree.heading(9, text="ADDRESS")
        self.tree.heading(10, text="Place_of_Birth")
        
        self.tree.column(1, width = 100)
        self.tree.column(2, width = 115)
        self.tree.column(3, width = 115)
        self.tree.column(4, width = 115)
        self.tree.column(5, width = 90)
        self.tree.column(6, width = 100)
        self.tree.column(7, width = 115)
        self.tree.column(8, width = 150)
        self.tree.column(9, width = 150)
        self.tree.column(10, width = 225)
    
        self.scrolly = Scrollbar(self.treeview_frame_residents, orient="vertical", command=self.tree.yview)
        self.scrolly.grid(row = 1, column = 1, sticky = "nesw")
        self.scrollx = Scrollbar(self.treeview_frame_residents, orient="horizontal", command=self.tree.xview)
        self.scrollx.grid(row = 2, column = 0, sticky = "nesw")
             
        self.tree.configure(yscrollcommand=self.scrolly.set)
        self.tree.configure(xscrollcommand=self.scrollx.set)

        self.cursor.execute("SELECT * FROM residents_db")
        self.fetch = self.cursor.fetchall()
        for data in self.fetch:
            self.tree.insert('', 'end', values=(data))

    def Update_fingerprint(self):
        self.update()
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        if list_values == "":
            messagebox.showerror("Error", "Please select a row", parent = self)
        else:
            self.treeview_frame_residents.pack_forget()
    
            self.update_finger_frame = Frame(self)
            self.update_finger_frame.pack(fill = "both", expand = 1)
            
            self.img_update_finger_resident = (Image.open("finger_register.png"))
            self.image_update_background_finger_resident = self.img_update_finger_resident.resize((self.ws,self.hs))
            
            self.img_update_background_finger_resident = ImageTk.PhotoImage(self.image_update_background_finger_resident)
            
            self.Label_update = Label(self.update_finger_frame, image = self.img_update_background_finger_resident, width = self.ws, height = self.hs)
            self.Label_update.grid(row = 0, column = 0, sticky = "nesw")
            
            self.Label_update.bind('<Enter>', self.Updated_fingerprint)
            
    def Updated_fingerprint(self, event):
        self.update()
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        print(list_values)# check the value of a dictionary
        if list_values[12] !='':
            try:
                f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                if ( f.verifyPassword() == False ):
                    raise ValueError('The given fingerprint sensor password is wrong!')

            except Exception as e:
                print('The fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))
        
            ## Gets some sensor information
            print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        
            ## Tries to delete the template of the finger
            positionNumber = list_values[12]
            positionNumber = int(positionNumber)
            print(positionNumber)
            if (f.deleteTemplate(positionNumber) == True):
                print('Template deleted!')
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
                    
            time.sleep(2)


                ## Wait that finger is read again
            while ( f.readImage() == False ):
                pass

                ## Converts read image to characteristics and stores it in charbuffer 2
            f.convertImage(0x02)

                ## Compares the charbuffers
            if ( f.compareCharacteristics() == 0 ):
                messagebox.showerror("Error", "Finger do not match\n Please try again", parent = self)          
                
                ## Creates a template
            else:
                f.createTemplate()
                characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
                ## Saves template at new position number
                positionNumber = f.storeTemplate()
                self.cursor.execute("UPDATE residents_db SET FINGER_TEMPLATE = %s WHERE ID = %s", (positionNumber, list_values[0]))
                self.db.commit()
                messagebox.showinfo("Success", "Fingerprint successfully updated", parent = self)
                self.update_finger_frame.destroy()
                self.treeview_frame_residents.pack(expand = 1, fill = "both")

        else:
            try:
                f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                if ( f.verifyPassword() == False ):
                    raise ValueError('The given fingerprint sensor password is wrong!')

            except Exception as e:
                print('The fingerprint sensor could not be initialized!')
                print('Exception message: ' + str(e))

            ## Gets some sensor information
            print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

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
                    
            time.sleep(2)

                ## Wait that finger is read again
            while ( f.readImage() == False ):
                pass

                ## Converts read image to characteristics and stores it in charbuffer 2
            f.convertImage(0x02)

                ## Compares the charbuffers
            if ( f.compareCharacteristics() == 0 ):
                messagebox.showerror("Error", "Finger do not match\n Please try again", parent = self)
                
            ## Creates a template
            else:
                f.createTemplate()
                characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
                    ## Saves template at new position number
                positionNumber = f.storeTemplate()
                self.cursor.execute("UPDATE residents_db SET FINGER_TEMPLATE = %s WHERE ID = %s", (positionNumber, str(list_values[0])))
                self.db.commit()
                messagebox.showinfo("Success", "Fingerprint successfully updated", parent = self)
                self.update_finger_frame.destroy()
                self.treeview_frame_residents.pack(expand = 1, fill = "both")
        
            
    def search_data(self):
        searching = str(self.search_bar.get())
        
        if (self.search_bar.get() != ""):
            self.tree.delete(*self.tree.get_children())
            if self.var.get() == "FIRST_NAME":
                self.cursor.execute("SELECT * FROM residents_db WHERE FIRST_NAME LIKE %s",('%'+searching+'%'))
                self.fetch = self.cursor.fetchall()

            elif self.var.get() == "MIDDLE_NAME":
                self.cursor.execute("SELECT * FROM residents_db WHERE MIDDLE_NAME LIKE %s",('%'+searching+'%'))
                self.fetch = self.cursor.fetchall()

            elif self.var.get() == "LAST_NAME":
                self.cursor.execute("SELECT * FROM residents_db WHERE LAST_NAME LIKE %s",('%'+searching+'%'))
                self.fetch = self.cursor.fetchall()
            for data in self.fetch:
                self.tree.insert('', 'end', values=(data))

    def reset_data(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM residents_db")
        self.fetch = self.cursor.fetchall()
        for data in self.fetch:
            self.tree.insert('', 'end', values=(data))

if __name__== "__main__":
    Update_residents().mainloop()
