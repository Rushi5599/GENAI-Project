def handle_emergency(load_type, from_city, to_city, resources):
    load_type = load_type.strip().title()

    action = resources.get(
        load_type,
        "Dispatch nearest available emergency truck immediately"
    )

    return {
        "priority": "HIGH",
        "action": action,
        "message": f"Emergency delivery arranged from {from_city} to {to_city}"
    }
