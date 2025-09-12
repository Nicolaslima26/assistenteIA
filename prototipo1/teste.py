import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.effects import normalize
from pydub.playback import play

# Função para gerar voz com Edge-TTS
async def gerar_audio(texto, nome_arquivo, voz="pt-BR-AntonioNeural"):
    tts = edge_tts.Communicate(texto, voz)
    await tts.save(nome_arquivo)

# Função para aplicar efeito de voz robótica
def efeito_robo(input_path, output_path):
    som = AudioSegment.from_file(input_path)
    # Filtro de frequências (mais metálico)
    som = som.low_pass_filter(1000)
    # Normaliza volume
    som = normalize(som)
    # Altera levemente o pitch (grave, robótico)
    som = som._spawn(som.raw_data, overrides={
        "frame_rate": int(som.frame_rate * 0.9)
    }).set_frame_rate(som.frame_rate)
    som.export(output_path, format="mp3")

# Função principal para falar
def falar(texto):
    # Gera voz base
    asyncio.run(gerar_audio(texto, "voz_original.mp3"))
    # Aplica efeito robô
    efeito_robo("voz_original.mp3", "voz_robo.mp3")
    # Reproduz o áudio final
    som = AudioSegment.from_file("voz_robo.mp3")
    play(som)

# Exemplo de uso
if __name__ == "__main__":
    falar("Olá mestre, estou pronto para obedecer seus comandos.")
