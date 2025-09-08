1. Bibliotecas utilizadas
difflib	Compara strings e encontra similaridade entre perguntas e respostas predefinidas.
datetime	Trabalha com datas (hoje, amanhã, ontem).
speech_recognition (sr)	Captura áudio do microfone e converte em texto.
gtts	Converte texto em áudio (Text-to-Speech).
os	Manipula arquivos do sistema, usado para deletar arquivos de áudio temporários.
playsound	Reproduz arquivos de áudio.
time	Cria pausas para evitar que o microfone capture a própria fala do TTS.
from inicio import reconhecer_Voz	Importa a função que captura a voz do usuário.
2. Respostas predefinidas
respostas = {
    "oi": "Bip bop! Sou seu R2-B2 seu assistente pessoal",
    "quem é você": "Sou o R2-B2, pronto para ajudar!",
    "qual sua missão": "Minha missão é ajudar você, mestre Jedi",
    "tchau": "Boop bip! Até logo, que a Força esteja com você!"
}


Um dicionário que mapeia perguntas conhecidas para respostas automáticas.

Permite adicionar novas respostas facilmente.

3. Função falar(texto)
def falar(texto):
    tts = gTTS(text=texto, lang="pt-br")
    filename = "resposta.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


Converte texto em áudio usando Google TTS.

Salva temporariamente em resposta.mp3.

Reproduz o áudio.

Deleta o arquivo após tocar.

4. Função assistente(pergunta)
4.1 Padronização da pergunta
pergunta = pergunta.lower().strip()


Converte a pergunta em letras minúsculas e remove espaços extras.

4.2 Comparação com respostas predefinidas
melhor_match = difflib.get_close_matches(pergunta, respostas.keys(), n=1, cutoff=0.7)
if melhor_match:
    return respostas[melhor_match[0]]


Encontra a pergunta mais próxima dentro do dicionário de respostas.

Retorna a resposta se houver correspondência.

4.3 Perguntas sobre datas

"hoje", "amanhã", "ontem" → retorna a data correspondente.

hoje = datetime.date.today()
hoje.strftime('%d/%m/%Y')  # formato dd/mm/aaaa
hoje.strftime('%A')         # dia da semana

4.4 Operações matemáticas simples
if any(op in pergunta for op in ["+", "-", "*", "/", "x"]):
    conta = pergunta.replace("x", "*")
    resultado = eval(conta)


Detecta operações matemáticas na pergunta.

Substitui x por * para multiplicação.

Calcula o resultado usando eval().

4.5 Resposta padrão
return "Bip... ainda não tenho resposta para isso."


Usada quando nenhuma das condições anteriores é atendida.

5. Loop principal
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


Inicializa o assistente.

Captura a voz do usuário.

Processa a pergunta e gera a resposta.

Converte a resposta em fala.

Pausa 1 segundo para evitar que o microfone capture o TTS.

Sai do loop se o usuário disser "sair", "exit" ou "quit".

6. Fluxo geral da IA

O programa inicia e exibe "Assistente ativado".

Aguarda a voz do usuário.

Converte áudio em texto (reconhecer_Voz()).

Passa o texto para a função assistente().

Mostra a resposta no console e fala com TTS.

Repete o processo até o comando de saída.
