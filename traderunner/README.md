# MY SQL Database set up instructions.

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

 Let the databae know that our user should have complete access to the database 
 
 ```
 
 -  GRANT ALL PRIVILEGES ON traderunner.* TO 'djangouser'@'%'
 -  FLUSH PRIVELEGES;
 
 ```
 

Amend Database settings in settings.py 

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

In the terminal run 

```
python3 manage.py migrate
```

