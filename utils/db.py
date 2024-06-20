import motor.motor_asyncio
from config import Config

client = motor.motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URI)
db = client.get_database()
wallets_collection = db.wallets

