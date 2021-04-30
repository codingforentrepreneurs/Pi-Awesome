# Get your IP Address or Hostname

> Are you looking to find devices on network with [macOS](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/List%20Network%20Devices%20on%20macOS%20and%20Linux%20with%20nmap.md), [linux](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/List%20Network%20Devices%20on%20macOS%20and%20Linux%20with%20nmap.md), or [windows](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/List%20Network%20Devices%20on%20macOS%20and%20Linux%20with%20nmap.md)?

### macOS
In *terminal* run:
```
HOST_IP=$(ipconfig getifaddr en0)
echo $HOST_IP
```
Verify with:
```
echo $HOST_IP
```


### Linux / Raspberry Pi OS
**Option 1**
In *terminal* run:
```
HOST_IP1=$(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
echo $HOST_IP1
```
Verify with:
```
echo $HOST_IP1
```


**Option 2**

In *terminal* run:
```
HOST_IP2=$(hostname  -I | cut -f1 -d' ')
```
Verify with:
```
echo $HOST_IP2
```


### Windows

In *powershell* run:
```
$env:HostIP = (
    Get-NetIPConfiguration |
    Where-Object {
        $_.IPv4DefaultGateway -ne $null -and
        $_.NetAdapter.Status -ne "Disconnected"
    }
).IPv4Address.IPAddress
```

Verify with:
```
$env:HostIP
```
