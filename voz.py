from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/vits")
tts.tts_to_file(text="Olá mestre Jedi, pronto para a missão!", file_path="fala.wav")
