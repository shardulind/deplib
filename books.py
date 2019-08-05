import mysql.connector as db
from db_credentials import setu
#Ab tak:
#1. is_book_registered
#2. insert_new_book
#3. delete_book
#4. list_all_books
#5. search_book





#tells if book is available to issue or not
def is_book_available(acn):
    book = search_book('accession_number', acn)
    if book == -1:
            return -1
    else:
        #print(book[0][6])
        return book[0][6]


#function search_book
#returns searched book
def search_book(searchby, searchfor):
    arz = setu.cursor()
    query = "SELECT accession_number, title, shelf_no, price, authors, publisher, is_available from books where "+searchby+" like \'"+str(searchfor)+"%\';"

    try:
        arz.execute(query)
    except db.error as err:
        print("\n@ list_all_books -> exception")

    books = arz.fetchall()
    if books == []:
        return -1;
    else:
        return books;




#function list all books
#return 2d lists of all books
def list_all_books():
    list = setu.cursor()
    query = "SELECT * from books";

    try:
        list.execute(query)
    except db.Error as err:
        print("\n@ list_all_books -> exception")

    books = list.fetchall()
    return books;




#returns true/false
def is_book_registered(acn):
    search = setu.cursor()
    query = "select * from books where accession_number = \'" + str(acn) + "\'";

    try:
        search.execute(query)
    except db.Error as err:
        print(err + " \n@ is_book_registered -> exception ")

    temp = search.fetchall()

    if search.rowcount > 0:
        return True;
    elif search.rowcount == 0:
        return False;




def insert_new_book(acn, title, shelf_no, price, author, publisher):
    add = setu.cursor()
    query = "INSERT INTO books(accession_number, title, shelf_no, price, authors, publisher, is_available) values(%s,%s,%s,%s,%s,%s,%s)"

    val = (acn, title, shelf_no, price, author, publisher,'1')
    try:
        add.execute(query,val)

    except db.Error as err:
        print(format(err))
        return err
    except db.IntegrityError as err:
        err="Error: {}".format(err)
        return err

    setu.commit()
    print(str(add.rowcount)+" Book added Successfully");
    return True;


def delete_book(acn):
    delete = setu.cursor()
    query = "delete from books where accession_number = \'" + str(acn) + "\'";

    try:
        delete.execute(query)
    except db.Error as err:
        print(err)
        return err

    setu.commit();
    print(str(delete.rowcount) + " Books Deleted Successfully")
    if delete.rowcount == 0:
        return -1;
    elif delete.rowcount == 1:
        return 1;
    else:
        return delete.rowcount

#insert_new_book('0001','C++','1', '199', 'Balag','TMH')
#delete_book('0001')

#function get book name
#input parameter : accession_number
#output parameter :

def getBookName(acn):
    shodh = setu.cursor()
    query = "SELECT title from books where accession_number = \'" + str(acn) + "\'"

    try:
        shodh.execute(query)
    except db.Error as err:
        print(err)
        return -1

    bname = shodh.fetchall()
    if len(bname) == 0:
        print("book not found")
        return False
    else:
        return str(bname[0][0])
