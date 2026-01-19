def handle_driver_emergency(emergency_type, location, rules):
    rule = rules.get(emergency_type)

    if not rule:
        return {
            "message": f"Emergency reported at {location}. Support team will contact you shortly.",
            "priority": "Medium",
            "helpline": "1800-SUPPORT"
        }

    return {
        "message": f"{rule['message']} Location noted: {location}.",
        "priority": rule["priority"],
        "helpline": rule["helpline"]
    }
