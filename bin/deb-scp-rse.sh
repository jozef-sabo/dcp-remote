#!/bin/sh

mkdir -p ../build/"deb-dcp-rse"
cp -R deb_metadata/* ../build/"deb-dcp-rse"

mkdir -p ../build/"deb-dcp-rse"/etc/pam.d
cp ../src/configs/vsftpd_virtual ../build/"deb-dcp-rse"/etc/pam.d/

mkdir -p ../build/"deb-dcp-rse"/usr/share/applications/sabo.dcpomatic-remote-server-encoding
cp ../src/configs/vsftpd.conf ../build/"deb-dcp-rse"/usr/share/applications/sabo.dcpomatic-remote-server-encoding/

sudo chown -R root:root ../build
sudo chmod -R 755 ../build
sudo dpkg-deb --build ../build/deb-dcp-rse ../build/dcpomatic-remote-server-encoding.deb

name=$(whoami)
sudo chown -R "$name":"$name" ../build

sudo rm -R ../build/deb-dcp-rse
