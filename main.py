import sys

from OCR import *
from TextCorrection import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.tname = None
        self.pb1, self.pb2, self.pb3 = None, None, None
        self.pbt1, self.pbt2 = None, None
        self.lb1, self.lb2, self.lbl, self.lbw = None, None, None, None
        self.te1, self.te2 = None, None
        self.fname = None
        uic.loadUi('PhotoLang.ui', self)
        self.pb1.clicked.connect(self.ImgFileSelect)
        self.pb2.clicked.connect(self.correction)
        self.pb3.clicked.connect(self.run)
        self.pbt1.clicked.connect(self.TextFileSelect)
        self.pbt2.clicked.connect(self.output_in_txt)

    def ImgFileSelect(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.png);;Картинка (*.jpg);;Все файлы (*)'
        )[0]
        self.fname = fname
        self.lang = None
        if fname:
            form2 = Dialog(fname)
            form2.exec_()
            self.lbl.setText(f'Выбран путь для изображения: \n {fname}')

    def run(self):
        print('Please wait...')
        if self.fname:
            if self.cbRU.isChecked() and not self.cbEN.isChecked():
                OCR_text = ('\n'.join(text_recognitionRu(self.fname)))
                print('Распознанный текст:')
                print(OCR_text.replace(':', '.'))
                self.lang = 'Ru'
                self.te1.setPlainText(OCR_text.replace(':', '.'))
                self.lb1.setText('Вы можете исправить ошибки распознавания в тексте:')

            elif not self.cbRU.isChecked() and self.cbEN.isChecked():
                OCR_text = ('\n'.join(text_recognitionEn(self.fname)))
                print('Recognited text:')
                print(OCR_text.replace(':', '.'))
                self.lang = 'En'
                self.te1.setPlainText(OCR_text.replace(':', '.'))
                self.lb1.setText('You can correct recognition errors in text:')

            elif self.cbRU.isChecked() and self.cbEN.isChecked():
                OCR_text = ('\n'.join(text_recognitionRuEn(self.fname)))
                print('Recognited text:\n Распознанный текст:')
                print(OCR_text.replace(':', '.'))
                self.lang = 'RuEn'
                self.te1.setPlainText(OCR_text.replace(':', '.'))
                self.lb1.setText('You can correct recognition errors in text:/\n'
                                 'Вы можете исправить ошибки распознавания в тексте:')
            elif not self.cbRU.isChecked() and not self.cbEN.isChecked():
                self.statusbar.showMessage('Не выбран язык для распознавания.')
        else:
            self.statusbar.showMessage('Не выбрано изображение.')

    def correction(self):
        print('Please wait...')
        text = self.te1.toPlainText()
        if self.lang == 'Ru':
            self.lb2.setText('Исправленный текст:')
            self.te2.setPlainText(str(correctionRu(text)))
            print('Исправленный текст:')
            print(str(correctionRu(text)))
        elif self.lang == 'En':
            self.lb2.setText('Corrected text:')
            self.te2.setPlainText(str(correctionEn(text)))
            print('Corrected text:')
            print(str(correctionEn(text)))
        elif self.lang == 'RuEn':
            self.lb2.setText('Исправленный текст:/\n'
                             'Corrected text:')
            self.te2.setPlainText(str(correctionRuEn(text)))
            print('Исправленный текст:/\n'
                  'Corrected text:')
            print(str(correctionRuEn(text)))

    def TextFileSelect(self):
        tname = QFileDialog.getOpenFileName(
            self, 'Выбрать текстовый файл', '',
            'Текст (*.txt);;Все файлы (*)'
        )[0]
        self.tname = tname

    def output_in_txt(self):
        if self.tname:
            with open(self.tname, 'wt', encoding='UTF-8') as file_txt:
                if self.te2.toPlainText():
                    file_txt.write(str(self.te2.toPlainText()))
                    self.statusbar.showMessage('Информация успешно записана в файл')
                    print(f'Информация успешно записана в файл по пути "{self.tname}" ')
                else:
                    self.statusbar.showMessage('Нечего записать в текстовый файл.')
                    print('Нечего записать в текстовый файл.')
        else:
            self.statusbar.showMessage('Не выбран текстовый файл.')
            print('Не выбран текстовый файл.')


class Dialog(QDialog):
    def __init__(self, fname):
        self.fname = fname
        super().__init__()
        uic.loadUi('Dialog.ui', self)
        print(f'Выбран путь для изображения: {fname}')
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
