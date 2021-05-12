# Add New User on Pi or Linux


### 1. Create User
```
sudo useradd -m tony
```
- `tony` is the username
- `-m` creates a home directory for `tony` (ie `/home/tony`)


### 2. Set User Password
```
sudo passwd tony
```
- `tony` is the username
- Be sure to set a secure password here

### 3. Add user to groups

```
sudo usermod -a -G www-logs,www-git,www-data tony
```
The groups `www-logs` and `www-git` where created at other times. In the [Pi Server](https://www.codingforentrepreneurs.com/projects/pi-server) tutorial series, we created these groups for special permissions. Read more about creating groups and user permissions [here](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/User%20Group%20Permissions.md)
