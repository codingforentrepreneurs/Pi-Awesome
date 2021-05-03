# Docker & Docker Compose on Raspberry Pi
Docker isolates our applications so it's much more reusable across any machine that runs docker. Docker Compose helps us manage several containers at once in coordination with each other. Learn more about [Docker & Docker Compose in this tutorial series](https://www.codingforentrepreneurs.com/projects/docker-and-docker-compose).


### 1. Update, Upgrade, & Clear Out the Old

```
sudo apt update && sudo apt upgrade
```

*Do you have `supervisor` running your apps like we did in [this one](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Supervisor%20as%20a%20Background%20Service%20Manager.md)? If so, remove supervisor as docker will manage itself*

```
sudo apt-get purge supervisor # removes everying including config files
```

*Do you have `nginx` running like we did in [this one](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Activate%20an%20Nginx%20%20Web%20Server%20on%20a%20Raspberry%20Pi%20or%20any%20Linux.md)? If so, remove it as we'll use Docker to run nginx:*

```
sudo apt-get purge nginx nginx-common # removes everying including config files
```

*Do you want to remove all of docker and start fresh?*

```
sudo apt remove docker-ce*
```

Remove stale packages:

```
sudo apt-get autoremove
```


### 2. Install Docker
```
curl -sSL https://get.docker.com | sh
```


### 3. Install Docker Compose
> At this time, `docker-compose` must be installed via your global python3 installation *after* docker is installed above.

```
which python3
```
> Does this return nothing? That means `python3` is not installed. Run `sudo apt install python3-pip python3`

```
sudo python3 -m pip install docker-compose
```

> In newer versions of Docker Destkop, Docker Compose is included in the docker installation which means you'll use `docker compose` instead of `docker-compose` like we do below. 



### 3. Minimal Gunicorn-based Flask App
For this example, I'll be using the directory `/var/www/flaskapp` to store all of the files created. 


`server.py`
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world!"
```

`wsgi.py`
```
from server import app


if __name__=="__main__":
    app.run()
```

requirements.txt
```
flask
gunicorn
```

`run.sh`
```
#!/bin/bash

RUN_PORT=${PORT:-8010}
/app/bin/gunicorn --pid /app/bin/flaskapp.pid --bind 0.0.0.0:$RUN_PORT  wsgi:app
```



### Minimal Dockerfile for Flask/Django/FastAPI

`Dockerfile`
```
FROM python:3.7-slim

COPY . /app
WORKDIR /app


RUN python3 -m venv .
RUN /app/bin/pip install pip --upgrade
RUN /app/bin/pip install -r requirements.txt

RUN chmod +x run.sh

CMD ["./run.sh"]
```

Also add:
`.dockerignore`
```
bin/
include/
lib/
share/
__py_cache__/
```



### 4. Minimal Nginx Configuration

```
upstream flaskappproxy {
    server flaskapp:8081;
}

server {
    listen       80;
    server_name  localhost;
    root   /www/html/;


    location / {
        proxy_pass http://flaskappproxy;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```
Be sure to note that `flaskapp` is the service name while `flaskappproxy` is merely the proxy name within nginx. The `flaskapp` service name will be used below in `docker-compose.yaml`. The port of `8081` will be reused below as well.

### 5. Dockerfile for `nginx`


`Dockerfile.nginx`
```
FROM nginx:latest

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
```


### Minimal `docker-compose.yaml`


```dockerfile
version: '3.2'
services:
    flaskapp:
        restart: 'always'
        build:
            context: .
            dockerfile: Dockerfile
        environment: 
            - PORT=8081
        expose: 
            - 8081
    nginx:
        restart: 'always'
        build:
            context: .
            dockerfile: Dockerfile.nginx
        ports:
            - 80:80
        volumes: 
            - ./nginx.conf:/etc/nginx/nginx.conf
        depends_on: 
            - flaskapp
```


### 6. Run Docker Compose

```
sudo docker-compose up -d --build
```
> Ensure this is in the root of your app or use the flag `-f path/to/your/docker-compose.yaml`

Let's break this down:

- **`sudo`** In order to allow the `ports` for nginx to exposed properly, we use the superuser
- **`docker-compose up`** this is how we bring up our docker compose network
- **`-d`** This puts `docker-compose` in detatched mode; which allows it to run in the background
- **`--build`** means `docker-compose` will build the necessary container images


### 7. Stop Docker Compose
Above we use `-d` to run `docker-compose` in detached mode. Now we can stop it with:
```
docker-compose down -f path/to/your/docker-compose.yaml
```


### 8. Update single service

```
docker-compose stop flaskapp
docker-compose rm -f  flaskapp
docker-compose up --build -d flaskapp 
```
> This will allow `nginx` to continue running while the `flaskapp` service is rebuilt



