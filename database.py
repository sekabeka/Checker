from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


client: AsyncIOMotorClient = AsyncIOMotorClient()
db: AsyncIOMotorDatabase = client['checker']

