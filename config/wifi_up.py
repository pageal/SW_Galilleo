import os
import time

time.sleep(5)
os.system("rfkill unblock all")
time.sleep(5)
os.system("ifup wlp0s20f3u1")

