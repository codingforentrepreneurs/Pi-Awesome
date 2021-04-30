# Activate an [Nginx](https://www.nginx.com/) Web Server on a Pi (or any Linux)


### 1. SSH into your host:
```
ssh pi@raspberrypi
```


### 2. Install Nginx

```
sudo apt update -y
sudo apt install nginx -y
```
> `-y` is a flag to accept the additional data sizes that come from the installation.

> *Optional* Are you using an `ufw` firewall? Enable *nginx* with: `sudo ufw allow 'Nginx Full'`


### 3. Open Browser with Host IP / Hostname

In step 1, I used `pi@raspberrypi` which means my hostname is `raspberrypi`. 


Let's get the IP ([reference](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Get%20IP%20Address%20or%20Hostname.md)):

**Option 1**
```
HOST_IP1=$(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
echo $HOST_IP1
```

**Option 2**

```
HOST_IP=$(hostname  -I | cut -f1 -d' ')
echo $HOST_IP
```

Now that we have `nginx` installend & our `host ip`, let's open our browser:

```
http://raspberrypi
```
or
```
http://192.168.86.24
```

> Do you have the wrong IP Address? Does the page never load? List list other devices on your newtork with `namp` on [mac](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/List%20Network%20Devices%20on%20macOS%20and%20Linux%20with%20nmap.md), [linux](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/List%20Network%20Devices%20on%20macOS%20and%20Linux%20with%20nmap.md), or [windows](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/List%20Network%20Devices%20on%20Windows%20with%20nmap.md). Listing the devices might help you find the correct IP address.



### 4. Review nginx default configuration

```
cat /etc/nginx/sites-enabled/default
```
> The actual source is linked from `/etc/nginx/sites-available`


### 5. Review the default nginx html page:

```
cat /var/www/html/*.html
```
> The actual source is `/var/www/html/index.nginx-debian.html`



### 6. Did you change anything in `nginx`?

```
sudo systemctl daemon-reload
```

```
sudo systemctl reload nginx
```
> Using `reload` will not stop nginx. Using `stop` and then `start` will. So will `restart`.



### 7. Next steps

Now you're ready to learn more about nginx and using it for: 
- Load Balancing
- Reverse Proxy
- API Gateway

And more.
