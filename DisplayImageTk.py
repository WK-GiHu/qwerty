from PIL import Image, ImageTk
import tkinter as tk
import pymysql
import io

db = pymysql.connect(host='localhost',user='root', password='', db = 'test')
cursor = db.cursor()

db.autocommit(True)
meow = "SELECT Image FROM testing"
cursor.execute(meow)

logo=cursor.fetchall()

img = Image.open(io.BytesIO(logo[0][0]))
phimg = ImageTk.PhotoImage(img)

root = tk.Tk()
panel = tk.Label(root, image = phimg)
panel.grid(row=0,rowspan=5,columnspan=2)
