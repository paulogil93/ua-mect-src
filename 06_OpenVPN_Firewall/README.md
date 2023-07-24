# VPN Firewall Guide

## FW1

### Configure IPv4 addresses and gateways

```bash
set system host-name FW1
set interfaces ethernet eth0 address 200.1.1.1/24
set interfaces ethernet eth1 address 192.1.1.1/24
set interfaces ethernet eth2 address 10.1.1.1/24
set protocols static route 10.8.0.0/24 next-hop 192.1.1.100
commit
save
```

### Configure flow control rules

```bash
set zone-policy zone OUTSIDE description "Outside (Internet)"
set zone-policy zone OUTSIDE interface eth0

set zone-policy zone DMZ description "DMZ"
set zone-policy zone DMZ interface eth1

set zone-policy zone INSIDE description "Inside (Internal Network)"
set zone-policy zone INSIDE interface eth2

set firewall name FROM-INSIDE-TO-DMZ rule 10 description "Accept Established-Related Connections"
set firewall name FROM-INSIDE-TO-DMZ rule 10 action accept
set firewall name FROM-INSIDE-TO-DMZ rule 10 state established enable
set firewall name FROM-INSIDE-TO-DMZ rule 10 state related enable
set firewall name FROM-INSIDE-TO-DMZ rule 10 destination address 10.8.0.0/24

set firewall name FROM-DMZ-TO-INSIDE rule 10 description "Allow remote users to access internal network"
set firewall name FROM-DMZ-TO-INSIDE rule 10 action accept
set firewall name FROM-DMZ-TO-INSIDE rule 10 protocol all
set firewall name FROM-DMZ-TO-INSIDE rule 10 source address 10.8.0.0/24
set firewall name FROM-DMZ-TO-INSIDE rule 10 destination address 10.1.1.0/24

set firewall name FROM-DMZ-TO-OUTSIDE rule 10 description "Accept Established-Related Connections"
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 action accept
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 state established enable
set firewall name FROM-DMZ-TO-OUTSIDE rule 10 state related enable

set firewall name FROM-OUTSIDE-TO-DMZ rule 20 description "Accept OpenVPN traffic - UDP port 1194"
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 action accept
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 protocol udp
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 destination address 192.1.1.100
set firewall name FROM-OUTSIDE-TO-DMZ rule 20 destination port 1194

set firewall name FROM-OUTSIDE-TO-INSIDE rule 10 description "Accept Established-Related Connections"
set firewall name FROM-OUTSIDE-TO-INSIDE rule 10 action accept
set firewall name FROM-OUTSIDE-TO-INSIDE rule 10 state established enable
set firewall name FROM-OUTSIDE-TO-INSIDE rule 10 state related enable

set zone-policy zone INSIDE from OUTSIDE firewall name FROM-OUTSIDE-TO-INSIDE
set zone-policy zone DMZ from INSIDE firewall name FROM-INSIDE-TO-DMZ
set zone-policy zone INSIDE from DMZ firewall name FROM-DMZ-TO-INSIDE
set zone-policy zone DMZ from OUTSIDE firewall name FROM-OUTSIDE-TO-DMZ
set zone-policy zone OUTSIDE from DMZ firewall name FROM-DMZ-TO-OUTSIDE
```

## OpenVPN Server

### Create the server and client keys/certificates

```bash
sudo su
cd /etc/openvpn
cp -r /usr/share/easy-rsa .
cd easy-rsa

./easyrsa init-pki
./easyrsa build-ca
./easyrsa build-server-full server
./easyrsa build-client-full client1
./easyrsa gen-dh

cd ../server
cp ../easy-rsa/pki/ca.crt .
cp ../easy-rsa/pki/dh.pem .
cp ../easy-rsa/pki/issued/server.crt .
cp ../easy-rsa/pki/private/server.key .

cp ../easy-rsa/pki/issued/client1.crt /home/labcom/
cp ../easy-rsa/pki/private/client1.key /home/labcom/
cp ../easy-rsa/pki/ca.crt /home/labcom/
chown labcom:labcom /home/labcom/*
```

### Active the OpenVPN IPv4 routing

> Uncomment the line "net.ipv4.ip_forward = 1" in the file **/etc/sysctl.conf**

```bash
sudo sysctl -p
```
### OpenVPN server configuration

> Create/use the OpenVPN server configuration file (server.conf in directory /etc/openvpn) with the following contents:

```bash
port 1194
proto udp
dev tun
ca /etc/openvpn/server/ca.crt
cert /etc/openvpn/server/server.crt
key /etc/openvpn/server/server.key
dh /etc/openvpn/server/dh.pem
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "redirect-gateway def1 bypass-dhcp"
keepalive 10 120
comp-lzo
user nobody
group nogroup
persist-key
persist-tun
status openvpn-status.log
verb 3
```