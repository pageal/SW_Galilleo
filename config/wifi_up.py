import os
import time

time.sleep(10)
os.system("rfkill unblock all")
time.sleep(10)
os.system("/usr/sbin/wpa_supplicant -u -iwlp0s20f3u1 -c/etc/wpa_supplicant.conf &")
time.sleep(10)
os.system("ifup wlp0s20f3u1")

