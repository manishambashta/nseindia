# nseindia
This is a simple app for showing top 10 gainers of NSE. The data get refreshed every 5 minutes.
This project uses Cherrypy and Redis

To run this project, essentials are : Python, Redis, pip, cherrypy, python-redis

Follow these steps

Step 1:
Run get_data.py , This file updates the data of NSE top gainers every 5 minutes

Step 2:
Run topgainers.py , This file creates and manages the server. The visual representation of top gainers of NSE is here

link to live app : http://topnse.ambashta.in/

There are two log files error.log is for get_data.py whereas topgainersError.log is for topgainers.py file
