from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient()
db = client.prices_bot
collection = db.users
