Project: Drone Operations Coordinator AI Agent
Candidate: Praveen Koppal

1. Overview

The goal of this project was to build an AI-powered Drone Operations Coordinator capable of managing pilots, drones, and missions across multiple projects using a conversational interface.

The system integrates with Google Sheets for real-time, two-way data synchronization and assists in assignment coordination, conflict detection, and urgent reassignments.

The solution was implemented as a backend AI agent using Python and FastAPI, with Google Sheets acting as the operational datastore.


2. Key Assumptions

Several assumptions were made to proceed efficiently under limited time and partially defined requirements:

2.1 Google Sheets as Source of Truth

All operational data (Pilot Roster, Drone Fleet, Missions) is assumed to be accurate and authoritative.
The AI agent does not maintain its own database.

2.2 Pilot Availability Interpretation

Available: Pilot can be assigned

Assigned: Pilot is currently on a mission

On Leave / Unavailable: Pilot cannot be reassigned

These values are interpreted directly from the status column in the Pilot_Roster sheet.

2.3 Mission Identification

Users may refer to missions by:

Project ID (e.g., PRJ001)

Location (e.g., Bangalore)

Priority keywords (e.g., urgent)

The agent therefore uses flexible matching instead of strict ID-only lookup.

2.4 Lightweight Natural Language Parsing

Instead of using full NLP or intent classification models, simple keyword-based parsing was used due to time constraints and to keep the system transparent and debuggable.


3. Architecture & Design Decisions
3.1 Technology Choices

Python + FastAPI
Chosen for rapid development, clear API structure, and automatic Swagger documentation for testing.

Google Sheets API + Drive API
Used to fulfill the requirement of two-way sync and to avoid setting up a separate database.

Rule-Based Agent Logic
Assignment decisions are made using deterministic rules (skills, location, availability) instead of ML models.
This ensures explainability and predictable behavior.

3.2 Separation of Concerns

The project was structured into separate modules:

sheets.py — Google Sheets read/write logic

matcher.py — Pilot and drone matching logic

coordinator.py — High-level decision making

app.py — Conversational API interface

This modular structure makes the system easier to extend, debug, and reason about.

4. Conflict Detection Strategy

The agent detects and explains conflicts instead of silently failing.

Pilot Conflicts

Pilot not available

Pilot already assigned to another project

Missing required skills or certifications

Location mismatch

Drone Conflicts

Drone under maintenance

Drone location mismatch

Instead of only returning “no pilots available”, the agent provides human-readable explanations, improving transparency and operational trust.

5. Interpretation of “Urgent Reassignments”
Interpretation

Urgent reassignments were interpreted as priority-based overrides, not blind force assignments.

Implemented Logic

If the user indicates urgency (keywords such as urgent or reassign), the agent:

Attempts to match a mission based on location

Falls back to the highest-priority mission if no location match exists

The agent selects a pilot who:

Is currently Assigned

Is not on leave

Causes minimal disruption (first eligible candidate)

The agent reports:

Which pilot was reassigned

From which project

To which urgent mission

This approach balances responsiveness with operational realism.

6. Trade-offs Made
6.1 No Frontend UI

A web frontend was not implemented. Instead, FastAPI’s Swagger UI and curl requests were used to save time and focus on backend logic and correctness.

6.2 Simple NLP Instead of LLM-Based Parsing

Keyword-based intent extraction was chosen over advanced NLP to reduce dependencies and keep behavior deterministic.

6.3 In-Memory Reasoning

All decisions are computed per request by reading Google Sheets. This avoids state inconsistency but may not scale well for very large datasets.

7. Error Handling & Robustness

The system gracefully handles:

Invalid pilot names

Invalid status values

Missing or unmatched missions

Runtime crashes (e.g., StopIteration in async execution) were prevented, and the API consistently returns user-friendly error messages instead of server errors.


8. What I Would Improve with More Time

With additional time, I would:

Add a frontend dashboard with chat interface

Use structured intent parsing or an LLM-based router

Add audit logs for reassignment decisions

Enforce stronger scheduling constraints using mission dates

Implement authentication and role-based access control



9. Final Notes

This project demonstrates:

Real-world system design

Clear separation of responsibilities

Robust error handling

Thoughtful interpretation of ambiguous requirements

The solution is modular, explainable, and ready for future expansion.

