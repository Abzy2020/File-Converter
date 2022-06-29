from file_converter import FileConverter

def main():
    print('Enter absolute path to file (dont forget file extension): ')
    convert_path = input()
    print('Enter the current file type: ')
    before_convert = input()
    print('Enter file type you wish to change it to: ')
    after_convert = input()
    print('Name the file: ')
    new_file_name = input()

    conversion = FileConverter(
                    before_convert=before_convert,
                    after_convert=after_convert,
                    convert_path=convert_path,
                    new_name=new_file_name)

    conversion.upload_file()
    conversion.convert_file()

if __name__ == '__main__':
    main()