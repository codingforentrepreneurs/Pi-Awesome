# Nginx Load Balancing & Backup Service in Docker Compose

## Current status

Our service have 3 primary components:
1. Docker & Docker Compose
2. A Python Flask Web App 
3. Nginx

This guide assumes you know how to use [Docker & Docker Compose](https://www.codingforentrepreneurs.com/projects/docker-and-docker-compose) and you can easily complete [this guide](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Docker%20%26%20Docker%20Compose%20on%20Raspberry%20Pi.md)


Our `docker-compose.yaml`
```docker-compose
version: '3.2'
services:
    flaskservice:
        restart: 'always'
        build:
            context: .
            dockerfile: Dockerfile.flask
        environment: 
            - PORT=8001
        expose: 
            - 8001
    nginx:
        restart: 'always'
        build:
            context: .
            dockerfile: Dockerfile.nginx
        ports:
            - 80:80
        depends_on: 
            - flaskservice
```

Our `nginx.conf`:

```nginx
upstream flaskappproxy {
    server flaskservice:8001;
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


## Load Balancing with a Docker Compose
First off, load balancing is about distributing traffic in a way that doesn't overload any one server (or in Docker Compose terms, service) by redirecting traffic (aka load) across all available servers/services.

Since we're using Docker compose, we need to create additional services to handle this load prior to updating our nginx configuration. We'll do that adding the `gotyourback` service to our `docker-compose.yaml`:

```
service:
    ...
    gotyourback:
        restart: 'always'
        build:
            context: .
            dockerfile: Dockerfile.flask
        environment: 
            - PORT=8002
        expose: 
            - 8002
```
> Notice the only change between the `flaskservice` and `gotyourback` is the `PORT` being used.

Now that we have this service we can update our nginx configuration. 

## Update nginx proxy

As of now, this is our nginx proxy server:
```
upstream flaskappproxy {
    server flaskservice:8001;
}
```

The `flaskservice:8001` is directly correlated to the `docker-compose.yaml` configuration for the `flaskservice` service. We can modify this proxy server to have additional entries:

```
upstream flaskappproxy {
    server flaskservice:8001;
    server gotyourback:8002;
}
```

And yes, we can add another service to `docker-compose.yaml`:

```
service:
    ...
    redudantservice:
        restart: 'always'
        build:
            context: .
            dockerfile: Dockerfile.flask
        environment: 
            - PORT=8003
        expose: 
            - 8003
    gotyourback:
        restart: 'always'
        build:
            context: .
            dockerfile: Dockerfile.flask
        environment: 
            - PORT=8002
        expose: 
            - 8002
```

And again, update `nginx.conf`:

```
upstream flaskappproxy {
    server flaskservice:8001;
    server gotyourback:8002;
    server redudantservice:8003;
}
```


By default, `nginx` uses a "round-robin" approach to picking which server to direct traffic to. This default just goes down the list of servers in the `upstream` configuration as they appear; there's nothing more to it. There are other [load balancing options](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/#) to this as well.


## A Backup Server

In many cases you'll want to implement a backup server so that you can take down other servers while still keep your overall project running.


This is a very simple change to our `upstream` configuration:

```
upstream flaskappproxy {
    server flaskservice:8001;
    server gotyourback:8002 backup;
    server redudantservice:8003;
}
```
Now, your traffic will only be routed to the `flaskservice` and the `redudantservice` service. If either of those are down (or not responsive), then the traffic will be routed to the `gotyourback` service.
