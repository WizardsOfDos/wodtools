import telnetlib
import logging

TEXT_PREAMBLE_SERVER = "Flag submission enterprise service\nCopyright (c) 1970-2014 Chaos Inc.\n"
TEXT_PREAMBLE_CLIENT = None
TEXT_FLAG_MSG = "{flag}\n"

ENCODING_SERVER = 'utf-8'


class TelnetSubmitter:

    def __init__(self, host, port, timeout=5, **team_context):
        self.logger = logging.getLogger(__name__)
        self._host = host
        self._port = port
        self._timeout = timeout
        self._telnet_client = None
        self._team_context = team_context

    def _init_client(self, force_reconnect=False):
        if force_reconnect:
            self._close()
        self._telnet_client = telnetlib.Telnet(host=self._host, port=self._port, timeout=self._timeout)
        self._telnet_client.read_until(TEXT_PREAMBLE_SERVER.encode(ENCODING_SERVER))
        if TEXT_PREAMBLE_CLIENT is not None:
            self._send(TEXT_PREAMBLE_CLIENT.format(**self._team_context))

    def _close(self):
        if self._telnet_client is not None and not self._telnet_client.eof:
            self._telnet_client.close()
        self._telnet_client = None

    def _send(self, msg):
        self._telnet_client.write(msg.encode(ENCODING_SERVER))

    def _ensure_initialized(self):
        if self._telnet_client is None:
            self._init_client()
        elif self._telnet_client.eof:
            self._init_client(True)

    def send_flag(self, flag, retries=3):
        try:
            self._ensure_initialized()
            self._telnet_client.read_eager()
            self._send(TEXT_FLAG_MSG.format(flag=flag, **TEAM_INFO))
            return self._telnet_client.read_some().decode(ENCODING_SERVER)
        except (OSError, EOFError) as er:
            if retries > 0:
                self._init_client(True)
                return self.send_flag(flag, retries-1)
            else:
                raise er


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    TEAM_INFO = {
        'team': 23,
    }
    DEMO_FLAGS = ("qrt3463ewetr",
                  "wfqa4tae5ta5EZe5aewrstwetwsadwe=",
                  "1337435qe5rzge4eRGFewrstwOIOIOI=",
                  "13374tae5ta5EZe5a4aewrstwetwdwe=",
                  "13374tae5ta5EZe5a4aewrstwetwdwe=",
    )

    submitter = TelnetSubmitter('127.0.0.1', 5001, **TEAM_INFO)

    for flag in DEMO_FLAGS:
        print("flag: {%s} => %s" % (flag, submitter.send_flag(flag)))

    submitter._close()
