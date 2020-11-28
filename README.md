# CSC211 Final Group Project: Virtual Painted Tunnel

## How to Develop

#### Setting up the Development Environment
1. To create your virtual python environment, navigate to the root `Virtual-Tunnel` directory and run `python -m venv venv`
2. Activate your virtual environment by running `venv\Scripts\activate` (Windows), or
`source venv/bin/activate` (macOS/Linux)
3. Install current dependencies by running `pip install -r requirements.txt`

#### Running the Application
From within the virtual environment (*venv*), run `flask run`

#### Adding new dependencies
If you add new dependencies (pip packages), you will need to update the `requirements.txt` file by running `pip freeze > requirements.txt`

If somebody else adds a new dependency, you will need to download that dependency to your own virtualenv by running `pip install -r requirements.txt` after pulling the updated requirements file.

#### Upgrading the Database
1. `flask db migrate`
2. `flask db upgrade`

Use these two commands to migrate the existing database to one with updated models. These are from the `flask-migrate` package.

## To-Do List

* Everything...

## Known Problems

* None!


Created by Ariel Hirschhorn, Mitch Jones, and Jess Palmisciano for CSC211.

Flask structure adapted from [Miguel Grinberg's Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).