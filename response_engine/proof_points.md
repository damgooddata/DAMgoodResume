# Proof Points

Verified achievements to reference in client communications. Pick the proof point that best matches the client's underlying problem. Use 1-2 per response unless a detailed case study is needed.

---

## Financial Impact

### Vendor Subsidy Platform — $25M Annual Profit
- **Problem:** Floor & Decor needed to recover costs from vendors across multiple subsidy programs (defect rates, late PO chargebacks, photo shoots, display boards, grand opening surcharges) but the process was entirely manual — one person's full-time job.
- **Solution:** Built a Python-based automation platform that processed 10,000+ vendor invoices per cycle via email-triggered workflows, SharePoint-integrated merchant audits, and automated remittance with PIM-driven access control.
- **Result:** Generated $25 million in annual profit and eliminated a full-time manual position.
- **Tags:** `automation` `python` `vendor-management` `sharepoint` `finance`

### Unpaid Rebate Recovery — $2.3M
- **Problem:** Southeastern Grocers' third-party warehouse vendor was not paying contractual rebates, and there was no systematic way to audit invoices against agreements.
- **Solution:** Developed a cost comparison tool (Python/VBA) to audit vendor invoices against contractual terms over a six-month period.
- **Result:** Uncovered and recovered $2.3 million in unpaid rebates.
- **Tags:** `audit` `python` `vba` `contract-compliance` `finance`

### DC Assignment Cost Avoidance — $93K
- **Problem:** Distribution center assignments were not optimized for cost at Interline Brands.
- **Solution:** Restructured DC assignments using data-driven analysis.
- **Result:** $93,000 in cost avoidance.
- **Tags:** `logistics` `optimization` `cost-reduction`

### LTL RFP Automation — $67K First-Year Savings
- **Problem:** LTL carrier RFP responses were processed manually, slowing negotiations.
- **Solution:** Built a custom program to automate RFP response analysis, reducing processing to under one day.
- **Result:** $67,000 in first-year cost avoidance through optimized carrier negotiations.
- **Tags:** `logistics` `automation` `procurement`

### Parcel Claims Recovery — $120K/Year
- **Problem:** Parcel shipping claims were not being systematically pursued across a $10M parcel budget.
- **Solution:** Engineered a parcel claims process with systematic tracking and recovery.
- **Result:** $120,000 recovered annually.
- **Tags:** `logistics` `claims` `process-design`

---

## Time and Efficiency

### Physical Inventory — 5 Days to 2 Days
- **Problem:** Physical inventory at Floor & Decor warehouses (1M+ sqft each) took nearly a full week, keeping the warehouse offline and blocking order fulfillment.
- **Solution:** Built real-time reconciliation reporting against Manhattan WMS data, refreshing every 15 minutes. Created error-detection formulas that identified whether counters entered eaches vs. cases, enabling immediate radio-directed recounts.
- **Result:** Reduced the full physical inventory process from nearly a week to 2 business days. Warehouse was pulling orders again by lunch on day two.
- **Tags:** `wms` `real-time` `inventory` `sql` `warehouse-operations`

### Yass Prize Review Cycle — 1 Month Faster
- **Problem:** The Yass Prize grant review for CER involved multiple peer review phases with manual Excel/Word document generation, updates, and distribution. The process was slow and error-prone.
- **Solution:** Evolved the process over 5 years: Excel cleanup to SQL database to API-driven ETL to a full React web application with admin portal, reviewer interface, and GoodGrants API integration.
- **Result:** Reduced the entire grant review period by one full month.
- **Tags:** `react` `python` `sql` `api` `nonprofit` `web-app`

### Freight Claims — 60% Faster Resolution
- **Problem:** Freight claim intake and approval was manual and slow.
- **Solution:** Built Microsoft Power Automate workflows with Power Apps Forms for structured intake and automated approval routing.
- **Result:** 60% reduction in claim resolution time.
- **Tags:** `power-automate` `power-apps` `workflow` `logistics`

### Internal Support Tickets — 35% Reduction
- **Problem:** Global Frontier Missions staff repeatedly asked the same operational questions, consuming leadership time.
- **Solution:** Engineered a RAG chatbot using Python, LangChain, vector databases (Pinecone/ChromaDB), and GPT-4o API with a FastAPI backend, grounded to internal SOPs and FAQs.
- **Result:** 35% reduction in internal support ticket volume.
- **Tags:** `ai` `rag` `python` `fastapi` `nonprofit`

---

## Operational Scale

### Warehouse Relocation — Near-Zero Loss
- **Problem:** Floor & Decor's LA warehouse needed to relocate without extended downtime. Manhattan WMS could not be used because the warehouse number was not changing.
- **Solution:** Built a supplemental WMS application supporting 10 mobile scanning stations, managing weight-based trailer loading (24,000 lb alerts), seal tracking, driver check-in/out with photo ID capture, BOL/packing list generation, and destination scanning for full chain of custody.
- **Result:** Complete warehouse relocation with near-zero product loss.
- **Tags:** `python` `vba` `warehouse` `scanning` `logistics` `chain-of-custody`

### Invoice Automation — 10,000+ Vendor Communications
- **Problem:** Vendor subsidy billing required manual calculation, Excel file creation, and individual email communication for each vendor every quarter.
- **Solution:** Automated the entire cycle: PO aggregation, subsidy calculation, merchant review via SharePoint, vendor billing, remittance file generation, and PIM-driven access control.
- **Result:** 10,000+ automated vendor communications per cycle with full audit trail.
- **Tags:** `python` `email-automation` `sharepoint` `vendor-management`

### Domestic Logistics Invoice Processing
- **Problem:** Home delivery logistics invoices from carriers required manual review, GL coding, and payment routing. The company would have needed to hire someone dedicated to this.
- **Solution:** Built an email-based automation that enforced strict invoice formatting, auto-rejected non-compliant submissions with explanations, matched invoices to customer orders, algorithmically assigned GL codes, and sent weekly summary reports for manager approval before routing to AP.
- **Result:** Saved the cost of a full-time employee. Vendors received faster payment.
- **Tags:** `python` `email-automation` `finance` `gl-coding` `logistics`

### Loss Prevention Cluster Model
- **Problem:** Stores were adjusting product to "manufacturer defect" instead of "damaged" to avoid budget impact. With 200+ stores and overseas vendors, traditional per-incident claims were impractical.
- **Solution:** Developed a fixed-rate vendor defect program with annual true-ups, plus a cluster model running every 15 minutes to flag statistically outlying adjustments for manager review. The model detected isolated adjustment patterns inconsistent with production-batch defect behavior.
- **Result:** Turned the manufacturer defect category into a profit center. Reduced store paperwork. Eliminated back-room product storage delays. Protected the company from internal misclassification.
- **Tags:** `python` `analytics` `loss-prevention` `cluster-model` `retail`

---

## Platform and Integration

### Salesforce Expense Approval — CER
- **Problem:** CER needed a multi-step expense approval process integrated across Salesforce, Bill.com, and Slack.
- **Solution:** Built orchestrated Salesforce Flows with dynamic approval hierarchy based on manager chain and request value. Custom LWC UI with granular line-item entry. Auto-provisioned vendors in Bill.com. Slack notifications with approve/reject buttons.
- **Result:** End-to-end expense-to-payment automation with full audit trail.
- **Tags:** `salesforce` `apex` `lwc` `bill.com` `slack` `flow`

### Computron — Agentic Scoping System
- **Problem:** Prospective clients needed a structured way to describe their automation needs and receive a scoping brief.
- **Solution:** Built a multi-phase automation scoping system using FastAPI, LangGraph, GPT-4o API, and Firestore. Conducts stateful multi-turn interrogation, computes weighted scores, conditionally triggers web research, and generates downloadable PDF automation briefs.
- **Result:** Automated lead qualification and scope documentation with email-validated capture.
- **Tags:** `ai` `fastapi` `langgraph` `firestore` `lead-gen`

### 30+ Manual Reports to Power BI
- **Problem:** Floor & Decor relied on 30+ manual Excel reports scattered across the organization.
- **Solution:** Led company-wide transition to dynamic Power BI dashboards, built a PO "Lifecycle" data cube, and moved to a network-scheduled environment.
- **Result:** Enhanced data accessibility and decision-making across the organization.
- **Tags:** `power-bi` `sql` `reporting` `data-cube` `etl`
