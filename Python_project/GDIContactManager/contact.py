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

    while True:
        phone_num_entered = input("Please Enter in a Phone Number (+1,xxx-xxx-xxxx): ")
        valid,formatted_num = get_phone(phone_num_entered)
        if valid == True:
            break
        else:
            chk = input("\nWould you like to try again? (Y/N)")
            if chk[:1].upper() == "Y":                
                continue
            elif chk[:1].upper() == "N":
                print("\nPhone Number couldn't be validated.")
                break    
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
    print(newString)
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    #if mainString[0] in "-" :
    #            mainString = mainString.replace("-", "" , 1)
                
    return  mainString

def main():
    print("\nWelcome to Contact Manager\n")
    menu()

if __name__ == "__main__":
    main()