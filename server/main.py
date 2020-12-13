import socket

from RequestHandler import RequestHandler
from ThreadPoolManger import ThreadPoolManger


if __name__ == '__main__':

    port = 8878
    host = '127.0.0.1'
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host,port))
    server_sock.listen(20)

    thread_pool = ThreadPoolManger(20)
    handler = RequestHandler()

    # debug messager
    print("Server start.\n")
    # handler.test()

    while True:
        conn_sock, addr = server_sock.accept()
        thread_pool.add_job(handler.handler, *(conn_sock, ))

    server_sock.close()