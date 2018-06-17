# smta
Simple Money Transfer Application

# Requirements
- Docker Compose ( https://docs.docker.com/compose/ )
- Pipenv ( https://github.com/pypa/pipenv )

# Running the application
Install Docker Compose (see above's reference) and execute:

```
$ docker-compose build
```

Then, just:

```
$ docker-compose run smta
```

Now you should be able to see the application running in localhost at port 8000

It is possible to log in using:

```
user: administrator
password: Barcelona2018
```

# Testing
In order to testing the application, just:

```
$ pipenv shell
$ pipenv install --dev
```

To create a new Pipenv environment with developing tools, and:

```
$ tox
```

Will execute all application tests as long as syntax spell checking.
