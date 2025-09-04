import pyttsx3

voz = pyttsx3.init()
voices = voz.getProperty('voices')

for i, v in enumerate(voices):
    print(f"{i}: {v.name} ({v.id})")
