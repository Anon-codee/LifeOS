from typing import Dict, Any

from .information_agent import InformationAgent
from .planning_agent import PlanningAgent
from .monitoring_agent import MonitoringAgent


class Orchestrator:
    """
    Orchestrator

    Controls the LifeOS agent workflow:

        Goal
          ↓
        Information Agent
          ↓
        Planning Agent
          ↓
        Monitoring Agent
          ↓
        Conflict / Disruption
          ↓
        Replanning
    """

    def __init__(self):
        self.information_agent = InformationAgent()
        self.planning_agent = PlanningAgent()
        self.monitoring_agent = MonitoringAgent()

    async def run_goal(self, goal: str) -> Dict[str, Any]:
        """
        Run the complete LifeOS workflow for a new goal.
        """

        activity = []

        # --------------------------------------------------
        # 1. UNDERSTAND / GATHER
        # --------------------------------------------------

        activity.append({
            "agent": "Information Agent",
            "action": "Gathering context",
            "status": "completed",
            "description": (
                "Collecting relevant information from "
                "email, calendar, travel, documents and events."
            ),
        })

        context = await self.information_agent.gather_context(goal)

        # --------------------------------------------------
        # 2. PLAN
        # --------------------------------------------------

        activity.append({
            "agent": "Planning Agent",
            "action": "Building plan",
            "status": "running",
            "description": (
                "Converting the goal into tasks, "
                "dependencies and deadlines."
            ),
        })

        plan = await self.planning_agent.create_plan(
            goal=goal,
            context=context,
        )

        activity[-1]["status"] = "completed"

        # --------------------------------------------------
        # 3. MONITOR
        # --------------------------------------------------

        activity.append({
            "agent": "Monitoring Agent",
            "action": "Checking plan",
            "status": "running",
            "description": (
                "Checking for conflicts, dependencies "
                "and critical tasks."
            ),
        })

        monitoring = await self.monitoring_agent.monitor_plan(
            plan=plan,
            context=context,
        )

        activity[-1]["status"] = "completed"

        # --------------------------------------------------
        # 4. DETERMINE NEXT ACTION
        # --------------------------------------------------

        if monitoring["requires_replanning"]:

            next_action = "human_approval_required"
            overall_status = "needs_attention"

        else:

            next_action = "execute_plan"
            overall_status = "ready"

        return {
            "goal": goal,

            "status": overall_status,

            "context": context,

            "plan": plan,

            "monitoring": monitoring,

            "next_action": next_action,

            "activity": activity,
        }

    async def simulate_disruption(
        self,
        goal: str,
        context: Dict[str, Any],
        current_plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Simulate a real-world disruption and prepare
        the information required for replanning.
        """

        disruption = (
            await self.monitoring_agent.simulate_disruption(
                context
            )
        )

        updated_context = disruption["updated_context"]

        return {
            "goal": goal,

            "disruption": disruption,

            "updated_context": updated_context,

            "current_plan": current_plan,

            "next_action": "replan",

            "status": "replanning_required",
        }

    async def replan(
        self,
        goal: str,
        context: Dict[str, Any],
        disruption: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create a new plan after a disruption.

        For the MVP, LifeOS proposes an alternative
        travel arrangement and rebuilds the plan.
        """

        updated_context = dict(context)

        # -----------------------------------------------
        # Proposed alternative
        # -----------------------------------------------

        updated_context["travel"] = {
            **context["travel"],

            "type": "alternative_train",

            "arrival": {
                **context["travel"]["arrival"],
                "time": "7:30 AM",
                "location": "Mumbai",
            },

            "alternative": True,

            "alternative_reason": (
                "Original train is delayed and would "
                "cause the user to miss the event."
            ),
        }

        # -----------------------------------------------
        # Build new plan
        # -----------------------------------------------

        new_plan = await self.planning_agent.create_plan(
            goal=goal,
            context=updated_context,
        )

        # -----------------------------------------------
        # Monitor new plan
        # -----------------------------------------------

        new_monitoring = (
            await self.monitoring_agent.monitor_plan(
                plan=new_plan,
                context=updated_context,
            )
        )

        return {
            "goal": goal,

            "status": (
                "ready"
                if not new_monitoring["requires_replanning"]
                else "needs_attention"
            ),

            "disruption": disruption,

            "updated_context": updated_context,

            "plan": new_plan,

            "monitoring": new_monitoring,

            "next_action": (
                "execute_plan"
                if not new_monitoring["requires_replanning"]
                else "human_approval_required"
            ),

            "activity": [
                {
                    "agent": "Monitoring Agent",
                    "action": "Detected disruption",
                    "status": "completed",
                    "description": disruption["message"],
                },
                {
                    "agent": "Planning Agent",
                    "action": "Generated alternative",
                    "status": "completed",
                    "description": (
                        "Found an alternative travel arrangement "
                        "that preserves the hackathon arrival window."
                    ),
                },
                {
                    "agent": "Monitoring Agent",
                    "action": "Validated new plan",
                    "status": "completed",
                    "description": (
                        "Checked the updated plan for conflicts "
                        "and dependencies."
                    ),
                },
            ],
        }


# ------------------------------------------------------
# Convenience functions
# ------------------------------------------------------

async def run_goal(goal: str) -> Dict[str, Any]:

    orchestrator = Orchestrator()

    return await orchestrator.run_goal(goal)


async def simulate_disruption(
    goal: str,
    context: Dict[str, Any],
    current_plan: Dict[str, Any],
) -> Dict[str, Any]:

    orchestrator = Orchestrator()

    return await orchestrator.simulate_disruption(
        goal=goal,
        context=context,
        current_plan=current_plan,
    )


async def replan(
    goal: str,
    context: Dict[str, Any],
    disruption: Dict[str, Any],
) -> Dict[str, Any]:

    orchestrator = Orchestrator()

    return await orchestrator.replan(
        goal=goal,
        context=context,
        disruption=disruption,
    )