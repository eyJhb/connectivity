# What is this?
This is a simple client server application that I wrote, to monitor my bandwidth using iperf3.

# Isn't there other programs for this?
Properly.

# How do I use it?
## Client
There is a .config.json in the client folder, rename that to config.json, and configure it as you wish.

## Server
First import the schema.sql to a database,eg.

'''
sqlite3 database.db < schema.sql
'''

Create a file named settings.py, which contains a DB_LOCATION, eg.

'''
DB_LOCATION = "/home/eyjhb/projects/connectivity/server/database.db"
'''

Then export the location to the settings.py, to you environment

'''
export CON_FLASK_SETTINGS=/home/eyjhb/projects/home/connectivity/server/settings.cfg
'''

And you are good to go!
