import random
import time

from flgproc.collector.demo import inpython_collector
from flgproc.exceptions import DuplicateFlagException, MalformedFlagException

flag_src = list("0123456789abcdef0123456789abcde")

""" submitting some flags into the processing queue """
for x in range(25):
    random.shuffle(flag_src)
    flag = ''.join(flag_src) + '='
    print("submitting flag: {0}".format(flag))
    inpython_collector(flag, service="demo", team=x)

time.sleep(2)
flag = ''.join(flag_src) + '='
print("resubmitting flag: {0} for duplicate check".format(flag))
try:
    inpython_collector(flag, service="duplicateFlagDemo", team=0)
except DuplicateFlagException:
    print("Exception was successfully raised!")
else:
    print("ERROR: No exception thrown!")

print("submitting invalid flag")
try:
    inpython_collector(flag[:15], service="invalidFlagDemo", team=23)
except MalformedFlagException:
    print("Exception was successfully raised!")
else:
    print("ERROR: No exception thrown!")