import textblob
from autocorrect import Speller

def correctionEn(text):
        textBlb = textblob.TextBlob(text)
        textCorrected = textBlb.correct()
        return textCorrected

def correctionRu(text):
    spell = Speller('ru')
    return spell(text)

def correctionRuEn(text):
    spell = Speller('ru')
    textBlb = textblob.TextBlob(spell(text))
    textCorrected = textBlb.correct()
    return textCorrected
