# Create Database on user SQL running my sql command (Database name used = traderunner)

# Open my sql using mysql -u root command in the terminal

# Run Command in mysql intergace - mysql > CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
 
 - user : djangouser
 - password : password 

 # Let the databae know that our user should have complete access to the database - run : mysql > GRANT ALL ON blog_data.* TO 'djangouser'@'%';

 - mysql> GRANT ALL PRIVILEGES ON test_traderunner.* TO 'djangouser'@'%'

 # mysql> FLUSH PRIVELEGES;

# Amend Database settings in settings.py 

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

# run python3 manage.py migrate

