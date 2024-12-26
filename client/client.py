import socket
from decoder import *

weather_data = ""

def main():

    # connect to tcp server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '192.168.0.10'
    port = 12345
    s.connect((host, port))

    # receive data
    while True:
        weather_data = s.recv(37).decode('utf-8')
        print(weather_data)
        debug_print(weather_data)


if __name__ == '__main__':
    main()