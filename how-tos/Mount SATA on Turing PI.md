# Mount a SATA Drive on Turing Pi 2 with Raspberry PI Compute Modules

## 1. Verify Drive

```
lsblk
```

Responds with
```
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda           8:0    0  1.8T  0 disk
mmcblk0     179:0    0 29.7G  0 disk 
├─mmcblk0p1 179:1    0  256M  0 part /boot
└─mmcblk0p2 179:2    0 29.5G  0 part /
```

Notice my SSD is named `sda` in this case and has no `MOUNTPOINT`. This is what we're going to change.

## 2. Format Drive
**This will wipe your drive completely, make sure you know this!**

```
sudo mkfs.ext4 /dev/sda
```
Replace `sda` in `/dev/sda` to the name of the drive you want to format so we can mount it

## 3. Make mounting destination

```
mkdir -p /media/ssd-1
```

## 4. Mount the drive

```
sudo mount /dev/sda /media/ssd-1
```
Remember that:
- `/dev/sda` is the location of my drive that's named `sda` found after we ran the `lsblk` command
- `/media/ssd-1` is the destination I created for this drive. You can mount it anwyhere you choose but `/media/` is one of the most common.


## 5. Verify again
```
lsblk
```

Responds with
```
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda           8:0    0  1.8T  0 disk /media/ssd-1
mmcblk0     179:0    0 29.7G  0 disk 
├─mmcblk0p1 179:1    0  256M  0 part /boot
└─mmcblk0p2 179:2    0 29.5G  0 part /
```

### Additional notes
Some posts mentioned installing `nfs-common` (`sudo apt install nfs-common -y`) will ensure the above works.
