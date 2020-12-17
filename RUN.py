#Here I have used multiprocessing to run both the programs together.
import speech_recognition as sr
import pyttsx3
import os
import random
import subprocess
import datetime 
import wikipedia
import webbrowser
import smtplib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import math
import pywhatkit
import pyjokes
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Assistant1 import Ui_MainWindow
import sys 
import multiprocessing

#To pop up the frontend of the assistant
def frontend():
    class Main(QMainWindow):
        def __init__(self):
            super().__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.movie = QtGui.QMovie("C:\\Users\\Jatin Dhall\\Desktop\\CS\\PYTHON\\PYTHON PROJECTSS\\BOT\\FinalModified\\Coolgif.gif")
            self.ui.AssistantUi.setMovie(self.ui.movie) 
            self.ui.movie.start()

    app=QApplication(sys.argv)
    assistant = Main()
    assistant.show()
    app.exec_()

def backend():
    r=sr.Recognizer()

    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)

    replies={"i am doing fine thank you":"Great so what can I do for you today?","not too great":"Oh, Is there something I can do to cheer you up?","thank you":"no problems at all sir"}
    #Add any custom replies here if you want
    contacts={}
    #Add your contact name as key and Phone number as value


    def wishme():
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            text="Good morning sir, what can I do for you"
        elif hour>=12 and hour<17:
            text="Good afternoon sir, what can I do for you"
        elif hour>=17 and hour<=0:
            text="Good evening sir, what can I do for you"
        texttospeech(text)

    def greet():
        hour = int(datetime.datetime.now().hour)
        if hour>=20 and hour<4:
            mytext="Ok sir, shutting down  Good night"
        elif hour>=4 and hour<20:
            mytext="Ok sir, shutting down   Hope you have a good day ahead of you"
        else:
            mytext="Ok sir, shutting down."
        texttospeech(mytext)

    def speechtotext():
            with sr.Microphone() as source:
                print("Mic ON")
                print("Say something : ")
                audio = r.listen(source)
                print("Mic Off")
            try:
                text = r.recognize_google(audio)
            except:
                text="Sorry, I didn't quite understand what you said"
            return text

    def texttospeech(mytext):
        engine.say(mytext)
        engine.runAndWait()
        return

    def opencalc():
        try:
            os.startfile('C:\\Windows\\System32\\calc.exe')
        except:
            subprocess.Popen('C:\\Windows\\System32\\calc.exe')

    def opennotepad():
        try:
            os.startfile('C:\\Windows\\System32\\notepad.exe')
        except:
            subprocess.Popen('C:\\Windows\\System32\\notepad.exe')

    def openword():
        try:
            os.startfile('C:\\Windows\\System32\\write.exe')
        except:
            subprocess.Popen('C:\\Windows\\System32\\write.exe')

    def wiki(mytext):
        x=mytext.replace("wikipedia","")
        try:
            result=wikipedia.summary(x,sentences=2)
            texttospeech("According to wikipedia")
            print(result)
            texttospeech(result)
        except:
            texttospeech("Sorry sir, I could not find anything.")

    def sendEmail(to,content):
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        password=""#################### Add your email password here
        server.login('',password) ################ Add your email id in the ' '
        server.sendmail('',to,content) #################### Add your email id in the ' '
        server.close()
        
    def Tasks():
        wishme()

        while True:
            flag=0
            mytext=speechtotext()
            n=mytext.lower()
            if "wikipedia" in mytext.lower():
                texttospeech("Searching wikipedia")
                wiki(mytext)
                flag=1
            elif "tell me the time" in mytext.lower():
                Time=datetime.datetime.now().strftime("%H:%M:%S")
                mytext="The current time is "+Time
                texttospeech(mytext) 
                flag=1
            elif "open calculator" in mytext.lower():
                mytext="Opening Calculator"
                texttospeech(mytext)
                opencalc()
                answer="yes"
                while answer.lower()=="yes":
                    mytext="Would you like me to calculate something for you?"
                    texttospeech(mytext)
                    answer=speechtotext()
                    if answer=="no":
                        texttospeech("Ok sir")
                        break
                    elif answer=="yes":
                        texttospeech("Tell me the calculation I need to do in the format    Calculate x + y for example")
                        calc=speechtotext()
                        l=calc.split()
                        if l[1]=="+":
                            calculation=int(l[0])+int(l[2])
                        elif l[1]=="-":
                            calculation=int(l[0])-int(l[2])
                        elif l[1]=="X" or l[1]=="x":
                            calculation=int(l[0])*int(l[2])
                        elif l[1]=="upon" or l[1]=="over":
                            calculation=int(l[0])/int(l[2])
                        elif l[1]=="power":
                            calculation=int(l[0])**int(l[2])
                        print(calculation)
                        texttospeech("The solution is "+str(calculation))
                    else:
                        texttospeech("Sorry sir, I didn't quite catch that")
                        answer="yes"
                        continue
                flag=1
            elif "send a whatsapp message" in mytext.lower():
                texttospeech(" Whom do I send the message to sir?")
                contact=speechtotext()
                print(contact)
                phnum="+91" #Change the country code as per your country.
                flag1=0
                for k,v in contacts.items():
                    if k==contact.lower():
                        phnum+=v
                        flag1=1
            
                print(phnum)
                hour = int(datetime.datetime.now().hour)
                minute = int(datetime.datetime.now().minute)
                print(hour)
                print(minute+2)
                answer="yes"
                answer1="yes"
                while answer=="yes" and answer1=="yes":
                    if flag1==0:
                        texttospeech(f"Sorry sir, I could not find the contact {contact}")
                        flag=1
                        break
                    texttospeech("Would you like me to send a message")
                    answer1=speechtotext()
                    if answer1=="yes":
                        texttospeech("What message would you like me to send?")
                        content=speechtotext()
                        texttospeech("The message is "+str(content)+" correct?")
                        answer=speechtotext()
                        if answer=="yes":
                            texttospeech("sending message")
                            try:
                                pywhatkit.sendwhatmsg(str(phnum),content,hour,minute+2,wait_time=20)
                                texttospeech("Message sent")
                            except:
                                texttospeech("Sorry sir, could not send the message")
                                answer="yes"
                                continue
                        if answer=="no":
                            answer="yes"
                            continue
                    else:
                        texttospeech("Ok sir")
                        break
                flag=1
            elif "play" in mytext.lower() and "on youtube" in mytext.lower():
                l=mytext.split()
                search=l[1]
                try:
                    texttospeech("Searching for "+search+" on youtube")
                    pywhatkit.playonyt(search)
                except:
                    texttospeech("Sorry sir I was unable to play "+search+" on youtube")
                flag=1
            
            elif "search" in mytext.lower() and "on google" in mytext.lower():
                l=mytext.split()
                search=l[1]
                try:
                    texttospeech("Searching "+search+" on google")
                    pywhatkit.search(search)
                except:
                    texttospeech("Sorry sir I was unable to search for "+search+" on google")
                flag=1

            elif "open notepad" in mytext.lower():
                mytext="Opening Notepad"
                texttospeech(mytext)
                opennotepad()
                flag=1
            elif "open word pad" in mytext.lower():
                mytext="Opening Word Pad"
                texttospeech(mytext)
                openword()
                flag=1
            elif "close calculator" in mytext.lower():
                mytext="Closing calculator"
                texttospeech(mytext)
                os.system('TASKKILL /F /IM calc.exe')
                flag=1
            elif "close notepad" in mytext.lower():
                mytext="Closing Notepad"
                texttospeech(mytext)
                os.system('TASKKILL /F /IM notepad.exe')
                flag=1
            elif "close word pad" in mytext.lower():
                mytext="Closing Word Pad"
                texttospeech(mytext)
                os.startfile('TASKKILL /F /IM write.exe')
                flag=1
            elif "open youtube" in mytext.lower():
                mytext="Opening Youtube"
                texttospeech(mytext)
                webbrowser.open("youtube.com")
                flag=1
            elif "open google" in mytext.lower():
                mytext="Opening Google"
                texttospeech(mytext)
                webbrowser.open("google.com")
                flag=1
            elif "open airtel stream" in mytext.lower():
                mytext="Opening Airtel X Stream"
                texttospeech(mytext)
                webbrowser.open("airtelxstream.in")
                flag=1
            elif mytext.lower()=="open stack overflow":
                mytext="Opening Stackoverflow"
                texttospeech(mytext)
                webbrowser.open("stackoverflow.com")
                flag=1
            elif "open vs code" in mytext.lower():
                print(mytext)
                mytext="Opening VS code"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(path)
                flag=1
            elif "open netflix" in mytext.lower():
                mytext="Opening Netflix"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\Desktop\\Netflix.lnk"
                os.startfile(path)
                flag=1
            elif "open spotify" in mytext.lower():
                mytext="Opening Spotify"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\Desktop\\Spotify.lnk"
                os.startfile(path)
                flag=1
            elif "open twitter" in mytext.lower():
                mytext="Opening Twitter"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\Desktop\\Twitter.lnk"
                os.startfile(path)
                flag=1
            elif "open instagram" in mytext.lower():
                mytext="Opening Instagram"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\Desktop\\Instagram.lnk"
                os.startfile(path)   
                flag=1
            elif "open ms teams" in mytext.lower():
                mytext="Opening MS TEAMS"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\Desktop\\Microsoft Teams.lnk"
                os.startfile(path)  
                flag=1
            elif "open amazon prime" in mytext.lower():
                mytext="Opening Amazon Prime"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\Desktop\\Amazon Prime Video for Windows.lnk"
                os.startfile(path)   
                flag=1 
            elif "open matlab" in mytext.lower():
                mytext="Opening matlab"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\Desktop\\Matlab\\MATLAB R2020b.lnk"
                os.startfile(path) 
                flag=1
            elif "open telegram" in mytext.lower():
                mytext="Opening Telegram"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\Desktop\\Telegram Desktop.lnk"
                os.startfile(path)   
                flag=1
            elif "open discord" in mytext.lower():
                mytext="Opening Discord"
                texttospeech(mytext)
                path="C:\\Users\\Jatin Dhall\\Desktop\\Discord.lnk"
                os.startfile(path)
                flag=1
            elif "open word" in mytext.lower():
                mytext="Opening MS Word"
                texttospeech(mytext)
                path="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"
                os.startfile(path)
                flag=1
            elif "open ppt" in mytext.lower():
                mytext="Opening MS Powerpoint Presentation"
                texttospeech(mytext)
                path="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PowerPoint.lnk"
                os.startfile(path)
                flag=1
            elif "open onenote" in mytext.lower():
                mytext="Opening MS One Note"
                texttospeech(mytext)
                path="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OneNote.lnk"  
                os.startfile(path)
                flag=1
            elif "open excel" in mytext.lower():
                mytext="Opening MS Excel"
                texttospeech(mytext)
                path="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel.lnk"       
                os.startfile(path)
                flag=1
            elif "open snipping tool" in mytext.lower():
                mytext="Opening Snipping Tool"
                texttospeech(mytext)
                path="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\Snipping Tool.lnk"
                os.startfile(path)
                flag=1
            elif "open paint" in mytext.lower():
                mytext="Opening Paint"
                texttospeech(mytext)
                path="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\Paint.lnk"
                os.startfile(path)
                flag=1
            elif "open whatsapp" in mytext.lower():
                texttospeech("Opening whatsapp")
                path="C:\\Users\\Jatin Dhall\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
                os.startfile(path)
                flag=1
            elif "send email" in mytext.lower():
                try:
                    answer="no"
                    while answer.lower()=="no":
                        texttospeech("What should I say?")
                        content = speechtotext()
                        print(content)
                        texttospeech(content)
                        texttospeech("correct?")
                        answer=speechtotext()
                    to = ""###################Add the email that you want to send to.......
                    sendEmail(to,content)
                    texttospeech("Email has been sent")
                except Exception as e:
                    print(e)
                    texttospeech("Sorry sir.I was not able to send the email")
                flag=1
                    
            elif "joke" in mytext.lower():
                mytext=pyjokes.get_joke()
                texttospeech(mytext)
                flag=1
            elif mytext.lower() in replies.keys():
                for k,v in replies.items():
                    if mytext.lower()==k.lower():
                        mytext=v
                        texttospeech(mytext)
                flag=1
            
            elif n=="close":
                greet()
                quit()
            
            else:
                texttospeech("Sorry sir, I didn't quite catch that    Could you please repeat that for me?")
            
            if flag==1:
                texttospeech("Is there anything else I can do for you?") 

    Tasks()
    
p1=multiprocessing.Process(target=frontend)
p2=multiprocessing.Process(target=backend)

if __name__=="__main__":
    p1.start()
    p2.start()
