import sys
import csv

contacts = []
contacts = [['Clark','Melanie','Melanie Clark','asldfj@lskdjf','23948-234'],['mel','Clark','Mel Clark','lskdfj@slkdjf','234']]

def menu():

    print("\nCommand Menu\n")
    print("list - Display all contacts")
    print("view - View a contact\n")
    print("add - Add a contact")
    print("del - Delete a contact")
    print("exit - Exit program\n")

    choice = input()
    choice = choice.lower()

    while True:
        if choice == "list":
            all_contacts()
        elif choice == "view":
            print("Command:  View")
            search = input("Search Name: ")
            view(search)
        elif choice == "add":
            add()
        elif choice == "del":
            print("Command:  Delete")
            search = input("Search Name: ")
            matches = view(search)
            if len(matches) <= 0:
                print("\nNo Matches Found.")
            else:
                delete(matches)
        elif choice == "exit":
            break
        else:
            print("\nYou must only select either list, view, del, or exit.")
            print("Please try again")
        menu()

    print("Exiting the Contact Manager")
    #Contacts are not to be saved
    contacts=[]
    sys.exit()

def all_contacts():
#lists all the contacts
    print("\nCommand: List")
    global contacts
    if active_list():
        for i, (lname,fname,fullname,email,number) in enumerate(contacts):
            print("{}. {}  Email:{}  Phone:({})".format(i+1,fullname,email,number))
            print()

def view(search):
#list one contact
    search_list = []
    if active_list():
        cnt = 0
        for item in contacts:
            if search.upper() in str(item).upper():
                #Display items that are possible matches and store
                print("{}. {}  Email:{}  Phone:({})".format(cnt+1,item[2],item[3],item[4]))
                search_list.append(item)
                cnt += 1
    return search_list

def getname():

    fullname = input("Name: ")
    lname = ""
    fname = ""

    if is_fullname(fullname) == False:
        getname()

    chk = "Y"
    #Check First Name and Last Name are correct.
    while chk != "Y":
        chk = input("Is the first name {} and last name {}? (Y/N)".format(fname,lname))
        lname = input("Enter the last name: ")
        lname = lname.capitalize()
        fname = input("Enter the first name: ")
        fname = fname.capitalize()
        fullname = fname + " " + lname
        chk = input("Is this correct " + fullname + "? (Y/N)")

    return fullname, lname, fname

def is_fullname(name):
    try:
        fname, lname = name.split(" ")
        return True
    except ValueError:
        print("\nLast and first name required.")
        return False

def add():
#(1)Identifies for duplicate names.
#(2)Adds one new contact.

    global contacts

    print("\nCommand:  Add")
    fullname, lname, fname = getname()
    email = input("Email: ")
    num = input("Phone: \n")

   #Check if Contact Exists
    res1 = any(fullname in sublist for sublist in contacts)
    if res1 == True:

        print("\nWarning:  This Contact May Exists")

        while True:
            chk = input("\nWould you like to continue? (Y/N)")
            if chk[:1].upper() == "Y":
                contacts.append([lname,fname,fullname,email,num])
                print("\n\n" + fullname + " was added.")
                break
                #print(contacts)
            elif chk[:1].upper() == "N":
                print("\nContact Not Added")
                break
    else:
        contacts.append([lname,fname,fullname,email,num])
        print(fullname + " was added.")

def active_list():
    if len(contacts) > 0:
        return True
    else:
        print("\nThe Contact List is Empty")
        return False

def is_number(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def delete(matches):
#(1)Displays lists of contacts
#(2)User selects one contact to delete

    rst = input("\nSelect a contact to be deleted from 1 to " + str(len(matches))+": ")

    try:
        if is_number(rst) == True:
            rst = int(rst)
            print(rst)
            if rst > 0 and rst <= len(matches):
                contacts.remove(matches[rst-1])
                print("\nDelete successful.")
            else:
                print("\nInvalid Selection.")
                menu()
        else:
            print("\nInvalid selection. Try again.")
            menu()
    except ValueError:
        print("\nInvalid selection.")
        menu()


def main():
    print("\nWelcome to Contact Manager\n")
    menu()

if __name__ == "__main__":
    main()