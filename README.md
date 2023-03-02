## Installation


### Creating and Activating a Virtual Environment


```bash    
  python3 -m venv django
  source django/bin/activate
  cd ..
  pip3 install Django
```

### Installation mysql-server and creating a database
```bash
  sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
  pip install mysqlclient
  sudo apt install mysql-server
  sudo mysql -u root -p
  create database 'database name';
```

### Creating a new user

```bash
  sudo mysql -u root -p
  CREATE USER 'username'@'localhost' IDENTIFIED BY 'user's password';
  quit
  sudo mysql -u username -p
```

### Giving mysql user access to database

```bash
  sudo mysql -u root -p
  GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost';
  quit
  sudo mysql -u username -p
  show databases;
```

### Creating migrations 

Create a model in myapp/models.py, than:

```bash
  python manage.py makemigrations
  python manage.py migrate
```

### Creating a superuser 

```bash
  python manage.py createsuperuser
```
