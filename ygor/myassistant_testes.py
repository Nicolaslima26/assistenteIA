import random
import speech_recognition as sr
import subprocess
import os
import tempfile
import time
from datetime import datetime
import requests

# CONFIGURAÇÃO AJUSTADA - usando plug e taxa correta
AUDIO_DEVICE = "plughw:2,0" # Usando plug para melhor compatibilidade
TROC_URL = "https://gist.githubusercontent.com/henrycunh/75abcf44146d5d9c0714932a386dbbf1/raw/558b97a002d578998720d76458641d4782c97d34/trocadilhos.json"

def obter_trocadilho():
    """Obter trocadilho aleatório do banco online"""
    try:
        resp = requests.get(TROC_URL)
        resp.raise_for_status()
        trocadilhos = resp.json()
        escolhido = random.choice(trocadilhos)
        return escolhido["pergunta"], escolhido["resposta"]
    except Exception as e:
        print(f"❌ Erro ao buscar trocadilho: {e}")
        return None, None

class VoiceAssistant:
    def __init__(self, volume=50):
        self.recognizer = sr.Recognizer()
        self.wake_word = "r2"
        self.volume = volume

    def speak(self, text):
        """Falar texto usando eSpeak"""
        print(f"🤖 Assistente: {text}")
        os.system(f'espeak -v pt -s 120 -a {self.volume} "{text}" 2>/dev/null')
    def calculate(self, command):
        """Tentar calcular uma expressão simples a partir do comando de voz"""
        try:
            # Substituir palavras por operadores
            command = command.replace("mais", "+").replace("menos", "-")
            command = command.replace("vezes", "*").replace("multiplicado", "*")
            command = command.replace("dividido", "/").replace("dividido", "/")

            # Extrair apenas números e operadores
            allowed_chars = "0123456789+-*/.() "
            expression = "".join(c for c in command if c in allowed_chars)

            if expression:
                result = eval(expression)
                self.speak(f"O resultado é {result}")
                return True
            else:
                return False
        except Exception as e:
            print(f"❌ Erro no cálculo: {e}")
            self.speak("Desculpe, não consegui calcular isso")
            return False

    def record_audio(self, filename, duration=5):
        """Gravar áudio com taxa de amostragem correta (44100Hz)"""
        try:
            # Usando 44100Hz que é a taxa nativa do microfone
            cmd = f"arecord -D {AUDIO_DEVICE} -d {duration} -f S16_LE -r 44100 -c 1 {filename}"
            subprocess.run(cmd, shell=True, check=True, timeout=duration+2)
            return True
        except Exception as e:
            print(f"❌ Erro na gravação: {e}")
            return False

    def listen(self):
        """Ouvir e reconhecer comando de voz"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                audio_file = tmp.name

            print("🎤 Ouvindo... (fale agora)")
            if self.record_audio(audio_file, duration=4):

                # Verificar se áudio foi gravado
                size = os.path.getsize(audio_file)
                print(f"📊 Tamanho do arquivo: {size} bytes")

                if size < 5000:
                    print("⚠️  Áudio muito curto")
                    os.remove(audio_file)
                    return ""

                print("🔍 Processando áudio...")
                with sr.AudioFile(audio_file) as source:
                    # Ajustar para a taxa de amostragem correta
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.record(source)

                    try:
                        text = self.recognizer.recognize_google(audio, language='pt-BR')
                        print(f"👤 Reconhecido: {text}")
                        return text.lower()
                    except sr.UnknownValueError:
                        print("❌ Não foi possível entender o áudio")
                        return ""
                    except sr.RequestError as e:
                        print(f"❌ Erro no serviço Google: {e}")
                        return ""

            return ""

        except Exception as e:
            print(f"❌ Erro geral: {e}")
            return ""
        finally:
            # Limpar arquivo temporário
            if os.path.exists(audio_file):
                os.remove(audio_file)
    

    def listen_for_wake_word(self):
        """Ouvir continuamente até detectar a wake word"""
        print(f"🔊 Aguardando: '{self.wake_word}'...")
        print("💡 Dica: Fale claramente 'R2'")

        attempts = 0
        while attempts < 100:  # Limitar tentativas para não ficar eternamente
            command = self.listen()
            if command and self.wake_word in command:
                self.speak("Sim senhor! Estou aqui!")
                return True
            attempts += 1
            time.sleep(0.5)

        print("⏰ Timeout - Nenhuma wake word detectada")
        return False

    def process_command(self, command):
        """Processar comandos do usuário"""
        if not command:
            self.speak("Não consegui entender, pode repetir?")
            return
        print(f"⚡ Comando recebido: {command}")
        
        # Tentar calcular se detectar palavras de operação
        if any(op in command for op in ["+", "-", "*", "/", "mais", "menos", "vezes", "dividido"]):
            if self.calculate(command):
                return

        # COMANDOS DE HORA E DATA
        if "hora" in command:
            now = datetime.now().strftime("%H:%M")
            self.speak(f"Agora são {now}")

        elif "data" in command or "dia" in command:
            hoje = datetime.now()
            dia = hoje.day
            mes = hoje.strftime("%B")
            ano = hoje.year
            self.speak(f"Hoje é dia {dia} de {mes} de {ano}")

        # COMANDOS DE SISTEMA
        elif "navegador" in command:
            self.speak("Abrindo navegador web")
            os.system("chromium-browser --no-sandbox &")

        elif "terminal" in command:
            self.speak("Abrindo terminal")
            os.system("lxterminal &")

        elif "youtube" in command:
            self.speak("Abrindo YouTube")
            os.system("chromium-browser https://www.youtube.com &")

        # COMANDOS DE INFORMAÇÃO
        elif "nome" in command:
            self.speak("Meu nome é R2-D2 seu assistente pessoal")
        elif "joão" in command:
            self.speak("joão é um cara muito legal e inteligente trabalha no I F C E")
        elif "igor" in command:
            self.speak("igor é um ótimo chefe e gente boa")
        elif "criadores" in command or "criador" in command:
            self.speak('fui criado por Igor, Nicolas, João Vitor, e um Lucas ')
        
        elif "como você está" in command:
            self.speak("Estou ótimo! Pronto para ajudar")

        elif "obrigado" in command:
            self.speak("De nada! Fico feliz em ajudar")

        # COMANDOS DE CONTROLE
        elif "parar" in command or "sair" in command or "chega" in command:
            self.speak("Até logo!")
            os.system(f"mpg123 -f {int(self.volume/60*32768)} ~/Desktop/voice_assistant/desligando.mp3")
            exit()

        elif "silêncio" in command:
            self.speak("Entendido, ficarei quietinho")
            time.sleep(3)
            
        # TROCADILHOS
        elif "piada" in command or "trocadilho" in command:
            pergunta, resposta = obter_trocadilho()
            if pergunta and resposta:
                self.speak(pergunta)
                time.sleep(2)  # Pausa para dar suspense
                self.speak(resposta)
            else:
                self.speak("Desculpe, não consegui buscar uma piada agora")
        

        # RESPOSTA PADRÃO
        else:
            self.speak("Desculpe, não conheço esse comando")
            self.speak("Tente perguntar a hora, data, ou abrir navegador")

    def run(self):
        """Executar o assistente principal"""
        os.system(f"mpg123 -f {int(self.volume/60*32768)} ~/Desktop/voice_assistant/ligando.mp3")
        self.speak("Sistema de voz inicializado com sucesso")
        self.speak("Microfone U S B configurado")
        self.speak("Diga R2 para começar")

        while True:
            print("\n" + "="*50)
            if self.listen_for_wake_word():

                # Ouvir comando principal
                command = self.listen()

                # Processar comando
                if command:
                    self.process_command(command)
                else:
                    self.speak("Não consegui ouvir seu comando")
                    self.speak("Por favor, repita")

                print("✅ Pronto para próximo comando")

def audio_test():
    """Teste completo de áudio"""
    print("=== TESTE COMPLETO DE ÁUDIO ===")

    # Testar gravação
    test_file = "test_audio.wav"
    try:
        print("🎤 Gravando 3 segundos com taxa 44100Hz...")
        cmd = f"arecord -D plughw:2,0 -d 3 -f S16_LE -r 44100 -c 1 {test_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            size = os.path.getsize(test_file)
            print(f"✅ Gravação bem-sucedida! Tamanho: {size} bytes")

            if size > 10000:
                print("🔊 Reproduzindo gravação...")
                os.system(f"aplay {test_file}")
                print("🎉 Sistema de áudio funcionando perfeitamente!")
            else:
                print("⚠️  Arquivo muito pequeno - verifique microfone")
        else:
            print(f"❌ Erro na gravação: {result.stderr}")

    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    print("=== ASSISTENTE DE VOZ RASPBERRY PI ===")
    print("Configurado para: USB PnP Sound Device (plughw:2,0)")
    print("Taxa de amostragem: 44100 Hz")
    print("======================================")

    # Executar teste ou assistente
    choice = input("Executar teste de áudio? (s/n): ").lower()

    if choice == 's':
        audio_test()
    else:
        assistant = VoiceAssistant()

        # Teste rápido antes de iniciar loop
        print("🔊 Testando síntese de voz...")
        assistant.speak("Teste de voz OK")

        print("🎤 Iniciando assistente...")
        assistant.run()