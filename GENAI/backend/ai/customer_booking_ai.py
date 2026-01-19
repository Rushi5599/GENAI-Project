def recommend_truck(load_type, weight, distance, trucks):
    load_type = load_type.strip().lower()
    generic_loads = ["box", "boxes", "goods", "package", "cargo"]

    for truck in trucks:
        supported = [x.lower() for x in truck.get("supportedLoads", [])]

        if (
            load_type in supported
            or load_type in generic_loads
            or "industrial" in load_type
        ) and weight <= truck["maxWeight"]:

            cost = distance * truck["costPerKm"]

            return {
                "truckType": truck["truckType"],
                "estimatedCost": round(cost, 2),
                "explanation": (
                    f"{truck['truckType']} is recommended because it can safely "
                    f"carry {weight} tons over a {distance} km route."
                )
            }

    # fallback → biggest truck
    biggest = max(trucks, key=lambda x: x["maxWeight"])

    return {
        "truckType": biggest["truckType"],
        "estimatedCost": round(distance * biggest["costPerKm"], 2),
        "explanation": (
            "No exact match found. AI selected the largest available truck "
            "to ensure safe transportation."
        )
    }
