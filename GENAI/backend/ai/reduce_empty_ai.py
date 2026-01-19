def reduce_empty_trips(location, loads):
    location = location.strip().title()

    for load in loads:
        if load["location"] == location:
            return {
                "recommendation": (
                    f"Return load available from {location} to "
                    f"{load['destination']} ({load['loadType']})"
                )
            }

    return {
        "recommendation": (
            f"No return load found near {location}. "
            "AI suggests checking nearby cities."
        )
    }
