# Flash Hypriot as your Raspberry Pi Operating System.

HypriotOS is a linux distro for the Raspberry Pi that focuses on using Docker. 


### 1. Download the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) (not the Raspberry Pi OS)

### 2. Download [hyriot os](https://blog.hypriot.com/downloads/)
- Hypriot is made to:
- Run on Raspberry Pi
- Run headless (ie no destkop)
- Run Docker
- Be 10-20x faster to flash than Raspberry Pi OS

### 3. Unzip hypriotos-rpi-vX.YY.Z.img.zip
Change `X.YY.Z` to the latest version, in my case it's `1.12.3`

### 4. Insert a microSD card* into your non-raspberry pi computer
*We are going to completely erase this card


### 5. Open Raspberry Pi Imager
__Under Operating System__
- Select Custom
- Navigate to your *unzipped* Hypriot OS (`hypriotos-rpi-vX.YY.Z.img` not `hypriotos-rpi-vX.YY.Z.img.zip`)
__Under Storage system__
- Select the microSD card you inserted in step 4
> When in doubt, do *not* just select anything. Eject your card, take note of available options on the Imager, insert card, select the new option.


### 6. Click `Write`
- Confirm warnings
- Wait about 2-10 minutes


### 7. Once complete, card will be ejected for you.

### 8. Re-insert card into your non-raspberry pi computer
### 9. Open up the contents of the mircoSD Card (should now be named `HypriotOS`)

###  10. Copy `user-data` to your non-raspberry pi computer and open in VSCode

`user-data` is just a `yaml` file.

### 11. Edit `user-data`.

The following items I tend to change:

- `hostname`
    - default is `black-pearl`
- `users.name`
    - default is `pirate`
- `users.gecos`
    - default is `Hypriot Pirate`
- `users.plain_text_passwd`
    - default is `hypriot`
- `users.ssh_authorized_keys`
    - This is an optional field, I add my public ssh key here.
- `timezone`
    - default is `America/Los_Angeles`
- `write_files.content.network.ssid`
    - default is `YOUR_WIFI_SSID`
- `write_files.content.network.psk`
    - default is `YOUR_WIFI_PASSWORD`

> `YOUR_WIFI_SSID` and `YOUR_WIFI_PASSWORD` are your wifi network name and wifi password respectively.

I recommend setting passwords using at least `plain_text_passwd`:

```
python3 -c "import secrets;print(secrets.token_urlsafe(32))"
```

Setting the `ssh_authorized_keys: ` will allow you to login without using a password. To get your ssh public key you can just:

__mac/Linux__
```
cat ~/.ssh/id_rsa.pub | pbcopy
```

__windows__
```
cat ~/.ssh/id_rsa.pub | type
```


Here's my working sample:
```yaml
#cloud-config
# vim: syntax=yaml
#

# Set your hostname here, the manage_etc_hosts will update the hosts file entries as well
hostname: tars-1
manage_etc_hosts: true

# You could modify this for your own user information
users:
  - name: cfe
    gecos: "CFE for Life"
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    groups: users,docker,video,input
    plain_text_passwd: qcxOIuSjAI1dKebYLwbzT7OciGNV5FpNe4Ij21BWRr0
    lock_passwd: false
    ssh_pwauth: true
    ssh_authorized_keys: 
        - ssh-rsa AAAAB3N... cfe@justins-mbp.lan
    chpasswd: { expire: false }

# # Set the locale of the system
locale: "en_US.UTF-8"

# # Set the timezone
# # Value of 'timezone' must exist in /usr/share/zoneinfo
timezone: "America/Los_Angeles"

# # Update apt packages on first boot
# package_update: true
# package_upgrade: true
# package_reboot_if_required: true
package_upgrade: false

# # Install any additional apt packages you need here
# packages:
#  - ntp

# # WiFi connect to HotSpot
# # - use `wpa_passphrase SSID PASSWORD` to encrypt the psk
write_files:
  - content: |
      allow-hotplug wlan0
      iface wlan0 inet dhcp
      wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
      iface default inet dhcp
    path: /etc/network/interfaces.d/wlan0
  - content: |
      country=de
      ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
      update_config=1
      network={
      ssid="WifiIsComing"
      psk="KingOfTheNorth"
      proto=RSN
      key_mgmt=WPA-PSK
      pairwise=CCMP
      auth_alg=OPEN
      }
    path: /etc/wpa_supplicant/wpa_supplicant.conf

# These commands will be ran once on first boot only
runcmd:
  # Pickup the hostname changes
  - 'systemctl restart avahi-daemon'
  # Activate WiFi interface
  - 'ifup wlan0'
```


### 12. Replace your local `user-data` with the microSD card's `user-data`

### 13. Eject microSD, insert into pi, and boot. Wait for initial boot. Restart the pi again to ensure the `user-data` (aka `cloud-init` config) changes take place from above.

> If you ever need to change `user-data` **after** you boot for the first time, you **must** reflash the OS and do steps 10-13 again.

### 14. To repeat on new raspberry pis, I recommend you change the `hostname` in `user-data` each time to something new. The reason I used `tars-1` is because my next few would be `tars-2`, `tars-3`, etc.

### 15. Use `grep` to find our new host ips:

__macOS__
```
nmap -sP "$(ipconfig getifaddr en0)/24" | grep "tars"
```
__linux__
```
nmap -sP "$(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')/24" | grep "tars"
```

__windows__ users use [this guide](https://www.piawesome.com/how-tos/List%20Network%20Devices%20on%20Windows%20with%20nmap)
