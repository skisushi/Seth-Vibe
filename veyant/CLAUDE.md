# Veyant.ai - Project Briefing for Claude Code

## Who We Are

Veyant is building AI orchestration infrastructure for corporate travel. The founder is Seth Horowitz (goes by Seth or Burton interchangeably in docs), CEO with 20+ years in airline technology including 60+ Passenger Service System (PSS) implementations globally at Navitaire/Amadeus.

Contact: seth@veyant.ai  
Status: Pre-seed fundraising, prototype development  
Based: Salt Lake City, Utah

---

## The Problem We Are Solving

AI agents (ChatGPT, Google AI, Claude) can SEARCH for travel options but cannot complete a booking. They are missing three things:

1. Traveler credentials and loyalty account access
2. Corporate travel policies and approval workflows
3. Live supplier API connectivity to actually transact

The result: 83% of TMC (Travel Management Company) service tickets are handled manually at $20+ per call. This is the "Discovery Bridge" problem -- AI stops at discovery and cannot cross to booking and servicing.

This is not a UI problem. It is an infrastructure problem. Veyant is the infrastructure.

---

## The Solution: Three-Cube Architecture

Veyant provides the missing layer through three data domains:

**My Travel Cube (the Brain)**
Owned by the traveler. Contains personal preferences, loyalty program credentials (airline status, hotel points), calendar data, past booking behavior, and ML-based predictions.

**Corporate Cube**
Owned by the company. Contains travel policy rules, negotiated supplier rates, preferred vendors, approval workflow configuration, and budget constraints.

**Supplier Cube (the Bridge)**
Owned by Veyant. Contains NDC and GDS API connectivity, live airline/hotel/car inventory access, real-time pricing, and transaction execution capability.

When all three cubes are available to the AI agent simultaneously, it can move from discovery to booking. That is the Discovery Bridge.

---

## December Prototype Goal

Build a demo-quality prototype that proves the concept to investors and TMC partners. This is NOT a production system. It is a compelling demo.

**Primary Success Metric:** An investor or TMC CTO watches the demo and says "when can we pilot this?"

**North Star Demo Scenario -- Sarah Chen:**

Traveler profile:
- Name: Sarah Chen
- Company: Acme Corp  
- Loyalty: SkyTeam Platinum Elite, Marriott Platinum
- Current trip: Boston to London (3 nights)

Initial request (natural language):
> "Please extend my London trip one day for extra meetings, and add a NYC stop to meet with a client with an escalated issue. Please get me the same room, best seats and upgrades."

The system should parse this multi-intent request, show transparent processing steps in real time, and present a complete solution in the Travel Cockpit dashboard -- including cost impact, policy compliance status, and automatically applied loyalty benefits.

**Target time:** 20-30 seconds end to end vs 25-30 minutes of manual TMC work.

---

## Technology Stack

| Layer | Technology | Why |
|---|---|---|
| Infrastructure | Azure PaaS | Founder's Navitaire background; integrated AI services |
| AI Engine | Anthropic Claude API (claude-sonnet-4-20250514) | Longer context window, better reasoning, commercial partnership potential |
| Agent Orchestration | KaibanJS | Visual Kanban board makes agent workflow visible during demo -- critical for investor storytelling. Plan to migrate to LangGraph post-prototype. |
| Primary Database | Azure Cosmos DB | Sub-10ms latency required for real-time agent coordination. Databricks was evaluated but has 1+ second latency (analytics use case, wrong tool). |
| Auth | OAuth / OIDC | Standard enterprise auth for supplier connectivity |
| Security | Azure Key Vault, AES-256 | Five-layer defense model |
| Analytics (future) | Azure Databricks | Post-prototype for data platform work |

---

## Agent Architecture (KaibanJS)

Five agents run in sequence via KaibanJS orchestration. The Kanban board visualization of these agents moving through states is a key demo element -- it makes the invisible visible.

**Agent 1: Context Agent (BRAIN)**
Gathers all traveler data from My Travel Cube. Loyalty status, preferences, calendar flexibility, past booking patterns. The BRAIN predicts the optimal solution without needing to search 47 options -- it already knows what the traveler wants.

**Agent 2: Policy Agent**
Fetches relevant corporate policy rules from the Corporate Cube. Validates the proposed solution for compliance. Routes exceptions to the appropriate approver if needed. Must complete in under 3 seconds.

**Agent 3: Search Agent**
Queries supplier inventory via the Supplier Cube. For the prototype this uses mock data. In production this hits live NDC/GDS APIs with real credentials.

**Agent 4: Booking Agent (BRIDGE)**
Executes the actual transaction using stored supplier credentials. Applies loyalty benefits automatically (elite status perks, points redemption, upgrade eligibility). This is the agent that crosses the Discovery Bridge.

**Agent 5: Notification Agent**
Updates the traveler with a summary. Updates the calendar with new itinerary details. Logs the completed workflow for audit.

KaibanJS task dependency chain: Context -> Policy -> Search -> Booking -> Notification. Each task declares its dependencies explicitly.

---

## Prototype Scope (December -- what to build)

**In scope:**

- Conversational AI chat interface (natural language input)
- Step-by-step transparent processing display (real-time agent status)
- Travel Cockpit dashboard (trip visualization, disruption alerts, alternatives)
- Mock data system for all three cubes (traveler, corporate, supplier data)
- Sarah Chen demo scenario end to end
- KaibanJS Kanban board visualization

**Explicitly out of scope for prototype:**

- Live supplier API integrations (use mock data only)
- Production-grade security and authentication (demo credentials only)
- Multi-tenant architecture (single tenant mock)
- Admin console beyond view-only mockups
- Mobile optimization beyond responsive web
- Real-time disruption monitoring (trigger manually for demo)
- PCI payment processing (not needed for prototype)
- E5/E6 epics: Platform Security and Developer APIs

If a feature is not on the Sarah Chen critical path, it goes to the parking lot.

---

## Epic Structure

The backlog has 6 epics. Only E1-E4 are December scope.

**E1: Conversational AI Interface** -- the chat experience (6 features, 19 user stories)  
**E2: Transparent Processing Display** -- step-by-step agent progress visible to user  
**E3: Travel Cockpit Dashboard** -- visual trip management (4 features, 14 user stories)  
**E4: Mock Data System** -- foundational data for all testing (5 features, 13 user stories)  
**E5: Demo Scenario Implementation** -- Sarah Chen scenario specifically (5 features, 17 user stories)  
**E6+: Out of scope for December**

Mock data (E4) is the critical path dependency. Build it first. Nothing else can be tested without it.

---

## Sprint Plan

**Week 1 (Foundation):** Mock data system, basic chat interface, trip dashboard skeleton  
**Week 2 (Core Intelligence):** NLP intent parsing, context display, processing steps visualization, alternative generation  
**Week 3 (Demo Scenario):** Sarah Chen setup, request processing, alternative generation, policy compliance, loyalty benefits  
**Week 4 (Polish):** UX refinement, demo script testing, bug fixes, visual polish

---

## Data Model Overview

### My Travel Cube (mock JSON structure)
```json
{
  "travelerId": "sarah-chen-001",
  "profile": { "name": "Sarah Chen", "company": "acme-corp" },
  "loyalty": {
    "airline": { "program": "SkyTeam", "status": "Platinum Elite", "credentials": "mock" },
    "hotel": { "program": "Marriott Bonvoy", "status": "Platinum", "credentials": "mock" }
  },
  "preferences": { "seat": "aisle", "hotel": "king-quiet-floor", "meal": "standard" },
  "calendar": { "source": "mock", "events": [] }
}
```

### Corporate Cube (mock JSON structure)
```json
{
  "companyId": "acme-corp",
  "policy": {
    "maxFlightCost": 3000,
    "hotelNightlyCap": 350,
    "requiresApprovalAbove": 5000,
    "preferredAirlines": ["Delta", "United", "British Airways"],
    "preferredHotels": ["Marriott", "Hilton"]
  },
  "approvalWorkflow": { "approver": "manager@acme.com", "autoApproveBelow": 2000 }
}
```

### Supplier Cube (mock JSON structure)
```json
{
  "flights": [ /* mock flight options with pricing and availability */ ],
  "hotels": [ /* mock hotel options */ ],
  "processingSimulation": {
    "steps": [ /* ordered array of processing steps with realistic timing */ ]
  }
}
```

---

## Payment Architecture (Important Constraint)

Veyant orchestrates payments but never processes them. Zero PCI compliance scope. This is intentional and strategic.

For the December prototype: use supplier-stored credentials pattern. The AI agent hands off to the supplier's stored payment method. No card data passes through Veyant systems ever.

Do not build any payment processing capability. If a feature requires touching raw card data, flag it and park it.

---

## Suggested Project Structure

```
/veyant-prototype
  /src
    /agents
      baseAgent.js          -- VeyantAgent class extending KaibanJS Agent
      contextAgent.js       -- BRAIN: traveler data assembly
      policyAgent.js        -- policy compliance checking
      searchAgent.js        -- inventory query (mock supplier calls)
      bookingAgent.js       -- BRIDGE: transaction execution
      notificationAgent.js  -- traveler updates and calendar sync
    /tasks
      contextTask.js
      policyTask.js
      searchTask.js
      bookingTask.js
      notificationTask.js
    /tools
      travelerProfileTool.js
      policyLookupTool.js
      flightSearchTool.js
      hotelSearchTool.js
      bookingExecutionTool.js
    /data
      /mock
        traveler-sarah-chen.json
        corporate-acme.json
        supplier-flights.json
        supplier-hotels.json
        processing-steps.json
    /components
      ChatInterface.jsx       -- conversational AI entry point
      ProcessingDisplay.jsx   -- real-time agent step visualization
      TravelCockpit.jsx       -- trip dashboard
      KanbanBoard.jsx         -- agent workflow visualization
      AlternativeCard.jsx     -- individual option display
    /api
      orchestration.js        -- KaibanJS team and workflow setup
  /public
  CLAUDE.md                   -- this file
  README.md
```

---

## Coding Guidelines

- JavaScript / React for frontend (confirm with dev if Vue is preferred -- this is TBD)
- KaibanJS for agent orchestration -- import from 'kaibanjs'
- Anthropic model: `claude-sonnet-4-20250514`
- All mock data lives in `/src/data/mock/` as JSON files
- No hardcoded credentials anywhere -- use environment variables
- Processing step timing should feel realistic (not instant) -- use simulated delays that match the narrative of what the agent is "doing"
- Console log agent execution in structured JSON format (this becomes training data)
- Keep components simple and focused -- we are building a demo, not a production app
- Error handling: catch gracefully and show user-friendly messages, do not crash the demo

---

## Design Philosophy

- Clean, minimalist interface -- clarity and speed over visual complexity
- Progressive disclosure -- show what the user needs, hide everything else
- Context awareness must be visible -- the system should clearly "know" Sarah's loyalty status, company policies, and preferences without her having to re-enter them
- Transparent processing -- users see each step the AI is taking, with realistic timing. This is what differentiates Veyant from a black-box AI response.
- The Kanban board is a demo feature as much as a technical feature -- it should look compelling on screen share

---

## What Makes a Good Build Decision

Ask: does this help the Sarah Chen demo work compellingly? If yes, build it. If no, park it.

The prototype succeeds if someone watching it says:
- "This actually understands context"
- "This would save us hours per service request"
- "I can see how it bridges the discovery gap"
- "When can we pilot this?"

---

## Competitive Moat (Context for Architectural Decisions)

The 80/20 rule: 80% of Veyant's value is connectivity expertise (60+ airline PSS implementations is the moat), 20% is AI orchestration (increasingly commoditized). Build decisions should reflect this. Don't over-engineer the AI layer. The hard part is the connectivity and credential management, not the LLM reasoning.

Veyant is not another AI travel chatbot. It is the infrastructure layer that makes AI travel agents actually work. Middleware. The Switzerland of travel AI -- neutral orchestration that works across all suppliers, TMCs, and AI providers.

---

## Design Reference: Wireframes

Two HTML wireframes are included in the repo as design intent references. Treat them as the target, not as code to copy verbatim. The component architecture should be built from scratch following these as a visual and UX guide.

**wireframe_1_chat_interface.html -- Primary interface, highest priority**

Three-column layout:
- Left sidebar: conversation history list (previous sessions)
- Center: main chat area (user messages, agent responses, processing steps display)
- Right panel: Active Context (traveler profile, loyalty accounts, policy constraints -- always visible)

Key design decisions to preserve:
- Font: Plus Jakarta Sans
- Brand color: `#2563EB` (Veyant blue)
- Background: `#F8FAFC` (off-white, not pure white)
- User message bubbles: blue (`#2563EB`)
- Agent response bubbles: light gray (`#F1F5F9`)
- Processing steps display: amber/yellow background (`#FEF3C7`) to visually distinguish from regular messages
- Processing step states: completed (green checkmark), active (animated dots), pending (bullet)
- Quick action buttons below input field (e.g. "Proceed with booking", "Show alternatives")
- Demo state switcher banner at the bottom (Empty / Processing / Complete / Error) -- critical for demo control
- The context panel on the right is always visible and labeled "Active Context" with a "Live" badge -- this is what proves the system "knows" the traveler

**wireframe_2_trip_cockpit.html -- Dashboard view, second priority**

Visual trip management dashboard that surfaces after the AI processes a request. Key elements:
- Alert system for at-risk trip segments (red alert styling: `#FEF2F2` background, `#FECACA` border)
- Alternative options presented in green cards (`#ECFDF5` background, `#6EE7B7` border)
- Consistent color system with the chat interface (same CSS variables)
- Same font and brand palette

**wireframe_3_corporate_policy_manager.html -- Secondary priority**

Policy management view. Not on the Sarah Chen critical path for December but include as a nav item if time permits. Do not build the underlying functionality -- a view-only mockup is sufficient.

**wireframe_4_data_firewall.html -- Do not build for prototype**

Security and data architecture view. Parking lot. Do not include in December scope.

### Design System (CSS Variables -- use these consistently across all components)

```css
--veyant-blue: #2563EB;
--veyant-blue-light: #3B82F6;
--veyant-blue-dark: #1D4ED8;
--success-green: #10B981;
--warning-yellow: #F59E0B;
--error-red: #EF4444;
--bg-light: #F8FAFC;
--bg-white: #FFFFFF;
--border-color: #E2E8F0;
--text-primary: #1E293B;
--text-secondary: #64748B;
--text-muted: #94A3B8;
--user-bubble: #2563EB;
--agent-bubble: #F1F5F9;
--processing-bg: #FEF3C7;
--alert-bg: #FEF2F2;
--alert-border: #FECACA;
--alternative-bg: #ECFDF5;
--alternative-border: #6EE7B7;
```

Font: `'Plus Jakarta Sans'` -- import from Google Fonts.

---

## Parking Lot (Good Ideas, Not December)

- Real LLM integration with live API calls (using scripted mock responses for prototype)
- Live NDC/GDS supplier API connections
- Production authentication and SSO
- Multi-tenant data isolation
- Admin console
- Mobile apps
- Proactive disruption monitoring (trigger manually in demo)
- Virtual card payment orchestration (Q1 2026)
- Open source Veyant.org foundation (post-funding)
- LangGraph migration from KaibanJS (post-prototype)

---

## Key Documents (Reference)

- `Veyant_Architecture_Overview.docx` -- master technical reference
- `Veyant_Prototype_Requirements_v1.docx` -- full requirements with Sarah Chen scenario detail
- `Veyant_KaibanJS_Implementation_Guide.docx` -- agent implementation specifics
- `Veyant_Technical_Architecture_Requirements_v2.docx` -- open technical questions and stack rationale
- `veyant_backlog_import.csv` -- full backlog with story points and sprint assignments

---

*Last updated: February 2026 | Status: Pre-seed | Contact: seth@veyant.ai*
