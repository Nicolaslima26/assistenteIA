import speech_recognition as sr
import pyttsx3
from playsound import playsound

iniciar = sr.Recognizer()
voz = pyttsx3.init()
voz.setProperty('rate', 125) 
voz.setProperty('volume', 1) 

voices = voz.getProperty('voices')
for v in voices:
    if "portuguese" in v.name.lower():
        voz.setProperty('voice', v.id)
        break

def falar(texto):
    voz.say(texto, name='teste')
    voz.runAndWait()
    
def reconhecer_Voz():
    while(1):
        try:
            with sr.Microphone() as source2:
                iniciar.adjust_for_ambient_noise(source2, duration= 0.8)
                print('reconhecendo...')
                
                audio2 = iniciar.listen(source2)
                
                texto = iniciar.recognize_google(audio2, language= "pt-BR")
                
                return texto
                
        except sr.RequestError as erro:
            print(f'erro na leitura de voz {format(erro)}')
            
        except sr.UnknownValueError:
            print('tendi NADA')
            
    return

def output_text_Arquivo(texto):
    f = open('output.txt', 'a', encoding='utf-8')
    f.write(texto)
    f.write('\n')
    f.close()
    
    return
while(1):
    texto = reconhecer_Voz()
    output_text_Arquivo(texto)
    if texto == "encerrar":
        playsound("Voicy_R2-D2 - 8.mp3")
        break
    
    print('AUDIO COMPREENDIDO')
    if texto == "teste":
        print('ola Nicolas tudo bem ?')