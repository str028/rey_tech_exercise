# Technical Execise by Reymart Betana

This is a simple python script that demonstrates server and clients communications using socket library.

There are two python scripts created for server and client, respectively. The server is capable of receiving messages from multiple client connections. The client is able to send/receive a message from the server

The script does not require any third party library and uses only default libararies so we don't have to install anything.

## Run the server script
```bash
python3 server.py --port=3000 --number_of_client=10
```

## Run the client (you can run multiple clients)
```bash
python3 client.py --port=3000
```
You will prompt with a message asking the client name.

Then send a message to server.

If you want to terminate the client instance, you can send a message 'exit'
