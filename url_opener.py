from sys import *
import webbrowser
import re
import urllib.request
import urllib.error
 

def is_connected():
    try:
        urllib.request.urlopen("https://216.58.192.142", timeout=1)
        return True
    except urllib.error.URLError as err:
        return False

def Find(string):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|[?:%[-9a-fA-F]))+',string)
    return url

def WebLauncher(path):
    with open(path) as fp:
        for line in fp:
            print(line)
            url = Find(line)
            print(url)
            for str in url:
                webbrowser.open(str,new = 2)

def main():
    print("-----------Rushikesh Kotule-----------------")

    print("URL Open Automation App  " +argv[0])

    if (len(argv)!=2):
        print("Invalid Number of Arguements")
        exit()
    
    if (argv[1] == "-h") or (argv[1] == "-H"):
        print("The Script is used to open the URLs which are written in file")
        exit()
    
    if (argv[1] == "-u") or (argv[1] == "-U"):
        print("Usage: urlopen.py Name_of_file")
        exit()

    try:
        connected = is_connected()

        if connected:
            WebLauncher(argv[1])
        else:
            print("Unable to Connect to Interenet")
    
    except ValueError:
        print("Error: Invalid datatype of input")
    
    except Exception as E:
        print("Error: Invalid Input", E)
    

if __name__ == "__main__":
    main()

