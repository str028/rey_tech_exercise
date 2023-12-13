import socket
import _thread
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("server_debug.log"),
        logging.StreamHandler()
    ]
)

ON_RCV_ERR_MSG = "Error occured while receiving a message:"
ON_SERVER_RUN_ERROR = "Error occured while running the server:"
ON_SOCKET_ERROR = "Error occured while stablising a connection with socket:"
SHUT_DOWN_MSG = "The server is shutting down."
BAD_FILE_DESCRIPTOR_ERROR = "Bad file descriptor"
BUFFER_SIZE = 1024
UNKNOWN = 'Unknown'


class Server(object):
    def __init__(self, port=3000, number_of_client=10, host=None):
        self.host = socket.gethostname() if host is None else host
        self.port = port
        self.number_of_client = number_of_client

    def on_new_client(self, clientsocket, address, port):
        try:
            while True:
                message = clientsocket.recv(BUFFER_SIZE).decode()
                if not message:
                    break
                logging.info(f"{str(address)}: {str(message)}")
                clientsocket.send(message.encode())
        except KeyboardInterrupt:
            clientsocket.close()
        except Exception as e:
            logging.error(f"{ON_RCV_ERR_MSG} {str(e)}")
        finally:
            clientsocket.close()

    def run(self):
        server = socket.socket()
        server.bind((self.host, self.port))
        server.listen(self.number_of_client)
        logging.info("Server has started.")
        try:
            while True:
                connection, address = server.accept()
                _thread.start_new_thread(self.on_new_client,(connection,address, self.port))
        except KeyboardInterrupt:
            connection.close()
        except socket.error as e:
            if BAD_FILE_DESCRIPTOR_ERROR in str(e):
                logging.info(SHUT_DOWN_MSG)
            else:
                logging.error(f"{ON_SOCKET_ERROR} {str(e)}")
        except Exception as e:
            logging.error(f"{ON_SERVER_RUN_ERROR} {str(e)}")
        finally:
            connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process server configurations.')
    parser.add_argument('--port', type=int, default=3000, help='Specify server port number.')
    parser.add_argument('--number_of_client', type=int, default=10, help='Specify number of clients.')
    args = parser.parse_args()

    server = Server(args.port, args.number_of_client)
    server.run()