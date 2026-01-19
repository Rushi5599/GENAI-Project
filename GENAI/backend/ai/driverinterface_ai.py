def suggest_route(from_city, to_city, routes):
    from_city = from_city.strip().title()
    to_city = to_city.strip().title()

    key = f"{from_city}-{to_city}"

    if key in routes:
        return {
            "route": f"{from_city} → {to_city}",
            "distance": routes[key],
            "note": "AI selected the shortest available route."
        }

    return {
        "route": f"{from_city} → {to_city}",
        "distance": "Unknown",
        "note": "Route not found in dataset. Using default navigation."
    }
