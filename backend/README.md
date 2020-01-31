# Backend

## Run the project 

You can use venv to start this project, you need virtualenv and python3-pip. 

```shell
$ virtualenv venv -p `which python3`
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
(venv)$ ./manage.py migrate
(venv)$ ./manage.py runserver
```

## Test the claims from backend 

You can test all the assertion from backend by:

```shell
(venv)$ ./manage.py test
```

## How to start?

The backend is constructed on top of [Django rest framework](https://www.django-rest-framework.org/). Most of the work is on [views](Bills/views.py) and [models](Bills/models.py) part of Bills. You can start from reading [bills' models](Bills/models.py) which will directly translate to tables in the database. 


