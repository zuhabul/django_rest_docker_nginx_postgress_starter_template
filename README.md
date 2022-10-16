# Server REST Backend Template
This is a Django Rest Backend Server quick-start template that is configured with the followings:
*Docker, *Nginx *Gunicorn *AWS S3 *PostgressSQL *Django API Tests basic setup with examples *Django REST API basic setup with examples *API Documentation setup with Swagger and Redoc. *And more..

## Requirements

1. Docker Installed on the environment

## Development

Uses the default Django development server.

1. Rename *.env.sample* to *.env.dev*
2. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
3. Build the images and run the containers dev environment:

    ```sh
    docker-compose build
    docker-compose up -d

    # Or

    docker-compose up -d --build

    # And then

    docker-compose up
    ```

    Test it out at [http://localhost](http://localhost). The "app" folder is mounted into the container and your code changes apply automatically.

### - To Rebuild the container

```sh
docker-compose down -v

# or

docker-compose -f docker-compose.yml down -v

# then again

docker-compose up -d --build

docker-compose up
```

### - To run a Django specific command

```sh
docker-compose run web /usr/local/bin/python manage.py createsuperuser
```

## Production

Uses gunicorn + nginx.

1. Rename *.env.sample* to *.env.prod* and *.env.db.sample* to *.env.prod.db* Update the environment variables.
2. Build the images and run the containers:

    ```sh
    docker-compose -f docker-compose.prod.yml up -d --build

    docker-compose -f docker-compose.prod.yml up
    ```

    Test it out at [http://localhost](http://localhost). No mounted folders. To apply changes, the image must be re-built.
## Useful Tips

### API Specification Sheet

*To view the backend API specification visit any of the following links:*

1. [http://localhost/redoc/](http://localhost/redoc/)
2. [http://localhost/swagger/](http://localhost/swagger/)

### To RE-BUILD and RUN Production

1. Run the following commands:

```sh
docker-compose -f docker-compose.prod.yml down -v

docker-compose -f docker-compose.prod.yml up -d --build

docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic

docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

docker-compose -f docker-compose.prod.yml up
```

### Docker Clean Everything

Prune everything including volumes:
```sh
 docker-compose -f docker-compose.prod.yml down -v
 docker system prune --volumes -f
 ```

### Docker Clean step by step
```sh
# 1. Put doen the docker containers

     docker-compose -f docker-compose.prod.yml down -v

# 2. To remove all images which are not used by existing containers:

     docker image prune -a

# 3. Prune containers:

     docker container prune

# 4. Prune volumes:

     docker volume prune

# 5. Prune networks:

     docker network prune

# 6. Prune networks:

     docker network prune
```
## Re-deploy the app in the EC2

### Run the following commands:
```sh
ssh -i ~/.ssh/key.pem ec2-user@15.206.177.161

cd project_dir

git pull

docker-compose -f docker-compose.prod.yml down -v

docker-compose -f docker-compose.prod.yml up -d --build

docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

docker-compose -f docker-compose.prod.yml up -d
```
### If database needs to be deleted, run:
```sh
docker-compose -f docker-compose.prod.yml exec web python manage.py flush --no-input
```

### To see running processes in the server:
```sh
top
```

### Disconnect current running server

1. To kill docker-compose up -d, run:
```sh
docker network disconnect -f eaf-backend_default eaf-backend_nginx_1
```
