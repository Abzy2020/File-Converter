import sys
from file_converter import FileConverter, create_token


def main(convert_path, before_convert, after_convert, new_file_name, new_dir):
    if not convert_path or not before_convert or not after_convert or not new_file_name:
        print('Convert a File: python converter.py <file_path> <path_before_convert> <path_after_convert> <new_file_name>')
        sys.exit()
    conversion = FileConverter(before_convert=before_convert,after_convert=after_convert,convert_path=convert_path,
                new_dir=new_dir,new_name=new_file_name)
    conversion.upload_file()
    conversion.convert_file()


if __name__ == '__main__':
    try:    
        if sys.argv[1] == '-t':
            create_token()
        else:
            main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[1])
    except:
        print('COMMANDS:')
        print('Convert a File: python converter.py <file_path> <fmt_before_convert> <fmt_after_convert> <new_file_name>')
        print('Generate a Token: python converter.py -t')
        sys.exit()