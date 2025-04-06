import datetime
import eel       #*
import pyttsx3  #*
import pyaudio
import speech_recognition as sr  #*
import wikipedia  #*             
import smtplib
import webbrowser as wb
import urllib.parse
import pywhatkit     #*
import pyautogui    #*
import os
import requests
import wolframalpha  #*
from playsound import playsound  #*
from time import sleep


eel.init("www")
engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)

def wishme():
    speak("Hello sir, I am Jarvis!")
    sleep(1)  # Wait for the Siri wave page to finish animation
    eel.DisplayMessage("How can I assist you today?")
    speak("How can I assist you today?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening . . .")
        r.pause_threshold = 1
        audio = r.listen(source, 10, 6)
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing . . ....")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        return query.lower()
    except Exception as e:
        print(e)
        eel.DisplayMessage("Say that again please...")        
        speak("Say that again please...")
        return "none"

def screenshot():
    img = pyautogui.screenshot()
    img.save("screenshot.png")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()

def open_application(query):
    if 'chrome' in query:
        speak("Opening Google Chrome")
        os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
    elif 'notepad' in query:
        speak("Opening Notepad")
        os.startfile('notepad.exe')
    elif 'calculator' in query:
        speak("Opening Calculator")
        os.startfile('calc.exe')
    else:
        speak("Application not found")

def send_whatsapp_message():
    try:
        speak("Please tell me the phone number of the recipient, including the country code")
        phone_number = takeCommand().replace(" ", "")
        eel.DisplayMessage(phone_number)
        speak(f"You said: {phone_number}. Is this correct? Please say 'yes' or 'no'.")
        confirmation = takeCommand()
        if 'yes' in confirmation:
            speak("What should I type in the message?")
            message = takeCommand()
            speak(f"You said: {message}")
            speak("Should I send it? Please say 'yes' to confirm or 'no' to cancel.")
            confirmation = takeCommand()
            if 'yes' in confirmation:
                pywhatkit.sendwhatmsg_instantly(phone_number, message)
                speak("Message has been sent!")
            else:
                speak("Message not sent")
        else:
            speak("Let's try again.")
            send_whatsapp_message()
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the message")

def get_weather():
    try:
        api_key = "bd5e378503939ddaee76f12ad7a97608"    
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        eel.DisplayMessage("Please tell me the city name")
        speak("Please tell me the city name")
        city_name = takeCommand()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            main = data["main"]
            weather = data["weather"]
            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            weather_description = weather[0]["description"]
            speak(f"The temperature in {city_name} is {temperature - 273.15:.2f} degrees Celsius")
            speak(f"The weather is {weather_description}")
            speak(f"The atmospheric pressure is {pressure} hPa")
            speak(f"The humidity level is {humidity}%")
        else:
            eel.DisplayMessage("City not found")
            speak("City not found")
    except Exception as e:
        print(e)
        eel.DisplayMessage("Unable to get the weather information at the moment..!")
        speak("Unable to get the weather information at the moment")
        

    
def calculate(query):
    app_id = '7T599E-433LT9KE64'
    client = wolframalpha.Client(app_id)
    ind = query.lower().split().index('calculate')
    text = query.split()[ind + 1:]
    result = client.query(" ".join(text))
    try:
        ans = next(result.results).text
        eel.DisplayMessage(ans)
        speak("The answer is " + ans)
        print("The answer is " + ans)
    except StopIteration:
        speak("I could not find the answer. Please try again")

def answer_general_query(query):
    app_id = '7T599E-433LT9KE64'
    client = wolframalpha.Client(app_id)
    try:
        ind = query.lower().index('what is') if 'what is' in query.lower() else \
              query.lower().index('who is') if 'who is' in query.lower() else \
              query.lower().index('which is') if 'which is' in query.lower() else None
        if ind is not None:
            text = query.split()[ind + 2:]
            result = client.query(" ".join(text))
            ans = next(result.results).text
            speak("The answer is " + ans)
            print("The answer is " + ans)
        else:
            eel.DisplayMessage("I could not find the answer. Please try again")
            speak("I could not find the answer. Please try again")
            print("I could not find the answer. Please try again")
    except StopIteration:
        speak("I could not find the answer. Please try again")

@eel.expose
def activate_jarvis():
    wishme()
    while True:
        query = takeCommand()
        eel.display_command(query)
        eel.DisplayMessage(query)  # Display recognized command on Siri Wave UI
        
        if "hello jarvis" in query:
            speak("Hello sir, I am Jarvis!")
            wishme()
        elif "time" in query:
            time()
            eel.DisplayMessage(f"Current time is {datetime.datetime.now().strftime('%I:%M:%S')}")
        elif "date" in query:
            date()
            eel.DisplayMessage(f"Current date is {datetime.datetime.now().strftime('%d-%m-%Y')}")
        elif "open" in query:
            open_application(query)
            eel.DisplayMessage(f"Opening {query}")
        elif "screenshot" in query:
            screenshot()
            eel.DisplayMessage("Screenshot taken...!")
        elif "email" in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("Who is the recipient?")
                recipient = takeCommand()
                sendEmail(recipient, content)
                eel.DisplayMessage(f"Email sent to {recipient} with content: {content}")
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Unable to send the email")
        elif "weather" in query:
            get_weather()
        elif "calculate" in query:
            eel.DisplayMessage(query)
            calculate(query)
        elif "wikipedia" in query:  # Big messages might be truncated on the UI
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            speak(results)
            print(results)
            eel.DisplayMessage(results)
        elif "search in chrome" in query:
            query = query.replace("search", "")
            query = urllib.parse.quote_plus(query)
            wb.open(f"https://www.google.com/search?q={query}")
            speak("Here are the search results")
            eel.DisplayMessage(f"Search results for: {query}")
        elif 'play songs' in query:
            eel.DisplayMessage("Which song do you want to play?")
            speak("Which song do you want to play?")
            song = takeCommand().lower()
            eel.DisplayMessage(f"Song is being played: {song}")
            eel.DisplayMessage("Playing.....")
            speak("Playing...")
            pywhatkit.playonyt(song)
        elif 'logout' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
        elif "youtube" in query:
            query = query.replace("youtube", "")
            query = urllib.parse.quote_plus(query)
            eel.DisplayMessage(query)
            wb.open(f"https://www.youtube.com/results?search_query={query}")
            speak("Here are the YouTube results")
        elif "remember" in query:
            rememberMessage = query.replace("remember that", "")
            speak("You asked me to remember: " + rememberMessage)
            with open("data.txt", "w") as f:
                f.write(rememberMessage)
        elif "do you remember" in query:
            try:
                with open("data.txt", "r") as f:
                    rememberMessage = f.read()
                    speak("You asked me to remember that " + rememberMessage)
            except FileNotFoundError:
                speak("I don't have any notes to remember.")
        elif "offline" in query:
            eel.DisplayMessage("Going offline. Goodbye!")
            speak("Going offline. Goodbye!")
            quit()
        else:
            answer_general_query(query)
            eel.DisplayMessage(query)

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

if __name__ == "__main__":
    eel.start("index.html")
