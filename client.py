import socket
import threading
import time
import argparse

parser = argparse.ArgumentParser(description='Process server configurations.')
parser.add_argument('--port', type=int, default=3000, help='Specify server port number.')
args = parser.parse_args()

port=args.port
host = socket.gethostname()
client = socket.socket()
client.connect((host, port))

name = input("Enter your name: ")

def send_messsage():
    try:
        message = input("Send a message: ")
        while message != 'exit':
            client.send(f"{name}: {message}".encode())
            time.sleep(1)
            message = input("Send another message: ")
    except Exception as e:
        print(f"Error occured while sending a message: {str(e)}")
        client.close()
    finally:
        client.close()

def recv_message():
    try:
        while True:
            recv_message = client.recv(port).decode()
            print(f"{recv_message}")
    except Exception as e:
        print(f"Error occured while receiving a message from the server: {str(e)}")
        client.close()

if __name__ == '__main__':
    thread_send = threading.Thread(target= send_messsage)
    thread_recv = threading.Thread(target=recv_message)

    thread_send.start()
    thread_recv.start()
