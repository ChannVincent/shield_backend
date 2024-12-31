# shield_backend

## get started

$ python3 -m venv env
$ source env/bin/activate
$ python -m pip install Django
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser (user=admin email=ad@min.com pass=admin)
$ python manage.py runserver

## dev

$ python manage.py startapp package_name
$ pip freeze --local > requirements.txt