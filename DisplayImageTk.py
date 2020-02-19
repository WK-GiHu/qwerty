from PIL import Image, ImageTk
import tkinter as tk
import pymysql
import io

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB(emp_id, name, photo):
    print("Inserting BLOB into python_employee table")
    db = pymysql.connect(host='localhost',user='root', password='', db = 'test')

    cursor = db.cursor()
    sql_insert_blob_query = """ INSERT INTO testing
                      (Image) VALUES (%s)"""

    empPicture = convertToBinaryData(photo)

    # Convert data into tuple format
    insert_blob_tuple = (empPicture)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    db.commit()
    print("Image and file inserted successfully as a BLOB into python_employee table", result)

   
insertBLOB("saved_img-final.jpg")

db = pymysql.connect(host='localhost',user='root', password='', db = 'test')
cursor = db.cursor()

root = tk.Tk()

db.autocommit(True)
meow = "SELECT Image FROM testing"
cursor.execute(meow)

logo=cursor.fetchall()
print (logo)
img = Image.frombytes("RGB",(3,2),logo[0][0])
img.show()
phimg = ImageTk.PhotoImage(img)

panel = tk.Label(root, image = phimg)
panel.grid(row=0,rowspan=5,columnspan=2)
