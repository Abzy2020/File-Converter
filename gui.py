import sys
import re
from file_converter import FileConverter
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QFileDialog, QWidget, QComboBox, QLineEdit


class Gui(QWidget):

    def __init__(self):
        super().__init__()

        self.filepath = 'path: '
        self.dirstring = 'conversion path: '
        self.before_convert = ''

        #Widgets
        self.search_button = QPushButton('search file')
        self.dir_button = QPushButton('select directory')
        self.convert_button = QPushButton('convert')
            #dropdown box
        self.dropdown = QComboBox(self)
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

        self.dropdown.activated.connect(self.select_conversion_handler)
            #rename file text edit
        self.rename = QLineEdit(self)
            #labels
        self.label = QLabel('select desired format', self)
        self.path_label = QLabel(self.filepath, self)
        self.dirpath_label = QLabel(self.dirstring, self)
        self.rename_label = QLabel('name new file')

        #Layouts
        self.my_layout = QVBoxLayout(self)
        self.my_layout.addWidget(self.path_label)
        self.my_layout.addWidget(self.search_button)
        self.my_layout.addWidget(self.dirpath_label)
        self.my_layout.addWidget(self.dir_button)
        self.my_layout.addWidget(self.label)
        self.my_layout.addWidget(self.dropdown)
        self.my_layout.addWidget(self.rename_label)
        self.my_layout.addWidget(self.rename)
        self.my_layout.addWidget(self.convert_button)

        #Signals
        self.search_button.clicked.connect(self.search_files_handler)
        self.dir_button.clicked.connect(self.search_dir_handler)
        self.convert_button.clicked.connect(self.make_conversion)


    def search_files_handler(self):
        print('searching files')
        self.search_files()


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
        converter.upload_file()
        converter.convert_file()


if __name__ == '__main__':
    app = QApplication([])
    #read and set stylesheet 
    with open(r'styles.qss', 'r') as f:
        app.setStyleSheet(f.read())
    widget = Gui()
    widget.resize(350, 120)
    widget.setWindowTitle('File converter')
    widget.show()

    sys.exit(app.exec())