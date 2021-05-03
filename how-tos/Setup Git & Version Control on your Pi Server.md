

### 1. Install `git` locally from [here](https://git-scm.com/downloads)


### 2. Install `git` on your Pi (or `Linux` server):

```
ssh pi@raspberry
sudo apt-get install git -y 
```


### 3. Set default branch name:

```
git config --global init.defaultBranch main
```
This will make our default global branch name to be `main` (this is important later)



### 4. Setup Repos Directory on your Pi (or `Linux` server):

```
sudo mkdir -p /var/repos/
```

### 5. Create `www-git` group and add our user to it:

```
sudo groupadd www-git
sudo usermod -a -G www-git $(whoami)
```
> The command `whoami` will return your current logged in user. Wrapping `$()` around a command uses it as a argument



### 6. Add `read`, `write`, & `execute` Permissions to our new `www-git` group:

```
sudo chgrp -R www-git /var/repos/
sudo chmod -R g+rwxs /var/repos/
```
> See all how to setup permissions [here](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/User%20Group%20Permissions.md)


### 7. Reboot
After you create a group, add a new user, and add permissions to that group, you should reboot your system.
```
sudo reboot
```



### 8. Create Bare Project Repo


```
mkdir -p /var/repos/flaskapp.git
```
> Change `flaskapp` as you see fit; leaving `.git` -- our project is merely named `flaskapp` so that's how I'll name this repo.

```
cd /var/repos/flaskapp.git
git init --bare
```
> Do you want to clone another repo? Use `git clone https://somewebsite.com/path/to/yourrepo . --bare`



### 9. Create Project Working Directory on your Pi (or `Linux` server)::

```
mkdir -p /var/www/flaskapp
python3 -m venv /var/www/flaskapp
```
> Permission errors? Check [this](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/User%20Group%20Permissions.md). You should not need to use *`sudo`* if your permissions are correct.


### 10. Add a `post-receive` hook for `git`
This `git` hook allows us to trigger:
- Updating our local project code (ie in `/var/www/flaskapp`)
- Update / reload our `supervisor` process
- Any other `bash` script we need to run.
- Run continous integration / continous deployment (`ci/cd`)

```
nano /var/repos/flaskapp.git/hooks/post-receive
```

Within `post-receive`:

```bash
#!/bin/bash

git --work-tree=/var/www/flaskapp/ --git-dir=/var/repos/flaskapp.git/ checkout -f
sudo supervisorctl restart flaskapp
```
Let's break this `post-receive` file down:

- **`git`**: this is the shell command for everything `git` related
- **`--work-tree`** This is our project's working directory.
- **`--git-dir`** this is the `git` managed directory where our code lives. I recommend keeping this seprate from your `--work-tree` to keep your running code isoloated from your code history.
- **`checkout`** this is a command to switch to the `HEAD` of your code (ie the most recent commit to the specificed/default branch).
- **`-f`** will force the code to change (ie ignoring any file changes in your `--work-tree`)



### 11. Update `run.sh`
In my project, I have a `run.sh` that `supervisor` calls. I will update this command to include a requirements install step.

```

#!/bin/bash

/var/www/flaskapp/bin/python -m pip install -r /var/www/flaskapp/requirements.txt;

exec /var/www/flaskapp/gunicorn --pid /var/www/flaskapp/flaskapp.pid --bind 0.0.0.0:8000  --workers 4 wsgi:app
```



### 12. Clone the Remote Code to your local machine (optional)
If your code is on your server and not on your local machine, do this step. 

```bash
mkdir -p /dev/flaskapp/
cd /dev/flaskapp
git clone ssh://pi@raspberry:/var/repos/flaskapp.git .
```

The format is `git clone ssh://<user>@<ip-or-host>/path/to/repo/<your-project>.git .`


### 13. Add Remote Repo to Local Machine

```
cd /dev/flaskapp
git remote add piserver ssh://pi@raspberry:/var/repos/flaskapp.git
```
> The format is `git remote add <remote-name> ssh://<user>@<ip-or-host>/path/to/repo/<your-project>.git`



> Do you have the correct [SSH login](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/SSH%20to%20Host%20without%20Password.md) or [User Group Permissions](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/User%20Group%20Permissions.md) for this `host`/`server`? 


### 14. Pull code from Remote Repo to Local Machine:

```
git pull piserver main
```
> The format is `git pull <remote-name> <branch-name>`


### 15. Make changes to Local code & commit those changes:

```
cd /dev/flaskapp
echo "hello world from local" > hello-world.txt
```

**Add file**
```
git add hello-world.txt
```

**Commit Changes**
```
git commit -m "Added hello-world.txt"
```

### 16. Push code from Local Machine to Remote Repo/Remote Server:
```
git push piserver main
```
> The format is `git push <remote-name> <branch-name>`


### 17. Verify changes


```
ssh pi@raspberry
cd /var/www/flaskapp/
cat hello-world.txt
```
> Did it work?


