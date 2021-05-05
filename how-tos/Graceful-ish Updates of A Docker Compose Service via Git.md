# Graceful-ish Updates of A Docker Compose Service via Git
The primary downside of using Docker Compose in production is the lack of native ability to gracefully replace services.

Kubernetes and Docker Swarm really excel at this but that adds another layer of complexity (not to mention the need for at least 2 more raspberry pis) we just do not want at this time.

Instead, let's update our `post-receive` hook along with the `nginx` backup service to ease our transition as we upgrade services.


## Update the Git `post-receive` Hook
The `post-receive` hook file was originally created [here](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Setup%20Git%20%26%20Version%20Control%20on%20your%20Pi%20Server.md) when we added the ability to push our code that includes `docker-compose.yaml` along with a number of other services.

The services mentioned below are defined in [the load balancer portion](https://github.com/codingforentrepreneurs/Pi-Awesome/blob/main/how-tos/Nginx%20Load%20Balancing%20%26%20Backup%20Service%20in%20Docker%20Compose.md) of these guides.

`/var/repos/flaskapp.git/hooks/post-receive`
```bash
#!/bin/bash

WORK_DIR=/var/www/flaskapp/
git --work-tree=$WORK_DIR --git-dir=/var/repos/flaskapp.git/ checkout HEAD -f

cd $WORK_DIR
bash "${WORK_DIR}build.sh"
```

Let's move our primary `post-receive` commands into a new bash script in the root of our project.

`build.sh`
```bash
#!/bin/bash
docker-compose build flaskservice


# # Here's an example of running tests in this recently built
# # service. This assumes you have `pytest` in `requirements.txt`
# # If the test fails, the post-hook will exit; not finishing the build.
# # If the test succeeds, the post-hook will continue with the build.
#
# echo "Testing..."
# TEST_RESULTS=$(docker-compose run flaskservice /app/bin/pytest -x)
# if [[ "$(echo $TEST_RESULTS)" =~ "failed" ]]; then
#     echo "Tests failed. Not finishing service update."
#     exit 400;
# fi

if [[ $(git -C /var/repos/flaskapp.git/ diff --name-only HEAD~1 HEAD | grep nginx.conf) ]]; then
    # check if `nginx.conf` changed; rebuild service.
    docker-compose build nginx;
    docker-compose stop nginx;
    docker-compose rm -f nginx;
    docker-compose up -d nginx;
fi

if [[ $(docker ps | grep nginx) == "" ]]; then
    # check nginx is down, bring up service
    docker-compose up -d --build nginx;
fi



if [[ $(docker ps | grep gotyourback) == "" ]]; then
    # check backup service is down, start it.
    docker-compose up --no-deps -d --build gotyourback;
fi

docker-compose stop flaskservice
docker-compose rm -f flaskservice
docker-compose up --no-deps --remove-orphans -d flaskservice 
```

Be sure to run `chmod +x /var/repos/flaskapp.git/hooks/post-receive` and `chmod +x /var/www/flaskapp/build.sh` if you haven't already.

Now just push your code and see the results.
