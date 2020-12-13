import socket
import sys

def register(sock, user_id: str, password: str, buffersize: int):
    data = ''
    data = data + 'Register\n'
    data = data + user_id + '\n'
    data = data + password + '\n'
    sock.sendall(data.encode('utf-8'))

    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8').split()
    
    if recv_data[1] =='True':
        # debug message
        # print("Register successfully!")
        return 1
    else:
        # debug message
        # print("Register failed!")
        return 0


def login(sock, user_id: str, password: str, buffersize: int):
    data = 'Login\n'
    data = data + user_id + '\n'
    data = data + password + '\n'

    sock.sendall(data.encode('utf-8'))
    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8').split()

    if recv_data[1] == str(True):
        # debug message
        # print("Login successfully!")
        return 1
    else:
        # debug message
        # print("Login failed!")
        return 0


def get_title(sock, title: str, buffersize: int):
    data = ''
    data = data + 'GetTitle\n'
    if title == '':
        title = '*'
    data = data + title + '\n'

    sock.sendall(data.encode('utf-8'))
    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8').split()
    print(recv_data)
    
    ret = []
    if recv_data[1] == 'True':
        # debug message
        # print("Found!")
        i = 2
        while i < len(recv_data):
            # debug message
            # print('%s'%recv_data[i][2:-3])
            string = recv_data[i][2:-3]
            ret.append(string)
            i += 1
    # else:
        # debug message
        # print("Not found!")
    return ret


def get_content(sock, title: str, page: str, buffersize: int):
    data = ''
    data = data + 'GetContent\n'
    data = data + title + '\n'
    data = data + page + '\n'
    
    sock.sendall(data.encode('utf-8'))
    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8')
    vec = recv_data.split()
    
    if vec[1] == 'True':
        # debug message
        # print("Found!")
        return (vec[2], recv_data[40:])


def get_path(sock, user_id, buffersize):
    data = ''
    data = data + 'GetPath\n'
    data = data + user_id + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8').split()

    title = []
    path = []

    if recv_data[1]=='True':
        # debug message
        # print("Found!")
        i = 2
        while i < len(recv_data):
            # debug message
            print('title: %s'%recv_data[i])
            title.append(recv_data[i])
            i += 1
            # debug message
            print('path: %s'%recv_data[i])
            path.append(recv_data[i])
            i += 1
    else:
        # debug message
        print("Not found!")

    return title, path


def add_path(sock, user_id, title, path, buffersize):
    data = ''
    data = data + 'AddPath\n'
    data = data + user_id + '\n'
    data = data + title + '\n'
    data = data + path + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8').split()
    
    if recv_data[1]=='True':
        # debug message
        # print("Success!")
        return 1
    else:
        # debug message
        # print("Failed!")
        return 0


def add_record(sock, user_id, local, title, page, buffersize):
    data = ''
    data = data + 'AddRecord\n'
    data = data + user_id + '\n'
    data = data + local + '\n'
    data = data + title + '\n'
    data = data + page + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8').split()
    
    if recv_data[1] == 'True':
        # debug message
        # print("Success!")
        return 1
    else:
        # debug message
        # print("Failed!")
        return 0


def get_record(sock, user_id, local, title,  buffersize):
    data = ''
    data = data + 'GetRecord\n'
    data = data + user_id + '\n'
    data = data + local + '\n'
    data = data + title + '\n'

    sock.sendall(data.encode('utf-8'))
    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8').split()

    if recv_data[1] == 'True':
        # debug message
        # print("Found!")
        return recv_data[2]
    else:
        # debug message
        # print("Not found!") 
        # print("add record")
        add_record(sock, user_id, local, title, "1", buffersize)
        return "1"

def delete_path(sock, user_id, title, buffersize):
    data = ''
    data = data + 'DeletePath\n'
    data = data + user_id + '\n'
    data = data + title + '\n'
    
    sock.sendall(data.encode('utf-8')) 
    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8').split()

    if recv_data[1] == 'True':
        # debug message
        # print("Success!")
        return 1    
    else:
        # debug message
        # print("Failed!")
        return 0 

def download(sock, title, buffersize):
    data = ''
    data = data + 'GetLastPage\n'
    data = data + title + '\n'

    sock.sendall(data.encode('utf-8'))  
    recv_data = sock.recv(buffersize)
    recv_data = recv_data.decode('utf-8').split()

    if recv_data[1] == 'True':
        # debug message
        print("Found!")
    else:
        # debug message
        print("Not found!")
        return

    last_page = int(recv_data[2])
    # debug message
    print(last_page)

    novel = ''
    for i in range(1, last_page + 1):
        data = ''
        data = data + 'GetContent\n' 
        data = data + title + '\n'
        data = data + str(i) + '\n'

        sock.sendall(data.encode('utf-8')) 
        recv_data = sock.recv(buffersize)
        recv_data = recv_data.decode('utf-8')

        novel = novel + recv_data[40:]

    return novel