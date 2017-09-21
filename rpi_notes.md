Getting RPI Zero W up and running:

Clear directions:
https://learn.adafruit.com/raspberry-pi-zero-creation/overview

Download the Linux image:
https://www.raspberrypi.org/downloads/raspbian/

Download the microsd card flasher:
https://etcher.io/

Enable ssh:
> touch boot/ssh
default user/pass: pi/raspberry

> vim boot/wpa_supplicant.conf

===
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    id_str="skynet"
    ssid="skynet"
    psk="password"
    scan_ssid=1
    proto=RSN
    key_mgmt=WPA-PSK
    pairwise=CCMP
    auth_alg=OPEN
}
===
http://weworkweplay.com/play/automatically-connect-a-raspberry-pi-to-a-wifi-network/

> ping raspberrypi.local
or
check router for ip address of rasperrypi

> ssh pi@raspberrypi.local
> passwd

========
AP SETUP

https://www.raspberrypi.org/forums/viewtopic.php?p=1204633&sid=246c7ea9634cf32b9c5ec81821e96930#p1204633
https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address
Deprecated: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md

> sudo apt-get update
> sudo apt-get dist-upgrade
> sudo apt-get install dnsmasq hostapd vim
> sudo systemctl stop dnsmasq
> sudo systemctl stop hostapd

-----------
/etc/dhcpcd.conf

interface wlan0
static ip_address=192.168.42.1/24
static routers=192.168.42.1
static domain_name_servers=8.8.8.8

-----------
/etc/dnsmasq.conf

interface=wlan0
domain-needed
bogus-priv
dhcp-range=192.168.42.2,192.168.42.21,24h

-----------
/etc/hostapd/hostapd.conf

interface=wlan0
driver=nl80211
ssid=HelloWorld
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=coolpassword
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

------------
/etc/default/hostapd

DAEMON_CONF="/etc/hostapd/hostapd.conf"

------------
/etc/wpa_supplicant/wpa_supplicant.conf

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1


> sudo service dnsmasq restart
> sudo service hostapd restart
> sudo service dhcpcd restart

# I had to restart
> sudo shutdown -r now


========
MOSQUITTO BROKER

> sudo apt-get install mosquitto

========
HELPFUL COMMANDS

> ip link
