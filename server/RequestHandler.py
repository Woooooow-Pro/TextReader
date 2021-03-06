import threading
import socket

from handlerfunc import ServerDispatchTable
 

class RequestHandler():
    def __init__(self):
        self.dispatch = ServerDispatchTable()

    def handler(self, sock):
        while True:
            rec_data = sock.recv(8 * 1024)
            rec_data = rec_data.decode('utf-8')

            # debug message
            thread_name = 'Client' + threading.current_thread().name
            print(thread_name)

            if len(rec_data) <= 0:
                print(f"Thread {thread_name} is closed")
                break

            data = rec_data.split()
            ret_data = self.dispatch.run(data[0], (data, ))

        
            sock.sendall(ret_data.encode('utf-8'))
        sock.close()

    # # test function
    # def test(self):
    #     a = 2333
    #     self.dispatch.run("test", (a,))