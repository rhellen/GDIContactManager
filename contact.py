import re
import sys

contacts = []
uids = []

class Contact:
#common base class for all Contacts
    
    #initializes our class; only UID, last name, first name, full name and email are required - phone is optional
    def __init__(self, uid, lname, fname, fullname, email, phone_number = None):
        
        self.uid = uid
        self.lname = lname
        self.fname = fname
        self.fullname = fullname
        self.email = email
        self.phone_number = phone_number
     
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
            print("Command:  List")
            all_contacts()
        elif choice == "view":
            print("Command:  View")
            view()
        elif choice == "add":
            add()
        elif choice == "del":
            print("Command:  Delete")
            delete()
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
    print ("Listing all contacts:")
    global contacts
    if active_list():
        for i in contacts:
            #print only their ID and full name
            print(f"{i.uid}, Full name: {i.fullname}")

def view():
#list one contact
    if active_list():
        all_contacts()
        selection = input("Enter the user's ID to view more details: \n")
        for entry in contacts:
            if int(selection) == int(entry.uid):
                print(f"User details for {entry.fullname}:\n")
                print(f"ID: {entry.uid}")
                print(f"Last name: {entry.lname}")
                print(f"First name: {entry.fname}")
                print(f"Full name: {entry.fullname}")
                print(f"E-mail: {entry.email}")
                if entry.phone_number:
                    print(f"Phone number: {entry.phone_number}")
                else:
                    print(f"Phone number: None provided")
        if int(selection) > len(contacts):
            print("\nContact not found. Please try again.")

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

    if len(uids) >0:
        #go through the UIDs so far and increment the last value by 1
        uid_val = uids[len(uids)-1]
  
        # create a new UID for the new contact
        new_uid = uid_val+1
    else:
        # our contact list is empty, so we start from 0 and give our first contact an ID of 1
        new_uid = 1

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    print("\nCommand:  Add")
    fullname, lname, fname = getname()
    
    email = input("Email: ")
    email_validated = re.search(regex, email)

    #check if the e-mail is the correct format
    while not email_validated:
        email = input("Please enter a valid e-mail: ")
        email_validated = re.search(regex, email)

    while True:
        phone_num_entered = input("Please Enter in a phone number (+1,xxx-xxx-xxxx) - this is optional: ")
        valid,formatted_num = get_phone(phone_num_entered)
        if valid == True:
            break
        else:
            chk = input("\nWould you like to try again? (Y/N) ")
            if chk[:1].upper() == "Y":     
                print (f"The phone number added is {formatted_num}")           
                continue
            elif chk[:1].upper() == "N":
                print("\nPhone Number couldn't be validated - no number was added.")
                break    
    

#Check if Contact Exists by checking for the same full name in the dictionary
    res1 = []

    for item in contacts:
        if fullname in item.fullname:
            res1.append(item)

    if len(res1) > 0:
        
        print(f"Warning: Similar contacts were found.  This may be a duplicate.")
        # from a customer perspective, we assume displaying the dupliate records are OK in this case
        # in other cases, we may not want to unless the user is an admin
        print (f"Here are the possible duplicates: \n")

        for con in res1:
            print(f"ID: {con.uid}, Fullname: {con.fullname}, Email: {con.email}, Phone number: {con.phone_number}")

        while True:
            chk = input("\nWould you like to continue? (Y/N)")
            if chk[:1].upper() == "Y":
                new_contact = Contact(new_uid, lname, fname, fullname, email, formatted_num)
                contacts.append(new_contact)
                uids.append(new_uid)
                print(f"\n\n {new_contact.fullname} was added")
                break
            elif chk[:1].upper() == "N":
                print("\nContact Not Added")
                break
    else:
        new_contact = Contact(new_uid, lname, fname, fullname, email, formatted_num)
        contacts.append(new_contact)
        uids.append(new_uid)
        print(f"Contact id: {new_uid} was added.")
        print(f"{new_contact.fullname} was added.")

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

def delete():
#(1)Displays lists of contacts
#(2)User selects one contact to delete

    all_contacts()
    record_to_delete = input("\nSelect a contact to be deleted by entering their User ID: ")
    
    try:
        if is_number(record_to_delete):
            record_to_delete = int(record_to_delete)

            #loop through all the entries and look at the first element
            records_deleted = 0
            
            for entry in contacts:
                if int(entry.uid) == record_to_delete:
                    contacts.remove(entry)
                    print("\nDelete successful.")
                    records_deleted += 1
            if records_deleted == 0:
                print("The record you've selected does not exist.  Please try again.")
                menu()
    except ValueError:
        print("\nInvalid selection.")
        menu()

def get_phone(phone):
    
    try:
        line = phone

        #line = "+1,(716)545-2718"
        #line = "+1,716 545-2718"
        #line = "+44 20 7987 0656"
        #line = "+1,716-454-1234"
        #line = "1,716 545 1212"
        #line = "(716)545 2718"
        #line = "7165452718"
        #line = "5454545"
        #line = "(716)lll545 2718"
        #line = "+1,7165452718"
        #line = "+17165452718"  Can't handle this case

        #Allowed characters striping letters
        newline = ""
        allowed = ['0','1','2','3','4','5','6','7','8','9','+','(',')'," ",',','-','.']        
        for char in line:
            if char in allowed:
                newline += char

        #Remove all extra characters in list and replace with space
        line = newline
        line = replaceMultiple(line, ['(' ,')' ,'.' ,'-' ,','] , " ")
        
        #Split the results
        line = line.lstrip()
        line = line.split(" ")
        rst = len(line)
        
        #International
        if "+" in line[0]:

            #"+ 1,716-454-1234"
            if rst == 5:
                return True,"{}{},({}){}-{}".format(line[0],line[1],line[2],line[3],line[4])
            #"+1,716-454-1234"
            elif rst == 4:
                return True,"{},({}){}-{}".format(line[0],line[1],line[2],line[3])
            elif rst == 2 and len(line[1])==10:
                numpart = str(line[1])
                return True, "{}({}){}-{}".format(line[0],numpart[0:3],numpart[3:6],numpart[6:10])
            else:
                print(f"Possible Error, International number (+1,xxx-xxx-xxxx): {phone}")
                return False, phone

        #Possible International
        #"1,716-545-2718"
        elif rst == 4:
            return True, "+{},({}){}-{}".format(line[0],line[1],line[2],line[3])

        #line = "(716)545 2718"
        elif rst == 3:
            if len(line[0])==3 and len(line[1])==3 and len(line[2])==4:
                return True, "({}){}-{}".format(line[0],line[1],line[2])
        #line="545 2121"
        elif rst == 2:
            if len(line[0])==3 and len(line[1])==4:
                return True, "{}-{}".format(line[0],line[1])
        elif rst == 1:
            numpart = str(line[0])
            if len(line[0])==10:                
                return True, "({}){}-{}".format(numpart[0:3],numpart[3:6],numpart[6:10])
            elif len(line[0])==7:                
                print ("Invalid format: {}-{}".format(numpart[0:3],numpart[3:6],numpart[6:9]))
                return False, phone                
            else:
                print(f"Possible Error, number (+1,xxx-xxx-xxxx): {phone}")
                return False, phone
        else:
            print(f"Possible Error, number (+1,xxx-xxx-xxxx): {phone}")            
            return False, phone
                
    except ValueError:
        print(f"Error: phone number (+1,xxx-xxx-xxxx): {phone}")
        return False, phone
        
def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    
    return  mainString

def main():
    # initialize a test list
    ramya = Contact(1, "Ramesh", "Ramya", "Ramya Ramesh", "rramesh1217@gmail.com", "(123)123-12345")
    uids.append(1)
    melanie = Contact(2, "Melanie", "Clark", "Melanie Clark", "test@test.com")
    uids.append(2)
    test_user = Contact(3, "Smith", "John", "John Smith", "johnsmith@gmail.com", "(412)412-4123")
    uids.append(3)
    
    contacts.append(ramya)
    contacts.append(melanie)
    contacts.append(test_user) 

    print("\nWelcome to Contact Manager\n")
    menu()

if __name__ == "__main__":
    main()
