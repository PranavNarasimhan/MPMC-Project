import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import pyttsx3
import os
import urllib.request
from bs4 import BeautifulSoup
import pathlib
import time
from mutagen.mp3 import MP3 
from PIL import Image 
from pathlib import Path
import smtplib
import imageio 
from moviepy import editor
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import tweepy
import twitter_api_keys

def convert(a):
    audio_path = os.path.join(os.getcwd(), "text.mp3") 
    video_path = os.path.join(os.getcwd(), "videos") 
    images_path = os.path.join(os.getcwd(), "images") 
    audio = MP3(audio_path) 
    audio_length = audio.info.length 
  
    list_of_images = [] 
    for image_file in os.listdir(images_path): 
        if image_file.endswith('.png') or image_file.endswith('.jpg'): 
            image_path = os.path.join(images_path, image_file) 
            image = Image.open(image_path).resize((400, 400), Image.ANTIALIAS) 
            list_of_images.append(image) 
  
    duration = audio_length/len(list_of_images) 
    imageio.mimsave('images.gif', list_of_images, fps=1/duration) 
  
    video = editor.VideoFileClip("images.gif") 
    audio = editor.AudioFileClip(audio_path) 
    final_video = video.set_audio(audio) 
    os.chdir(video_path) 
    final_video.write_videofile(fps=60, codec="libx264", filename="video.mp4") 

def notify_pib_officer():
    subject = "Press Release Audio Ready for Review"
    body = "Dear PIB Officer,\n\nThe audio version of the press release is ready for your review. " \
           "Please log in to the system to listen and provide your approval.\n\nBest Regards,\nPress Release System"
    sender_email = "kalyapranavnarasimhan@gmail.com"
    sender_password = "xdradhswdznddtvf"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    pib_officer_email= "kalyapranavnarasimhan@gmail.com"

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = pib_officer_email
    msg.attach(MIMEText(body,'plain'))
    filename ='text.mp3'
    attachment= open(filename, 'rb')
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(attachment_package)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [pib_officer_email], msg.as_string())
        text=msg.as_string()

        print("Audio File sent to PIB officer for review.")
    #vetting_process()
'''
def vetting_process(s):
    account_sid = 'ACdc490dc2ce250597449d10b06847ad62'
    auth_token = '[AuthToken]'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='+17209612976',
        to="+15558675310"
        body="Please review the generated audio file and let us know if we can proceed" 
     )

def upload_to_social_media():
    consumer_key = twitter_api_keys.consumer_key
    consumer_secret = twitter_api_keys.consumer_secret
    access_token = twitter_api_keys.access_token
    access_token_secret = twitter_api_keys.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    media = api.media_upload(convert('text.mp3'))
    tweet_text = "New press release audio: [Press Release Title] #PressRelease #PIB"
    api.update_status(status=tweet_text, media_ids=[media.media_id])

    print("Audio uploaded to Twitter.")

upload_to_social_media()
'''
def Output1():
    root=Tk()
    root.title("Text To Speech")
    root.geometry("900x450+200+200")
    root.resizable(False,False)
    root.configure(bg="#305065")

    engine = pyttsx3.init()

    def speaknow():
        text=text_area.get(1.0,END)
        gender=gender_combobox.get()
        speed=speed_combobox.get()
        voices=engine.getProperty('voices')
        def setvoice():
            if gender=='Male':
                engine.setProperty('voice',voices[0].id)
                engine.say(text)
                engine.runAndWait()
            else:
                engine.setProperty('voice',voices[1].id)
                engine.say(text)
                engine.runAndWait()
                
        if(text):
            if speed=="Fast":
                engine.setProperty('rate',250)
                setvoice()
            elif speed=='Normal':
                engine.setProperty('rate',150)
                setvoice()
            else:
                engine.setProperty('rate',60)
                setvoice()
                
    def download():
        text=text_area.get(1.0,END)
        gender=gender_combobox.get()
        speed=speed_combobox.get()
        voices=engine.getProperty('voices')
        def setvoice():
            if gender=='Male':
                engine.setProperty('voice',voices[0].id)
                path=filedialog.askdirectory()
                os.chdir(path)
                engine.save_to_file(text,'text.mp3')
                engine.runAndWait()
                notify_pib_officer()
                
            else:
                engine.setProperty('voice',voices[1].id)
                path=filedialog.askdirectory()
                os.chdir(path)
                engine.save_to_file(text,'text.mp3')
                engine.runAndWait()
                notify_pib_officer()
        if(text):
            if speed=="Fast":
                engine.setProperty('rate',250)
                setvoice()
            elif speed=='Normal':
                engine.setProperty('rate',150)
                setvoice()
            else:
                engine.setProperty('rate',60)
                setvoice()





    #icon
    image_icon=PhotoImage(file="speak.png")
    root.iconphoto(False,image_icon)

    #top frame
    Top_frame=Frame(root,bg="white",width=900,height=100)
    Top_frame.place(x=0,y=0)
    Logo=PhotoImage(file="speaker logo.png")
    Label(Top_frame,image=Logo,bg="white").place(x=10,y=5)
    Label(Top_frame,text="TEXT TO SPEECH",font="arial 20 bold",bg="white",fg="black").place(x=100,y=30)


    text_area=Text(root,font="Robote 20",bg="white",relief=GROOVE,wrap=WORD)
    text_area.place(x=10,y=150,width=500,height=250)

    Label(root,text="Voice",font="arial 15 bold",bg="#305065",fg="white").place(x=580,y=160)
    Label(root,text="Speed",font="arial 15 bold",bg="#305065",fg="white").place(x=760,y=160)

    gender_combobox=Combobox(root,values=['Male','Female'],font="arial 14",state="r",width=10)
    gender_combobox.place(x=550,y=200)
    gender_combobox.set('Male')


    speed_combobox=Combobox(root,values=['Fast','Normal','Slow'],font="arial 14",state="r",width=10)
    speed_combobox.place(x=730,y=200)
    speed_combobox.set('Normal')

    imageicon=PhotoImage(file='speak.png')
    btn=Button(root,text="Speak",compound=LEFT,image=imageicon,width=130,font="arial 14 bold",command=speaknow)
    btn.place(x=550,y=280)

    imageicon2=PhotoImage(file='download.png')
    save=Button(root,text="Save",compound=LEFT,image=imageicon2,width=130,bg='#39c790',font="arial 14 bold",command=download)
    save.place(x=730,y=280)

    root.mainloop()
#######################################################################################################################################################################
def Output2(text):
    root=Tk()
    root.title("Text To Speech")
    root.geometry("900x450+200+200")
    root.resizable(False,False)
    root.configure(bg="#305065")

    engine = pyttsx3.init()

    def speaknow(text):
        gender=gender_combobox.get()
        speed=speed_combobox.get()
        voices=engine.getProperty('voices')
        def setvoice():
            gender=input("Enter Gender:")
            if gender=='Male':
                engine.setProperty('voice',voices[0].id)
                engine.say(text)
                engine.runAndWait()                
            else:
                engine.setProperty('voice',voices[1].id)
                engine.say(text)
                engine.runAndWait()
        if(text):
            speed=input("Enter Speed:")
            if speed=="Fast":
                engine.setProperty('rate',250)
                setvoice()
            elif speed=='Normal':
                engine.setProperty('rate',150)
                setvoice()
            else:
                engine.setProperty('rate',60)
                setvoice()
                
    def download(text):
        gender=gender_combobox.get()
        speed=speed_combobox.get()
        voices=engine.getProperty('voices')
        def setvoice():
            gender=input("Enter Gender to be used in the save file:")
            if gender=='Male':
                engine.setProperty('voice',voices[0].id)
                path=filedialog.askdirectory()
                os.chdir(path)
                engine.save_to_file(text,'text.mp3')
                engine.runAndWait()
                
                a=pathlib.Path().absolute()
                res=[]
                for path in os.listdir(a):
                    if os.path.isfile(os.path.join(a,path)):
                        res.append(path)
                for i in res:
                    if i=='text.mp3':
                        notify_pib_officer()
            else:
                engine.setProperty('voice',voices[1].id)
                path=filedialog.askdirectory()
                os.chdir(path)
                engine.save_to_file(text,'text.mp3')
                engine.runAndWait()
                notify_pib_officer()
                
        if(text):
            speed=input("Enter Speed to be used in the save file:")
            if speed=="Fast":
                engine.setProperty('rate',250)
                setvoice()
            elif speed=='Normal':
                engine.setProperty('rate',150)
                setvoice()
            else:
                engine.setProperty('rate',60)
                setvoice()





    #icon
    image_icon=PhotoImage(file="speak.png")
    root.iconphoto(False,image_icon)

    #top frame
    Top_frame=Frame(root,bg="white",width=900,height=100)
    Top_frame.place(x=0,y=0)
    Logo=PhotoImage(file="speaker logo.png")
    Label(Top_frame,image=Logo,bg="white").place(x=10,y=5)
    Label(Top_frame,text="TEXT TO SPEECH",font="arial 20 bold",bg="white",fg="black").place(x=100,y=30)


    text_area=Text(root,font="Robote 20",bg="white",relief=GROOVE,wrap=WORD)
    text_area.place(x=10,y=150,width=500,height=250)

    Label(root,text="Voice",font="arial 15 bold",bg="#305065",fg="white").place(x=580,y=160)
    Label(root,text="Speed",font="arial 15 bold",bg="#305065",fg="white").place(x=760,y=160)

    gender_combobox=Combobox(root,values=['Male','Female'],font="arial 14",state="r",width=10)
    gender_combobox.place(x=550,y=200)
    gender_combobox.set('Male')


    speed_combobox=Combobox(root,values=['Fast','Normal','Slow'],font="arial 14",state="r",width=10)
    speed_combobox.place(x=730,y=200)
    speed_combobox.set('Normal')

    imageicon=PhotoImage(file='speak.png')
    btn=Button(root,text="Speak",compound=LEFT,image=imageicon,width=130,font="arial 14 bold",command=speaknow(text))
    btn.place(x=550,y=280)

    imageicon2=PhotoImage(file='download.png')
    save=Button(root,text="Save",compound=LEFT,image=imageicon2,width=130,bg='#39c790',font="arial 14 bold",command=download(text))
    save.place(x=730,y=280)

    root.mainloop()

def get_press_release_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def get_press_release_text_from_api(api_url):
    urllib.request.urlretrieve(api_url,"F:/MPMC project/example.txt")
 
    file = open("example.txt", "r")
    contents = file.read()
    soup = BeautifulSoup(contents, 'html.parser')
    return soup
print("Press Release Converter Menu:")
print("1. Read from a Text File")
print("2. Fetch from an API")
print("3. Enter Text Interactively")
choice = input("Enter your choice (1/2/3): ")
if choice == '1':
    file_path = input("Enter the path to the text file: ")
    text= get_press_release_text_from_file(file_path)
    Output2(text)
elif choice == '2':
    api_url = input("Enter the API URL: ")
    text= get_press_release_text_from_api(api_url)
    Output2(text)
elif choice == '3':
    Output1()
else:
    print("Invalid choice. Exiting......")

