import json
from pprint import pprint
import requests
from tkinter import *

root = Tk()
#frontPage = Tk()
#searchGUI = Text(frontPage, height=50, width=50)
resultGUI = Text(root, height=50, width=50)

L = list(input('What do you want to search for: '))
for y in range(len(L)):
    if L[y] == " ":
        L[y]="+"
        
f = requests.get("https://www.googleapis.com/books/v1/volumes?q="+(''.join(L))+"&callback=handleResponse")
json_string = (f.text)[31:-2]

#text_file = open("Output.json", "w", encode = 'utf-8')

text_file = open("Output.json", "w")
text_file.write(json_string)
text_file.close()


#data = json.load(open('Output.json', encode = 'utf-8'))

data = json.load(open('Output.json'))

#pprint(data)

title = "blank"
isbn_type = "blank"
isbn_num = "blank"
isbn_num_clean = "blank"
publisher = "blank"
author = "blank"
date = "blank"
date_flipped = "blank"
image_url = "blank"
price = "blank"


for x in range(10):


    #Extracts each bit of data from the json file
    #TITLE EXTRACT
    title = data["items"][x]["volumeInfo"]["title"]

    #The json file puts isbn 10 and 13 in random order need if to workout which to print
    #ISBN EXTRACT
    try:
        if ((data["items"][x]["volumeInfo"]["industryIdentifiers"][0]["type"]) == "ISBN_13"):
            isbn_type = data["items"][x]["volumeInfo"]["industryIdentifiers"][0]["type"]
            isbn_num = data["items"][x]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
        elif ((data["items"][x]["volumeInfo"]["industryIdentifiers"][0]["type"]) == "ISBN_10"):
            isbn_type = data["items"][x]["volumeInfo"]["industryIdentifiers"][1]["type"]
            isbn_num = data["items"][x]["volumeInfo"]["industryIdentifiers"][1]["identifier"]
        else:
            isbn_num = "NO ISBN NUMBER"
    except (KeyError):
        isbn_num = 'this is a bug';
    
    #AUTHOR EXTRACT
    try:
        author = data["items"][x]["volumeInfo"]["authors"]
    except KeyError:
        pass

    #PUBLISHER EXTRACT
    try:
        publisher = data["items"][x]["volumeInfo"]["publisher"]
    except KeyError:
        pass
    
    date = data["items"][x]["volumeInfo"]["publishedDate"]

    if(data["items"][x]["saleInfo"]["saleability"]=="FOR_SALE"):
        price = '$'+str(data["items"][x]["saleInfo"]["listPrice"]["amount"])
    else:
        price = "NOT_FOR_SALE"
    
    title = data["items"][x]["volumeInfo"]["title"]

    #changes formatting of data that is in the incorrect format
    if isbn_num != "NO ISBN NUMBER":
        isbn_num_clean = isbn_num[:3] + '-' + isbn_num[3:]
    else:
        isbn_num_clean = isbn_num
    if (len(date) == 4):
        date_flipped = date
    elif (len(date) == 7):
        date_flipped = date[-2:]+'/'+date[:4]
    else:
        date_flipped = date[-2:]+'/'+date[5:-3]+'/'+date[:4]

    resultGUI.insert(END,"\n" + title + "\n" + isbn_type + ":" + isbn_num + "\n")
    #for i in author:
    #    if 'A' <= i <= 'Z':
    #        i = " "+ i
    #    resultGUI.insert(INSERT, i)
    resultGUI.insert(END, ' & '.join(author))
    resultGUI.insert(END, "\n" + publisher + ":" + date_flipped + "\nPrice:" + price + "\n\n==================================================\n")
    #    + 
    
    resultGUI.pack()

S = Scrollbar(root)
S.pack(side=RIGHT, fill=Y)
resultGUI.pack(side=LEFT, fill=Y)
S.config(command=resultGUI.yview)
resultGUI.config(yscrollcommand=S.set)

root.mainloop()



input ("Press enter to exit")





























