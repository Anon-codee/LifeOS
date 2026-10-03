from typing import Dict, Any, List


class PlanningAgent:
    """
    Planning Agent

    Converts gathered information into a dependency-aware plan.

    Responsibilities:
        - Create tasks
        - Build dependencies
        - Detect scheduling conflicts
        - Determine whether replanning is required
    """

    async def create_plan(
        self,
        goal: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        tasks: List[Dict[str, Any]] = [
            {
                "id": "registration",
                "title": "Complete hackathon registration",
                "category": "Event",
                "status": "completed",
                "priority": "high",
                "depends_on": [],
            },
            {
                "id": "project_submission",
                "title": "Submit final project",
                "category": "Project",
                "status": "pending",
                "priority": "critical",
                "deadline": context["email"]["project_deadline"]["deadline"],
                "depends_on": [],
            },
            {
                "id": "travel",
                "title": "Travel to Mumbai",
                "category": "Travel",
                "status": "pending",
                "priority": "high",
                "depends_on": [],
            },
            {
                "id": "hotel",
                "title": "Check into hotel",
                "category": "Accommodation",
                "status": "planned",
                "priority": "medium",
                "depends_on": ["travel"],
            },
            {
                "id": "preparation",
                "title": "Prepare for hackathon",
                "category": "Preparation",
                "status": "in_progress",
                "priority": "high",
                "depends_on": [
                    "project_submission",
                    "registration",
                ],
            },
            {
                "id": "attend_event",
                "title": "Attend hackathon",
                "category": "Event",
                "status": "planned",
                "priority": "critical",
                "depends_on": [
                    "travel",
                    "registration",
                    "preparation",
                ],
            },
        ]

        conflict = self._detect_travel_conflict(context)

        return {
            "goal": goal,
            "success_condition": (
                "User reaches the hackathon prepared and on time."
            ),
            "tasks": tasks,
            "dependencies": self._build_dependencies(tasks),
            "conflict": conflict,
            "plan_status": (
                "conflict_detected"
                if conflict["detected"]
                else "ready"
            ),
        }

    # --------------------------------------------------
    # DEPENDENCY GRAPH
    # --------------------------------------------------

    def _build_dependencies(
        self,
        tasks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        dependencies = []

        for task in tasks:

            for dependency in task.get("depends_on", []):

                dependencies.append(
                    {
                        "from": dependency,
                        "to": task["id"],
                    }
                )

        return dependencies

    # --------------------------------------------------
    # TRAVEL CONFLICT DETECTION
    # --------------------------------------------------

    def _detect_travel_conflict(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        travel = context.get("travel", {})
        event = context.get("event", {})

        arrival_time = travel.get(
            "arrival",
            {}
        ).get(
            "time"
        )

        event_start = event.get("start")

        venue_travel_minutes = travel.get(
            "venue_travel_minutes",
            0
        )

        if not arrival_time or not event_start:

            return self._no_conflict()

        # Convert times into minutes after midnight.

        arrival_minutes = self._time_to_minutes(
            arrival_time
        )

        event_minutes = self._time_to_minutes(
            event_start
        )

        if arrival_minutes is None or event_minutes is None:

            return self._no_conflict()

        estimated_venue_arrival = (
            arrival_minutes
            + venue_travel_minutes
        )

        delay_minutes = (
            estimated_venue_arrival
            - event_minutes
        )

        # ----------------------------------------------
        # Conflict detected
        # ----------------------------------------------

        if delay_minutes > 0:

            return {
                "detected": True,

                "type": "travel_event_conflict",

                "severity": (
                    "critical"
                    if delay_minutes >= 30
                    else "high"
                ),

                "title": (
                    "Travel arrival conflicts "
                    "with hackathon start"
                ),

                "message": (
                    f"Estimated arrival at venue is "
                    f"{self._minutes_to_time(estimated_venue_arrival)}, "
                    f"but the hackathon starts at "
                    f"{event_start}."
                ),

                "impact": (
                    f"User may arrive approximately "
                    f"{delay_minutes} minutes late."
                ),

                "arrival_time": arrival_time,

                "event_start": event_start,

                "venue_travel_minutes": venue_travel_minutes,

                "estimated_venue_arrival": (
                    self._minutes_to_time(
                        estimated_venue_arrival
                    )
                ),

                "delay_minutes": delay_minutes,
            }

        # ----------------------------------------------
        # No conflict
        # ----------------------------------------------

        return self._no_conflict()

    # --------------------------------------------------
    # TIME HELPERS
    # --------------------------------------------------

    def _time_to_minutes(
        self,
        time_string: str,
    ) -> int | None:

        try:

            # Remove date information if present.
            # Example:
            # "Saturday, 9:00 AM" → "9:00 AM"

            if "," in time_string:

                time_string = (
                    time_string
                    .split(",")[-1]
                    .strip()
                )

            parts = time_string.split()

            if len(parts) != 2:
                return None

            time_part = parts[0]
            period = parts[1].upper()

            hour, minute = map(
                int,
                time_part.split(":")
            )

            if period == "PM" and hour != 12:
                hour += 12

            if period == "AM" and hour == 12:
                hour = 0

            return hour * 60 + minute

        except (ValueError, AttributeError):

            return None

    def _minutes_to_time(
        self,
        minutes: int,
    ) -> str:

        minutes = minutes % (24 * 60)

        hour = minutes // 60
        minute = minutes % 60

        period = "AM"

        if hour >= 12:
            period = "PM"

        display_hour = hour % 12

        if display_hour == 0:
            display_hour = 12

        return f"{display_hour}:{minute:02d} {period}"

    # --------------------------------------------------
    # EMPTY CONFLICT
    # --------------------------------------------------

    def _no_conflict(self) -> Dict[str, Any]:

        return {
            "detected": False,
            "type": None,
            "severity": None,
            "title": None,
            "message": None,
            "impact": None,
        }


# ------------------------------------------------------
# Convenience function
# ------------------------------------------------------

async def create_plan(
    goal: str,
    context: Dict[str, Any],
) -> Dict[str, Any]:

    agent = PlanningAgent()

    return await agent.create_plan(
        goal=goal,
        context=context,
    )