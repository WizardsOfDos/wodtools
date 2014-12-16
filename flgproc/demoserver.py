from threading import Thread
import socketserver
import logging
import re
import time

flag_pattern = "[a-zA-Z0-9]{31}="

def parse_data(data):
    if not re.fullmatch(flag_pattern, data):
        return False, "Wrong pattern"
    if data.startswith("1337"):
        return True, "Success!"
    return False, "Invalid Flag!"


class InputTCPServer(socketserver.ThreadingTCPServer):
    request_list = []
    def close_request(self, request):
        self.request_list.remove(request)
        super().close_request(request)

    def process_request(self, request, client_address):
        self.request_list.append(request)
        super().process_request(request, client_address)


class InputTcpHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            self.wfile.write("Flag submission enterprise service\nCopyright (c) 1970-2014 Chaos Inc.\n".encode("utf8"))
            while(True):
                data = self.rfile.readline().strip().decode("utf8")
                if len(data) == 0:
                    self.wfile.write("bye\n".encode("utf8"))
                    return
                (ok, answer) = parse_data(data)
                self.wfile.write((answer+"\n").encode("utf8"))
                if ok:
                    pass
        except BrokenPipeError:
            return


class InputServer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.server = InputTCPServer(('',50031), InputTcpHandler)

    def run(self):
        try:
            self.server.serve_forever()
        except Exception as e:
            logger = logging.getLogger("main")
            logger.exception(e)
            raise e

    def stop(self):
        self.server.shutdown()
        for request in self.server.request_list:
            request.shutdown(socketserver.socket.SHUT_RDWR)


if __name__ == "__main__":
    server = InputServer()
    server.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    server.stop()