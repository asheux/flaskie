# flaskie

![Travis](https://img.shields.io/travis/asheuh/flaskie.svg) [![Coverage Status](https://coveralls.io/repos/github/asheuh/flaskie/badge.svg?branch=develop)](https://coveralls.io/github/asheuh/flaskie?branch=develop) [![Heroku](http://heroku-badge.herokuapp.com/?app=flaskie&style=flat)](https://bashtech-heroku.herokuapp.com/api/v1/)

#### Overview

A simple flask api to handle user authentication based on Flask and flask-RESTPlus

#### Required Features

- Users can create an account and log in.
- Users can update thier details
- Users can delete thier account
- Users can view the account details
- Admin can view all users in the app
- Admin can view his/her details
- Admin can delete a user with the specified user_id
- Admin can get a user with the specified user_id
- Admin can update a user with the specified user_id
- Role based permission system
- It is auto documented

##Exploring the demo.\n"

Create a new user at the 'POST /auth/user' endpoint. Get the user access token from the response.
Click the authorize button and add the token in the following format.

`Bearer (jwt-token without the brackets)`

There is also a built-in user:

`paulla` (administrator with all permissions) with password `mermaid`

## Authorization token(with the help of)\n"
`Jwt-Extended`"

![Flaskie Endpoints overview](https://user-images.githubusercontent.com/22955146/42416014-1837d00c-826c-11e8-86e7-03ef24ea80fa.png)


# Installation and Setup
Clone the repository.

```
git clone https://github.com/asheuh/flaskie
```
## Navigate to the API folder
```
bash
cd flaskie
```

## Create a virtual environment and activate

On linux

```
$ python -m venv venv
$ source venv/bin/activate
```

On Windows

```
py -3 -m venv venv
venv\Scripts\activate
```

## Install requirements( with pip)

```
$ pip install -r requirements/dev.txt
```

## Running the application

After the configuration, you will run the app 

Setup the application for develepment to make sure all the requiremente are installed
```
$ python setup.py develop
```

Run the application
```
$ python run.py
```

## Url for endpoints

```
http://localhost:5000/api/v1/

```
## The app is deploy to heroku with the following url

* [here is the live demo on heroku](https://bashtech-heroku.herokuapp.com/api/v1/)
