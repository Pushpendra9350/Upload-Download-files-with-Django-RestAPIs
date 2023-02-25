## Secure file upload Rest Api's

### Follow given instructions to run this project.
### We have postman collection also to test APIs Named as(APIs.postman_collection.json)
Python verison used
```git
Python 3.9.16
```

Install virtualenv to create virtual environment
```git 
pip install virtualenv
```

After creating a directory create a virtual environment by running
```git
virtualenv venv
```

Now activate virtual environment
```git
source venv/bin/activate
```

Now clone git repository
```git
git clone https://github.com/Pushpendra9350/Upload-Download-files-with-Django-RestAPIs.git
```

Now go to your working directory where all files exists

Now install all required packages
```git
pip install -r requirements.txt
```

Required file structire
```git
├── Accounts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── renderers.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils_token.py
│   └── views.py
├── FilesApp
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── templates
│   │   └── FilesApp
│   │       └── get_token.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── README.md
├── SecureUpload
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
└── templates
    └── base.html
```

Now run some of these commands to create models in database 
```git
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Now we can run our local server by this command
```git
python manage.py runserver
```
