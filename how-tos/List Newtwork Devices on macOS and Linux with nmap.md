# List Network Devices on macOS on Linux with `nmap`

### 1. Install nmap

#### on macOS
Install nmap via [homebrew](https://brew.sh)
```
brew install nmap
```

#### on Linux
```
sudo apt install nmap -y
```


### 2. Get your network IP Address

#### on macOS
```
IP_ADD=$(ipconfig getifaddr en0)
```
> Run `echo $IP_ADD` to see the result. Mine is `192.168.86.20`


#### on Linux
```
IP_ADD=$(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
```


### 3. Use `nmap` to find other hosts/devices on your network


```
TARGET_HOST=raspberry
nmap -sn $IP_ADD/24 | grep "${TARGET_HOST}"
```
> `grep` will perform a search on the results of `nmap -sn $IP_ADD/24`

The above command (in my case) maps to `nmap -sn 192.168.86.20/24 | grep "raspberry"`. If you need to manually execute commands, you can do so.