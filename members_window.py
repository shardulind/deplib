import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Progressbar
from members import *
import borrows_window
import re

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
# for validating an Email
def isemail(email):

    # pass the regualar expression
    # and the string in search() method
    if(re.search(regex,email)):
        return True

    else:
        return False



def start_reg_member():

    reg_win = tk.Tk()
    reg_win.title("Member Registration")
    v=tk.IntVar()
    reg_win.geometry('450x400+750+600')
    member_types_array = ['Student','Faculty']

    def validation():
        if reg_win_fname.get() == '' or reg_win_mno.get() == '' or reg_win_email.get() == '':
            return "Dont keep First Name, Mobile Number and Email ID fields EMPTY"
        elif reg_win_fname.get().isdigit() and reg_win_lname.get().isdigit():
            return "Name must be alphabets and NOT the numbers!"
        elif reg_win_mno.get().isdigit() == False :
            return "invalid mobile number"
        elif isemail(reg_win_email.get()) == False:
            return "Invalid Email ID"
        else:
            return True

    def register_user():
        valid_pass = validation()
        if valid_pass == True:

            fn=reg_win_fname.get() + " " + reg_win_lname.get()
            msg = add_new_member(member_types_array[v.get()], reg_win_mno.get(), reg_win_email.get(),fn.upper())

            #if member added Successfully
            if msg == 1:
                messagebox.showinfo("Successful","Member added Successfully")
                reg_win.destroy()
                print("Member" + fn +" Added Successful !!!")


            else:
                messagebox.showinfo('Member Already Exist',msg)
                reg_win.destroy()
        else:
            #pop some error ;; pop valid_pass
            messagebox.showinfo('Form Validation Error', valid_pass)


    Label(reg_win, text="Library member Registration Form").grid(row=0,column=4)
    Label(reg_win, text="First Name").grid(row=3,column=3)
    Label(reg_win, text="Last Name").grid(row=4,column=3)
    Label(reg_win, text="Member Type").grid(row=5,column=3)
    Label(reg_win, text="Mobile Number:").grid(row=6,column=3)
    Label(reg_win, text="Email Id:").grid(row=7,column=3)
    reg_win_fname = Entry(reg_win)
    reg_win_lname = Entry(reg_win)
    reg_win_mtype1 = tk.Radiobutton(reg_win, text="Student", padx = 20, variable = v, value=0)
    reg_win_mtype2 = tk.Radiobutton(reg_win, text="Faculty", padx= 20, variable = v, value=1)
    reg_win_mno = Entry(reg_win)
    reg_win_email = Entry(reg_win)

    reg_win_fname.grid(row=3,column=4)
    reg_win_lname.grid(row=4,column=4)
    reg_win_mtype1.grid(row=5,column=4)
    reg_win_mtype2.grid(row=5, column=5)
    reg_win_mno.grid(row=6,column=4)
    reg_win_email.grid(row=7,column=4)

    Button(reg_win, text='Close', command=reg_win.destroy).grid(row=10,column=4, sticky=W, pady=4)
    Button(reg_win, text='Register', command=register_user).grid(row=10,column=5, sticky=W, pady=4)

    mainloop()



def clearTable(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)


def start_listAll_members(cached_acn_no='',memberID=''):
    reg_win = tk.Tk()
    reg_win.title("Search Member")
    reg_win.geometry("900x600+750+300")
    allMembers=getAllMembers()

    def trig_issue_book():
        CurItem = tree.selection()
        focus = tree.item(CurItem)
        val = focus['values']
        if val != '':
            #print(val)
            memberID = str(val[0])
            reg_win.destroy()
            borrows_window.start_issueBook_win(cached_acn_no,memberID)

    def searchMem():
        clearTable(tree)
        searchedMembers=searchMember('full_name',str(searchField.get()))

        if searchedMembers == False:
            messagebox.showinfo("","Member Not Found")
            reg_win.destroy()
            start_listAll_members()
        else:
            for member in searchedMembers:
                tree.insert('',0,text='', value = member)


    Label(reg_win, text="Search Member :").pack()
    searchField = Entry(reg_win)
    searchBy = "full_name"
    searchField.pack()
    Button(reg_win, text="Search", command=searchMem).pack()
    Button(reg_win, text="Exit", command=reg_win.destroy)



    tree = ttk.Treeview(reg_win)

    tree["columns"]=("member_id", "full_name", "mobile_number", "email_id","member_type")
    tree.column("#0", width=1)
    tree.column("member_type", width=100)
    tree.column("member_id", width=100)
    tree.column("full_name", width=250)
    tree.column("mobile_number", width=130)
    tree.column("email_id", width=230)
    tree.heading("member_type", text="Type")
    tree.heading("member_id", text="Member ID")
    tree.heading("full_name", text="Name")
    tree.heading("mobile_number", text="Mobile No.")
    tree.heading("email_id",text="Email ID")

    for member in allMembers:
        tree.insert('',0, text='', value = member)
    tree.pack()

    Button(reg_win, text= "Issue Book", command = trig_issue_book).pack()

    reg_win.mainloop()
