from deta import Deta  # Import Deta
import os
from dotenv import load_dotenv

#load environment variable
load_dotenv("/home/niranjan/Desktop/my_projects/.env")
deta_key=os.getenv("deta_key") # Initialize with a Project Key


# locally, set the project key in an env var called DETA_PROJECT_KEY
deta = Deta(deta_key)

# # This how to connect to or create a database.
db = deta.Base("base")

# To put data in to database
def insert_field_db(key,dict):
    return db.put(key=key,data=dict)

# To get data from database

def get_data(key):
    item=db.get(key)
    return item 





