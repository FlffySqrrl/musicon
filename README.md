# MusicOn

## Setup for Development
1. Create a local MySQL database with `create database musicon;`.
2. Go inside the project folder and do the following:
  * `python manage.py collectstatic` to collect all static files.
  * `python manage.py syncdb` to set up the database and create a superuser for admin access.
  * `python manage.py validate` to validate all installed models.
3. Go to the directory that the project folder is in and start the server with `dev_appserver.py [project-folder]`.
4. See the project in action at `localhost:8080`. Access the admin interface at `localhost:8080/admin`.
