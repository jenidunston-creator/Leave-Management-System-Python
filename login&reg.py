import sqlite3
from datetime import datetime
con = sqlite3.connect("mini.db")
c=con.cursor()

c.execute("PRAGMA foreign_keys=ON")

c.execute("""CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT 
                );
""")


c.execute("""CREATE TABLE IF NOT EXISTS leave_request (
            leave_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            leave_date TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
            );
""")

# c.execute("""INSERT INTO leave_request (user_id, leave_date, reason) VALUES(?,?,?)""",(5,"15-06-2026","Personal Commitment"))
# con.commit()


# c.execute("DELETE FROM leave_request WHERE leave_id = ?", (3,))
# con.commit()
#
# c.execute("DELETE FROM user WHERE id=?", (7,))
# con.commit()

#REGISTER FUNCTION

def regfn():

    u=input("Enter username : ")
    p=input("Enter password: ")
    user_type=input("Enter user type:Employer/Employee: ")
    if u=="":
        print("Username cannot be empty")
        return
    if p=="":
        print("Password cannot be empty")
        return
    if user_type=="":
        print("User type cannot be empty")
        return
    if user_type not in ['Employee','Employer']:
        print("Invalid user type")
        return
    #CHECK DUPLICATE
    c.execute("SELECT * FROM user WHERE username=?",(u,))
    x=c.fetchone()
    if x:
        print("username already exists")
        return

    try:
        c.execute("INSERT INTO user (username,password,user_type) VALUES (?,?,?)",(u,p,user_type))
        con.commit()
        print("Registration Successful")
    except:
        print("Registration failed. Try again.")

#Employee Menus:


def apply_leave(user_id):
    leave_date = input("Enter Leave Date (DD-MM-YYYY): ")
    reason = input("Enter Reason: ")

    if leave_date=="":
        print("Leave Date cannot be empty")
        return
    if reason=="":
        print("Reason cannot be empty")
        return
    try:
        datetime.strptime(leave_date, "%d-%m-%Y")
    except ValueError:
        print("Leave Date is not a valid date")
        return

    c.execute("SELECT * FROM leave_request WHERE user_id=? AND leave_date=?",(user_id, leave_date))

    if c.fetchone():
        print("Leave request already exists for this date")
        return

    c.execute(
        "INSERT INTO leave_request(user_id, leave_date, reason) VALUES(?,?,?)",(user_id, leave_date, reason))

    con.commit()
    print("Leave Applied Successfully")

def view_my_leave(user_id):
    c.execute(
        "SELECT * FROM leave_request WHERE user_id=?",(user_id,))
    rows = c.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No Leave Requests Found")

def delete_my_leave(user_id):

    try:
        leave_id = int(input("Enter Leave ID to Delete: "))
    except ValueError:
        print("Please enter a valid Leave ID:")
        return

    c.execute("DELETE FROM leave_request WHERE leave_id=? AND user_id=? AND status='Pending'",(leave_id, user_id))
    con.commit()

    if c.rowcount>0:
        print("Leave Deleted")
    else:
        print("No matching pending leave found")

def update_my_leave(user_id):

    try:
        leave_id = int(input("Enter Leave ID: "))
    except ValueError:
        print("Please enter a valid Leave ID")
        return

    c.execute(
        "SELECT * FROM leave_request WHERE leave_id=? AND user_id=? AND status='Pending'",(leave_id, user_id))

    if c.fetchone() is None:
        print("Only Pending leave can be updated")
        return

    new_date = input("Enter New Leave Date (DD-MM-YYYY): ")
    new_reason = input("Enter New Reason: ")

    if new_date == "":
        print("Leave Date cannot be empty")
        return

    if new_reason == "":
        print("Reason cannot be empty")
        return
    try:
        datetime.strptime(new_date, "%d-%m-%Y")
    except ValueError:
        print("Invalid Date Format")
        return

    c.execute("SELECT * FROM leave_request WHERE user_id=? AND leave_date=? AND leave_id<>?",(user_id, new_date, leave_id))

    if c.fetchone():
        print("Leave request already exists for this date")
        return

    c.execute(
        "UPDATE leave_request SET leave_date=?, reason=? WHERE leave_id=?",(new_date, new_reason, leave_id) )

    con.commit()
    print("Leave Updated Successfully")

#Employer Menus:
def view_all_leave():

    c.execute("SELECT * FROM leave_request")

    rows = c.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No Leave Requests Found")

def approve_leave():
    try:
        leave_id = int(input("Enter Leave ID to Approve: "))
    except ValueError:
        print("Please enter a valid Leave ID:")
        return

    c.execute(
        "UPDATE leave_request SET status='Approved' WHERE leave_id=? AND status='Pending'",(leave_id,))
    con.commit()
    if c.rowcount>0:
        print("Leave Approved")
    else:
        print("No Pending Leave Record Found")

def reject_leave():
    try:

        leave_id = int(input("Enter Leave ID to Reject: "))
    except ValueError:
        print("Please enter a valid Leave ID:")
        return

    c.execute(
        "UPDATE leave_request SET status='Rejected' WHERE leave_id=? AND status='Pending'",(leave_id,))

    con.commit()
    if c.rowcount>0:
        print("Leave Rejected")
    else:
        print("No Pending Leave Record Found")

#login function
def loginfn():
    u=input("Enter username: ")
    p=input("Enter password: ")
    user_type = input("Enter user type:Employer/Employee: ")
    c.execute("SELECT * FROM user WHERE username=? AND password=? AND user_type=?", (u, p, user_type))

    x=c.fetchone()

    if x:
        print("Welcome", x[1], "Role:", x[3])
        if x[3]=="Employer":
            while True:
                print("1. View Leave Requests")
                print("2. Approve Leave")
                print("3. Reject Leave")
                print("4. Exit")
                try:
                    a = int(input("Enter your choice: "))
                except ValueError:
                    print("Please enter a number")
                    continue
                if a == 1:
                    view_all_leave()
                elif a == 2:
                    approve_leave()
                elif a == 3:
                    reject_leave()
                elif a == 4:
                    print("Exit")
                    break
                else:
                    print("Invalid choice")


        elif x[3]=="Employee":
            while True:
                print("1. Apply Leave & Reason")
                print("2. View My Leave Requests")
                print("3. Delete My Leave Request")
                print("4. Update My Leave Request")
                print("5. Exit")
                try:
                    a = int(input("Enter your choice: "))
                except ValueError:
                    print("Please enter a number")
                    continue
                if a == 1:
                    apply_leave(x[0])
                elif a == 2:
                    view_my_leave(x[0])
                elif a == 3:
                    delete_my_leave(x[0])
                elif a==4:
                    update_my_leave(x[0])
                elif a==5:
                    break
                else:
                    print("Invalid Choice")

    else:
        print("Invalid Credentials")
while True:
    print("Leave Management System")
    print("1 = Registration")
    print("2 = Login")
    print("3 = Exit")
    try:
        a=int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a number")
        continue
    if a==1:
        regfn()
    elif a==2:
        loginfn()
    elif a==3:
        print("Thank You")
        break
    else:
          print("Invalid Choice")
