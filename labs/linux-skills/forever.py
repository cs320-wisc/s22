import time, signal

def ignore(*args):
    print("hahaha, good try")

signal.signal(signal.SIGINT, ignore)
signal.signal(signal.SIGTERM, ignore)

try:
    while True:
        count = 0
        while int(time.time()) % 2 == 0:
            count += 1
        print("running")
        time.sleep(1)
except:
    pass
