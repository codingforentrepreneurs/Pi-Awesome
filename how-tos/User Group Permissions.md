# User Group Permissions
Use this as a general reference to setting up user groups for your various app / processes on your Raspberry Pi. 

> **If you find errors, please submit a pull request / issue so we can solve this. Permissions are tightly coupled with security and we want great security!**


Below I'll be using the following:
- Group `www-data`
- User `pi`

**Create group**
```
sudo groupadd www-data
```

**Add user to group**
```
sudo usermod -a -G www-data pi
```
> Remove user from group `sudo gpasswd -d pi www-data`

**View users in group**
```
grep www-data /etc/group
```

**Change folder ownership**
```
sudo chgrp -R www-data /var/www/
```

**Add (`+`) permssion to make files in folder readable (`r`), writable (`w`), and excutable (`x`) for the `group`**
```
sudo chmod -R g+rwxs /var/www/
```

Now all users in the group `www-data` have read, write, and execute access to everything within `/var/www/`

Let's check:

**Review Folder Ownership**
```
ls -al /var | grep www
```

**Reboot & Test**

```
sudo Reboot
```

```
touch /var/www/deleteme
rm /var/www/deleteme
```
No permission errors? Nice.

Permission errors? Perhaps you need to run it again or run `sudo reboot` (if you didn't)
