from threading import Thread
import socketserver
import logging
import re
import time


from flgproc import conf as config


def parse_data(data):
    if not re.fullmatch(config.FLAG_PATTERN, data):
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
    def write_text(self, text, end="\n", encoding="utf-8"):
        self.wfile.write("{text}{end}".format(text=text, end=end).encode(encoding))

    def handle(self):
        try:
            self.write_text("Flag submission enterprise service\nCopyright (c) 1970-2014 Chaos Inc.")
            while True:
                data = self.rfile.readline().strip().decode("utf8")
                if len(data) == 0:
                    self.write_text("bye")
                    return
                (ok, answer) = parse_data(data)
                self.write_text(answer)
                if ok:
                    pass
        except BrokenPipeError:
            return


class InputServer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.server = InputTCPServer(('', config.SUBMIT_SERVER_PORT), InputTcpHandler)

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