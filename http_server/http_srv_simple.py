import time
import threading
import os
import glob
import commands
import re
import struct
import ctypes
import socket
import SocketServer
import BaseHTTPServer

the_report_period = 10
timezone = 7200
http_port = 8100

PAGE_CHARGERS = \
"""
<!DOCTYPE html>
<html>
<body>
    <h1> Haifa local time: {} </h1>
    <h1> Nearby chargers [count={}]: </h1>
    <h3> - Name: {} Charge level: {} </h3>
</body>
</html>
"""

globals()["g_count_of_chargers"] = 0
globals()["g_count _of_power_meters"] = 0.0

class temperature_resolver(object):
    def __init__(self):
        #initialize device
        os.system("modprobe w1-gpio")
        os.system("modprobe w1-therm")
        self.dev_dir = '/sys/bus/w1/devices/'

        try:
            self.ds18b20_folder = glob.glob(self.dev_dir + '28*')[0]
            self.ds18b20_data_file = self.ds18b20_folder + '/w1_slave'
        except:
            print("temperature_resolver initialization failed")
            return

    def temp_read(self):
        try:
            f = open(self.ds18b20_data_file, "r")
            lines = f.readlines()
            f.close()
            t_pos = lines[1].find('t=')
            if(t_pos != -1):
                self.raw_temp_str = lines[1][t_pos+2:]
                self.temp_c = float(self.raw_temp_str)/1000.0
                self.temp_f = self.temp_c * 9.0/5.0 + 32.0
        except:
            self.temp_c = 0.0
            self.temp_f = 0.0
        return self.temp_c, self.temp_f

class direction_resolver(object):
    def __init__(self):
        self.north = 1.29
        self.ne1 = 1.34
        self.ne2 = 0.37
        self.east = 0.59
        self.se1 = 0.92
        self.se2 = 1.13
        self.south = 1.65
        self.sw1 = 1.57
        self.sw2 = 1.99
        self.west = 2.01
        self.nw1 =  1.80
        self.nw2 =  1.96

        self._amp_to_dir_name = {self.north:"N", self.ne1:"NE", self.ne2:"NE",
                            self.east:"E", self.se1:"SE", self.se2:"SE",
                            self.south :"S",  self.sw1:"SW", self.sw2:"SW",
                            self.west:"W", self.nw1:"NW", self.nw2:"NW"}

    def resolve(self, sig_amp):
        sig_amp_str = "%0.2f"%sig_amp
        try:
            dir_name = self._amp_to_dir_name[float(sig_amp_str)]
            return dir_name
        except Exception:
            return " "

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    _preview = False
    _camera = None
    stop_streaming = False
    _dr = direction_resolver()

    def requestline(self):
        return 1

    def request_version(self):
        return 'HTTP/5.0'

    def handle(self):

        print("handle request request")
        the_page = PAGE_CHARGERS.format(time.ctime(int(time.time()+timezone)),
                    globals()["g_count_of_chargers"],
                    "test", "[|||||  ]")

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(the_page)))
        self.send_header("refresh", str(the_report_period))
        self.request.send(the_page)
        self.end_headers()



class NETTYPE:
    LAN = 1
    WLAN = 2
    CELL = 3

class DataServerHTTP :
    _stop_server = False
    _main_thread = None
    _nettype = NETTYPE.LAN

    def GetLocalIP(self):
        ifconfig_cmd = commands.getoutput("ifconfig")
        patt = re.compile(r'inet\s*\w*\S*:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        addr_list = patt.findall(ifconfig_cmd)
        for addr in addr_list:
            if addr == "127.0.0.1":
                continue
            if(self._nettype == NETTYPE.CELL):
                if(addr.find("192.168.") == 0):
                    continue
            if(addr.find('.')>0):
                return addr
        return "127.0.0.1"


    def _HTTPThread(self):
        IP = self.GetLocalIP()
        print("http server started at " + IP + ":" + str(http_port))
        while (self._stop_server == False):
            self._http_srv = BaseHTTPServer.HTTPServer((IP, http_port),HTTPHandler)
            self._http_srv.rbufsize = -1
            self._http_srv.wbufsize = 100000000
            try:
                self._http_srv.handle_request()
            except Exception as e:
                pass
            self._http_srv.socket.close()
        print("http server finished")

    def start(self):
        self._main_thread = threading.Thread(target=self._HTTPThread)
        self._main_thread.start()

    def stop(self):
        self._stop_server=True
        self._http_srv.socket.close()


class energy_server():
    _thread = None
    _stop_requested = False

    _IPAddr = "127.0.0.1"
    _CtrlPort = 8300

    def GetLocalIP(self):
        ifconfig_cmd = commands.getoutput("ifconfig")
        patt = re.compile(r'inet\s*\w*\S*:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        addr_list = patt.findall(ifconfig_cmd)
        for addr in addr_list:
            if addr == "127.0.0.1":
                continue
##            if(self._nettype == NETTYPE.CELL):
##                if(addr.find("192.168.") == 0):
##                    continue
            if(addr.find('.')>0):
                return addr
        return "127.0.0.1"

    def __init__(self, report_period = the_report_period):
        self._IPAddr = self.GetLocalIP()


    def start(self):
        self._stop_requested = False
        self._thread = threading.Thread(target=self._thread_method)
        self._thread.start()


    def _thread_method(self):
        print("energy_server thread started")

        last_voltage = 0
        while(self._stop_requested != True):
            time.sleep(0.01)
        print("energy_server thread finished")

    def stop(self):
        if(self._thread == None):
            return
        self._stop_requested = True
        if(self._thread.isAlive()):
            self._thread.join();
        self._thread = None

sm = energy_server()
sm.start()

srv = DataServerHTTP()
srv.start()
