import reflex as rx
from .data_store import (
    SESSION_1_QUIZ,
    SESSION_2_QUIZ,
    SESSION_3_QUIZ,
    SESSION_4_QUIZ,
    SESSION_5_QUIZ,
    SESSION_6_QUIZ,
    SESSION_7_QUIZ,
)

# Helper styles
BOX_STYLE = {
    "background_color": "#1e293b",
    "border": "1px solid #334155",
    "border_radius": "12px",
    "padding": "20px",
    "width": "100%",
    "margin_bottom": "16px",
}

EXPANDER_STYLE = {
    "background_color": "#0f172a",
    "border": "1px solid #1e293b",
    "border_radius": "8px",
    "padding": "16px",
    "width": "100%",
    "margin_bottom": "12px",
}

# Cross-platform compatible alert box replacement
def render_alert(text: str, color_scheme: str = "blue") -> rx.Component:
    if color_scheme == "red":
        bg, border, text_color = "rgba(239, 68, 68, 0.15)", "1px solid rgba(239, 68, 68, 0.3)", "#fca5a5"
    elif color_scheme == "green":
        bg, border, text_color = "rgba(16, 185, 129, 0.15)", "1px solid rgba(16, 185, 129, 0.3)", "#a7f3d0"
    elif color_scheme == "yellow":
        bg, border, text_color = "rgba(245, 158, 11, 0.15)", "1px solid rgba(245, 158, 11, 0.3)", "#fde047"
    else: # blue
        bg, border, text_color = "rgba(59, 130, 246, 0.15)", "1px solid rgba(59, 130, 246, 0.3)", "#bfdbfe"
        
    return rx.box(
        rx.text(text, color=text_color, font_size="13px", font_weight="600"),
        background_color=bg,
        border=border,
        border_radius="6px",
        padding="10px 14px",
        width="100%",
        margin_top="4px",
        margin_bottom="4px",
    )

# Session 1: Systems Thinking Sandbox
def session_1_sandbox(state):
    return rx.vstack(
        rx.heading("🎮 Interactive Sandbox: Feedback Loops & Trade Requirements", size="4", color="#38bdf8", margin_bottom="8px"),
        
        # Panic buying simulator
        rx.vstack(
            rx.text("🔄 Simulator: Panic Buying Reinforcing Loop", font_weight="bold", color="#f8fafc"),
            rx.text("Simulate how positive feedback loops lead to stock depletion and how negative loops restore balance.", font_size="13px", color="#94a3b8"),
            
            rx.vstack(
                rx.text("Apply Stabilization Policy (Negative Loop):", font_size="13px", color="#f8fafc"),
                rx.select(
                    ["None (Runaway Panic)", "Rationing Rules (Cap allocations)", "Price Ceiling Controls"],
                    value=state.s1_policy,
                    on_change=state.set_s1_policy,
                    size="2",
                ),
                rx.text(f"Initial Panic Level: {state.s1_panic_level}", font_size="13px", color="#f8fafc"),
                rx.slider(
                    value=[state.s1_panic_level],
                    min_value=1,
                    max_value=10,
                    on_change=state.set_s1_panic_level,
                ),
                width="100%",
                spacing="2",
                align_items="start",
            ),
            
            # Simulation Run Results
            rx.vstack(
                rx.text("Simulation Run (5 Days Stock Reserves Output):", font_weight="bold", font_size="13px", color="#f8fafc", margin_top="12px"),
                rx.cond(
                    state.s1_stock_depleted,
                    render_alert("🚨 System Failure: Food/Resource stock depleted due to runaway buying loop!", "red"),
                    render_alert("✅ System Stabilized: Reserves maintained through the balancing feedback loop.", "green")
                ),
                rx.text(f"Day 5 Final Stock Reserves: {state.s1_final_stock}%", font_size="13px", color="#34d399"),
                width="100%",
                align_items="start",
            ),
            style=EXPANDER_STYLE,
            align_items="start",
        ),
        
        # Requirements Classifier
        rx.vstack(
            rx.text("📝 Lab: Requirements Classification Matrix", font_weight="bold", color="#f8fafc"),
            rx.text("Select and classify the trade system requirements based on syllabus guidelines:", font_size="13px", color="#94a3b8"),
            rx.select(
                [
                    "Clerk must record every grain allocation.",
                    "Access tokens must be encrypted.",
                    "Ledger must support 10,000 active users.",
                    "Portal screen must load in under 2 seconds.",
                    "Ledger must be readable by local supervisors."
                ],
                value=state.s1_req_item,
                on_change=state.set_s1_req_item,
                size="2",
                width="100%",
            ),
            rx.radio(
                ["Functional Requirement", "Non-Functional: Security/Performance", "Human-Centered Design"],
                value=state.s1_req_class,
                on_change=state.set_s1_req_class,
                direction="row",
                spacing="3",
                margin_top="8px",
            ),
            rx.cond(
                state.s1_req_correct,
                rx.text("🎯 Correct! Well done.", color="#10b981", font_size="13px", font_weight="600"),
                rx.text("ℹ️ Select the correct category matching slide definitions.", color="#38bdf8", font_size="13px")
            ),
            style=EXPANDER_STYLE,
            align_items="start",
        ),
        width="100%",
        align_items="start",
    )

# Session 2: Ethical Decision Sandbox
def session_2_sandbox(state):
    return rx.vstack(
        rx.heading("🎮 Interactive Sandbox: Ethical Governance & AI Decision Maker", size="4", color="#38bdf8", margin_bottom="8px"),
        rx.vstack(
            rx.text("⚖️ Manager Tool: Ethical Assessment Matrix", font_weight="bold", color="#f8fafc"),
            rx.text("Run a proposed technology deployment through the 4-Question Ethical Checklist.", font_size="13px", color="#94a3b8"),
            
            rx.select(
                [
                    "Workplace biometric scans to access trade ledgers",
                    "AI automated rationing based on biometric data",
                    "Public community trade logging board"
                ],
                value=state.s2_proposal,
                on_change=state.set_s2_proposal,
                size="2",
                width="100%",
                margin_bottom="12px",
            ),
            
            rx.checkbox("Q1: Is it compliant with local privacy laws?", checked=state.s2_q1, on_change=state.set_s2_q1, color_scheme="teal", margin_bottom="6px"),
            rx.checkbox("Q2: Is it fair and free from system bias?", checked=state.s2_q2, on_change=state.set_s2_q2, color_scheme="teal", margin_bottom="6px"),
            rx.checkbox("Q3: Is this the minimum intrusion necessary?", checked=state.s2_q3, on_change=state.set_s2_q3, color_scheme="teal", margin_bottom="6px"),
            rx.checkbox("Q4: Do benefits outweigh long-term tracking risks?", checked=state.s2_q4, on_change=state.set_s2_q4, color_scheme="teal", margin_bottom="12px"),
            
            rx.hstack(
                rx.text(f"Ethical Alignment Score: {state.s2_score} / 4", font_weight="bold", color="#f8fafc"),
                spacing="2",
            ),
            rx.cond(
                state.s2_score == 4,
                render_alert("🚀 Proposal APPROVED. Fully compliant with managerial ethics guidelines.", "green"),
                rx.cond(
                    state.s2_score >= 2,
                    render_alert("⚠️ Revision needed. Integrate safeguards or reduce data scope.", "yellow"),
                    render_alert("❌ Proposal REJECTED. High ethical risk. Redesign system rules.", "red")
                )
            ),
            style=EXPANDER_STYLE,
            align_items="start",
            width="100%",
        ),
        width="100%",
        align_items="start",
    )

# Session 3: SDLC Selector Sandbox
def session_3_sandbox(state):
    return rx.vstack(
        rx.heading("🎮 Interactive Sandbox: SDLC Model Matcher & DIKW Builder", size="4", color="#38bdf8", margin_bottom="8px"),
        rx.vstack(
            rx.text("🎯 Decision Tool: SDLC Suitability Matrix", font_weight="bold", color="#f8fafc"),
            rx.text("Input your project parameters to identify the best lifecycle model.", font_size="13px", color="#94a3b8"),
            
            rx.text("Requirement Stability:", font_size="13px", color="#f8fafc", margin_top="8px"),
            rx.radio(
                ["Completely Fixed & Policy-governed", "Iterative/Requires User Feedback", "Highly Uncertain & Risky"],
                value=state.s3_stability,
                on_change=state.set_s3_stability,
                spacing="2",
            ),
            
            rx.text("Timeline Pressure:", font_size="13px", color="#f8fafc", margin_top="8px"),
            rx.select(
                ["Generous/Quality-focused", "Extremely urgent/Need immediate working prototype"],
                value=state.s3_timeline,
                on_change=state.set_s3_timeline,
                size="2",
                width="100%",
                margin_bottom="12px",
            ),
            
            render_alert(f"💡 Recommended Model: {state.s3_recommendation}", "blue"),
            style=EXPANDER_STYLE,
            align_items="start",
            width="100%",
        ),
        width="100%",
        align_items="start",
    )

# Session 4: Hardware Stack Sandbox
def session_4_sandbox(state):
    return rx.vstack(
        rx.heading("🎮 Interactive Sandbox: Hardware-Cloud Stack Architect", size="4", color="#38bdf8", margin_bottom="8px"),
        rx.vstack(
            rx.text("⚙️ Lab: Digital Stack Cost & Performance Builder", font_weight="bold", color="#f8fafc"),
            rx.text("Configure hardware/cloud layers and verify system capacity constraints.", font_size="13px", color="#94a3b8"),
            
            rx.text("Processor Chipset Tier:", font_size="13px", color="#f8fafc", margin_top="8px"),
            rx.select(
                ["Standard Core CPU (Low Overhead)", "Enterprise AI GPU/TPU (High performance)"],
                value=state.s4_chip,
                on_change=state.set_s4_chip,
                size="2",
                width="100%",
            ),
            
            rx.text("Cloud Hosting Strategy:", font_size="13px", color="#f8fafc", margin_top="8px"),
            rx.radio(
                ["IaaS (EC2/Azure VMs - Complete control)", "SaaS (Fully managed cloud services)"],
                value=state.s4_cloud,
                on_change=state.set_s4_cloud,
                spacing="2",
            ),
            
            rx.text(f"Target Monthly Active Users: {state.s4_users:,}", font_size="13px", color="#f8fafc", margin_top="8px"),
            rx.slider(
                value=[state.s4_users],
                min_value=1000,
                max_value=200000,
                on_change=state.set_s4_users,
            ),
            
            rx.cond(
                state.s4_bottleneck,
                render_alert("🚨 Chip bottlenecks detected! Standard CPUs cannot handle the query volume.", "red"),
                render_alert("🚀 Stack configuration validated. Compute resources are balanced.", "green")
            ),
            style=EXPANDER_STYLE,
            align_items="start",
            width="100%",
        ),
        width="100%",
        align_items="start",
    )

# Session 5: Backlog Matrix Sandbox
def session_5_sandbox(state):
    return rx.vstack(
        rx.heading("🎮 Interactive Sandbox: Backlog Priority Matrix", size="4", color="#38bdf8", margin_bottom="8px"),
        rx.vstack(
            rx.text("📊 Manager Tool: Strategic Backlog Prioritizer", font_weight="bold", color="#f8fafc"),
            rx.text("Evaluate backlog features using Strategic Importance and Cost of Change.", font_size="13px", color="#94a3b8"),
            
            rx.text(f"Strategic Business Importance (1-10): {state.s5_benefit}", font_size="13px", color="#f8fafc", margin_top="8px"),
            rx.slider(value=[state.s5_benefit], min_value=1, max_value=10, on_change=state.set_s5_benefit),
            
            rx.text(f"Development Cost / Complexity (1-10): {state.s5_cost}", font_size="13px", color="#f8fafc", margin_top="8px"),
            rx.slider(value=[state.s5_cost], min_value=1, max_value=10, on_change=state.set_s5_cost),
            
            rx.hstack(
                rx.text(f"Calculated Priority Score: {state.s5_priority}", font_weight="bold", color="#34d399"),
                spacing="2",
            ),
            
            rx.cond(
                state.s5_priority >= 5,
                render_alert("🔥 Priority: High. Schedule for the next development sprint.", "red"),
                rx.cond(
                    state.s5_priority >= 1,
                    render_alert("⚡ Priority: Medium. Keep in backlog for future sprint cycles.", "yellow"),
                    render_alert("💤 Priority: Low / Defer. Resource investment does not align with business value.", "blue")
                )
            ),
            style=EXPANDER_STYLE,
            align_items="start",
            width="100%",
        ),
        width="100%",
        align_items="start",
    )

# Session 6: Buy vs Build Sandbox
def session_6_sandbox(state):
    return rx.vstack(
        rx.heading("🎮 Interactive Sandbox: Buy vs Build Decision Grid", size="4", color="#38bdf8", margin_bottom="8px"),
        rx.vstack(
            rx.text("⚖️ Manager Tool: Acquisition Selection matrix", font_weight="bold", color="#f8fafc"),
            rx.text("Select the option matching your organizational constraints:", font_size="13px", color="#94a3b8"),
            
            rx.checkbox("Company has experienced internal dev team?", checked=state.s6_has_devs, on_change=state.set_s6_has_devs, color_scheme="teal", margin_bottom="6px"),
            rx.checkbox("Application is primary source of competitive edge?", checked=state.s6_need_diff, on_change=state.set_s6_need_diff, color_scheme="teal", margin_bottom="6px"),
            rx.checkbox("Timeline is extremely critical (<30 days)?", checked=state.s6_tight_time, on_change=state.set_s6_tight_time, color_scheme="teal", margin_bottom="12px"),
            
            render_alert(f"💡 Verdict: {state.s6_verdict}", "blue"),
            style=EXPANDER_STYLE,
            align_items="start",
            width="100%",
        ),
        width="100%",
        align_items="start",
    )

# Session 7: BCP Sandbox
def session_7_sandbox(state):
    return rx.vstack(
        rx.heading("🎮 Interactive Sandbox: RTO / RPO Cost Optimizer", size="4", color="#38bdf8", margin_bottom="8px"),
        rx.vstack(
            rx.text("🚨 BCP Tool: Disaster Continuity Planner", font_weight="bold", color="#f8fafc"),
            rx.text("Balance backup frequency against infrastructure costs to plan your BCP parameters.", font_size="13px", color="#94a3b8"),
            
            rx.text("Select Backup Frequency:", font_size="13px", color="#f8fafc", margin_top="8px"),
            rx.select(
                ["Hourly", "Daily", "Weekly"],
                value=state.s7_freq,
                on_change=state.set_s7_freq,
                size="2",
                width="100%",
            ),
            
            rx.text("Redundancy Zones:", font_size="13px", color="#f8fafc", margin_top="8px"),
            rx.radio(
                ["Single Datacenter (Low cost)", "Multi-Region Cloud (High cost)"],
                value=state.s7_zones,
                on_change=state.set_s7_zones,
                spacing="2",
            ),
            
            rx.vstack(
                rx.text(f"▸ RPO Data Loss Risk: {state.s7_rpo} Hours", color="#38bdf8", font_size="13px"),
                rx.text(f"▸ RTO Recovery Downtime: {state.s7_rto} Hours", color="#38bdf8", font_size="13px"),
                rx.heading(f"Total BCP Infrastructure Cost: ${state.s7_cost:,}/year", size="3", color="#34d399", margin_top="8px"),
                align_items="start",
                spacing="1",
                width="100%",
            ),
            style=EXPANDER_STYLE,
            align_items="start",
            width="100%",
        ),
        width="100%",
        align_items="start",
    )

# 📚 LECTURE NOTES DATA
S1_NOTES_LEFT = """
##### 📖 Week 1: Systems Thinking & Feedback Loops
Organizations are interconnected webs. Managers must understand system functions and workflows before applying technology.

**System Characteristics:**
* **Components:** People, Process, Tech, Info, Governance.
* **Relationships:** Workflows and connections.
* **Boundaries:** Internal control vs. external parameters.
* **Goals:** The unified objective components work toward.

**Feedback Loops:**
* *Positive (Reinforcing):* Drives growth (e.g. viral network adoption) or runaway panic buying loops.
* *Negative (Balancing):* Corrects errors, maintaining stability (e.g. thermostat, inventory thresholds).
"""

S1_NOTES_RIGHT = """
##### 📖 Week 2: Technology Planning & Requirements Analysis
* Focus on solving real business problems, not chasing tech hype.
* Avoid **Tech-First Thinking** (selecting tools before problems are scoped).

**Syllabus Requirements Categories:**
* **Functional:** *What* the system does (e.g. log transactions, track resources).
* **Non-Functional:** *How* it performs (e.g. reliability, security, scalability, uptime).
* **Human-Centered:** Simplicity, accessibility, and trust.
"""

S2_NOTES_LEFT = """
##### 📖 Week 3: Systems Design & Problem Analysis
* Transforms requirements into implementable blueprints.
* **Conceptual Design:** Focuses on purpose, workflows, and relationship rules. (Manager-facing level).
* **Technical Design:** Focuses on database schema, APIs, and code structure. (Developer-facing level).

**Digital Transformation Roadmap Stages:**
1. Manual Operations (paper-based workflows)
2. Organized Processes (standard operating procedures)
3. Digital Records (databases/ledgers)
4. Integrated Systems (connected departments)
5. Intelligent Systems (analytics and AI support)
"""

S2_NOTES_RIGHT = """
##### 📖 Week 4: Information Ethics & Privacy Guidelines
* **Data Protection:** Safeguarding credentials, identity logs, and financial balances.
* **AI and DSS:** Decisional assistants spot trends, but humans remain fully accountable.

**The Ethical Checklist for Managers:**
1. *Is it legal?* (Compliance validation)
2. *Is it fair?* (Equity and balance check)
3. *Is it necessary?* (Purpose & Scale constraints)
4. *What are the consequences?* (Risk/Benefit analysis)
"""

S3_NOTES_LEFT = """
##### 📖 Week 5: SDLC Models & Suitability
Structured approach to plan, design, build, test, and maintain enterprise information networks.

**Syllabus SDLC Models:**
* **Waterfall Model:** Sequential, documentation-driven. Ideal for fixed regulations, stable currencies, and well-understood systems.
* **Spiral Model:** Iterative, focusing on risk analysis. Ideal for highly complex, high-risk systems.
* **Prototyping Model:** Rapid build-and-learn cycle. Ideal for experimental features with unclear requirements.
* **Agile Model:** Highly flexible, user-feedback loop driven. Ideal for fast-changing requirements.
"""

S3_NOTES_RIGHT = """
##### 📖 Week 6: IT Frameworks, TPS & DIKW Hierarchy
**Information Processing Stack:**
* **TPS (Transaction Processing Systems):** Records routine daily activities.
* **DSS (Decision Support Systems):** Evaluates alternatives using TPS data.

**The DIKW Hierarchy:**
1. **Data:** Raw transactional facts (e.g. "Clerk logs 10 kg").
2. **Information:** Structured reports (e.g. "Monthly grain storage trends").
3. **Knowledge:** Actionable relationships (e.g. "Rain failure triggers 15% drop").
4. **Wisdom:** Strategic management rules (e.g. "Enact emergency distribution").
"""

S4_NOTES = """
##### 📖 Week 8: Semiconductors, Platforms & Cloud Stack
**The Digital & Hardware Stack**
1. **Applications (SaaS):** Frontend tools (e.g. Salesforce, Slack).
2. **Cloud Infrastructure (IaaS/PaaS):** Compute/storage layers (AWS, Azure, GCP).
3. **Telecommunication Networks:** 5G, fiber, satellite data relays.
4. **Semiconductors (Chips):** Silicon CPUs, GPUs, memory. (The foundation).

**Semiconductor Industry Dynamics:**
* Chips power all modern computing infrastructure.
* Silicon is the fundamental element (semi-conductor of electrical currents).
* Key Players: Nvidia (GPU/AI), Intel (CPU), TSMC (Fabrication).

**Telecom Regulations:**
* Allocating radio bandwidth channels.
* Local vs long-distance transmission limits.
"""

S5_NOTES = """
##### 📖 Week 9 & 10: APM, Prioritization & Backlog Management
**Application Portfolio Management (APM)**
Managers systematically classify software assets to optimize maintenance, upgrade pathways, or retire obsolete systems.

**Key Decisions:**
* **Maintenance vs Enhancement:** Patching bugs vs building new features.
* **Cost of Change:** Changes late in the SDLC cost significantly more than early design adjustments.
* **Governance:** Avoiding ad-hoc requests by prioritizing items using business case metrics.
"""

S6_NOTES = """
##### 📖 Week 11 & 12: Buy vs Build & Network Zonation
**System Acquisition Alternatives**
* **Outsourcing:** Transferring development/operations to external partners.
* **Buy vs. Build:**
  * *Buy (SaaS):* Fast rollout, predictable license costs, vendor lock-in risk.
  * *Build (Custom):* High upfront CapEx, competitive differentiation, custom fit.
  
**Intranets vs Extranets:**
* **Intranet:** Internal private corporate network. High security restrictions.
* **Extranet:** Shared network zone extending database access to partners/suppliers.
"""

S7_NOTES = """
##### 📖 Week 13: BCP, Change Management & Resilience
**Business Continuity Planning (BCP)**
* Proactive planning to maintain operations in crisis.
* **RTO (Recovery Time Objective):** Max acceptable downtime before recovery.
* **RPO (Recovery Point Objective):** Max acceptable data loss interval.

**Change Management Frameworks:**
* Managing user anxiety, training, and operational transitions during new software rollouts.
"""

# Render Layout functions for the 7 sessions (compile-time safe)
def render_session_1(state):
    return rx.grid(
        rx.vstack(rx.markdown(S1_NOTES_LEFT), rx.markdown(S1_NOTES_RIGHT), style=BOX_STYLE, align_items="start"),
        session_1_sandbox(state),
        columns="2",
        spacing="4",
        width="100%",
    )

def render_session_2(state):
    return rx.grid(
        rx.vstack(rx.markdown(S2_NOTES_LEFT), rx.markdown(S2_NOTES_RIGHT), style=BOX_STYLE, align_items="start"),
        session_2_sandbox(state),
        columns="2",
        spacing="4",
        width="100%",
    )

def render_session_3(state):
    return rx.grid(
        rx.vstack(rx.markdown(S3_NOTES_LEFT), rx.markdown(S3_NOTES_RIGHT), style=BOX_STYLE, align_items="start"),
        session_3_sandbox(state),
        columns="2",
        spacing="4",
        width="100%",
    )

def render_session_4(state):
    return rx.grid(
        rx.vstack(rx.markdown(S4_NOTES), style=BOX_STYLE, align_items="start"),
        session_4_sandbox(state),
        columns="2",
        spacing="4",
        width="100%",
    )

def render_session_5(state):
    return rx.grid(
        rx.vstack(rx.markdown(S5_NOTES), style=BOX_STYLE, align_items="start"),
        session_5_sandbox(state),
        columns="2",
        spacing="4",
        width="100%",
    )

def render_session_6(state):
    return rx.grid(
        rx.vstack(rx.markdown(S6_NOTES), style=BOX_STYLE, align_items="start"),
        session_6_sandbox(state),
        columns="2",
        spacing="4",
        width="100%",
    )

def render_session_7(state):
    return rx.grid(
        rx.vstack(rx.markdown(S7_NOTES), style=BOX_STYLE, align_items="start"),
        session_7_sandbox(state),
        columns="2",
        spacing="4",
        width="100%",
    )
