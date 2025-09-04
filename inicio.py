import speech_recognition as sr
import pyttsx3

iniciar = sr.Recognizer()

def reconhecer_Voz():
    while(1):
        try:
            with sr.Microphone() as source2:
                iniciar.adjust_for_ambient_noise(source2, duration= 0.2)
                
                audio2 = iniciar.listen(source2)
                
                texto = iniciar.recognize_google(audio2)
                
                return texto
                
        except sr.RequestError as erro:
            print(f'erro na leitura de voz {format(erro)}')
            
        except sr.UnknownValueError:
            print('tendi porra nenhuma')
            
    return
