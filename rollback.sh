python3 manage.py reset_db
python3 manage.py migrate
python3 manage.py createsuperuser --username admin --email foo@foo.foo
python3 manage.py loaddata fixtures/*
python3 manage.py runserver
