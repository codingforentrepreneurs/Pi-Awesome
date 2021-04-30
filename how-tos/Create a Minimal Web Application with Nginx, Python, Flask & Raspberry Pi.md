# Create a Minimal Web Application with Nginx, Python, Flask & Raspberry Pi


### SSH into the Pi
```
ssh pi@raspberry
```


### Install system dependancies
```
sudo apt install update
sudo apt install python3-venv  -y
```


### Designate app folder
```
cd ~/
mkdir app
cd app
```


### Create a Python Virtual Environment
```
python3 -m venv .
```


### Activate the Python Virtual Environment
```
source bin/activate
```


### Denote the Python being used (in the virtual environment)
```
which python
```


### Install our Python Web Application Framework (Flask) using Pip (in the virtual environment)
```
pip install flask
```


### Create our "Server" with `server.py`
> Note that `server.py` is a name I made up for this app. You can call it `welcome.py` or whatever you like; `server.py` makes sense for this app and for future devs to use it.

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8123)
```
> Note the values for `host` and `port` in this example. `host="0.0.0.0"` and `port=8123`. We need these for later.

### Run our Python Web application

```
/home/pi/app/bin/python /home/pi/app/server.py
```
- **`pi`** is my user
- **`/home/pi`** is my users' root. (A shortcut to this path is `cd ~/`)
- **`/home/pi/app/bin/python`** is what `which python` gave us from above
- **`/home/pi/app/server.py`** is the absolute to my `server.py` file I made above.



### Create a custom nginx config 

`/home/pi/app/nginx.conf`
```
upstream flaskapp {
    server localhost:8123;
}

server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
        location / {
                proxy_pass http://flaskapp;
                proxy_redirect off;
        }

}
```

- the `upstream` **`flaskapp`** name is used 2 times and is arbitary
- `server localhost:8123;` references the `host` and `port` values from the Flask app above.
- `"0.0.0.0"` *is* `localhost`
- `proxy_pass` references the `upstream` name and *not* the localhost.


### Replace default nginx configuration

```
sudo cp /home/pi/app/nginx.conf /etc/nginx/sites-enabled/default
```
- `/etc/nginx/sites-enabled/default` is linked to `/etc/nginx/sites-available/default` (so you can recover if you need)


### Reload Nginx

```
sudo systemctl reload nginx
```


### Run Flask Application Server

```
/home/pi/app/bin/python /home/pi/app/server.py
```
> This value is discussed above.


### Open your browser!
If you open your browser at `http://raspberrypi` you should see the Flask application data.
