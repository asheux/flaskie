# flaskie

![Travis](https://img.shields.io/travis/asheuh/flaskie.svg)


#### Overview

A simple flask api to handle user authentication based on Flask and flask-RESTPlus

#### Required Features

- Users can create an account and log in.
- Users can update thier details
- Users can delete thier account
- Users can view the account details

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