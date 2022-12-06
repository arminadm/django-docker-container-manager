# django-docker-container-manager

# WARNING: This app requires linux and docker
this app shares host's Docker daemon with guest's container, so you should have installed Docker and using linux os for the best experience

# How to Setup
### 1- Clone the project
### 2- run **docker-compose up --build** for setting up
### 3- run **docker-compose exec backend sh -c "python3 manage.py createsuperuser"** for creating admin panel user
### 4- (optional) run **docker-compose exec backend sh -c "python3 manage.py generate_fake_data"** for generating fake data so you can have better testing experience
### 5- (optional) run **docker-compose exec backend sh -c "python3 manage.py test"** for testing the endpoints functionality

# How to use
## CRUD operations are available by 
http://127.0.0.1:8000/manage_apps/ <br/> (get: list of apps, post: create new app) <br/>
http://127.0.0.1:8000/manage_apps/detail/(int:pk)/ <br/>(get: retrieve single app info, put: update selected app info, delete: delete selected app)

## Create a container from an app
by the following url you can run a container from the selected app (using app's id as pk in url) <br/>
http://127.0.0.1:8000/run_container/(int:pk)/
### Important Note: 
you can create more than one container from the same app (container name will automatically get changed for preventing name conflict)

## Monitoring the containers
use http://127.0.0.1:8000/container_monitoring/ for getting info about running or exited containers (id, name, status, args, started_at, finished_at)
### Important Note:
this endpoint will display all the containers which are available in both HOST and the ones which are created by this app (GUEST)