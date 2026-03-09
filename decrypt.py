import os
from cryptography.fernet import Fernet #type: ignore

key = b'0wYSjevFZjq7oOqtHx0PSxXwEMf1Zb0m3tAXXBmQYlk='

cipher = Fernet(key)
folder = 'files'
for root, folders, files in os.walk(folder):
    for file in files:
        if not file.endswith('.encrypted'):
            continue
        try:
            full = os.path.join(root, file)
            with open(full, 'rb') as f:
                data = f.read()
                f.close()
            decrypted = cipher.decrypt(data)
            with open(full, 'wb') as f:
                f.write(decrypted)
                f.close()
            newpath = full.replace('.encrypted','')
            os.rename(full,newpath)
            print(f"decrypted file: {newpath}")
        except PermissionError:
            print(f"permission denied to edit file {full}")
        except Exception as error:
            print(f"got error: {error}")