from ..core.database import get_db
from app.schemas.reportSchema import ReportType, ReportFormat
from bson.objectid import ObjectId
from datetime import datetime

# Get the MongoDB collection
db = get_db()
reports_collection = db.reports  # Assuming 'reports' is the collection name

class ReportModel:
    @staticmethod
    async def create_report(report_data: dict):
        # Insert the report document into the MongoDB collection
        result = await reports_collection.insert_one(report_data)
        # Fetch and return the inserted document
        return await reports_collection.find_one({"_id": result.inserted_id})

    @staticmethod
    async def get_report_by_id(report_id: str):
        return await reports_collection.find_one({"_id": ObjectId(report_id)})

    @staticmethod
    async def get_reports_by_user(user_id: str):
        cursor = reports_collection.find({"user_id": user_id})
        return await cursor.to_list(length=100)

    @staticmethod
    async def update_report(report_id: str, update_data: dict):
        result = await reports_collection.update_one(
            {"_id": ObjectId(report_id)}, {"$set": update_data}
        )
        if result.modified_count > 0:
            return await reports_collection.find_one({"_id": ObjectId(report_id)})
        return None

    @staticmethod
    async def delete_report(report_id: str):
        report = await reports_collection.find_one({"_id": ObjectId(report_id)})
        if report:
            await reports_collection.delete_one({"_id": ObjectId(report_id)})
        return report
