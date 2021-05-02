# Gunicorn & Supervisor

In [this post](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Supervisor%20as%20a%20Background%20Service%20Manager.md) we setup supervisor to run gunicorn. In this one, we're going to dive in a little deeper and create a more resilient method for running this application.



via a development server. Now we're going to setup supervisor to use [gunicorn](https://gunicorn.org/) as a production-ready web server gateway interface (wsgi).

### Current Status

My app `Supervisor` config (`project.supervisor.conf`)
```
[program:flaskapp]
user=pi
directory=/home/pi/app
command=/home/pi/app/bin/gunicorn wsgi:app
 
autostart=true
autorestart=true
stdout_logfile=/var/log/www/flaskapp/stdout.log
stderr_logfile=/var/log/www/flaskapp/stderr.log
```
> As mentioned in the linked post above, we have the [correct permissions](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/User%20Group%20Permissions.md) for each folder listed above.

This line `/home/pi/app/bin/gunicorn wsgi:app` does not cover the possible configuration we might need for gunicorn. So we're going to convert it to run off a bash script called `run.sh` located right in our project directory (`/home/pi/app`). This means my supervisor configuration won't have to change when my gunicorn configuration does. 


### 1. Create `run.sh`
I create a bash script as my entry command for running my python web application.

In my case, the root of my application is on `/home/pi/app` so that's where I'll store it: `/home/pi/app/run.sh`

```
#!/bin/bash

exec /home/pi/app/bin/gunicorn --pid /home/pi/app/flaskapp.pid  --bind 0.0.0.0:8000 wsgi:app
```
Let's break this down:

- **`#!/bin/bash`**: This header declares which shell to execute the file with. In this case we're using the `bash` shell. 
- **`exec`**: this means execute. If you omit this line, supervisor will not monitor gunicorn but rather `run.sh`. (Thanks to [this wonderful comment](https://github.com/benoitc/gunicorn/issues/520#issuecomment-48244743).)
- **`/home/pi/app/gunicorn`** this is the absolute path to the Python virtual envioronment-installed gunicorn.
- **`--pid /home/pi/app/flaskapp.pid`** (you can use `-p` or `--pid`). This line designates were to store the process id. (more on this later)
- **`--bind 0.0.0.0:8000`**: this is binding our gunicorn app to `PORT` 8000 on the localhost (`0.0.0.0`)
- **`wsgi:app`** this is the python module `wsgi.py` that has the `app` variable to run our actual python web server. (In this case a Flask app but can be a Django, fastapi, or many other apps as well).



### 2. Update `/etc/supervisor/conf.d/project.supervisor.conf`
```
[program:flaskapp]
user=pi
directory=/home/pi/app
command=sh run.sh
 
autostart=true
autorestart=true
stdout_logfile=/var/log/www/flaskapp/stdout.log
stderr_logfile=/var/log/www/flaskapp/stderr.log
```
The only change is `command=sh run.sh`


### 3. Reread and Update `supervisor`

```
sudo supervisorctl reread
sudo supervisorctl update
```

### 4. Revisiting Process ID File (PID) 
What was the point of adding `--pid /home/pi/app/flaskapp.pid` to our `run.sh`?

There's a few questions that come to mind that `pid` can help solve:

- What processes are running on `PORT` 8000?
- How can I kill my current gunicorn application if I forgot (or don't know) that `supervisor` is managing it?
- What if `supervisor` says that my `gunicorn` app is stopped but `gunicorn` is actually still up?

There are likely many other questions that come to mind but to me these are the questions I get the most often.

##### How to check what's running on any `PORT`?
```
sudo lsof -i :8011
```
or 
```
sudo lsof -i :8000
```
If there is a process running, this command will show it. Just change `8011` or `8000` to the port number you want to review. If you have nginx listening on `PORT` `80` you could try `sudo lsof -i :80` to see if it's actually listening.

Here's an example response:

```
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
gunicorn 4892   pi    5u  IPv4  62193      0t0  TCP localhost:8000 (LISTEN)
gunicorn 4895   pi    5u  IPv4  62193      0t0  TCP localhost:8000 (LISTEN)
```
If you wanted to `stop/kill` one of these processes, you can just run `kill <pid>` like:

```
kill 4892
```

You can also use the `--pid /home/pi/app/flaskapp.pid` to do this with less steps:

```
kill $(cat /home/pi/app/flaskapp.pid)
```
> `cat /home/pi/app/flaskapp.pid` will yield the contents of the file (as you may know). `$(cat /home/pi/app/flaskapp.pid)` yeilds the contents of the file as an argument to a command.
If you have `supervisor` setup correctly, a new `flaskapp.pid` file should so up almost right away. This is because we have our `supervisor` config to include `autorestart=true`.

Pretty neat huh?

### 5. Standard Supervisor control commands for our app

```
sudo supervisorctl status 
sudo supervisorctl status flaskapp
sudo supervisorctl start flaskapp
sudo supervisorctl stop flaskapp
sudo supervisorctl restart flaskapp
```
