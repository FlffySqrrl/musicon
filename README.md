# MusicOn

![MusicOn Logo](https://github.com/chriscyang/musicon/blob/master/musicon/static/img/musicon.png)

## Requirements
* `python 2.7`
* `django 1.5`
* `mysql`

## Setup for Development
1. Create a local MySQL database with `create database musicon;`.
2. Go inside the project folder and do the following:
  * `python manage.py collectstatic` to collect all static files.
  * `python manage.py syncdb` to set up the database and create a superuser for admin access.
  * `python manage.py validate` to validate all installed models.
3. Go to the directory that the project folder is in and start the server with `dev_appserver.py [project-folder]`.
4. See the project in action at `localhost:8080`. Access the admin interface at `localhost:8080/admin`.

## Contributors
* [chriscyang](http://www.github.com/chriscyang)
* [mwkim0919](https://github.com/mwkim0919)
* [Lewinalle](https://github.com/Lewinalle)
* [baek4055](https://github.com/baek4055)

## API
![Songkick Logo](https://github.com/chriscyang/musicon/blob/master/musicon/static/img/sk_full.png)

**MusicOn** uses the [Songkick API](http://www.songkick.com/developer).
