## Installation


### Creating and Activating a Virtual Environment


```bash    
  python3 -m venv django
  source django/bin/activate
  cd ..
  pip3 install -r requirements.txt
```

### Installation mysql-server and creating a database
```bash
  sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
  pip3 install mysqlclient
  sudo apt install mysql-server
  sudo mysql -u root -p
  CREATE DATABASE 'database name';
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
  SHOW DATABASES;
```

### Creating migrations 

Create a model in myapp/models.py, than:

```bash
  python3 manage.py makemigrations
  python3 manage.py migrate
```

### Creating a superuser 

```bash
  python3 manage.py createsuperuser
```

### Installing Redis
```commandline
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```
#### Start redis server

```commandline
sudo service redis-server start
```
