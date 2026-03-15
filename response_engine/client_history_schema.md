# Client History Schema

This file defines the structure for logging client communications. Each client gets their own directory under `client_logs/`. Communication history enables the bot to personalize responses and measure effectiveness over time.

---

## Directory Structure

```
response_engine/
  client_logs/
    {client_name}/
      profile.md          # Client profile and preferences
      communication_log.md # Chronological log of all interactions
```

---

## Client Profile Template

Create `profile.md` for each new client:

```markdown
# Client Profile: {Client Name}

## Basic Info
- **Company:** {Company name}
- **Contact:** {Primary contact name}
- **Role:** {Their role/title}
- **Industry:** {Their industry}
- **Source:** {How they found David — Upwork, referral, LinkedIn, etc.}
- **First Contact:** {Date}
- **Status:** {Active / Completed / Paused / Lost}

## Their Business
- **What they do:** {Brief description}
- **Team size:** {Approximate}
- **Tech stack:** {What they currently use}

## Their Pain Points
- {Pain point 1}
- {Pain point 2}
- {Pain point 3}

## What They Value
- {What matters most to them — speed, cost, quality, simplicity, etc.}

## Communication Preferences
- **Tone preference:** {Formal / Casual / Technical / Non-technical}
- **Response length:** {Brief / Detailed}
- **Preferred channel:** {Email / Slack / Platform messages}

## Notes
- {Any relevant context — budget constraints, timeline pressure, past bad experiences, etc.}
```

---

## Communication Log Template

Create `communication_log.md` for each client:

```markdown
# Communication Log: {Client Name}

## Entry Format

Each entry follows this structure:

---

### {Date} — {Direction: Inbound/Outbound} — {Channel: Email/Upwork/Slack/etc.}

**Context:** {What prompted this communication}

**Summary:** {1-2 sentence summary of the message}

**Message Type:** {Proposal / Follow-up / Scope Discussion / Status Update / Close}

**Response Style Used:** {Template name from response_templates.md, or "Custom"}

**Key Points Made:**
- {Point 1}
- {Point 2}

**Proof Points Referenced:** {Which proof points from proof_points.md were used, if any}

**Client Reaction:** {Positive / Neutral / Negative / No Response}

**Effectiveness Notes:** {What worked, what didn't, what to adjust next time}

**Follow-Up Needed:** {Yes/No — if yes, what and by when}

---
```

---

## Effectiveness Tracking Fields

Over time, these fields enable pattern analysis:

| Field | Purpose |
|-------|---------|
| **Response Style Used** | Track which templates perform best per client |
| **Proof Points Referenced** | Track which proof points resonate most |
| **Client Reaction** | Measure response effectiveness |
| **Effectiveness Notes** | Capture qualitative feedback for style tuning |
| **Message Type** | Analyze what stage of the pipeline communications fall in |

---

## Metrics to Track Per Client

When enough history accumulates, analyze:

- **Response rate:** What % of outbound messages get a reply?
- **Conversion rate:** What % of proposals lead to engagement?
- **Best-performing proof points:** Which achievements resonate with this client type?
- **Optimal response length:** Does this client prefer brief or detailed?
- **Tone effectiveness:** Which tonal approach gets the best reaction?
- **Time to response:** How quickly does the client reply?

---

## Aggregate Analysis

Across all clients, periodically review:

- Which **industries** have the highest conversion rate?
- Which **proof points** are used most and convert best?
- Which **response templates** produce the most positive reactions?
- What **message length** correlates with engagement?
- Are there **tone adjustments** that consistently improve outcomes?

Store aggregate findings in `response_engine/effectiveness_insights.md` (create when enough data exists).

---

## Example Entry

```markdown
### 2026-03-15 — Outbound — Upwork

**Context:** Client posted looking for Salesforce + API integration help

**Summary:** Submitted proposal highlighting CER expense approval system and multi-platform integration experience.

**Message Type:** Proposal

**Response Style Used:** Short Proposal Reply

**Key Points Made:**
- Built Salesforce + Bill.com + Slack approval automation for a nonprofit
- Approach starts with workflow mapping before building

**Proof Points Referenced:** Salesforce Expense Approval — CER

**Client Reaction:** Positive — invited to interview

**Effectiveness Notes:** Leading with nonprofit experience resonated. Client mentioned they appreciated the "workflow first" framing.

**Follow-Up Needed:** Yes — interview scheduled for 2026-03-18
```

---

## Getting Started

1. Create `response_engine/client_logs/` directory
2. For each new client, create a subdirectory with their name
3. Add `profile.md` and `communication_log.md` using the templates above
4. Update the log after every interaction
5. Review patterns monthly to refine approach
