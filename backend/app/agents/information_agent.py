from typing import Dict, Any


class InformationAgent:
    """
    Information Agent

    Responsible for gathering relevant context from connected
    sources such as email, calendar, documents and travel data.

    For the MVP, these sources are simulated.
    Later, each source can be replaced with a real API connector.
    """

    def __init__(self):
        self.sources = {
            "email": True,
            "calendar": True,
            "documents": True,
            "travel": True,
            "event": True,
        }

    async def gather_context(self, goal: str) -> Dict[str, Any]:
        """
        Gather all information relevant to the user's goal.
        """

        # For the current prototype we use simulated data.
        context = {
            "goal": goal,

            "email": {
                "hackathon_confirmation": {
                    "subject": "Hackathon Mumbai — Registration Confirmed",
                    "date": "Saturday, 12 October",
                    "registration_time": "9:00 AM",
                },
                "project_deadline": {
                    "subject": "Final Project Submission",
                    "deadline": "Friday, 11:59 PM",
                },
            },

            "calendar": [
                {
                    "title": "Team Meeting",
                    "date": "Friday",
                    "time": "2:00 PM",
                    "duration_minutes": 60,
                },
                {
                    "title": "Hackathon",
                    "date": "Saturday",
                    "time": "9:00 AM",
                    "duration_minutes": 480,
                },
            ],

            "travel": {
                "type": "train",
                "booking_status": "confirmed",
                "departure": {
                    "date": "Friday",
                    "time": "6:30 AM",
                    "location": "Pune",
                },
                "arrival": {
                    "date": "Saturday",
                    "time": "8:30 AM",
                    "location": "Mumbai",
                },
                "venue_travel_minutes": 40,
            },

            "hotel": {
                "name": "Mumbai City Hotel",
                "check_in": "Friday, 2:00 PM",
                "check_out": "Sunday, 11:00 AM",
                "status": "confirmed",
            },

            "event": {
                "name": "Mumbai AI Hackathon",
                "location": "Mumbai",
                "venue": "Innovation Convention Centre",
                "start": "Saturday, 9:00 AM",
                "registration_deadline": "Saturday, 9:00 AM",
            },

            "documents": [
                {
                    "name": "Hackathon Guidelines.pdf",
                    "type": "event_guidelines",
                    "status": "available",
                },
                {
                    "name": "Project Presentation.pdf",
                    "type": "project_document",
                    "status": "available",
                },
            ],
        }

        return context


# Convenient function for the orchestrator
async def gather_information(goal: str) -> Dict[str, Any]:
    agent = InformationAgent()

    return await agent.gather_context(goal)