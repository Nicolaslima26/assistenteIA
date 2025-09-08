from TTS.api import TTS
import simpleaudio as sa
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig

# Permite que PyTorch carregue os objetos necessários
torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig])

# Inicializa o modelo xtts_v2
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)

# Texto a ser falado
texto = (
    "Bip bop! Sou seu R2-B2, seu assistente pessoal. "
    "Minha missão é ajudar você, mestre Jedi."
)

# Arquivo de saída
arquivo = "fala.wav"

# Gera o áudio
tts.tts_to_file(
    text=texto,
    file_path=arquivo,
    language="pt"
    # speaker_wav="voz_masculina.wav"  # opcional: voz personalizada
)

print("Áudio gerado com sucesso!")

# Reproduz o áudio
wave_obj = sa.WaveObject.from_wave_file(arquivo)
play_obj = wave_obj.play()
play_obj.wait_done()