import os
import json
import requests
import base64
import io
from cryptography.fernet import Fernet
from PIL import Image
from dotenv import load_dotenv


#loads env variables
load_dotenv()

class FileConverter:
    
    def __init__(self, before_convert, after_convert, convert_path, new_dir, new_name):
        #environment variables
        self.TOKEN = os.environ['TOKEN']
        self.API_SECRET = os.environ['API_SECRET']
        self.API_KEY = os.environ['API_KEY']
        self.CIPHER = os.environ['CIPHER']
        #class attributes
        self.encrypt = False
        self.convert_path = convert_path
        self.before_convert = before_convert    #file format before conversion
        self.after_convert = after_convert      #file format after conversion
        self.new_name = new_name
        self.new_dir = new_dir
        self.file_id = ''
        self.file_name = ''
        self.file_extension = ''
        self.file_url = ''


    #file_id setter
    def set_file_attributes(self, file_id, file_name, file_extension, file_url):
        self.file_id = file_id
        self.file_name = file_name
        self.file_extension = file_extension
        self.file_url = file_url


    #upload file
    def upload_file(self):
        #get file data in binaray and post request
        with open(f"{self.convert_path}", "rb") as file:
            b = file.read()
        post_files = {"filename": b,}
        headers = {'Content-Disposition': 'form-data',}
        payload = ''
        url = f"https://v2.convertapi.com/upload?Secret={self.API_SECRET}&FileName={self.convert_path}"
        session = requests.Session()
        response = session.request('POST', url, data=payload, files=post_files, headers=headers)
        response = json.loads(response.text)
        print(response)
        self.set_file_attributes(response['FileId'],self.new_name,
            response['FileExt'], response['Url'])


    #convert uploaded file
    def convert_file(self):
        headers = {"Accept": "*/*",}
        payload = ''
        url = f'https://v2.convertapi.com/convert/{self.before_convert}/to/{self.after_convert}?Secret={self.API_SECRET}&File={self.file_id}'
        session = requests.Session()
        response = session.request('GET', url, data=payload, headers=headers)
        data = json.loads(response.text)
        data = data['Files']
        data = data[0]
        data = data['FileData']
        self.file_data = self.convert_to_bytes(data)
        self.recieve_file(self.file_data)


    #convert file data to base64
    def convert_to_bytes(self, msg):
        msg_bytes = msg
        msg_bytes = msg_bytes.encode('ascii')
        b64_bytes = base64.b64encode(msg_bytes)
        return b64_bytes


    def save_file(self, file_data, path):
        data = file_data
        f = Fernet(self.CIPHER)
        if self.encrypt == True:
            data = f.encrypt(data)
        try:
            img = Image.open(io.BytesIO(data))
            img.show()
            img.save(path)
        #if file is document
        except:
            with open(path, 'wb') as file:
                file.write(data)
                file.close()
                os.startfile(path)
        os.startfile(path)
        #change current file to new file


    def recieve_file(self, file_data):
        path = rf'{self.new_dir}\{self.new_name}.{self.after_convert}'
        #creates the blank file placeholder
        with open(path, 'wb') as file:
            data = file_data
            data = base64.b64decode(data)
            file.write(data)
        file.close()
        #writes file data to the blank placeholder
        with open(path, 'rb') as file:
            b = file.read()
            b = base64.b64decode(b)
            self.save_file(b, path)
        file.close()


    def toggle_encrypt(self, value):
        self.encrypt = value


    #generate a token for auth
    def create_token():
        params = {
            'Secret': os.environ['API_SECRET'],
            'RequestCount': '999999999',
            'Lifetime': '315569520',
            'Count': '1'
        }
        response = requests.post('https://v2.convertapi.com/token/create?', params=params)
        print(response.content)

