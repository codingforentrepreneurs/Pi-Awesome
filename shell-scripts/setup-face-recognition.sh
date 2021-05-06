#!/bin/bash

# PiCamera, dlib, face recognition compiler and installer script
#
# This script is specifically created for Raspbian http://www.raspbian.org
# and Raspberry Pi http://www.raspberrypi.org but should work over any
# Debian-based distribution

# Created and mantained by Justin Mitchel
# Please send any feedback or comments to https://github.com/codingforentrepreneurs
# Updated for dlib by Davis E. King
# dlib repo: https://github.com/davisking/dlib
# Updated for face_recognition 1.2.1 by Adam Geitgey
# face_recognition repo: https://github.com/ageitgey/face_recognition

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 



if [ "$(whoami)" != "root" ]; then
    echo "Sorry, this script must be executed with sudo or as root"
    exit 1
fi



echo
echo "----------------"
echo "Updating sources"
echo "----------------"
echo


apt-get update
apt-get upgrade


echo
echo "-----------------------"
echo "Installing dependencies"
echo "-----------------------"
echo


apt-get install -y build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-pip \
    zip



apt-get clean

echo
echo "-----------------------"
echo "Installing PiCamera"
echo "-----------------------"
echo

apt-get install -y python3-picamera
pip3 install --upgrade picamera[array]


echo
echo "-----------------------"
echo "Temp resize of memory swapfile"
echo "-----------------------"
echo

sed -i -e 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile stop
/etc/init.d/dphys-swapfile start



echo
echo "-----------------------"
echo "Install dlib"
echo "-----------------------"
echo


mkdir -p /dlib
git clone -b 'v19.6' --single-branch https://github.com/davisking/dlib.git /dlib/
cd /dlib
python3 setup.py install --compiler-flags "-mfpu=neon"




echo
echo "-----------------------"
echo "Install face recognition"
echo "-----------------------"
echo


pip3 install face_recognition



echo
echo "-----------------------"
echo "Revert memory swapfile"
echo "-----------------------"
echo
sed -i -e 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile stop
/etc/init.d/dphys-swapfile start



echo
echo "-----------------------"
echo "Testing face recognition code examples"
echo "-----------------------"
echo

cd ~/
mkdir face-rec-examples && cd face-rec-examples
git clone --single-branch https://github.com/ageitgey/face_recognition.git .
cd ./examples
python3 facerec_on_raspberry_pi.py