import skpy
import sys
import getpass

def login_func():
    #Get Credentials from user
    while True:
        print("Enter your Skype Credentials")
        username = input(" Enter Skype Email id or Mobile Number:   ")
        password = getpass.getpass(prompt=" Enter Your Password: \t")

    #Validate
        if not username or not password:
            print("Please enter both Username and Password..\n")
        
        else:
            try:
                login = skpy.Skype(username,password)
                return login
            except skpy.core.SkypeAuthException:
                print("*****Please enter Valid Credentials***** \n\n:")    

login = login_func()

while True:
    #Desired Groups input from user
    print("\n\n",80*"*","\n",80*"*")
    print("\n\n\tImportant Steps to Use this Bot\n\t 1) Please Enter Your Group Options (Comma Seperated)\n\t 2) To mention @all you can use this on new line -->     Hi <at id=\"*\">all </at>\n\t 3) Enter your Message. You can use new line\n\t 4)Use <b>text</b> to make the required text in Bold Format\n\t 5)Once all message completed Press Enter and then Press CTRL+Z on new line to finish\n\t 6) Enter to send the Message")
    print("\n\n",80*"*","\n",80*"*")
    print("\n\n List of Groups: \n\t1: Here goes the list of groups")
    user_input = input("\nPlease Enter Your Group Options (Comma Seperated) \t")
    choices = user_input.split(",")
    choices = [int(c.strip()) for c in choices]
    group_selected = []

    #Groups Ids to match with entered input
    options = {
        1:login.chats["list of group ids"],
        2:login.chats["list of group ids"],
        17:login.chats["list of group ids"],
    }

    try:
        if not choices or any((not isinstance(c,int)) or c not in range(1,17) for c in choices):
            print("******Invalid Input has been Entered!!*******")

        else:
            #If user wants to select all Groups option except first one
            if 18 in choices:
                group_selected = [login.chats["list of group ids "],
                                ]
                
            #Else message will get sent to customized input
            else:
                for selected in choices:
                    if isinstance(options[selected],skpy.SkypeGroupChat):
                        group_selected.append(options[selected])
                    
                    else:
                        group_selected += options[selected]
        
        if not group_selected:
            print("Invalid data, program will now exit")
            sys.exit()

    except ValueError:
        print("You have entered wrong inputs...try again")
    
    print("Type/Paste Your Message below \n")
    msg = sys.stdin.read()
    for group_chat in group_selected:
        group_chat.sendMsg(msg, rich=True)
    
    ch= input("\nDo you want to continue\t YES/NO:\t")

    if ch.lower()=="no":
        sys.exit()
    else:
        continue
