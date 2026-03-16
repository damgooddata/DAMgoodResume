# Client Profile: JJ Motorsports

## Basic Info
- **Company:** JJ Motorsports (jj-motorsports.com)
- **Contact:** Dustin Hammerle
- **Role:** Director of eCommerce
- **Industry:** Motorsports / eCommerce / Retail (helmets, gear, accessories)
- **Source:** Upwork — Public posting ("Power Query and Access Automation")
- **First Contact:** March 3, 2026 (job posted); first direct message March 3, 2026
- **Status:** Active — Proposal Sent, Awaiting Decision
- **Contract Rate:** $4,700 fixed price proposed (client budget: $1,200–$2,500)
- **Contract Limit:** N/A — fixed price project
- **Contract Start:** Not yet contracted
- **NDA:** None signed
- **LinkedIn:** https://www.linkedin.com/in/dustin-hammerle-8548081a7/
- **Education:** University of Michigan

## Their Business
- **What they do:** eCommerce retailer in the motorsports/powersports space — sells helmets, gear, and accessories through a BigCommerce storefront. Manages a large multi-supplier catalog (~750k SKU rows across 4 suppliers).
- **Team size:** Unknown — Dustin appears to be the primary eCommerce decision-maker; likely a small-to-mid-size operation
- **Tech stack:**
  - BigCommerce (storefront and product catalog)
  - Spark Shipping (current supplier feed management — $250/mo, looking to replace)
  - CSV/Excel flat files from 4 suppliers
  - Power Query / Microsoft Access (client's preferred tooling in original ask)
  - OneDrive (file storage)
  - Power Automate (client mentioned as optional)

## Their Pain Points
- Currently paying $250/month for Spark Shipping to manage supplier feed imports — wants to eliminate this recurring cost
- 750k+ SKU rows across 4 supplier feeds need to be cleaned, grouped by ParentKey, and formatted for BigCommerce import
- BigCommerce CSV import has a 10k row per file limit — requires manual batching
- No delta sync — full catalog re-imports are slow and inefficient
- Manual CSV formatting and uploads are error-prone and time-consuming
- Catalog is expected to grow, and current approach does not scale well
- Needs variant/option grouping logic (e.g., one helmet in multiple sizes = parent product + size variants)

## What They Value
- **Cost savings** — primary motivation is eliminating the $250/mo Spark Shipping fee; set a $1,200–$2,500 budget
- **Reliability** — wants something that works consistently without manual intervention
- **Scalability** — mentioned concern about catalog growing beyond current tooling capacity
- **Documentation & training** — explicitly requested full documentation, 1-hour screen-share training, and handover file
- **Proven experience** — asked for similar project links/screenshots and proof of handling 100k+ row catalogs
- **Ownership** — wants a one-time build he controls, not another SaaS dependency

## Communication Preferences
- **Tone preference:** Professional but casual — comfortable asking for phone calls, brief messages
- **Response length:** Moderate — engages with detailed proposals but prefers direct conversation for complex topics
- **Preferred channel:** Upwork messages for async; prefers phone/Zoom calls for discussion (asked to do phone call instead of Zoom initially)
- **Scheduling:** Responsive — scheduled a call same day; willing to work around constraints
- **Tech comfort:** Familiar with eCommerce tools and data concepts (BigCommerce CSV imports, Power Query, APIs) but not a developer

## Dustin's Communication Patterns
Mirror these when drafting messages:
- Brief, direct messages: "Do you have time today?"
- Asks practical questions: "would this be on a token plan that we would have to subscribe for use"
- Comfortable with informal scheduling: "can we do call over phone call? instead of Zoom"
- Responds to detailed proposals with specific follow-up questions rather than broad feedback
- Signs off without formal closings in chat

## David's Tone Adjustments for This Client
- Keep proposals detailed but structured — Dustin engages with specifics when organized clearly
- Lead with cost savings and ROI framing — this is his primary decision driver
- Use phase-based breakdowns to make larger scope digestible
- Offer calls proactively — Dustin prefers verbal discussion for complex topics
- Frame the upsell (API architecture vs. Power Query) as a long-term business decision, not a technical preference
- Include concrete comparisons (Spark Shipping cost vs. build cost vs. 3-year savings)

## Known Triggers to Avoid
- **Budget shock without context:** The proposal came in at nearly 2x his stated budget ceiling — always pair higher pricing with clear ROI math and cost-of-ownership comparisons
- **Dismissing his original approach:** Dustin asked for Power Query/Access — David offered a better path but must always validate the original ask as viable too
- **Overcomplicating the tech:** Dustin understands eCommerce operations, not cloud architecture — keep Azure/API explanations grounded in business outcomes
- **Ignoring his timeline:** He wants this built, not workshopped — keep momentum and avoid long discovery phases

## Notes
- Project scope evolved significantly between initial posting and post-call proposal: original ask was Power Query/Access CSV batching; David proposed a full Azure-based API automation service with 4 phases
- Dustin sent two documents after the call (Mar 7): "Database Project (1).docx" (his requirements list) and "Suppliers Data.docx" (supplier feed details)
- David's proposal includes 4 phases: (1) Supplier API Integration & Data Pipeline, (2) BigCommerce Sync & Catalog Logic, (3) Assortment Management Web App, (4) AI Product Descriptions / RAG
- 6-month break/fix warranty included in proposal (above industry standard of 30–90 days)
- AI product description feature uses token-based API billing — Dustin asked about ongoing costs; David explained batch pricing ($10–$250 per 20k descriptions depending on model)
- Key ROI argument: Spark Shipping at 4 suppliers = ~$500/mo ($6K/year); David's solution hosting = $30–60/mo; build pays for itself within first year, $5K+ annual savings thereafter
- Dustin went to University of Michigan — use Michigan sports as ice-breaker in follow-ups
- Follow-up sent March 10 — no response yet as of last message exchange (March 10)
- Dustin's last message was March 10 asking about AI token costs — David responded same day with detailed cost breakdown
