from PIL import Image, ImageTk
import tkinter as tk
import pymysql
import io

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB(photo):
    print("Inserting BLOB into python_employee table")
    db = pymysql.connect(host='localhost',user='root', password='', db = 'test')

    cursor = db.cursor()
    sql_insert_blob_query = """INSERT INTO testing
                      (Image) VALUES (%s)"""

    empPicture = convertToBinaryData(photo)

    # Convert data into tuple format
    insert_blob_tuple = (empPicture)
    cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    db.commit()
    
   
insertBLOB("saved_img.jpg")

db = pymysql.connect(host='localhost',user='root', password='', db = 'test')
cursor = db.cursor()

root = tk.Tk()
db.autocommit(True)
cursor.execute("SELECT Image FROM testing")
Image=cursor.fetchall()
byte_image = io.BytesIO(Image[0][0])
print(byte_image)
img = Image.open(byte_image)
img.show()
phimg = ImageTk.PhotoImage(img)

panel = tk.Label(root, image = phimg)
panel.grid(row=0,rowspan=5,columnspan=2)
