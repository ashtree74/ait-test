import openai
import speech_recognition as sr
import os
import tempfile
import pyttsx3 

# Set the organization ID (replace the placeholder with your actual organization ID)
openai.organization = "***"

# Set the API key by fetching it from an environment variable
openai.api_key = "***"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Save the recorded audio to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            filename = fp.name
            with open(fp.name, "wb") as file:
                file.write(audio.get_wav_data())

        # Transcribe the audio using the OpenAI API
        with open(filename, "rb") as file:
            transcription = openai.Audio.transcribe("whisper-1", file)

        # Remove the temporary file after transcription
        os.remove(filename)

        return transcription["text"]
    except Exception as e:
        print("Error recognizing speech:", e)
        return ""

def get_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    if "choices" not in response or "message" not in response.choices[0]:
        print("Error in API response:", response)
        return "An error occurred while processing the request. Please try again."

    return response.choices[0].message.content.strip()

def speak_text(text):
    try:
        engine = pyttsx3.init()  # Initialize pyttsx3 engine
        engine.setProperty('rate', 180)  # Set speech rate
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.zosia')  # Set voice to Zosia (Polish)
        engine.say(text)  # Say the text
        engine.runAndWait()  # Wait for the speech to finish
    except Exception as e:
        print("Error while using pyttsx3 text-to-speech:", e)

def main():
    while True:
        input_text = recognize_speech()
        if not input_text:
            continue

        print("You said:", input_text)
        response_text = get_response(input_text)
        print("AI:", response_text)
        speak_text(response_text)

if __name__ == "__main__":
    main()
