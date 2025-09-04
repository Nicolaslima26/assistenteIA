import speech_recognition as sr
import pyttsx3

iniciar = sr.Recognizer()

def reconhecer_Voz():
    while(1):
        try:
            with sr.Microphone() as source2:
                iniciar.adjust_for_ambient_noise(source2, duration= 0.2)
                
                audio2 = iniciar.listen(source2)
                
                texto = iniciar.recognize_google(audio2, language= "pt-BR")
                
                return texto
                
        except sr.RequestError as erro:
            print(f'erro na leitura de voz {format(erro)}')
            
        except sr.UnknownValueError:
            print('tendi NADA')
            
    return

def output_text_Arquivo(texto):
    f = open('output.txt', 'a')
    f.write(texto)
    f.write('\n')
    f.close()
    
    return
while(1):
    texto = reconhecer_Voz()
    output_text_Arquivo(texto)
    
    print('AUDIO COMPREENDIDO')
    if texto == "teste":
        print('ola Nicolas tudo bem ?')