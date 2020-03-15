from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
import time
from PIL import Image, ImageTk
from datetime import datetime, date
from FingerprintDevice import FingerprintThread
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import pymysql

class Update_residents(Toplevel):
    def __init__(self, app):
        super().__init__(app)
        
        self.app = app
        
        self.attributes("-fullscreen", True)
        self.db = pymysql.connect(host = "192.168.1.9",port = 3306, user = "root",passwd = "justin",db= "thesis_main")

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

        self.tree = Treeview(self.treeview_frame_residents,selectmode="browse", columns = (1,2,3,4,5,6,7,8,9,10,11,12), height = 48, show = "headings")
        self.tree.grid(row = 1, column = 0)
        self.app.bind('<<FINGERPRINT>>', self.on_fingerprint) 
        self.bind("<Destroy>", self.on_destroy)
        
        self.update_finger_button = Button(self.bottom, text = "Update Fingerprint", bg = "white", command = self.Update_fingerprint)
        self.update_finger_button.grid(row = 0, column = 3)

        self.back_button = Button(self.bottom, text = "Back", bg = "white", command = self.destroy)
        self.back_button.grid(row = 0, column = 5)
                
        self.tree.heading(1, text="ID")
        self.tree.heading(2, text="LAST NAME")
        self.tree.heading(3, text="FIRST NAME")
        self.tree.heading(4, text="MIDDLE NAME")
        self.tree.heading(5, text="SEX")
        self.tree.heading(6, text="BIRTH DATE")
        self.tree.heading(7, text="CIVIL_STATUS")
        self.tree.heading(8, text="YEAR OF RESIDENCY")
        self.tree.heading(9, text="ADDRESS")
        self.tree.heading(10, text="PLACE OF BIRTH")
        self.tree.heading(11, text="CONTACT NUMBER")
        self.tree.heading(12, text="FINGER TEMPLATE")
        
        self.tree.column(1, width = 100)
        self.tree.column(2, width = 115)
        self.tree.column(3, width = 115)
        self.tree.column(4, width = 115)
        self.tree.column(5, width = 90)
        self.tree.column(6, width = 100)
        self.tree.column(7, width = 115)
        self.tree.column(8, width = 150)
        self.tree.column(9, width = 150)
        self.tree.column(10, width = 50)
        self.tree.column(11, width = 50)
        self.tree.column(12, width = 50)
        
        self.scrolly = Scrollbar(self.treeview_frame_residents, orient="vertical", command=self.tree.yview)
        self.scrolly.grid(row = 1, column = 1, sticky = "nesw")
        self.scrollx = Scrollbar(self.treeview_frame_residents, orient="horizontal", command=self.tree.xview)
        self.scrollx.grid(row = 2, column = 0, sticky = "nesw")
             
        self.tree.configure(yscrollcommand=self.scrolly.set)
        self.tree.configure(xscrollcommand=self.scrollx.set)
        
        self.cursor.execute("SELECT ID, LAST_NAME, FIRST_NAME, MIDDLE_NAME, SEX, BIRTH_DATE, CIVIL_STATUS, YEAR_OF_RESIDENCY, ADDRESS, PLACE_OF_BIRTH, Contact_No, FINGER_TEMPLATE FROM residents_db")
        self.fetch = self.cursor.fetchall()
        for data in self.fetch:
            self.tree.insert('', 'end', values=(data))
    
    def on_fingerprint(event):
        print('on_fingerprint()  template_id={}'.format(event.state)) 
        if event.state >= 0:
            curItem = self.tree.focus()
            inter_var=self.tree.item(curItem)
            list_values=inter_var['values']
            template_id = event.state
            self.cursor.execute("UPDATE residents_db SET FINGER_TEMPLATE = %s WHERE ID = %s", (template_id, list_values[0]))
            self.db.commit()
            messagebox.showinfo("Success", "Fingerprint successfully updated", parent = self)
            self.update_finger_frame.destroy()
            self.treeview_frame_residents.pack(expand = 1, fill = "both")
        elif event.state ==-1:
            messagebox.showerror("Notice!", "Fingerprint already registered")
        elif event.state ==-2:
            messagebnox.showerror("Notice!", "Fingerprint does not match")
        
    def Update_fingerprint(self):
        self.update()
        curItem = self.tree.focus()
        inter_var=self.tree.item(curItem)
        list_values=inter_var['values']
        print(list_values)
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
            
            if list_values[12] != "":
                # .delete template ID
                print('delete_template({})'.format(template_id))
                self.app.fp.delete_template(template_id)
                # Change or continue to REGISTER
            
            print('set mode REGISTER')
            self.app.fp.set_mode(FingerprintDevice.REGISTER)
            
    def on_destroy(self, event):
        # Change back to continius SEARCH mode
        self.app.bind('<<FINGERPRINT>>', self.on_fingerprint)
        print('set mode SEARCH')
        self.app.fp.set_mode(FingerprintDevice.SEARCH)
        
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
    root = Tk()
    Update_residents(root)
    fp = FingerprintThread()
    root.mainloop()
