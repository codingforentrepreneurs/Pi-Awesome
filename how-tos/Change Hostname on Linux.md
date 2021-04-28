## Change Hostname on Linux
Test on Rasbian OS but should work on other linux distros too.
**1. Edit `/etc/hostname`**
```
sudo nano /etc/hostname
```
Change `raspberrypi` to `yourchoice`

**2. Edit `/etc/hosts`**
```
sudo nano /etc/hosts
```
Replace: 
```
127.0.1.1       raspberrypi
```
with
```
127.0.1.1       yourchoice
```

**3. Reboot**
```
sudo reboot
```

## Using Hypriot OS

#### Before *first* boot.
Right after you flash hypriot on a microsd, reinsert the card into your computer, and edit the `user-data` file within that drive.
```
cat /Volumes/HypriotOS/user-data
```
This is the default HypriotOS user data. The *only* time edits make a difference is before the *first boot*.


#### After *first* boot

```
sudo nano /etc/cloud/cloud.cfg
```
change `preserve_hostname` to `true`

Now use the same steps as `Change Hostname on Linux` with `/etc/hostname` and `/etc/hosts` and `reboot`


