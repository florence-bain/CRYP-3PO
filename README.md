

# Traderunner

Makers finale project - Automated cryptocurrency trading bot 

## Developers 

- Florence Bain (florence-bain)
- Jessica Bulman (jessocxz98)
- Osneil Drakes (odrakes1992)
- Harry Parsons (drkitsch)

## Our initial wireframe ideas for our program
![wireframes](https://user-images.githubusercontent.com/78934464/142075218-6854f157-6a15-4b59-b7a4-989d4a4e3649.jpeg)

## Installation

- Git clone this repo 
- You will need to have Django & MySQL installed
- Setup your database with the instructions below 
- Once this is done, run 'python manage.py runserver' 
  which will start up your server and provide a url address.
- You will be prompted to sign up before you can access the main page.

## MySQL Database set up instructions.

From the terminal run the following to install mysql

```
- brew install mysql
```

Install SQL/Python connector, from the terminal run either of the following

```
- pip install mysql-connector-python
- pip3 install mysql-connector-python
```

Enter mysql

```
- mysql.server start.

- mysql -u root
```

Create Database on user SQL running my sql command (Database name used = traderunner)

```
- create database [databasename];
```

Create General User

```
- CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY 'password';

```

The user details will be

- user : djangouser
- password : password

Let the database know that our user should have complete access to the database

```

-  GRANT ALL PRIVILEGES ON traderunner.* TO 'djangouser'@'%'
-  FLUSH PRIVILEGES;

```

Amend Database settings in settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sample',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'djangouser',
        'PASSWORD': 'password',
    }
}


```

In the terminal run

```
- python3 manage.py migrate
```

