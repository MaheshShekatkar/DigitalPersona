import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# recognizer = sr.Recognizer()
#   with sr.Microphone() as source:
#         print("Please speak something...")
        
#         audio = recognizer.listen(source)
#         try:
#             text = recognizer.recognize_google(audio)
#             print(f"You said: {text}")
#             return text
#         except sr.UnknownValueError:
#             print("Google Speech Recognition could not understand audio")
#             return None
#         except sr.RequestError:
#             print("Could not request results from Google Speech Recognition service")
  
  
# def text_to_speech(text, lang='en'):
#     tts = gTTS(text=text, lang=lang)
#     filename = "response.mp3"
#     tts.save(filename)
#     st.audio(filename, format="audio/mp3")
#     playsound(filename)
#     os.remove(filename)  # Remove the file after playing