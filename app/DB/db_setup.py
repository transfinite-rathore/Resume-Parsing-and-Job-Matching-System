from pymongo import AsyncMongoClient
from dotenv import dotenv_values

config=dotenv_values(".env")


## For creating connection
async def startup_db_client(app):
    try:
        app.mongo_client=AsyncMongoClient(config["DB_URI"])
        app.mongo_db= app.mongo_client.get_database(config["DB_NAME"])
        print("Congrats!! Database Connection Successfull")
    except Exception as e:
        print("Exception ",e)


## For closing connection
async def shutdown_db_client(app):
    await app.mongo_client.close()
    print("Database closed Successfully")