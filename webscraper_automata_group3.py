import customtkinter
import tkinter
from bs4 import BeautifulSoup
import requests
import re
import string
import urllib
import os
import html.parser
import html.entities

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x500")
app.title("Web Scraping Tool")

def newWindow():
    
    #request webpage
    site = url_entry.get()
    page = requests.get(str(site))
    class_name = class_entry.get()
    soup = BeautifulSoup(page.content, 'html.parser')
    
    
    #new window
    newWindow = customtkinter.CTkToplevel(app)
    newWindow.title("Broken Url Display")
    newWindow.geometry("800x500")
    
    n = radio_var.get()
    if n == 2:
        
        url = soup.find_all(class_=str(class_name))
        url = str(url)
        print(url)
        
        list = re.findall('>(.*?)<', url)
        print(str(list))

        with open("\\Downloads\\text_scraped.txt", "w") as f:
            for data in list:
                f.write(data + "\n")
                
        #soup label
        scrape_label = customtkinter.CTkLabel(newWindow, font=("Roboto", 15), text="Scraped Url:")
        scrape_label.pack()
        broken_url = customtkinter.CTkTextbox(newWindow, font=("Roboto", 13), width=790, height=450)
        broken_url.pack(pady=20)
        broken_url.insert("0.0", url + "\n")
        
    elif n == 1:
        
        
        #imgdata = []
        img = soup.find_all(class_=str(class_name))
        img = str(img)
        
        scrape_label = customtkinter.CTkLabel(newWindow, font=("Roboto", 15), text="Scraped Url:")
        scrape_label.pack()
        broken_url = customtkinter.CTkTextbox(newWindow, font=("Roboto", 13), width=790, height=450)
        broken_url.pack(pady=20)
        broken_url.insert("0.0", img + "\n")
        
        img_src = 'src="(.*?)"'
        src = re.findall(img_src, img)
        print(str(src))
        
        parent_dir = "\\Downloads\\"
        directory = "image"
        path = os.path.join(parent_dir, directory)
        mode = 0o666
        os.makedirs(path, mode)
        
        filename = "image{}.jpg"
        for i in range(len(src)):
            print(f"img {i+1} / {len(src)+1}")
            s = site + "/" + str(src[i])
            print(str(s))
            try:
                r = requests.get(str(s), stream=True)
                with open("\\Downloads\\image\\" + filename.format(i), "wb") as f:
                    f.write(r.content)
            except:
                print("null")
              

#screen
frame = customtkinter.CTkFrame(master=app)
frame.pack(padx=20, fill="both", expand=True)
frame2 = customtkinter.CTkFrame(master=app)
frame2.pack(padx=20, fill="both", expand=True)


#title
title = customtkinter.CTkLabel(master=frame, text="Web Scraping Tool", font=("Roboto", 30, "bold"))
title.pack(pady=20, padx=20)


#user entry url - step 1
url_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter Url")
url_entry.pack(padx=70, fill="both")
class_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter Class Name")
class_entry.pack(pady=9, padx=70, fill="both")


#radiobutton for user option on text or image - step 1
radio_var = customtkinter.IntVar()
label_radio = customtkinter.CTkLabel(master=frame, text="Choose what do you want to scrape: ", font=("Roboto", 13, "italic"))
label_radio.pack(padx=50)
image_radio = customtkinter.CTkRadioButton(master=frame, variable=radio_var, value=1)
image_radio.pack(pady=10, padx=50)
text_radio = customtkinter.CTkRadioButton(master=frame, variable=radio_var, value=2)
text_radio.pack(padx=50)


#submit - step 1
url_button = customtkinter.CTkButton(master=frame)
url_button.pack(pady=20, padx=20)

#set values - step 1
image_radio.configure(text="Image")
text_radio.configure(text="Text")
url_button.configure(text="Submit", command=newWindow)



app.mainloop()

