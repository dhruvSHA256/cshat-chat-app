# Realtime Flask Chat App

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Socket.io](https://img.shields.io/static/v1?style=for-the-badge&message=Socket.io&color=010101&logo=Socket.io&logoColor=FFFFFF&label=)
![PostgreSQL](https://img.shields.io/static/v1?style=for-the-badge&message=PostgreSQL&color=4169E1&logo=PostgreSQL&logoColor=FFFFFF&label=)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)

- realtime chat application using
  [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) ([learn more about
  websockets](https://www.youtube.com/watch?v=2Nt-ZrNP22A))
- user credentials are stored in [PostgreSQL](https://www.postgresql.org/)
- have registration and authentication functionally
- user sessions are stores using [Flask-Session](https://flask-session.readthedocs.io/) 
- frontend is built using [bootstrap](https://getbootstrap.com/)

## Demo
- the final project is hosted on heroku
- <a href="https://warm-oasis-70461.herokuapp.com/" target="_blank"> view live demo</a>

## Setup

- ensure python3 is installed on your system
- clone the project and cd into the project directory
```bash
$ git clone https://github.com/dhruvSHA256/cshat-chat-app
$ cd cshat-chat-app
```
- make python virtual env for current project and use it
```bash 
$ /usr/bin/python3 -m venv .venv && source ./.venv/bin/activate
```
- install required packages
```bash
$ pip install -r requirements.txt
```
- export PostgreSQL database
```bash
$ export DB_URL="<your_database_url>"
```
- export secret key used by flask
```bash
$ export SECRET_KEY="<your_secret_key>"
```
- run the app
```bash
$ python app.py
```

## Host it on heroku
- install heroku-cli (refer [official heroku docs](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)) 
- create heroku project using heroku-cli
```bash
$ heroku create
```
- push project
```bash
$ git push heroku main
```
- set config vars 
```bash
$ heroku config:set DB_URL="<your_database_url>"
$ heroku config:set SECRET_KEY="<your_secret_key>"
```
- open the live project
```bash
$ heroku open
```

![Made with love in India](https://madewithlove.now.sh/in?colorA=%233d3846&colorB=%23f66151&template=for-the-badge)
