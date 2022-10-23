import sys

from OCR import *
from TextCorrection import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('PhotoLang.ui', self)
        self.fname = None
        self.pb1.clicked.connect(self.FileSelect)
        self.pb2.clicked.connect(self.correction)
        self.pb3.clicked.connect(self.run)


    def FileSelect(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.png);;Картинка (*.jpg);;Все файлы (*)'
        )[0]
        self.fname = fname
        self.lang = None
        if fname:
            form2 = Dialog(fname)
            form2.exec_()

    def run(self):
        if self.fname:
            if self.cbRU.isChecked() and not self.cbEN.isChecked():
                OCR_text = ('\n'.join(text_recognitionRu(self.fname)))
                print(OCR_text)
                self.lang = 'Ru'
                self.te1.setPlainText(OCR_text)
                self.lb1.setText('Вы можете исправить ошибки распознавания в тексте:')

            elif not self.cbRU.isChecked() and self.cbEN.isChecked():
                OCR_text = ('\n'.join(text_recognitionEn(self.fname)))
                print(OCR_text)
                self.lang = 'En'
                self.te1.setPlainText(OCR_text)
                self.lb1.setText('You can correct recognition errors in text:')

            elif self.cbRU.isChecked() and self.cbEN.isChecked():
                OCR_text = ('\n'.join(text_recognitionRuEn(self.fname)))
                print(OCR_text)
                self.lang = 'RuEn'
                self.te1.setPlainText(OCR_text)
                self.lb1.setText('You can correct recognition errors in text:/\n'
                                 'Вы можете исправить ошибки распознавания в тексте:')
            elif not self.cbRU.isChecked() and not self.cbEN.isChecked():
                self.statusbar.showMessage('Не выбран язык для распознавания.')
        else:
            self.statusbar.showMessage('Не выбран файл.')

    def correction(self):
        text = self.te1.toPlainText()
        if self.lang == 'Ru':
            self.lb2.setText('Исправленный текст:')
            self.te2.setPlainText(str(correctionRu(text)))
            print(str(correctionRu(text)))
        elif self.lang == 'En':
            self.lb2.setText('Corrected text:')
            self.te2.setPlainText(str(correctionEn(text)))
            print(str(correctionEn(text)))
        elif self.lang == 'RuEn':
            self.lb2.setText('Исправленный текст:/\n'
                             'Corrected text:')
            self.te2.setPlainText(str(correctionRuEn(text)))
            print(str(correctionRuEn(text)))



class Dialog(QDialog):
    def __init__(self, fname):
        self.fname = fname
        super().__init__()
        uic.loadUi('Dialog.ui', self)
        print(fname)
        pixmap = QPixmap(self.fname)
        self.lbl.setPixmap(pixmap)

    def accept(self):
        Dialog.hide(self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wd = MyWidget()
    wd.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
