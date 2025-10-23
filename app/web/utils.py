from googletrans import Translator

translator = Translator()

def translate_to_en(text):
    return translator.translate(text, src='ar', dest='en').text

def translate_to_ar(text):
    return translator.translate(text, src='en', dest='ar').text
