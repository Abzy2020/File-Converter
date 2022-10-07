import sys
import re
from file_converter import FileConverter
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QFileDialog, QWidget, QComboBox, QPlainTextEdit


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.filepath = 'path: '
        self.dirstring = 'conversion path: '

        #Widgets
        self.search_button = QPushButton('search file')
        self.dir_button = QPushButton('select directory')
        self.convert_button = QPushButton('convert')

        self.dropdown = QComboBox(self)
        self.options = ['png', 'jpg', 'gif', 'pdf', 'docx']
        self.dropdown.addItems(self.options)
        self.dropdown.activated.connect(self.select_conversion_handler)

        self.rename = QPlainTextEdit(self)

        self.label = QLabel('select desired format', self)
        self.path_label = QLabel(self.filepath, self)
        self.dirpath_label = QLabel(self.dirstring, self)

        #Layouts
        self.my_layout = QVBoxLayout(self)
        self.my_layout.addWidget(self.path_label)
        self.my_layout.addWidget(self.search_button)
        self.my_layout.addWidget(self.dirpath_label)
        self.my_layout.addWidget(self.dir_button)
        self.my_layout.addWidget(self.label)
        self.my_layout.addWidget(self.dropdown)
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
        self.filename = QFileDialog.getOpenFileName()
        self.filepath = self.filename[0]
        self.before_convert = re.search('[^.]+$', self.filepath).group().lower()

        self.path_label.setText(f'path: {self.filepath}')
        print(self.filepath)


    def search_dir_handler(self):
        print('searching directories')
        self.search_dirs()


    def search_dirs(self):
        self.dirpath = QFileDialog.getExistingDirectory()
        self.dirpath_label.setText(f'conversion path: {self.dirpath}')
        print(self.dirpath)


    def select_conversion_handler(self, index):
        #selected file will be passed to the conversion func
        self.selection = self.options[index]
        print(f'Activated index: {self.selection}')
        self.convert_confirmation(self.selection)


    def convert_confirmation(self, after_convert):
        self.after_convert = after_convert
        print(f'from: {self.before_convert}')
        print(f'to: {self.after_convert}')
        print(f'rename to: {self.rename.toPlainText()}')


    def make_conversion(self):
        converter = FileConverter(                    
                    before_convert=self.before_convert,
                    after_convert=self.after_convert,
                    convert_path=self.filepath,
                    new_name=self.rename.toPlainText(),
                    new_dir=self.dirpath)
        converter.upload_file()
        converter.convert_file()


if __name__ == '__main__':
    app = QApplication([])

    with open('file-conversion\styles.qss', 'r') as f:
        app.setStyleSheet(f.read())

    widget = MyApp()
    widget.resize(350, 120)
    widget.setWindowTitle('File converter')
    widget.show()

    sys.exit(app.exec())