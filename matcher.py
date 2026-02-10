# Pilot & drone matching logic (to be filled by user)
def find_matching_pilots(pilots, mission):
    matched = []

    req_skills = set(mission["required_skills"].split(","))
    req_certs = set(mission["required_certifications"].split(","))

    for p in pilots:
        if p["status"] != "Available":
            continue
        if p["location"] != mission["location"]:
            continue

        pilot_skills = set(p["skills"].split(","))
        pilot_certs = set(p["certifications"].split(","))

        if not req_skills.issubset(pilot_skills):
            continue
        if not req_certs.issubset(pilot_certs):
            continue

        matched.append(p)

    return matched


def find_matching_drones(drones, mission):
    matched = []

    req_caps = set()
    if mission.get("required_capabilities"):
        req_caps = set(mission["required_capabilities"].split(","))

    for d in drones:
        if d.get("status") != "Available":
            continue
        if d.get("location") != mission.get("location"):
            continue

        drone_caps = set(d.get("capabilities", "").split(","))

        if req_caps and not req_caps.issubset(drone_caps):
            continue

        matched.append(d)

    return matched
