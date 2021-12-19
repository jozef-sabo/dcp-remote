#!/bin/sh

mkdir -p ../build/"deb-dcp-remote"
cp -R deb_metadata/* ../build/"deb-dcp-remote"

mkdir -p ../build/"deb-dcp-remote"/etc/pam.d
cp ../src/configs/vsftpd_virtual ../build/"deb-dcp-remote"/etc/pam.d/

mkdir -p ../build/"deb-dcp-remote"/usr/lib/dcp-remote/.configs/
cp ../src/configs/vsftpd.conf ../build/"deb-dcp-remote"/usr/lib/dcp-remote/.configs/

mkdir -p ../build/"deb-dcp-remote"/etc/ufw/applications.d/
cp ../src/configs/dcp-remote ../build/"deb-dcp-remote"/etc/ufw/applications.d/dcp-remote

mkdir -p ../build/"deb-dcp-remote"/usr/bin/dcp-remote
cp ../src/bin/* ../build/"deb-dcp-remote"/usr/bin/dcp-remote/

sudo chown -R root:root ../build
sudo chmod -R 755 ../build
sudo dpkg-deb --build ../build/deb-dcp-remote ../build/dcp-remote.deb

name=$(whoami)
sudo chown -R "$name":"$name" ../build

sudo rm -R ../build/deb-dcp-remote
