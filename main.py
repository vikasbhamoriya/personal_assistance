###### important modules ##########################################################################################
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
from AppOpener import open,close 
import screen_brightness_control as sbc
import os 
##########################################################################################################################
'''
................................buddy can perform......................................................... 
1. Speech Output:
    Utilizes the pyttsx3 module for speech synthesis to communicate with the user.
2.Voice Input:
    Utilizes the speech_recognition module to recognize voice commands from the user.
3.Time Greetings:
    Greets the user based on the current time of the day (morning, afternoon, evening).
4.Application Management:
    Opens and closes applications using the AppOpener module.   
    Can open websites based on user commands.
5.Screen Brightness Control:
    Adjusts the screen brightness based on user commands.
6.Wikipedia Search:
    Searches Wikipedia for information based on user queries.
7.General Conversations:
    Responds to general queries and engages in simple conversations with the user.
8.Exit and Shutdown:
    Allows the user to exit the program or shut down the assistant.
9.Self-Introduction:
    Responds to queries like "tell me about yourself."
10.Continuous Operation:
    Runs in a continuous loop, waiting for user commands and responding accordingly.
'''
engine =  pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

# this function is use for speaking by buddy
def speak(audio):
    print("buddy:- "+audio)
    engine.say(audio)
    engine.runAndWait()
# it take the command from user by microphone
def TakeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        # print("listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        # print("recognizing")
        query = r.recognize_google(audio,language='en-in')
        print(f"user:- {query}")
    except Exception as e:
        print("buddy:-.......?")
        return "none"
    return query
#this function is for whising the user
def WishMe():
    hour = int(datetime.datetime.now().hour)
    if(hour<12 and hour>4):
        speak("good morning sir ")
    elif(hour>12 and hour<18):
        speak("good afternoon sir  ")
    else:
        speak("good evening sir")
    speak("my name is buddy and i am your personal assistant.how can i help you....")
    # this function is for opening the app in 
# this function is for clossing the running app
def app_close(app_name):
    try:
        close(app_name, match_closest=True, throw_error=True)
        print(f"closing {app_name}")
    except:
        speak("app is not found or running")
# this function is for the apps and websites
def openwebapp(query):
    words = query.split()
    app_name = "."
    for i in words:
        if i == "open":
            pass
        else:
            app_name=app_name+i
    if (words[0]=="open"):
            try:
                open(app_name, match_closest=True, throw_error=True)
                speak(f"opening {words[1]}")
                clossing_app = TakeCommand()
                apps = clossing_app.split()
                if (apps[0]=="close" or apps[0]=="exit" or apps[0:2]=="exit the"):
                    app_close(app_name)
            except Exception as e:
                speak(f"opening {words[1]}")
                webbrowser.open(f"https://www{app_name}.com",0)
    return None
# this is brightness controll function
def brightness_controll(query,query_word_set):
    words = ""
    try:
        level = int(query_word_set[-1])
    except:
        temp = sbc.get_brightness()
        level = int(temp[0])
    for word in query_word_set:
        if (word=="set" or word== "increase" or word=="decrease"or word=="brightness"):
            words = words + word
    if(words=="setbrightness"):
        speak("brightness set")
        sbc.set_brightness(level)   
    if(words=="increasebrightness"or words=="brightnessincrease"):
                brightness_level = sbc.get_brightness()
                print(f"the brightness is {brightness_level[0]}")
                sbc.set_brightness(brightness_level[0]+10)
                if brightness_level[0]==100:
                    speak("maximum brightness")
    elif(words=="decreasebrightness" or words=="brightnessdecrease"):
                brightness_level = sbc.get_brightness()
                print(f"the brightness is {brightness_level[0]}")
                sbc.set_brightness(brightness_level[0]-10)
                if brightness_level[0]==0:
                    speak("minimum brightness")
# this function is for wiki[idia search
def wikipidia_search(query):
    try:
        print(wikipedia.summary(query,sentences=5))
    except:
        speak("try again , i can't")
# this function is use to introduce the buddy
def self_introduction():
    print(
        "Hello, I'm buddy, your personal assistant. I was created on December 4, 2023, by Vikas Bhamoriya. "
        "I'm here to assist you with various tasks. My capabilities include opening and closing applications, "
        "adjusting screen brightness, providing the current time, and even searching Wikipedia for you. Feel free "
        "to ask me anything or give me commands, and I'll do my best to help. I'm designed to make your life a bit easier. "
    )
# this is our main function 
if __name__=="__main__":
    print("start.....")  
    while True:
        start_buddy = input("user: ")
        # start_buddy = TakeCommand().lower()
        if "ok buddy" == start_buddy or  "hello buddy" ==start_buddy or "hey buddy"==start_buddy:
            WishMe()
            program = True
            while program:
                # query = TakeCommand().lower()
                query = input("user:- ")
                query_word_list= query.split()
                if (query_word_list[0]=="exit"or query_word_list[0]== "exit" or "shutdown"==query_word_list[0]):
                    speak("buddy system is shutting down")
                    program = False
                # this is for user enterface
                elif query_word_list[-1]=="buddy":
                    if(query=="what are you doing" or query  =="what r u doing "or " tum kya kr rhe ho" ):
                        speak("i am hear to helping you sir...")
                    else:
                        speak(f"{query} sir, how can i help you")
                elif (query=="tum kaise ho" or query=="how are you" or query == "how r u"):
                    speak("i am fine how are you ")
                
                #..........this is for the apps and websites...............................
                elif "open"==query_word_list[0]:
                    openwebapp(query)        
                #................................................................
                elif(query_word_list[0]=="close"):
                    app_close(query)
                #...........this is for controll britness.............................................
                elif "brightness" in query_word_list:
                    brightness_controll(query,query_word_list)
                #...........this is for reading time...................................................................
                elif "what" in query_word_list and "time" in query_word_list:
                    hour = int(datetime.datetime.now().hour)
                    minute = int(datetime.datetime.now().minute)
                    second= int(datetime.datetime.now().second)
                    speak(f"its {hour}:{minute}:{second} O'clock")
                #  this s for wikipifia search
                elif "tell" in query_word_list and "about" in query_word_list:
                    wikipidia_search(query)
                # this is for not response:
                else:
                    speak("sorry i can't understand")
                if(query=="tell me about yourself"):
                    self_introduction()
                    # os.open('buddy_history')      
        elif (start_buddy=="stop"):
            break

