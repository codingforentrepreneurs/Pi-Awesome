# Upgrade Docker on a Raspberry Pi.
Docker needs to be updated from time to time. This guide is how you do it *assuming* you have docker installed via [Hypriot](https://blog.hypriot.com/) and/or the `https://get.docker.com` setup script (like what we did [here](https://www.piawesome.com/how-tos/Docker%20%26%20Docker%20Compose%20on%20Raspberry%20Pi))


### Are you impatient and didn't let things finish? Run this first
```
sudo dpkg --configure -a
```

### Upgrading your system and packages is the way to go.
```
sudo apt update -y && sudo apt upgrade -y && sudo apt dist-upgrade -y && sudo apt full-upgrade -y
```
This should complete the upgrade of Docker but I was having issues building images on Hypriot so we need to install `backports` & `libseccomp2`



### Docker Building Issues on Hypriot? 
Installing `backports` & `libseccomp2` solved my installation issues.

___Update your keys__
```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138
```

___Update your sources__
```
echo "deb http://deb.debian.org/debian buster-backports main" | sudo tee -a /etc/apt/sources.list.d/buster-backports.list
```

__Update apt__
```
sudo apt update
```

__Install backports__
```
sudo apt install -t buster-backports libseccomp2
```
