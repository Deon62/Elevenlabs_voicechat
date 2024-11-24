import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
#from elevenlabs import generate_and_play_audio, set_api_key
from config1 import GEMINI_API_KEY, ELEVEN_API_KEY
from elevenlabs import Voice, VoiceSettings, generate, play

genai.configure(api_key=GEMINI_API_KEY)
from elevenlabs import set_api_key


set_api_key(ELEVEN_API_KEY)
# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()




import pygame
from io import BytesIO

def speak_response(text):
    audio = generate(
        text=text,
        voice=Voice(
            #voice_id="21m00Tcm4TlvDq8ikWAM",
            #voice_id="jsCqWAovK2LkecY7zXl4", 
            voice_id="zrHiDhphv9ZnVXBqCLjz",

            settings=VoiceSettings(stability=0.71, similarity_boost=0.5)
        )
    )
    # Play using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(BytesIO(audio))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="youre a funny bot for deox food website that offers food delivery services around egerton university"
)

def get_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError:
            print("Could not request results")
            return None



# Create the chat session, initializing the history
history = []

# Start the chat session
print("Welcome to DeoxFoods Delivery!")
print("\nChoose your preferred input method:")
print("1. Voice commands")
print("2. Text input")

while True:
    choice = input("Enter your choice (1 or 2): ")
    if choice in ['1', '2']:
        break
    print("Invalid choice. Please enter 1 or 2.")

input_mode = "voice" if choice == "1" else "text"

print(f"\nGreat! Using {input_mode} input mode. Type or say 'switch' to change modes, 'quit' to exit")
speak_response("Welcome to Deoxfoods How can I help you today?")

while True:
    if input_mode == "voice":
        print("Listening...")
        user_input = get_voice_input()
    else:
        user_input = input("You: ")
    
    if user_input and user_input.lower() == 'switch':
        input_mode = "text" if input_mode == "voice" else "voice"
        print(f"\nSwitched to {input_mode} input mode")
        continue
    
    if user_input and user_input.lower() == 'quit':
        break
    
    if user_input:
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        model_response = response.text
        
        print("Bot:", model_response)
        speak_response(model_response)
        
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]}) 
