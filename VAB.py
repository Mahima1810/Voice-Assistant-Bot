import speech_recognition as sr
import pyttsx3
import datetime
import openai

# Set your OpenAI API key here
openai.api_key = 'YOUR_OWN_APIKEY '

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not catch that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
    return ""

def process_command(command):
    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif 'date' in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
    elif 'your name' in command:
        speak("I am your virtual assistant.")
    else:
        # If connected with OpenAI API, use it for more complex queries
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=command,
            max_tokens=50
        )
        speak(response.choices[0].text.strip())

def main():
    wake_up_command = 'hey zoro'
    
    while True:
        # Listen for the wake-up command
        print("Say 'hey assistant' to start.")
        command = listen()
        if wake_up_command in command:
            speak("How can I assist you?")
            while True:
                command = listen()
                if 'exit' in command or 'stop' in command:
                    speak("Goodbye!")
                    return
                process_command(command)

if __name__ == "__main__":
    main()
