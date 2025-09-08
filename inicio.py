from gtts import gTTS

texto = "Olá! Esta é uma voz divertida e robotizada 😎"
tts = gTTS(texto, lang="pt", tld="com.br")
tts.save("voz.mp3")
