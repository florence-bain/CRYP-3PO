# Download mysql 

# Create Database on user SQL running my sql command - call database 'traderunner'

# Open my sql using mysql -u root command in the terminal

# Run Command in mysql interface - 

 - mysql > CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
 
 - user : djangouser
 - password : password 

 # Let the database know that our user should have complete access to the database - run :
 
 - mysql > GRANT ALL ON traderunner_data.* TO 'djangouser'@'%';

 - mysql> FLUSH PRIVELEGES;

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

