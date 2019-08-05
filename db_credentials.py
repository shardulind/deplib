import mysql.connector as db
import tkinter as tk
from tkinter import messagebox

try:
 setu = db.connect(
    host = "localhost",
    user="root",
    passwd="Advaita@1998",
    database="library"
 )
except db.Error as err:
    print(err); #debug
    t_error = 'Error' + str(err.errno)
    t_msg = err.sqlstate + ' ' + err.msg
    messagebox.showinfo(t_error, t_msg)
