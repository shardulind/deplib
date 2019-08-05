import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from borrows import *
from members import *
from books import *
import books_window
import members_window
import datetime

def datePicker():

        root = tk.Tk()
        def print_sel():
            sel = cal.selection_get()
            print(sel)
            #cal.see(datetime.date(year=2016, month=2, day=5))
            root.destroy()
            return sel
        top = tk.Toplevel(root)
        import datetime
        today = datetime.date.today()
        mindate = datetime.date(year=2018, month=1, day=21)
        maxdate = today + datetime.timedelta(days=1)
        #print(mindate, maxdate)
        print(today.year)
        print(today.month)
        print(today.day)
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1", year=today.year, month=today.month, day=today.day)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel).pack()
        root.mainloop()


def clearTable(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)



def start_listUnreturned_books():
    book_win = tk.Tk()
    book_win.title("Unreturned Books")
    book_win.geometry("900x600+750+300")

    def trig_returnBook():
        CurItem = tree.selection()
        focus = tree.item(CurItem)
        val = focus['values']
        if val != '':
            print(str(cal.get_date()))
            print(val)
            memID = str(val[5])
            acn = str(val[0])
            returnDate = str(cal.get_date())
            remark = ''
            confirm = messagebox.askyesno('Return Book',"Title: " + str(val[1]) + "\nMember: " + str(val[2]) + "\nReturn Date: " + str(val[3])  )
            if confirm:
                status = return_book(memID, acn, returnDate, remark)
                if status:
                    messagebox.showinfo("Book Returned","Book Returned Successfully")
                    book_win.lift()
            else:
                return



    def shodha():
        dict = {"Title":"title", "Member":"full_name", "Accession No.":"borrows.accession_number"}
        clearTable(tree)
        #print(tkvar.get())
        unreturnedBooks = getUnreturnedBooks(dict[tkvar.get()], searchField.get())

        if unreturnedBooks == False:
            messagebox.showinfo('','Not Found!')
            book_win.destroy()
        elif unreturnedBooks == -1:
            messagebox.showerror('Error','Some error occured')
            book_win.destroy()
        else:
            for book in unreturnedBooks:
                tree.insert('',0,text='', value = book)

    v = IntVar()
    tkvar = StringVar(book_win)
    Label(book_win, text="Search Book by: ").pack()
    searchField = Entry(book_win)
    searchBy = ['Member','Title','Accession No.']
    tkvar.set('Title')
    popupMenu = OptionMenu(book_win, tkvar, *searchBy)
    searchField.pack()
    popupMenu.pack()
    Button(book_win, text='Search', command = shodha).pack()

    #books table
    tree = ttk.Treeview(book_win)
    tree["column"] = ("acn","title","imname","issue_date","mno","memid")
    tree.column("#0", width=1)
    tree.column("acn", width=200)
    tree.column("title", width=250)
    tree.column("imname", width=200)
    tree.column("issue_date", width=100)
    tree.column("mno", width=150)
    tree.column("memid", width=50)
    tree.heading("acn", text = "Accession Number")
    tree.heading("title",text = "Title")
    tree.heading("imname",text = "Issuers Name")
    tree.heading("issue_date",text = "Issue Date")
    tree.heading("mno", text="Mobile Number")
    tree.heading("memid", text="Member ID")
    tree.pack()


#add those min date and maxdate parameters too
    today = datetime.date.today()
    Label(book_win, text='Choose Return date\n(DD/MM/YY)').pack()
    cal = DateEntry(book_win, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)
    return_button = Button(book_win, text="Return Book", command = trig_returnBook)
    return_button.pack()

    book_win.mainloop()





def start_issueBook_win(acn='', mem_id=''):

    def trig_issueBook():
        acn = str(to_be_issued_book_accn.get())
        mem_id = str(issuers_id.get())

        #food for thought about validation
        bookTitle = getBookName(acn)
        memberName = getMemberNameFromID(mem_id)
        issueDate = str(cal.get_date())

        if memberName == bookTitle == False:
            messagebox.showerror("Error","Incorrect Accession Number and MemberID")
            return
        elif bookTitle == False:
            messagebox.showerror("Error","Incorrect Accession Number\n Check it in Book Search Window")
            issue_win.lift()
            return
        elif memberName == False:
            messagebox.showerror("Error","Incorrect Member ID\n Check it in Member Search Window")
            issue_win.lift()
            return

        msg = "Book Title: "+bookTitle+"\nAccession Number: " + acn + "\nMember Name: "+memberName+"\nIssue Book ?"
        confirm = messagebox.askyesno("Book Issue",msg)

        if confirm:
            ### we are struck at getting date parameter hahahah
            zhenda = issue_book(mem_id, acn, issueDate)
            if zhenda == -1:
                messagebox.showerror("Error","Member ID NOT found!")
            elif zhenda == -2:
                messagebox.showerror("Error","Book Already Issued to !")
            elif zhenda == True:
                messagebox.showinfo("Success","Book Issued Successfully!")
                issue_win.destroy()
                ## what to do after issuing book
            elif zhenda == False:
                messagebox.showerror("Major Error","Bug exist.")
        else:
            pass

    def trig_searchBook_win():
        temp = issuers_id.get()
        issue_win.destroy()
        books_window.start_searchBook_win(cached_mem_id = str(temp))

    def trig_searchMem_win():
        temp = to_be_issued_book_accn.get()
        issue_win.destroy()
        #member search list
        members_window.start_listAll_members(cached_acn_no = str(temp))

    issue_win = tk.Tk()
    issue_win.title("Issue Book")
    issue_win.geometry("500x250+800+450")

    #labels
    Label(issue_win, text="Member ID:").grid(row=0,column=1);
    Label(issue_win, text="Accession Number:").grid(row=1,column=1);
    #buttons to get_data
    Button(issue_win, text='Search Book', command = trig_searchBook_win).grid(row=1,column=4, sticky=W, pady=4)
    Button(issue_win, text='Search MemberID', command = trig_searchMem_win).grid(row=0,column=4, sticky=W, pady=4)

    #text entry field
    issuers_id = Entry(issue_win)
    issuers_id.delete(0,END)
    issuers_id.insert(0,mem_id)
    to_be_issued_book_accn = Entry(issue_win)
    to_be_issued_book_accn.delete(0,END)
    to_be_issued_book_accn.insert(0,str(acn))


    #add those min date and maxdate parameters too
    today = datetime.date.today()
    Label(issue_win, text='Choose Issue date\n(DD/MM/YY)').grid(row=3, column=1)
    cal = DateEntry(issue_win, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.grid(row=3, column=2)

    Button(issue_win, text='Issue Book', command = trig_issueBook).grid(row=4,column=1, sticky=W, pady=4)
    Button(issue_win, text='Cancle', command = issue_win.destroy).grid(row=4,column=2,sticky=W, pady=4)

    to_be_issued_book_accn.grid(row=1,column=2)
    issuers_id.grid(row=0,column=2)

    #issue_win.mainloop()
    issue_win.lift()
