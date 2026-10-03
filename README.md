# LifeOS — Hackathon Prototype

A frontend-only, hackathon demo of the LifeOS autonomous personal operations agent.

## Demo flow

1. Open `index.html` in a browser.
2. The dashboard shows an active goal: **Attend Hackathon in Mumbai**.
3. Click **Review** / **View Options** under the travel conflict.
4. Choose an alternative train.
5. LifeOS displays **Plan changed. Replanning...** and then updates the dashboard.
6. You can also edit the goal at the top and click the arrow to replay the agent workflow.

## What is simulated

The prototype simulates email, calendar, document and travel sources. No real accounts or bookings are accessed. This keeps the demo safe and reliable while demonstrating the agent loop: **understand → gather → plan → execute → monitor → replan → human approval**.

## Files

- `index.html` — dashboard and modal UI
- `styles.css` — responsive visual design
- `app.js` — interactive agent workflow
