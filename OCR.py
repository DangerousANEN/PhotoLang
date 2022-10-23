import easyocr


def text_recognitionRu(file_path):
    reader = easyocr.Reader(['ru'])
    result = reader.readtext(file_path, detail=0, paragraph=True)
    return result

def text_recognitionEn(file_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path, detail=0, paragraph=True)
    return result

def text_recognitionRuEn(file_path):
    reader = easyocr.Reader(['ru', 'en'])
    result = reader.readtext(file_path, detail=0, paragraph=True)
    return result
