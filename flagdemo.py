# Generate flags and send them to the flagserver

import random
import urllib.request
import time

FLAGSERVER_HOST = "localhost"
FLAGSERVER_PORT = 5000

flag_source = "0123456789abcdef"


def generate_flag(valid=False):
    if valid:
        flag = "1337"+''.join([random.choice(flag_source) for i in range(27)]) + '='
    else:
        flag = ''.join([random.choice(flag_source) for i in range(31)]) + '='
    return flag


def send_flags(flags, team, service):
    try:
        url = "http://{host}:{port}/flag?team={team}&service={service}"
        url = url.format(host=FLAGSERVER_HOST, port=FLAGSERVER_PORT, team=team, service=service)
        request = urllib.request.Request(url, data='\n'.join(flags).encode("utf8"))
        request.add_header("Content-Type", "text/plain")
        ans = urllib.request.urlopen(request)
        print(ans.read().decode('utf8'))
    except Exception as e:
        print(e)


def demo(numTeams):
    for i in range(50):
        for j in range(numTeams):
            flags = [generate_flag() for _ in range(random.randint(10,20))]
            send_flags(flags, j, "testService")
        time.sleep(10)


if __name__ == "__main__":
    demo(20)
