def home_summary(stats):
    return {
        "message": "GenAI Transport System Operational",
        "totalBookings": stats["totalBookings"],
        "activeDrivers": stats["activeDrivers"],
        "emergencyHandled": stats["emergencyHandled"]
    }
