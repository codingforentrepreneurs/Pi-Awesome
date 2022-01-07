# Configure PI User for Ansible


## 1. Create user [like in this guide](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Add%20New%20User%20on%20Pi%20or%20Linux.md)
```
sudo useradd -m justin
```

Add password:

```
sudo passwd justin
```


## 2. Add user to sudo group

```
sudo usermod -a -G sudo justin
```

Update `/etc/sudoers`

```
# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL
justin  ALL=(ALL:ALL) NOPASSWD:ALL
```
> Notice that I added `justin  ALL=(ALL:ALL) NOPASSWD:ALL` under than `%sudo`

## 3. Update hostname

```
sudo hostnamectl set-hostname node-xyz
```
> Change `node-xyz` to the name 

```
sudo nano /etc/hosts
```
Add

```
127.0.0.1  node-xyz
```

## 4. Reboot

```
sudo reboot
```

## 5. Add Local SSH Key to Authorized Keys (optional)
