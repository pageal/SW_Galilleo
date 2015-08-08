import os
import time

time.sleep(10)
os.system("rfkill unblock 0")
time.sleep(10)
os.system("ifup wlp0s20f3u1")
