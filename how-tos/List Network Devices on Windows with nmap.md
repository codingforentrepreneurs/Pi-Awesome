# List Network Devices on Windows with `nmap`
Find devices on network with Windows

Open powershell and type the following commands

```
$env:HostIP = (
    Get-NetIPConfiguration |
    Where-Object {
        $_.IPv4DefaultGateway -ne $null -and
        $_.NetAdapter.Status -ne "Disconnected"
    }
).IPv4Address.IPAddress
```
Verify with 
```
$env:HostIP
```
> This number should also be listed in the results of `arp -a


Search using `nmap`

```
$env:PI_Name = "raspberry"
nmap -sP $env:HostIP/24 | Select-String $env:PI_Name
```

The `| Select-String $env:PI_Name` is optional but helps narrow our search to `raspberry` in this case.

The above command (in my case) maps to:
```
nmap -sP 192.168.86.24/24 | Select-String "raspberry"
```
So you can see the final result without environment variables.