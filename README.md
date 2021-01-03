# Fyyur
Download files
'''
git clone -b fyyur https://github.com/boramgwon/udacity.git fyyur
'''

Install the dependencies
'''
pip3 install -r requirements.txt
'''

Run the postgreSQL server
'''
sudo service postgresql start
'''

Run the development server
'''
export FLASK_APP=app; export FLASK_ENV=development; flask run
'''

Verify on the Browser
Navigate http://localhost:5000
