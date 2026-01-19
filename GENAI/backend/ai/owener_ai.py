# backend/ai/owener_ai.py

def analyze_owner(fleet, location, status, rules):
    """
    fleet   : truck type / fleet description
    location: current location
    status  : running / idle / maintenance
    rules   : owner rules json
    """

    insights = []

    if status.lower() in ["idle", "no"]:
        insights.append("Some trucks are idle. Consider assigning return loads.")

    if "pune" in location.lower():
        insights.append("Pune has high demand routes. Good location for profits.")

    insights.append("Regular maintenance improves fleet life.")
    insights.append("AI suggests reducing empty trips to increase revenue.")

    return {
        "fleet": fleet,
        "location": location,
        "status": status,
        "ai_insights": insights,
        "recommendation": "Optimize routes and reduce idle time for higher profit."
    }
