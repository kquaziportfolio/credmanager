# credmanager
Credmanager is a Python project using <a href="https://pymongo.readthedocs.io/en/stable/">PyMongo</a> and <a href="https://www.mongodb.com/">MongoDB</a>. It uses the MongoDB
database to store temporary login session data that can be stored in cookies. It automatically expires credentials when they are accessed if the timestamps don't match. I
use this library in Flask webservers that require authentication.
