import mysql.connector as ms
from db_credentials import setu
from datetime import datetime
from books import is_book_available
from members import does_member_exist
#1. issue_book(mem_id, acn, issue_date)
#2. is_book_issued(acn):
#3. return_book(mem_id, acn, return_date, remark)
#4. getUnreturnedBooks()









#book issue
#input parameters : member id, accession_number, issue dinank
#issues book to the member
#checks if book is available
#if available then issues book
#return: -1 --> member does not exist
#return -2 --> book is not available
#return True --> Vijay
#return False --> gadbad
def issue_book(mem_id, acn, issue_date):
    tray = setu.cursor()

    #validation of parameters
    mem_status = does_member_exist(mem_id) #
    book_status = is_book_available(acn)    # if returns -1 pop error " wrong accession no." (book exists check is implicit)


    if mem_status and book_status:
        #print(acn + " " + mem_id)
        #print(issue_date)
        query = "INSERT into borrows(issue_date, issuers_id, accession_number) values(%s, %s, %s)";
        query1= "UPDATE books set is_available = 0 where accession_number=\'" + str(acn) + "\'";
        values = (issue_date, mem_id, acn)

        try:
            tray.execute(query,values)
            tray.execute(query1)
        except ms.IntegrityError as err:
            print("Intergrity Error: " + str(err))
        except ms.Error as err:
            print("Other Error: " + str(err))

        print(str(tray.statement))

        if(tray.rowcount == 1):
            setu.commit()
            print(str(tray.rowcount) + " Book issues")
            return True
        elif (tray.rowcount == -1):
            print("Error ala re")
            return False
        else:
            print("Jast books issue zhale wattat " + str(tray.rowcount))
            return False
    else:
        if mem_status == False:
            return -1;
        elif book_status == False:
            return -2;



#is book issued??? function
#input parameters: acn
#check prescence of book in borrows table where return date must be null
def is_book_issued(acn):
    check = setu.cursor()
    query = "SELECT * from borrows where accession_number = \'" + acn + "\' and return_date is NULL;"

    try:
        check.execute(query)
    except db.Error as err:
        print(str(err))



    book_count = len(check.fetchall())
    if book_count > 1 or book_count < 0:
        return False;
    else:
        return book_count



#return book funtion
#input parameters : mem_id, accession_number, return_date, remarks
#returns : -1 -> member does not exist
#          -2 -> book is not issued
def return_book(mem_id, acn, return_date, remark):
    tray = setu.cursor()
    #validation of parameters
    mem_status = does_member_exist(mem_id)
    book_issued = is_book_issued(acn)



    query = "UPDATE borrows SET return_date = %s, remarks = %s where issuers_id = %s and accession_number = %s;"
    values = (return_date, remark, mem_id, acn)
    query1 = "UPDATE books SET is_available = 1 where accession_number = \'" + acn + "\'"

    if mem_status and book_issued:
        try:
            tray.execute(query, values)
            tray.execute(query1)
        except ms.IntegrityError as err:
            print("Intergrity Error: " + str(err))
        except ms.Error as err:
            print("Other Error: " + str(err))

        if(tray.rowcount == 1):
            setu.commit()
            print(str(tray.rowcount) + " Book Returned")
            return True
        elif (tray.rowcount == -1):
            print("Error ala re")
        else:
            print("Jast books returned zhale wattat " + str(tray.rowcount))
    else:
        if mem_status == False:
            return -1;
        elif book_issued == False:
            return -2;


#get unreturned books all
#
#returns all unreturned books
def getUnreturnedBooks(searchBy ,searchFor):
    pustak = setu.cursor()

    query = """select borrows.accession_number, books.title, members.full_name, borrows.issue_date, members.mobile_number, members.member_id
    from((borrows inner join members on borrows.issuers_id = members.member_id and return_date is NULL)
    inner join books on borrows.accession_number = books.accession_number )
    where """+searchBy+""" like \'"""+searchFor+"""%\' order by borrows.issue_date desc ;"""

    try:
        pustak.execute(query)
    except ms.Error as err:
        print(err)
        return -1

    books = pustak.fetchall()

    if len(books) == 0:
        return False
    else:
        return books;
