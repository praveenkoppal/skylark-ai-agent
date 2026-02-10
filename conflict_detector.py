# Conflict detection logic (to be filled by user)
from datetime import datetime

def overlap(a_start, a_end, b_start, b_end):
    return not (a_end < b_start or b_end < a_start)


def pilot_conflicts(pilot, mission):
    issues = []

    if pilot["current_assignment"]:
        issues.append("Pilot already assigned to another project")

    return issues


def drone_conflicts(drone):
    issues = []

    if drone["status"] == "Maintenance":
        issues.append("Drone is under maintenance")

    return issues


def location_mismatch(pilot, drone):
    return pilot["location"] != drone["location"]
