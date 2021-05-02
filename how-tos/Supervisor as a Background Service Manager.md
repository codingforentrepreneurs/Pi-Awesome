# Supervisor as a Background Service Manager
[Supervisor](http://supervisord.org/), often called supervisord, is a simple way to manage processes that you need your pi to run. In our case, we're using it to run a [minimal python web application (flask)](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Create%20a%20Minimal%20Web%20Application%20with%20Nginx%2C%20Python%2C%20Flask%20%26%20Raspberry%20Pi.md).



### 1. Install
```
sudo apt install supervisor -y
```

### 2. Start Supervisor

```
sudo service supervisor start
```

### 3. Create a Supervisor Process
> Be sure to [enable the correct permissions](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/User%20Group%20Permissions.md) on the `user` or the user's `group` so the below process can actually run. 

All of your custom processes will live in the following directory:
```
/etc/supervisor/conf.d/
```

Create file `project.supervisor.conf` and put:

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

- **`[program:<appname>]`** The `<appname>` setting here is the name of the supervisor process so we can run various commands (see step 4). Again, `flaskapp` is the `<appname>`

- **`user`** is the user you want this process to run as. We'll stick with our default `pi` user.

- **`directory`**: Default working directory

- **`command`**: What command do we need this process to run? In my case, I'm using a Python virtual environment (ie `/home/pi/app/bin/`) with [gunicorn](https://gunicorn.org/) installed. This command can be any valid `bash shell` command. For more on [gunicorn & supervisor go here](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Gunicorn%20%26%20Supervisor.md).

- **`autostart`**: start on system boot (true / false)
- **`autorestart`** Restart on failure (true / false)
- **`stdout_logfile`** `stdout` log file location
- **`stderr_logfile`** `stderr` log file location

#### 4. Update Supervisor
```
sudo supervisorctl reread
sudo supervisorctl update
```
> These two commands will let supervisor know of our new process (`reread`) and it will run it (`update`).


#### 5. Verify Commands

```
sudo supervisorctl status flaskapp
sudo supervisorctl start flaskapp
sudo supervisorctl stop flaskapp
sudo supervisorctl restart flaskapp
```


#### 6. Check logs

In our `project.supervisor.conf` from Step 3, we have the following log paths:

```
/var/log/www/flaskapp/stdout.log
```
and 
```
/var/log/www/flaskapp/stderr.log
```
These logs are useful to uncover errors with your application running.
