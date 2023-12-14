import socket
import threading
import time
import argparse
import signal

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("client_debug.log"),
        logging.StreamHandler()
    ]
)

EXIT_KEY = "exit"
CHAT_PROMPT = "(Type 'exit' to terminate) Send a message: "
ON_RCV_ERR_MSG = "Error occured while receiving a message from the server:"
ON_SND_ERR_MSG = "Error occured while sending a message:"
ON_SOCKET_ERROR = "Error occured while stablising a connection with socket:"
BAD_FILE_DESCRIPTOR_ERROR = "Bad file descriptor"
SHUT_DOWN_MSG = "The client is shutting down."
CONNECTION_REFUSED_MSG = "Cannot establish connection to the server. Ensure that the server is running with the correct port"

BUFFER_SIZE = 1024
SEND_TIMEOUT = 1

exit_event = threading.Event()

class Client(object):
    def __init__(self, client_name, port, host=None):
        self.host = socket.gethostname() if host is None else host
        self.port = port
        self.client_name = client_name

    def initialize_connection(self):
        try:
            self.client = socket.socket()
            self.client.connect((self.host, self.port))
            signal.signal(signal.SIGINT, self.signal_handler)
            self.thread_send = threading.Thread(target= self.on_send_messsage)
            self.thread_recv = threading.Thread(target=self.on_recv_message)
            self.thread_send.start()
            self.thread_recv.start()
        except ConnectionRefusedError as e:
            logging.error(f"{CONNECTION_REFUSED_MSG}")
        except socket.error as e:
            logging.error(f"{ON_SOCKET_ERROR} {str(e)}")
        
    def on_send_messsage(self):
        try:
            message = input(CHAT_PROMPT)
            while message != EXIT_KEY:
                if exit_event.is_set():
                    break
                self.client.send(f"{self.client_name}: {message}".encode())
                time.sleep(SEND_TIMEOUT)
                message = input(CHAT_PROMPT)
        except socket.error as e:
            logging.error(f"{ON_SOCKET_ERROR} {str(e)}")
        except Exception as e:
            logging.error(f"{ON_SND_ERR_MSG} {str(e)}")
        finally:
            self.client.close()

    def on_recv_message(self):
        try:
            while True:
                if exit_event.is_set():
                    break
                recv_message = self.client.recv(BUFFER_SIZE).decode()
                if not recv_message:
                    break
                logging.info(f"{recv_message}")
        except socket.error as e:
            if BAD_FILE_DESCRIPTOR_ERROR in str(e):
                logging.info(SHUT_DOWN_MSG)
            else:
                logging.error(f"{ON_SOCKET_ERROR} {str(e)}")
        except Exception as e:
            logging.error(f"{ON_RCV_ERR_MSG} {str(e)}")
        finally:
            self.client.close()

    def signal_handler(self, signum, frame):
        exit_event.set()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process server configurations.')
    parser.add_argument('--host', type=str, default=None, help='Specify server hostname.')
    parser.add_argument('--port', type=int, default=3000, help='Specify server port number.')
    args = parser.parse_args()
    
    name = input("Enter your name: ")
    client = Client(client_name=name, port=args.port)
    client.initialize_connection()
