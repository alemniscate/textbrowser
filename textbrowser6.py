import sys
import os.path
from collections import deque
import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Style

def show_and_save(url, path):  
    try: 
        res = requests.get(url)
        if res.status_code != 200:
            return False
    except Exception:
        return False
    
    text = res.text
    soup = BeautifulSoup(text, 'html.parser')
    body = soup.body
    text = ""
    for elm in body:
        if elm == "\n":
            continue
        for a in elm.find_all("a"):
            atext = a.get_text()
            text += Fore.BLUE + atext + Style.RESET_ALL + "\n"
        text += re.sub("\n+", "\n", elm.get_text())
 
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)

    print()
    print(text)
    print()
    return True

if len(sys.argv) > 1:
    dirname = sys.argv[1]
    if not os.path.exists(dirname):
        os.mkdir(dirname)
else:
    dirname = "test"

stack = deque()

while True:
    command = input()
    if command == "exit":
        break
    elif command == "back":
        if stack:
            text, path = stack.pop()
        else:
            continue
        if stack:
            text, path = stack.pop()
            show_and_save(text, path)

    url = "https://" + command
    path = dirname + "/" + os.path.splitext(os.path.basename(command))[0]
    if not show_and_save(url, path):
        print("Incorrect URL")