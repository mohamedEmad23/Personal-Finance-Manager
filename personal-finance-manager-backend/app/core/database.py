from motor.motor_asyncio import AsyncIOMotorClient
from .config import get_settings

settings = get_settings()

# MongoDB connection
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client.get_database()  # Connect to the MongoDB database specified in the URI

# Function to get the MongoDB database object
def get_db():
    return db  # Return the database instance directly, no need for session management
