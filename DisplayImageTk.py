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
                      (ID, Name, Image) VALUES (%s,%s,%s)"""

    empPicture = convertToBinaryData(photo)

    # Convert data into tuple format
    insert_blob_tuple = (emp_id, name, empPicture)
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    db.commit()
    print("Image and file inserted successfully as a BLOB into python_employee table", result)

   
insertBLOB(1, "Justin", "saved_img-final.jpg")

db = pymysql.connect(host='localhost',user='root', password='', db = 'test')
cursor = db.cursor()

db.autocommit(True)
cursor.execute("CREATE TABLE testing (Image MEDIUMBLOB)"
image_query = "SELECT Image FROM testing"
cursor.execute(image_query)

image=cursor.fetchall()

img = Image.open(io.BytesIO(image[0][0]))
phimg = ImageTk.PhotoImage(img)

root = tk.Tk()
panel = tk.Label(root, image = phimg)
panel.grid(row=0,rowspan=5,columnspan=2)
