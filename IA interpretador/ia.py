import difflib
import datetime
import inicio as reconhecer_Voz
# respostas
respostas = {
    "oi": "Bip bop! Sou seu R2-B2 seu assistente pessoal",
    "quem é você": "Sou o R2-B2, pronto para ajudar!",
    "qual sua missão": "Minha missão é ajudar você, mestre Jedi",
    "tchau": "Boop bip! Até logo, que a Força esteja com você!"
}

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

    # caso n tenha nenhuma outra mensagem
    return "Bip... não entendi, mestre Jedi. Pode repetir?"

# Loop de teste
print("Assistente ativado")
while True:
    user = reconheer_Voz()
    if user.lower() in ["sair", "exit", "quit"]:
        print("Droide: Desligando... ")
        break
    print("Droide:", assistente(user))
