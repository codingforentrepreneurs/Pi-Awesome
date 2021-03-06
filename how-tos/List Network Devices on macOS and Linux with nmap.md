# List Network Devices on macOS on Linux with `nmap`
Find devices on network with macOS or Linux. Looking for [Windows](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/List%20Network%20Devices%20on%20Windows%20with%20nmap.md)?


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
HOST_IP=$(ipconfig getifaddr en0)
```
> Run `echo $HOST_IP` to see the result. Mine is `192.168.86.20`


#### on Linux
```
HOST_IP=$(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
```


### 3. Use `nmap` to find other hosts/devices on your network


```
TARGET_HOST=raspberry
nmap -sP $HOST_IP/24 | grep "${TARGET_HOST}"
```
The `| grep "${TARGET_HOST}` is optional but helps narrow our search to `raspberry` in this case.

The above command (in my case) maps to:
```
nmap -sP 192.168.86.20/24 | grep "raspberry"
```
So you can see the final result without environment variables.


### 4. (Optional) Add shortcut to Bash Profile or Zshell Profile

macOS / zshell
```
sudo nano ~/.zshrc
```

Linux / bash

```
sudo nano ~/.bashrc
```

Add the following line:
```
alias devices='nmap -sP $(ipconfig getifaddr en0)/24'
```

Save and close. 


Run `source ~/.zshrc` / `source ~/.bashrc` or open a new terminal window.

```
devices
```
