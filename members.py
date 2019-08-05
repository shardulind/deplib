import mysql.connector as ms
from db_credentials import setu
#1. getMemberNameFromID
#2. does_member_exist
#3. delete_member_by_id
#4. add_new_member
#5. getAllMembers






#get member Name
#input parameter: member idea
#returns: member name
#returns -1 -->error
#return False --> member doesnot exist
def getMemberNameFromID(mem_id):
    shodh = setu.cursor()
    query = "SELECT full_name from members where member_id = " + str(mem_id)
    try:
        shodh.execute(query)
    except ms.Error as err:
        print(err)
        return -1

    mname = shodh.fetchall()
    if len(mname) == 0:
        return False
    else:
        return str(mname[0][0])



#does member exist
#input parameters: memid

def does_member_exist(mid):
    shodh = setu.cursor()
    query = "select * from members where member_id = " + str(mid)
    try:
        shodh.execute(query)
    except db.Error as err:
        print(err)

    #print(shodh.statement)
    results = shodh.fetchall()
    if len(results) == 1:
        return True;
    else:
        return False;



#delete member using members id
def delete_member_by_id(mid):
    nsht = setu.cursor()
    query = "delete from members where member_id = " + str(mid) + ";"
    try:
        nsht.execute(query)
        setu.commit()
    except db.Error as err:
        print(err)

    print(str(nsht.rowcount) + " member deleted Successfully");

    if nsht.rowcount == 0:
        return -1;
    elif nsht.rowcount == 1:
        return 1;
    else:
        return nsht.rowcount

#add new memeber
#returns integrity error if Error
#or returns 1 for success
def add_new_member(mtype, mmno, emailid, fname):
    add = setu.cursor()
    query = "insert into members(member_type, mobile_number ,email_id, full_name ) values(%s,%s,%s,%s)"
    val = (mtype.upper(), mmno, emailid, fname.upper())
    try:
        add.execute(query,val)
        setu.commit()
    except ms.IntegrityError as err:
        return err

    print(add.rowcount," Members added into Database")
    return 1;


#get allmembers
#returns list of all numbers
#("member_id", "full_name", "mobile_number", "email_id","member_type")

def getAllMembers():
    yadi = setu.cursor()
    query = "SELECT member_id, full_name, mobile_number, email_id, member_type FROM members"
    try:
        yadi.execute(query)
    except db.Error as err:
        print(err)
        return -1

    members = yadi.fetchall()
    #print(members)
    return members


#search member by
#input search_by,search_for
#return members
#return false

def searchMember(searchBy, searchFor):
    shodh = setu.cursor()
    query = "SELECT member_id, full_name, mobile_number, email_id, member_type FROM members where "+searchBy+" like \'"+searchFor+"%\'"

    try:
        shodh.execute(query)
    except db.Error as err:
        print(err)
        return -1

    members = shodh.fetchall()
    if len(members) == 0:
        return False
    else:
        return members
