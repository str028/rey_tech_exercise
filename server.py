import socket
import _thread
import argparse

def on_new_client(clientsocket, address, port):
    try:
        while True:
            message = clientsocket.recv(port).decode()
            print(f"{str(address)}: {str(message)}")
            clientsocket.send(message.encode())
    except Exception as e:
        print(f"Error occured while receiving a message: {str(e)}")
        clientsocket.close()


def run_server(port=3000, number_of_client=10):
    host = socket.gethostname()
    server = socket.socket()
    server.bind((host, port))
    server.listen(number_of_client)
    print("Server has started.")
    try:
        while True:
            connection, address = server.accept()
            _thread.start_new_thread(on_new_client,(connection,address, port))
    except Exception as e:
        print(f"Error occured: {str(e)}")
        connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process server configurations.')
    parser.add_argument('--port', type=int, default=3000, help='Specify server port number.')
    parser.add_argument('--number_of_client', type=int, default=10, help='Specify number of clients.')
    args = parser.parse_args()
    run_server(args.port, args.number_of_client)