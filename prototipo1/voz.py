from TTS.api import TTS
import simpleaudio as sa
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig


torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig])


tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)

texto = (
    "Roda, roda e vira, solta a roda e ve Me passaram a mão na bunda e ainda não comi ninguém Roda, roda e vira, solta a roda e vem Neste raio de suruba já me passaram a mão na bunda E ainda não comi ninguém"
    "Minha missão é ajudar você, mestre Jedi."
)

arquivo = "fala.wav"


tts.tts_to_file(
    text=texto,
    file_path=arquivo,
    language="pt"
)

print("Áudio gerado com sucesso!")

wave_obj = sa.WaveObject.from_wave_file(arquivo)
play_obj = wave_obj.play()
play_obj.wait_done()