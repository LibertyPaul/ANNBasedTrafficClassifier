#!/bin/sh

sudo tcpdump -i 'enp3s0' -w /tmp/ssh.cap -c 1000 'tcp port 22'
sudo tcpdump -i 'enp3s0' -w /tmp/ftp.cap -c 1000 'tcp port 21'
sudo tcpdump -i 'enp3s0' -w /tmp/http.cap -c 1000 'tcp port 80'

