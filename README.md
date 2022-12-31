# BUG-ROBOT-Backend
The back-end implementation of simple game using Django and django-rest-framework.
You Can see the front-end part [here](https://github.com/nejadipour/BUG-ROBOT-Frontend).

## Run Locally
Clone the project
```
git clone git@github.com:nejadipour/BUG-ROBOT-Backend.git
```
Go to the project directory
```
cd BUG-ROBOT-Backend
```
After creating a virtual environment, Install dependecies
```
pip install -r requirements.txt
```
Make migrations and migrate to the database. (default is a sqlite3 database)
```
python3 manage.py makemigrations
python3 manage.py migrate
```
To run locally
```
python3 manage.py runserver
```
This will run the server on port 8000.

## Models
### Board
Board model includes general properties like the shape or name.
The ```robot_strength``` field is a number that is used for handling actions of the robot. This field indicates the distance you can attack bugs or move the robot by one step.
### Square
State of each position and also handling the user's actions are handled using this model.

## API Documentation
After running the server, you can see the API documentation here: ```localhost:8000/swagger```

![image](https://user-images.githubusercontent.com/78561069/209984614-97101055-ab3a-4180-ab8b-361b1bd111aa.png)

## Test
You can test the endpoints that are working correctly by running this command:
```
python3 manage.py test
```
