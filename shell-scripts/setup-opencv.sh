#!/bin/bash

# OpenCV 3 compiler and installer script
#
# This script is specifically created for Raspbian http://www.raspbian.org
# and Raspberry Pi http://www.raspberrypi.org but should work over any
# Debian-based distribution
# Created and mantained by Justin Mitchel
# Please send any feedback or comments to https://github.com/jmitchel3
# Updated for OpenCV 3.4.0 by https://opencv.org

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

apt-get update -qq


echo
echo "----------------"
echo "Purging unneeded libraries"
echo "----------------"
echo
apt-get -y purge wolfram-engine
apt-get -y purge libreoffice*
apt-get -y clean
apt-get -y autoremove 




echo
echo "----------------"
echo "Update & Upgrade"
echo "----------------"
echo
apt-get -y update
apt-get -y upgrade


echo
echo "-----------------------"
echo "Installing dependencies"
echo "-----------------------"
echo

apt-get install -y build-essential cmake pkg-config 
apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
apt-get install -y libxvidcore-dev libx264-dev
apt-get install -y libgtk2.0-dev libgtk-3-dev

apt-get install -y libatlas-base-dev gfortran
apt-get install -y python2.7-dev python3-dev


echo
echo "-----------------------"
echo "Installing more dependencies"
echo "-----------------------"
echo
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.0.zip
unzip -o opencv.zip

wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.0.zip
unzip -o opencv_contrib.zip



echo
echo "-----------------------"
echo "Install Pip"
echo "-----------------------"
echo


cd ~
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
python3 get-pip.py


echo
echo "-----------------------"
echo "Begin Compile OpenCV"
echo "-----------------------"
echo
cd ~/opencv-3.4.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.0/modules \
    -D WITH_GPHOTO2=ON \
    -D BUILD_EXAMPLES=ON ..


echo
echo "-----------------------"
echo "Updaating Swap Space Size"
echo "to use all 4 cores."
echo "-----------------------"
echo

# replace CONF_SWAPSIZE from 100 to 1024 in the `/etc/dphys-swapfile` file.
sed -i -e 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile stop
/etc/init.d/dphys-swapfile start


echo
echo "-----------------------"
echo "Final OpenCV Compile"
echo "-----------------------"
echo

make -j4
make install
ldconfig



echo
echo "-----------------------"
echo "Reverting Swap Space Size"
echo "-----------------------"
echo

# replace CONF_SWAPSIZE from 100 to 1024 in the `/etc/dphys-swapfile` file.
sed -i -e 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
/etc/init.d/dphys-swapfile stop
/etc/init.d/dphys-swapfile start



echo
echo "-----------------------"
echo "Creating Dev Folder && OpenDLSR's Python3 Virtualenv"
echo "This virtualenv will have OpenCV installed by Default"
echo "-----------------------"
echo

cd ~/
mkdir Dev
cd Dev
python -m virtualenv -p python3 --system-site-packages opendslr
cd opendslr
source bin/activate
echo
echo "Do you see a version number or an error?"
python -c "import cv2; print(cv2.__version__)"
echo

deactivate
cd ~/


echo
echo "-----------------------"
echo
echo
echo "You're ready."
echo "Your virtualenv is waiting in ~/Dev/opendslr"
echo
echo
echo "-----------------------"
echo