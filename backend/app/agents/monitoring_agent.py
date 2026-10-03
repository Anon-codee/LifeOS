from typing import Dict, Any, List


class MonitoringAgent:
    """
    Monitoring Agent

    Continuously evaluates whether the current plan is still valid.

    It looks for:
    - conflicts
    - missed deadlines
    - changed events
    - dependency failures
    - travel disruptions

    If something changes, it creates a structured
    disruption that the Orchestrator can send to
    the replanning stage.
    """

    async def monitor_plan(
        self,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        issues: List[Dict[str, Any]] = []

        # Check the conflict already identified by the planner.
        conflict = plan.get("conflict", {})

        if conflict.get("detected"):
            issues.append(
                {
                    "id": "travel_conflict",
                    "type": conflict["type"],
                    "severity": conflict["severity"],
                    "title": conflict["title"],
                    "message": conflict["message"],
                    "impact": conflict["impact"],
                    "requires_replanning": True,
                }
            )

        # Check whether a critical task is still incomplete.
        for task in plan.get("tasks", []):

            if (
                task.get("priority") == "critical"
                and task.get("status") == "pending"
            ):
                issues.append(
                    {
                        "id": f"task_{task['id']}",
                        "type": "incomplete_critical_task",
                        "severity": "medium",
                        "title": f"Critical task pending: {task['title']}",
                        "message": (
                            f"The task '{task['title']}' "
                            "has not been completed."
                        ),
                        "impact": "The goal may be affected.",
                        "requires_replanning": False,
                    }
                )

        requires_replanning = any(
            issue.get("requires_replanning")
            for issue in issues
        )

        return {
            "monitoring_status": (
                "attention_required"
                if issues
                else "healthy"
            ),
            "issues": issues,
            "requires_replanning": requires_replanning,
            "issue_count": len(issues),
        }

    async def simulate_disruption(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Simulates a real-world event changing after the
        original plan was created.

        This is used for the hackathon demo.
        """

        original_arrival = context["travel"]["arrival"]["time"]

        disrupted_context = dict(context)

        disrupted_context["travel"] = {
            **context["travel"],
            "arrival": {
                **context["travel"]["arrival"],
                "time": "10:30 AM",
            },
        }

        return {
            "type": "travel_delay",
            "title": "Train delayed by 2 hours",
            "message": (
                f"Your train arrival changed from "
                f"{original_arrival} to 10:30 AM."
            ),
            "impact": (
                "The current itinerary can no longer get "
                "you to the hackathon on time."
            ),
            "requires_replanning": True,
            "updated_context": disrupted_context,
        }


async def monitor_plan(
    plan: Dict[str, Any],
    context: Dict[str, Any],
) -> Dict[str, Any]:

    agent = MonitoringAgent()

    return await agent.monitor_plan(
        plan=plan,
        context=context,
    )