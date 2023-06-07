import sys
import re
from PyQt6.QtWidgets import (QApplication, QPushButton, QTabWidget , QCheckBox, QLabel, 
                            QGridLayout,QFileDialog, QWidget, QComboBox, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from file_converter import FileConverter
from file_encryptor import FileEncryptor


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.filepath = 'path: '
        self.e_filepath = ''
        self.dirstring = 'conversion path: '
        self.before_convert = ''
        #Settings
        self.setWindowTitle('File Manager')
        self.resize(350, 120)
        self.setFixedSize(350, 310)
        self.setObjectName('main_window')
        #Widgets
        self.tab_widget = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.tab_1.setObjectName('tab_1')
        self.tab_2.setObjectName('tab_2')
        #Layouts
        self.tab_widget.addTab(self.tab_1, 'file conversion')
        self.tab_widget.addTab(self.tab_2, 'file encryption')
        self.conversion_tab()
        self.encryption_tab()
        self.main_layout = QGridLayout(self)
        self.main_layout.addWidget(self.tab_widget)
        #Signals
        self.search_button.clicked.connect(self.search_files_handler)
        self.dir_button.clicked.connect(self.search_dir_handler)
        self.convert_button.clicked.connect(self.make_conversion)
        self.encrypt_dropdown.activated.connect(self.encryption_handler)
        self.search_button_e.clicked.connect(self.search_encryption_handler)
        self.activate_button_e.clicked.connect(self.en_or_de)


    def conversion_tab(self):
        self.search_button = QPushButton('search file')
        self.dir_button = QPushButton('select directory')
        self.convert_button = QPushButton('convert')
        self.encrypt_button = QCheckBox('encrypt?')
        #dropdown box
        self.dropdown = QComboBox(self)
        self.dropdown.activated.connect(self.select_conversion_handler)
        self.jpg_to_other = ['compress', 'gif', 'jpg', 'pdf', 'pdfa', 'png', 'svg', 'tiff', 'watermark', 'webp']
        self.png_to_other = ['gif', 'jpg', 'pdf', 'pdfa', 'png', 'svg', 'tiff', 'watermark', 'webp']
        self.csv_to_other = ['jpg', 'pdf', 'pdfa', 'png', 'tiff', 'webp', 'xls', 'xlsx']
        self.gif_to_other = ['png', 'jpg', 'gif', 'pdf', 'pdfa', 'svg', 'tiff', 'webp']
        self.svg_to_other = ['jpg', 'pdf', 'pdfa', 'png', 'svg', 'tiff', 'webp']
        self.pdf_to_other = ['csv', 'ocr', 'txt']
        self.docx_to_other = [
            'compare', 'doc', 'docx', 'encrypt', 'html', 'jpg', 'mhtml', 'odt', 'pdf', 'png', 
            'rtf', 'tiff', 'txt', 'webp', 'xml', 'xps'
        ]
        #rename file text edit
        self.rename = QLineEdit(self)
        #labels
        self.label = QLabel('select desired format', self)
        self.path_label_c = QLabel(self.filepath, self)
        self.dirpath_label = QLabel(self.dirstring, self)
        self.rename_label = QLabel('name new file:')
        #layout
        self.my_layout = QGridLayout(self)
        self.my_layout.addWidget(self.path_label_c)
        self.my_layout.addWidget(self.search_button)
        self.my_layout.addWidget(self.dirpath_label)
        self.my_layout.addWidget(self.dir_button)
        self.my_layout.addWidget(self.label)
        self.my_layout.addWidget(self.dropdown)
        self.my_layout.addWidget(self.rename_label)
        self.my_layout.addWidget(self.rename)
        self.my_layout.addWidget(self.encrypt_button) 
        self.my_layout.addWidget(self.convert_button)
        self.tab_1.setLayout(self.my_layout)


    def encryption_tab(self):
        self.path_label_e = QLabel(self.filepath, self)
        self.img_label = QLabel(self)
        self.path_label_e.setObjectName('path_label_e')
        self.search_button_e = QPushButton('search file')
        self.encrypt_dropdown = QComboBox(self)
        self.activate_button_e = QPushButton('encrypt file')
        self.my_layout2 = QGridLayout(self)
        if self.e_filepath:
            self.pixmap = QPixmap(self.e_filepath)
            self.img_label.setPixmap(self.pixmap)
        self.encrypt_dropdown.addItems(['encrypt', 'decrypt'])
        self.my_layout2.addWidget(self.encrypt_dropdown)
        self.my_layout2.addWidget(self.path_label_e)
        self.my_layout2.addWidget(self.img_label)
        self.my_layout2.addWidget(self.search_button_e)
        self.my_layout2.addWidget(self.activate_button_e)
        self.my_layout2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tab_2.setLayout(self.my_layout2)


    def encryption_handler(self):
        if self.encrypt_dropdown.currentText() == 'encrypt':
            self.activate_button_e.setText('encrypt file')
        else:
            self.activate_button_e.setText('decrypt file')


    def search_encryption_handler(self):
        self.e_filepath = QFileDialog.getOpenFileName()
        self.e_filepath = self.e_filepath[0]
        self.path_label_e.setText(f'path: {self.e_filepath}')
        self.pixmap = QPixmap(self.e_filepath)
        self.img_label.setPixmap(self.pixmap)
        self.pixmap.scaledToHeight(100)

    
    def en_or_de(self):
        file_translator = FileEncryptor(self.e_filepath)
        if self.encrypt_dropdown.currentText() == 'encrypt':
            file_translator.encrypt_file()
        else:
            self.activate_button_e.setText('decrypt file')
            file_translator.decrypt_file()


    def search_files_handler(self):
        print('searching files')
        self.search_files()
    

    def clear_choices(self):
        self.dropdown.clear()
        self.dropdown.addItem('select desired format')
        self.rename.clear()
        self.filepath = 'path: '
        self.dirpath = 'conversion path: '
        self.before_convert = ''
        self.after_convert = ''
        self.encrypt_button.setChecked(False)


    def search_files(self):
        #select file to be converted
        self.filename = QFileDialog.getOpenFileName()
        self.filepath = self.filename[0]
        #get the file extension before conversion
        try:
            self.before_convert = re.search('[^.]+$', self.filepath).group().lower()
        except:
            print('please select file')
            return
        self.path_label.setText(f'path: {self.filepath}')
        #set conversion options based on selected file
        if self.before_convert == 'gif':
            self.dropdown.addItems(self.gif_to_other)
        elif self.before_convert == 'jpg':
            self.dropdown.addItems(self.jpg_to_other)
        elif self.before_convert == 'png':
            self.dropdown.addItems(self.png_to_other)
        elif self.before_convert == 'svg':
            self.dropdown.addItems(self.svg_to_other)
        elif self.before_convert == 'csv':
            self.dropdown.addItems(self.csv_to_other)
        elif self.before_convert == 'docx':
            self.dropdown.addItems(self.docx_to_other)
        else:
            print('please select file')
        print(self.filepath)


    def search_dir_handler(self):
        print('searching directories')
        self.search_dirs()


    def search_dirs(self):
        #select directory where converted files will go
        self.dirpath = QFileDialog.getExistingDirectory()
        self.dirpath_label.setText(f'conversion path: {self.dirpath}')
        print(self.dirpath)


    def select_conversion_handler(self, index):
        #selected file will be passed to the conversion func
        if self.before_convert == 'gif':
            self.selection = self.gif_to_other[index]
        elif self.before_convert == 'jpg':
            self.selection = self.jpg_to_other[index]
        elif self.before_convert == 'png':
            self.selection = self.png_to_other[index]
        elif self.before_convert == 'svg':
            self.selection = self.svg_to_other[index]
        elif self.before_convert == 'csv':
            self.selection = self.csv_to_other[index]
        elif self.before_convert == 'docx':
            self.selection = self.docx_to_other[index]
        else:
            print('please select file')
        print(f'Activated index: {self.selection}')
        self.convert_confirmation(self.selection)


    def convert_confirmation(self, after_convert):
        self.after_convert = after_convert
        #if there is a selected file print it out
        try:
            print(f'from: {self.before_convert}')
            print(f'to: {self.after_convert}')
            print(f'rename to: {self.rename.text()}')
        #if there isn't a selected file, prompt a selection
        except AttributeError.with_traceback():
            print(f'from: please select a file')
            print(f'to: {self.after_convert}')
            print(f'rename to: {self.rename.text()}')


    def make_conversion(self):
        if not self.filepath or not self.dirpath or not self.after_convert or not self.before_convert or not self.rename.text():
            print('please select file and conversion path')
            return
        converter = FileConverter(                    
                    before_convert=self.before_convert,
                    after_convert=self.after_convert,
                    convert_path=self.filepath,
                    new_name=self.rename.text(),
                    new_dir=self.dirpath)
        self.encrypt = True if self.encrypt_button.isChecked() else False
        converter.toggle_encrypt(self.encrypt)
        converter.upload_file()
        converter.convert_file()


if __name__ == '__main__':
    app = QApplication([])
    #read and set stylesheet 
    with open(r'styles.qss', 'r') as f:
        app.setStyleSheet(f.read())
    widget = Gui()
    widget.show()
    sys.exit(app.exec())