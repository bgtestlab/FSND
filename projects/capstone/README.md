# FSND Final Project

## Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 
There are three types of roles - casting assistant, casting director and executive producer.

1) Allow the casting assitant to view actors and movies.
2) Allow the casting director to create or delete actors and edit existing actors or movies as well as view actors and movies.
3) Allow the executive producer to create or delete actors or movies and edit existing actors or movies as well as view actors and movies.

Casting Agency has been deployed to Heroku and it is up and running from https://capstone-agency-br.herokuapp.com which doesn't have graphics from frontend.

## Endpoints and permissions
JWT was set up for each role as for:
- Casting Assistant
    - can 'get:actors', 'get:movies'
- Casting Director
    - can 'patch:actors', 'patch:movies', 'post:actors', 'delete:actors' in addition to Casting Assisant's permission
- Executive Producer
    - can perform all actions

## Authentication setup
For Postman:
Please make sure to set up the variable 'host' as 'https://capstone-agency-br.herokuapp.com. 
If you import the udacity-capstone.postman_collection.json in the project folder, Auth0 Bearer tokens are already set up.
Please try 'get' end points first and manipulate the numbers in either 'delete' or 'patch' end points.

For local testing:
JWTs for each role are stored in the 'setup.sh' file.

## Testing
To run the tests, set up virtual environment first and then config:
```
pip3 install -r requirements.txt   
source venv/bin/activate; source setup.sh
```
and then set up database:
```
service postgresql start
dropdb agency_test
createdb agency_test
psql -d agency_test -U your_db_user -a -f agency_test.psql
```
fianlly run it by:
python3 test_app.py
```
