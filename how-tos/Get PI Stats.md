# Get Raspberry Pi Stats
Various commands to get stats on your Raspberry PI.


### CPU Information
**Command**
```
lscpu
```

** Example Results**
```
Architecture:        armv7l
Byte Order:          Little Endian
CPU(s):              4
On-line CPU(s) list: 0-3
Thread(s) per core:  1
Core(s) per socket:  4
Socket(s):           1
Vendor ID:           ARM
Model:               3
Model name:          Cortex-A72
Stepping:            r0p3
CPU max MHz:         1500.0000
CPU min MHz:         600.0000
BogoMIPS:            108.00
Flags:               half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32
```
**Using python**
```
import subprocess
cli_cmd = "lscpu"
output = subprocess.check_output(cli_cmd.split()).decode()
unzipped = [ [y.strip() for y in x.split(":")] for x in output.split('\n') if x]
keys = [x[0] for x in unzipped if x]
values = [x[1] for x in unzipped if x]
data = dict(zip(keys, values))
print(data)
```

### Memory Information

#### Overview (quick)
**Command**
```
free
```
> use `free -h` for human readable response

**Example Results**
```
              total        used        free      shared  buff/cache   available
Mem:        8208420      136356     7842076       16796      229988     7840268
Swap:             0           0           0
```


#### Overview (Detail)
```
cat /proc/meminfo
```
To narrow results use `grep` such as:

**Command**
```
grep MemTotal /proc/meminfo
```
**Example Results**
```
MemTotal:        8208420 kB
```
or


**Command**
```
grep MemFree /proc/meminfo
```
**Example Results**
```
MemFree:         7842052 kB
```


**Using python**
```
import subprocess
cli_cmd = "cat /proc/meminfo"
output = subprocess.check_output(cli_cmd.split()).decode()
unzipped = [ [y.strip() for y in x.split(":")] for x in output.split('\n') if x]
keys = [x[0] for x in unzipped if x]
values = [x[1] for x in unzipped if x]
data = dict(zip(keys, values))
print(data)
```




### Tempature


#### CPU Temp
**Command**
```
CPU_TEMP=$(</sys/class/thermal/thermal_zone0/temp)
echo "$((CPU_TEMP/1000)) c"
```
> You can also use `vcgencmd measure_temp`
**Example Results**
```
temp=46.0'C
```

**Using Python**
```python
import subprocess
cli_cmd = "cat /sys/class/thermal/thermal_zone0/temp"
cpu_temp = subprocess.check_output(cli_cmd.split()).decode()
cpu_temp = int(cpu_temp) / 1000
print(cpu_temp, 'c')
```


#### GPU Temp
**Command**
```
/opt/vc/bin/vcgencmd measure_temp
```
> You can also use `vcgencmd measure_temp`
**Example Results**
```
temp=46.0'C
```


**Using Python**
```python
import subprocess
import re
cli_cmd = "/opt/vc/bin/vcgencmd measure_temp"
gpu_temp = subprocess.check_output(cli_cmd.split()).decode()
matches = re.findall(r"(?P<temp>\d+\.\d+)", gpu_temp)
print(matches[0], 'c')
```