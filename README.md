# [Pi Awesome](https://www.piawesome.com)

References and guides to using & setting up a raspberry pi for your projects.
### Resources:
- [Github Repo](https://github.com/codingforentrepreneurs/Pi-Awesome)
- [Website](https://www.piawesome.com)
> Find errors? Please submit an [issue](https://github.com/codingforentrepreneurs/Pi-Awesome/issues/new) or [pull request](https://github.com/codingforentrepreneurs/Pi-Awesome/pulls).

### Courses
- [Pi Server](https://cfe.sh/projects/pi-server)
- [Pi Ansible](https://cfe.sh/projects/pi-ansible)




### [How-Tos](/how-tos)
- [List Network Devices on macOS and Linux with nmap](/how-tos/List%20Network%20Devices%20on%20macOS%20and%20Linux%20with%20nmap.md)

- [Mount SATA on Turing PI](/how-tos/Mount%20SATA%20on%20Turing%20PI.md)

- [Docker & Docker Compose on Raspberry Pi](/how-tos/Docker%20%26%20Docker%20Compose%20on%20Raspberry%20Pi.md)

- [Get PI Stats](/how-tos/Get%20PI%20Stats.md)

- [Gunicorn & Supervisor](/how-tos/Gunicorn%20%26%20Supervisor.md)

- [Create a Minimal Web Application with Nginx, Python, Flask & Raspberry Pi](/how-tos/Create%20a%20Minimal%20Web%20Application%20with%20Nginx%2C%20Python%2C%20Flask%20%26%20Raspberry%20Pi.md)

- [Graceful-ish Updates of A Docker Compose Service via Git](/how-tos/Graceful-ish%20Updates%20of%20A%20Docker%20Compose%20Service%20via%20Git.md)

- [Flash Hypriot as your Pi OS](/how-tos/Flash%20Hypriot%20as%20your%20Pi%20OS.md)

- [Get IP Address or Hostname](/how-tos/Get%20IP%20Address%20or%20Hostname.md)

- [SSH to Host without Password](/how-tos/SSH%20to%20Host%20without%20Password.md)

- [Supervisor as a Background Service Manager](/how-tos/Supervisor%20as%20a%20Background%20Service%20Manager.md)

- [Setup Git & Version Control on your Pi Server](/how-tos/Setup%20Git%20%26%20Version%20Control%20on%20your%20Pi%20Server.md)

- [Mange Pi with Ansible](/how-tos/Mange%20Pi%20with%20Ansible.md)

- [Add New User on Pi or Linux](/how-tos/Add%20New%20User%20on%20Pi%20or%20Linux.md)

- [Change Hostname on Linux](/how-tos/Change%20Hostname%20on%20Linux.md)

- [Upgrade Docker](/how-tos/Upgrade%20Docker.md)

- [List Network Devices on Windows with nmap](/how-tos/List%20Network%20Devices%20on%20Windows%20with%20nmap.md)

- [Nginx Load Balancing & Backup Service in Docker Compose](/how-tos/Nginx%20Load%20Balancing%20%26%20Backup%20Service%20in%20Docker%20Compose.md)

- [Activate an Nginx  Web Server on a Raspberry Pi or any Linux](/how-tos/Activate%20an%20Nginx%20%20Web%20Server%20on%20a%20Raspberry%20Pi%20or%20any%20Linux.md)

- [User Group Permissions](/how-tos/User%20Group%20Permissions.md)




## Shell scripts

**Under construction**

These setup scripts are designed and tested on [Raspbian](http://www.raspbian.org); other systems may not work correctly. 

Find errors? Please submit an [issue](https://github.com/codingforentrepreneurs/Pi-Awesome/issues/new) or [pull request](https://github.com/codingforentrepreneurs/Pi-Awesome/pulls).

### `gphoto2-updater.sh`
[Download](shell-scripts/gphoto2-updater.sh) | [Raw](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/shell-scripts/gphoto2-updater.sh)

gPhoto2 is a tool to control digital cameras with code and a USB connection. [Supported Cameras](http://www.gphoto.org/doc/remote/).



```
curl -sSL https://www.piawesome.com/shell-scripts/gphoto2-updater.sh | sudo sh 
```
Or
```
curl https://www.piawesome.com/shell-scripts/gphoto2-updater.sh -O gphoto2-updater.sh
chmod +x gphoto2-updater.sh
sh gphoto2-updater.sh
```

### `setup-face-recognition.sh`
[Download](shell-scripts/setup-face-recognition.sh) | [Raw](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/shell-scripts/setup-face-recognition.sh)


```
curl -sSL https://www.piawesome.com/shell-scripts/setup-face-recognition.sh | sudo sh 
```
Or
```
curl https://www.piawesome.com/shell-scripts/setup-face-recognition.sh -O setup-face-recognition.sh
chmod +x setup-face-recognition.sh
sh setup-face-recognition.sh
```

### `setup-opencv.sh`
[Download](shell-scripts/setup-opencv.sh) | [Raw](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/shell-scripts/setup-opencv.sh)

OpenCV is a great tool for performing computer vision analysis on your Pi.



```
curl -sSL https://www.piawesome.com/shell-scripts/setup-opencv.sh | sudo sh 
```
Or
```
curl https://www.piawesome.com/shell-scripts/setup-opencv.sh -O setup-opencv.sh
chmod +x setup-opencv.sh
sh setup-opencv.sh
```

