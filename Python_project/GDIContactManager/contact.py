import random
import re
import sys

from random import choice

contacts = []
uids = []
#contacts = [['Clark','Melanie','Melanie Clark','asldfj@lskdjf','23948-234'],['mel','Clark','Mel Clark','lskdfj@slkdjf','234']]

def menu():

    print("\nCommand Menu\n")
    print("list - Display all contacts")
    print("view - View a contact")
    print("add - Add a contact")
    print("del - Delete a contact")
    print("exit - Exit program\n")

    choice = input("Enter a command from the above list: ")
    choice = choice.lower()

    while True:
        if choice == "list":
            all_contacts()
        elif choice == "view":
            print("Command:  View")
            search = input("Search Name (first and last): ")
            view(search)
        elif choice == "add":
            add()
        elif choice == "del":
            print("Command:  Delete")
            search = input("Search Name (first and last): ")
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
        for i in contacts:
            print(i)

def view(search):
#list one contact
    search_list = []
    if active_list():
        cnt = 0
        for entry in contacts:
            if search.upper() in str(entry).upper():
                #Display items that are possible matches and store
                print(entry)
                search_list.append(entry)
                cnt += 1
    return search_list

def getname():

    verified_name = False

    #check if the user has entered their fullname before proceding
    while not verified_name:
        fullname = input("Name (first and last): ")
        verified_name = is_fullname(fullname)

    #create the variables to hold first name and last name
    fname, lname = fullname.split(" ")

    #check First Name and Last Name are correct.
    chk = input(f"Is the full name *{fname} {lname}* correct? (Y/N) ")
    accepted_answers = ["Y", "y", "YES", "yes", "yup", "Yes"]
    
    if chk not in accepted_answers:
        #re-run the function
        getname()

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
    random_uid = None

    if len(uids) >0:
        # create a new random UID for this addition, and then append the UID list
        random_uid = choice([i for i in range(0,100) if i not in uids])
    else:
        random_uid = random.randint(0, 100)

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    print("\nCommand:  Add")
    fullname, lname, fname = getname()
    
    email = input("Email: ")
    email_validated = re.search(regex, email)

    #check if the e-mail is the correct format
    while not email_validated:
        email = input("Please enter a valid e-mail: ")
        email_validated = re.search(regex, email)

    phone_num_entered = input("Please enter a phone number: ")

    phone_num = []

    for n in phone_num_entered:
        if n.isdigit():
            phone_num.append(n)
    
    formatted_num = "".join(phone_num)
    
    print (f"The phone number added is {formatted_num}")

   #Check if Contact Exists
    res1 = any(fullname in sublist for sublist in contacts)

    if res1 == True:
        
        print(f"Warning: A similar contact was found.  This may be a duplicate. {res1}")

        while True:
            chk = input("\nWould you like to continue? (Y/N)")
            if chk[:1].upper() == "Y":
                contacts.append([random_uid,lname,fname,fullname,email,formatted_num])
                uids.append(random_uid)
                print(f"\n\n {fullname} was added")
                break
                #print(contacts)
            elif chk[:1].upper() == "N":
                print("\nContact Not Added")
                break
    else:
        contacts.append([random_uid, lname,fname,fullname,email,formatted_num])
        uids.append(random_uid)
        print(f"{fullname} was added.")

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

    record_to_delete = input("\nSelect a contact to be deleted by entering their User ID: ")

    try:
        if is_number(record_to_delete):
            record_to_delete = int(record_to_delete)

            #loop through all the entries and look at the first element
            records_deleted = 0
            
            for entry in contacts:
                if int(entry[0]) == record_to_delete:
                    contacts.remove(entry)
                    print("\nDelete successful.")
                    records_deleted += 1
            if records_deleted == 0:
                print("The record you've selected does not exist.  Please try again.")
                menu()
    except ValueError:
        print("\nInvalid selection.")
        menu()


def main():
    print("\nWelcome to Contact Manager\n")
    menu()

if __name__ == "__main__":
    main()