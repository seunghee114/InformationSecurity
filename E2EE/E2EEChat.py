from os import read
import socket
import threading
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util import Padding
from base64 import b64encode, b64decode

global KEY, IV, PUBLIC
KEY = {}        # key : Receiver / value : key of AES-256-CBC
IV = {}         # key : Receiver / value : IV of AES-256-CBC
PUBLIC = {}     # key : Receiver / value : public key of Receiver

# 서버 연결정보; 자체 서버 실행시 변경 가능
SERVER_HOST = "homework.islab.work"
SERVER_PORT = 8080

# private key, public key create
global private_key, public_key
private_key = RSA.generate(1024)
public_key = private_key.publickey()

connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectSocket.connect((SERVER_HOST, SERVER_PORT))

def socket_read():
    global KEY, IV, PUBLIC
    mode = AES.MODE_CBC
    bs = 16
    while True:
        readbuff = connectSocket.recv(2048)

        # extract method
        idx = readbuff.index('\n'.encode('utf-8'))
        extract_method = readbuff[:idx]
        method = extract_method.decode('utf-8').split(" ")
        method = method[1]
        payload = []
        msg = None
        
        if method == "MSGRECV":
            check = readbuff.count('rsa-publickey'.encode('utf-8'))
            if check == 0:      # encrypted message receive
                # separate readbuff into payload(readbuff) and encrypted message(msg)
                payloadIdx = idx
                msg = readbuff[payloadIdx+1:]
                for i in range(4):
                    tempidx = msg.index('\n'.encode('utf-8'))
                    payloadIdx += tempidx
                    msg = msg[tempidx+1:]
                readbuff = readbuff[:payloadIdx+3]
                recv_payload = readbuff.decode('utf-8')
                print(recv_payload)
                count = recv_payload.count('\n')
                count = min(count, 7)
                temp = recv_payload.split("\n", maxsplit = count)
                
                for i in range(len(temp)):
                    if i == 0:
                        payload += temp[i].split(" ")
                    else:
                        payload += temp[i].split(":", 1)

            else:                   # publickey receive
                # recv_payload = payload + publickey
                recv_payload = readbuff.decode('utf-8')
                print(recv_payload)
                count = recv_payload.count('\n')
                count = min(count, 6)
                temp = recv_payload.split("\n", maxsplit = count)
            
                for i in range(len(temp)):
                    if i == 0:
                        payload += temp[i].split(" ")
                    else:
                        payload += temp[i].split(":", 1)
        else:
            recv_payload = readbuff.decode('utf-8')
            print(recv_payload)
            count = recv_payload.count('\n')
            count = min(count, 7)
            temp = recv_payload.split("\n", maxsplit = count)
            
            for i in range(len(temp)):
                if i == 0:
                    payload += temp[i].split(" ")
                else:
                    payload += temp[i].split(":", 1)

        if method == "KEYXCHG" or method == "KEYXCHGRST":
            Algo = payload[3]
            From = payload[5]
            To = payload[7]
            key = payload[11]
            iv = payload[12]
            if Algo == "AES-256-CBC":
                KEY[From] = key.encode('utf-8')
                IV[From]= iv.encode('utf-8')

        elif method == "MSGRECV":
            From = payload[5]
            To = payload[7]
            check = payload.count('rsa-publickey')
            if check != 0:      # publickey receive
                PUBLIC[From] = RSA.import_key(payload[10])
            else:               # encrypted message receive
                # get aes-256-cbc key and iv 
                key = KEY[From]
                iv = IV[From]

                # decrypt encrypted message
                msg = msg.decode('utf-8')
                msg = b64decode(msg.encode('utf-8'))
                cipher_aes = AES.new(key, mode, iv)
                message = Padding.unpad(cipher_aes.decrypt(msg), bs).decode('utf-8')
                print("")
                print(message)
        
        
def socket_send():
    global KEY, IV, PUBLIC
    global private_key, public_key
    mode = AES.MODE_CBC
    bs = 16
    while True:
        input_str = ""
        while True:
            temp = input()
            if temp == "END":
                break
            input_str += temp + '\n'
        input_str = input_str[:len(input_str)-1]
        split = input_str.split("\n")
        payload = []
        for i in range(len(split)):
            if i == 0:
                payload += split[i].split(" ")
            else:
                payload += split[i].split(": ")

        method = payload[1]
        if method == "KEYXCHG" or method == "KEYXCHGRST":
            Algo = payload[3]
            From = payload[5]
            To = payload[7]
            # when key is encoded with utf-8, it must be 256 bits
            # ex) 'WhnhP6bbp6WXElQacdJKwlTDY0FKmKU='
            # when iv is encoded with utf-8, it must be 128 bits
            # ex) 'f8uAIIpdnFj0+w=='
            key = payload[9]
            iv = payload[10]
            
            # save key and iv
            KEY[To] = key.encode('utf-8')
            IV[To] = iv.encode('utf-8')
            connectSocket.sendall(input_str.encode('utf-8'))

        elif method == "MSGSEND":
            From = payload[3]
            To = payload[5]
            message = payload[9]
            if message == 'rsa-publickey':  # publickey send
                exPublic = public_key.export_key()
                input_str += '\n'
                connectSocket.sendall(input_str.encode('utf-8') + exPublic)
            else:                           # message send
                message = Padding.pad(message.encode('utf-8'), bs)

                # get aes-256-cbc key and iv 
                key = KEY[To]
                iv = IV[To]

                # encrypt message
                cipher_aes = AES.new(key, mode, iv)
                message = b64encode(cipher_aes.encrypt(message)).decode('utf-8')
                rSplit = input_str.rsplit('\n', 1)
                input_str = rSplit[0] + '\n'
                input_str += message
                connectSocket.sendall(input_str.encode('utf-8'))
        else:
            connectSocket.sendall(input_str.encode('utf-8'))
       

reading_thread = threading.Thread(target=socket_read)
sending_thread = threading.Thread(target=socket_send)

reading_thread.start()
sending_thread.start()

reading_thread.join()
sending_thread.join()