from tornado.websocket import WebSocketHandler
from tornado.web import Application
from tornado.ioloop import IOLoop,PeriodicCallback
from threading import Thread
import time
import Queue
import socket

queue = Queue.Queue()

class WebSocket_1(WebSocketHandler):
    waiters = set()

    def open(self):
        WebSocket_1.waiters.add(self)
        print("WebSocket opened")
        WebSocket_1.update_coords()

    def on_message(self, message):
        pass

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True

    @classmethod
    def update_coords( self ):
        global queue
        if not queue.empty():
            WebSocket_1.send_updates(queue.get())

    @classmethod
    def send_updates(cls, msg ):
        for waiter in cls.waiters:
            try:
                waiter.write_message( msg )
            except:
                pass
    

def thr_serv():
    global queue
    sock = socket.socket()
    sock.bind(('', 555))
    sock.listen(1)
    while 1:
        conn, addr = sock.accept()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                queue.put(data)
        conn.close()



if __name__ == "__main__":
    st = Thread( target = thr_serv )
    st.start()

    app = Application([
        (r"/ws", WebSocket_1)
    ])
    app.listen(55)
    io_loop = IOLoop.instance()
    PeriodicCallback( WebSocket_1.update_coords, 100.0, io_loop=io_loop ).start()
    io_loop.start()
