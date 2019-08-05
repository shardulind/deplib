import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from books import *
#from borrows_window import start_issueBook_win
import borrows_window


def clearTable(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)


# search book win
def start_searchBook_win(acn='',cached_mem_id=''):
     def trig_deleteBook():
         CurItem = tree.selection()
         print(type(CurItem))
         focus = tree.item(CurItem)
         val = focus['values']
         print(val)
         msg = "Delete Book: "+val[1]+" Accn. No: "+str(val[0])
         x = messagebox.askokcancel("Delete Book!",msg)
         if(x):
             print(str(val[0]))
             delete_book(str(val[0]))
        #     book_win.destroy()
            #refresh table ___to__do___



     def trig_issueBook():
         CurItem = tree.selection()
         focus = tree.item(CurItem)
         val = focus['values']
         if val != '':
             print(val)
             acn = val[0]
             #print(acn)
             msg = "Book Title: " + str(val[1]) + " Accn. No: "  + str(val[0])
             if is_book_available(val[0]):
                 #issue book
                 print("is book available true")
                 book_win.destroy()
                 borrows_window.start_issueBook_win(str(acn), cached_mem_id)


             elif is_book_available(val[0]) == 0:
                 #book is alreadyissue,,, display who issued the book with duration
                 print("is book available false")
                 pass
             elif is_book_available(val[0]) == -1:
                 messagebox.showerror("Error","Accession number not found in Database")
         else:
             return

     book_win = tk.Tk()
     #book_win.overrideredirect(1)
     book_win.title("Search Book")
     book_win.geometry("960x600+750+300")
     v=IntVar()
#MAE/COMP/1213/1077
##     def selectItem(a):
#         def trig_deleteBook():
#             val = focus['values']
#             #print(val)
#             msg = "Delete Book: "+val[1]+" Accn. No: "+str(val[0])
#             x = messagebox.askokcancel("Delete Book!",msg)
#
#             if(x):
#                 delete_book(str(val[0]))
#                 book_win.destroy()
#                 #delete that button

#         CurItem = tree.focus()
#         print(tree.item(CurItem))
#         #del_button = Button(book_win, text="Delete Book Detail", command = trig_deleteBook)
#         #del_button.pack(side=LEFT)
#         focus = tree.item(CurItem)

     def searchit():
         clearTable(tree)
         print(tkvar.get())
         searchedBook = search_book(tkvar.get(), searchField.get())

         if searchedBook == -1:
             messagebox.showinfo("","Book Not Found")
             book_win.destroy()
         else:
             for book in searchedBook:
                 #print(book)
                 tree.insert('',0, text='', value = book)





     tkvar = StringVar(book_win)
     Label(book_win, text="Search Book By :").pack()
     searchField = Entry(book_win)
     searchBy = ['title', 'accession_number', 'author', 'publisher']
     tkvar.set('title')

     popupMenu = OptionMenu(book_win, tkvar, *searchBy)
     searchField.pack()
     popupMenu.pack()
     #   Button(book_win, text='Search',command=searchit).grid(row=5, column=3, sticky = W, pady=4)
     Button(book_win, text='Search',command=searchit).pack()
     Button(book_win, text='Exit', command = book_win.destroy)
     #Book table
     tree = ttk.Treeview(book_win)
     tree["column"] = ("acn", "title", "author", "shlfno.", "publisher", "price", "Available")
     tree.column("#0", width=10)
     tree.column("acn", width=100)
     tree.column("title", width=150)
     tree.column("author", width=100)
     tree.column("shlfno.", width=80)
     tree.column("publisher", width=100)
     tree.column("price", width=50)
     tree.column("Available", width=70)
     tree.heading("acn", text="Accession No.")
     tree.heading("title", text="Title")
     tree.heading("author", text="Author")
     tree.heading("shlfno.", text="Shelf no")
     tree.heading("publisher", text="Publisher")
     tree.heading("price", text="Price")
     tree.heading("Available",text="Available")
#     tree.bind('<ButtonRelease-1>', selectItem)
#     tree.bind('<Double-1>',selectItem)
     del_button = Button(book_win, text="Delete Book", command = trig_deleteBook)
     del_button.pack(side=BOTTOM)
     issue_button = Button(book_win, text="Issue Book", command = trig_issueBook)
     issue_button.pack(side=BOTTOM)

     tree.pack(fill=tk.X)
     mainloop()



## Function start_addbook_win
#
def start_addbook_win():
    book_win = tk.Tk()
    book_win.title("Add New Book")
    book_win.geometry("350x300+900+450")

    def validate():
        if book_win_price.get().isdigit() and book_win_title.get() != "" and book_win_acno.get() != "":
            #print("Validated @price is digit")
            return True
        else:
            return False

    def addBook():
        flag0 = is_book_registered(book_win_acno.get());
        if flag0 == True:
            print("Accession number already exist in Database")
            messagebox.showerror(title='Error',message = "Accession Number already exist in Database")
            # Accession number already registered
            #break from here itself
            ## todo: Show the book title of already existing acn

        valid = validate()
        if valid==True and flag0 == False:
            ##Add book to database
            status = insert_new_book(book_win_acno.get(), book_win_title.get(), book_win_shelfno.get(), book_win_price.get(), book_win_author.get(), book_win_pub.get())
            if status == 1:
                #message book added Successfully
                temp = book_win_title.get()
                msg = temp + ' Added into Database successfully'
                book_win.withdraw()
                messagebox.showinfo('Success',msg)
                book_win.destroy()

            else:
                #got some error
                messagebox.showerror('Error', status)
        elif valid == False and flag0 == False:
            messagebox.showerror('Data Format error', 'The entered Data is in invalid Format\n')
        #    book_win_price.focus_set()


    def focus1(event):
        book_win_title.focus_set()
    def focus2(event):
        book_win_shelfno.focus_set()
    def focus3(event):
        book_win_price.focus_set()
    def focus4(event):
        book_win_author.focus_set()
    def focus5(event):
        book_win_pub.focus_set()


    Label(book_win, text="Accession Number:").grid(row=1,column=4)
    Label(book_win, text="Title:").grid(row=2,column=4)
    Label(book_win, text="Shelf No:").grid(row=3,column=4)
    Label(book_win, text="Price:").grid(row=4,column=4)
    Label(book_win, text="Author:").grid(row=5, column=4)
    Label(book_win, text="Publisher:").grid(row=6, column=4)

    book_win_acno = Entry(book_win)
    book_win_title = Entry(book_win)
    book_win_shelfno = Entry(book_win)
    book_win_price = Entry(book_win)
    book_win_author = Entry(book_win)
    book_win_pub = Entry(book_win)

    book_win_acno.grid(row=1,column=5)
    book_win_title.grid(row=2,column=5)
    book_win_shelfno.grid(row=3,column=5)
    book_win_price.grid(row=4,column=5)
    book_win_author.grid(row=5,column=5)
    book_win_pub.grid(row=6,column=5)


    #bind method used to bind the functions with the event
    book_win_acno.bind("<Return>", focus1)
    book_win_title.bind("<Return>", focus2)
    book_win_shelfno.bind("<Return>", focus3)
    book_win_price.bind("<Return>", focus4)
    book_win_author.bind("<Return>", focus5)

    Button(book_win, text='Add Book', command = addBook).grid(row=7,column=4,sticky=W, pady=4)
    Button(book_win, text='Close', command = book_win.destroy).grid(row=7,column=5,sticky=W, pady=4)

    mainloop()
