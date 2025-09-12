import difflib
import datetime
import speech_recognition as sr
from gtts import gTTS
import os
import playsound
from prototipo1.inicio import reconhecer_Voz
import time

print('iniciarrrr')
# respostas
respostas = {
    "oi": "Bip bop! Sou seu R2-B2 seu assistente pessoal",
    "quem é você": "Sou o R2-B2, pronto para ajudar!",
    "qual sua missão": "Minha missão é ajudar você, mestre Jedi",
    "tchau": "Boop bip! Até logo, que a Força esteja com você!"
}

def falar(texto):
    tts = gTTS(text=texto, lang="pt-br")
    filename = "resposta.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  
    

def assistente(pergunta):
    pergunta = pergunta.lower().strip()

    # pré-definidas
    melhor_match = difflib.get_close_matches(pergunta, respostas.keys(), n=1, cutoff=0.7)
    if melhor_match:
        return respostas[melhor_match[0]]

    #tenta descobrir sobre data
    if "hoje" in pergunta:
        hoje = datetime.date.today()
        return f"Bip bop! Hoje é {hoje.strftime('%d/%m/%Y')} ({hoje.strftime('%A')})."
    if "amanhã" in pergunta:
        amanha = datetime.date.today() + datetime.timedelta(days=1)
        return f"Boop! Amanhã será {amanha.strftime('%d/%m/%Y')} ({amanha.strftime('%A')})."
    if "ontem" in pergunta:
        ontem = datetime.date.today() - datetime.timedelta(days=1)
        return f"Bip! Ontem foi {ontem.strftime('%d/%m/%Y')} ({ontem.strftime('%A')})."

    #operaçoes da matemática simple
    if any(op in pergunta for op in ["+", "-", "*", "/", "x"]):
        try:
            conta = pergunta.replace("x", "*")
            resultado = eval(conta)
            return f"Beep boop! O resultado é {resultado}"
        except:
            return "Erro ao calcular... bip "

    return "Bip... ainda não tenho resposta para isso."

print("Assistente ativado")
while True:
    pergunta = reconhecer_Voz()
    if not pergunta:
        continue
    print("Você disse:", pergunta)

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Droide: Desligando... ")
        break
    
    resposta = assistente(pergunta)
    print("Droide:", resposta)       
    falar(resposta)
    time.sleep(1)