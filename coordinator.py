from sheets import SheetsClient
from matcher import find_matching_pilots, find_matching_drones


class Coordinator:
    def __init__(self):
        self.sheets = SheetsClient()

    # -----------------------------
    # Smart Mission Finder
    # -----------------------------
    def _find_mission(self, missions, user_input: str):
        user_input = user_input.lower()

        # 1️⃣ Match by project_id (PRJ001 etc.)
        for m in missions:
            if str(m.get("project_id", "")).lower() in user_input:
                return m

        # 2️⃣ Match by location (bangalore, mumbai, etc.)
        for m in missions:
            location = str(m.get("location", "")).lower()
            if location and location in user_input:
                return m

        # 3️⃣ Match by priority (urgent, high, medium)
        for m in missions:
            priority = str(m.get("priority", "")).lower()
            if priority and priority in user_input:
                return m

        return None

    # -----------------------------
    # Main Assignment Recommendation
    # -----------------------------
    def recommend_assignment(self, user_input: str):
        pilots, _ = self.sheets.read("Pilot_Roster")
        drones, _ = self.sheets.read("Drone_Fleet")
        missions, _ = self.sheets.read("Missions")

        mission = self._find_mission(missions, user_input)

        if not mission:
            return {
                "error": "No matching mission found. Please specify project ID, location, or priority."
            }

        matched_pilots = find_matching_pilots(pilots, mission)
        matched_drones = find_matching_drones(drones, mission)

        return {
            "mission": mission.get("project_id"),
            "location": mission.get("location"),
            "pilots": matched_pilots,
            "drones": matched_drones
        }


    def update_pilot_status(self, pilot_name: str, new_status: str):
        valid_statuses = ["available", "on leave", "assigned", "unavailable"]

        if new_status.lower() not in valid_statuses:
            return {
                "error": "Invalid status. Use Available, Assigned, On Leave, or Unavailable."
            }

        updated = self.sheets.update_pilot_status(pilot_name, new_status.title())

        if not updated:
            return {
                "error": f"Pilot '{pilot_name}' not found in Pilot Roster."
            }

        return {
            "success": f"Pilot {pilot_name} status updated to {new_status.title()}."
        }

    def urgent_reassignment(self, user_input: str):
        pilots, _ = self.sheets.read("Pilot_Roster")
        missions, _ = self.sheets.read("Missions")

        user_input = user_input.lower()

        # 1️⃣ Find best mission candidate (location preferred)
        urgent_mission = None

        # First: try location-based match
        for m in missions:
            if m.get("location", "").lower() in user_input:
                urgent_mission = m
                break

        # Fallback: pick highest priority mission
        if not urgent_mission and missions:
            priority_order = {"urgent": 3, "high": 2, "medium": 1, "low": 0}
            urgent_mission = sorted(
                missions,
                key=lambda m: priority_order.get(m.get("priority", "").lower(), 0),
                reverse=True
            )[0]

        if not urgent_mission:
            return {
                "error": "No mission available for urgent reassignment."
            }

        # 2️⃣ Find reassignable pilot
        reassignable_pilots = [
            p for p in pilots
            if p["status"].lower() == "assigned"
        ]

        if not reassignable_pilots:
            return {
                "error": "No pilots available for urgent reassignment."
            }

        # 3️⃣ Choose least disruptive pilot (first for now)
        pilot = reassignable_pilots[0]

        return {
            "urgent_mission": urgent_mission["project_id"],
            "pilot": pilot["name"],
            "previous_assignment": pilot["current_assignment"],
            "new_location": urgent_mission["location"]
        }

