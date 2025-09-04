import speech_recognition as sr
from gtts import gTTS
import os
import playsound

iniciar = sr.Recognizer()


def falar(texto):
    tts = gTTS(text=texto, lang="pt-br")
    filename = "resposta.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  
    
def reconhecer_Voz():
    while(1):
        try:
            with sr.Microphone() as source2:
                iniciar.adjust_for_ambient_noise(source2, duration= 0.2)
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
    if texto == "R2 morrer":
        falar('encerrando o sistema')
        break
    print('AUDIO COMPREENDIDO')
    
    if texto == "r2":
        falar('ola, tudo bem o que deseja?')
    falar(texto)
