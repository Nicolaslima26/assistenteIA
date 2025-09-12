import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import time

iniciar = sr.Recognizer()


def falar(texto):
    tts = gTTS(text=texto, lang="pt-br")
    filename = "resposta.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  
    
def  reconhecer_Voz():
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                print('reconhecendo...')
                audio = r.listen(source)
            texto = r.recognize_google(audio, language="pt-BR")
            return texto
        except sr.RequestError as e:
            print(f'erro na leitura de voz: {e}')
            return ""
        except sr.UnknownValueError:
            print('não entendi — fale novamente')
            # continua o loop para tentar de novo

def output_text_Arquivo(texto):
    f = open('output.txt', 'a', encoding='utf-8')
    f.write(texto)
    f.write('\n')
    f.close()
    return

if __name__ == "__main__":
    while(1):
        texto = reconhecer_Voz()
        output_text_Arquivo(texto)
        if texto == "R2 morre":
            falar('encerrando o sistema')
            break
        print('AUDIO COMPREENDIDO')
        
        if texto == "R2" or texto == "r2":
            falar('ola, tudo bem o que deseja?')
        else:
            falar(texto)
