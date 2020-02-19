from PIL import Image, ImageTk
import tkinter as tk
import pymysql
import io

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
