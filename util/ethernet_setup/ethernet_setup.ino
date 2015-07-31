void setup() {
 system("telnetd -l /bin/sh");
 system("ifconfig eth0 192.168.1.200 netmask 255.255.255.0 up");
}

void loop() {
  // put your main code here, to run repeatedly:

}
