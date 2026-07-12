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
from .mot_layouts import (
    render_session_1,
    render_session_2,
    render_session_3,
    render_session_4,
    render_session_5,
    render_session_6,
    render_session_7,
)

# Master list of session quizzes
QUIZZES = [
    SESSION_1_QUIZ,
    SESSION_2_QUIZ,
    SESSION_3_QUIZ,
    SESSION_4_QUIZ,
    SESSION_5_QUIZ,
    SESSION_6_QUIZ,
    SESSION_7_QUIZ,
]

SESSION_TITLES = [
    "Session 1: Weeks 1 & 2",
    "Session 2: Weeks 3 & 4",
    "Session 3: Weeks 5 & 6",
    "Session 4: Weeks 7 & 8",
    "Session 5: Weeks 9 & 10",
    "Session 6: Weeks 11 & 12",
    "Session 7: Week 13"
]

class SubjectState(rx.State):
    current_tab: str = "MIS/IT"
    
    # Week selector for MIS/IT
    mis_active_week: str = "Week 1: Virtualization"
    
    # Hypervisor performance simulation type
    week1_hypervisor_type: str = "Type 1: Bare-Metal"
    
    # Week 2 sliders
    week2_iso_size: float = 3.2
    week2_usb_speed: int = 20
    
    # Week 3 scenario inputs
    week3_solar_panels: int = 2500
    week3_water_flow: int = 8500
    
    # --- MOT MBA PORTAL NAVIGATION & QUIZ STATES ---
    active_session_idx: int = 0
    active_sub_tab: str = "notes"  # "notes" or "quiz"
    quiz_mode: str = "Study Mode"
    quiz_user_answers: dict[str, str] = {}  # key format: "session_qidx"
    quiz_submitted: dict[str, bool] = {}  # key format: "session"
    
    # --- MOT MBA SANDBOX STATES ---
    # Session 1: Systems Thinking
    s1_policy: str = "None (Runaway Panic)"
    s1_panic_level: int = 3
    s1_req_item: str = "Clerk must record every grain allocation."
    s1_req_class: str = "Functional Requirement"
    
    # Session 2: Ethics
    s2_proposal: str = "Workplace biometric scans to access ledgers"
    s2_q1: bool = False
    s2_q2: bool = False
    s2_q3: bool = False
    s2_q4: bool = False
    
    # Session 3: SDLC Selector
    s3_stability: str = "Completely Fixed & Policy-governed"
    s3_timeline: str = "Generous/Quality-focused"
    
    # Session 4: Hardware Stack
    s4_chip: str = "Standard Core CPU (Low Overhead)"
    s4_cloud: str = "IaaS (EC2/Azure VMs - Complete control)"
    s4_users: int = 50000
    
    # Session 5: Backlog Priority
    s5_benefit: int = 8
    s5_cost: int = 3
    
    # Session 6: Buy vs Build
    s6_has_devs: bool = False
    s6_need_diff: bool = False
    s6_tight_time: bool = False
    
    # Session 7: BCP Planner
    s7_freq: str = "Daily"
    s7_zones: str = "Single Datacenter (Low cost)"
    
    def set_tab(self, tab_name: str):
        self.current_tab = tab_name
        
    def set_mis_week(self, week_name: str):
        self.mis_active_week = week_name
        
    def set_hypervisor_type(self, value: str):
        self.week1_hypervisor_type = value
 
    def set_iso_size(self, val: list[float]):
        self.week2_iso_size = float(val[0])
 
    def set_usb_speed(self, val: list[int]):
        self.week2_usb_speed = int(val[0])
 
    def set_solar_panels(self, val: list[int]):
        self.week3_solar_panels = int(val[0])
 
    def set_water_flow(self, val: list[int]):
        self.week3_water_flow = int(val[0])
 
    @rx.var
    def week1_simulation_result(self) -> str:
        if "Type 1" in self.week1_hypervisor_type:
            return "⚡ Type 1 Hypervisor: 98-99% direct hardware access efficiency. Recommended for production datacenters (Proxmox VE, ESXi)."
        return "💻 Type 2 Hypervisor: 85-95% efficiency due to host OS abstraction. Recommended for localized learning (VirtualBox, VMware Workstation)."
 
    @rx.var
    def week2_flash_duration(self) -> str:
        est_time_seconds = (self.week2_iso_size * 1024) / max(self.week2_usb_speed, 1)
        minutes = int(est_time_seconds // 60)
        seconds = int(est_time_seconds % 60)
        return f"{minutes}m {seconds}s"
 
    @rx.var
    def week3_power_available(self) -> str:
        power = self.week3_solar_panels * 60.0
        return f"{power:,.1f} W (60% estimated efficiency)"
 
    @rx.var
    def week3_water_capacity(self) -> str:
        capacity = int(self.week3_water_flow / 3.0)
        return f"{capacity:,} survivors supported/day"

    # --- MOT MBA HANDLERS & VARS ---
    def set_session_idx(self, idx: int):
        self.active_session_idx = idx
        
    def set_sub_tab(self, sub: str):
        self.active_sub_tab = sub
        
    def set_quiz_mode(self, mode: str):
        self.quiz_mode = mode
        
    def select_quiz_answer(self, q_idx: int, option: str):
        key = f"{self.active_session_idx}_{q_idx}"
        self.quiz_user_answers[key] = option
        
    def submit_quiz(self):
        key = f"session_{self.active_session_idx}"
        self.quiz_submitted[key] = True
        
    def retake_quiz(self):
        for q_idx in range(len(QUIZZES[self.active_session_idx])):
            key = f"{self.active_session_idx}_{q_idx}"
            if key in self.quiz_user_answers:
                del self.quiz_user_answers[key]
        sub_key = f"session_{self.active_session_idx}"
        self.quiz_submitted[sub_key] = False

    def set_s1_policy(self, val: str): self.s1_policy = val
    def set_s1_panic_level(self, val: list[int]): self.s1_panic_level = int(val[0])
    def set_s1_req_item(self, val: str): self.s1_req_item = val
    def set_s1_req_class(self, val: str): self.s1_req_class = val

    @rx.var
    def s1_final_stock(self) -> int:
        panic = self.s1_panic_level
        stock = 100
        for _ in range(5):
            if self.s1_policy == "None (Runaway Panic)":
                demand = panic * 8
                panic += 2
            elif self.s1_policy == "Rationing Rules (Cap allocations)":
                demand = min(panic * 3, 15)
                panic = max(1, panic - 1)
            else: # Price Ceiling
                demand = panic * 5
                panic = max(1, panic - 0.5)
            stock = max(0, stock - demand)
        return int(stock)

    @rx.var
    def s1_stock_depleted(self) -> bool:
        return self.s1_final_stock == 0

    @rx.var
    def s1_req_correct(self) -> bool:
        item = self.s1_req_item
        cat = self.s1_req_class
        if "record every" in item and cat == "Functional Requirement": return True
        if ("encrypted" in item or "active users" in item or "2 seconds" in item) and cat == "Non-Functional: Security/Performance": return True
        if "readable" in item and cat == "Human-Centered Design": return True
        return False

    def set_s2_proposal(self, val: str): self.s2_proposal = val
    def set_s2_q1(self, val: bool): self.s2_q1 = val
    def set_s2_q2(self, val: bool): self.s2_q2 = val
    def set_s2_q3(self, val: bool): self.s2_q3 = val
    def set_s2_q4(self, val: bool): self.s2_q4 = val

    @rx.var
    def s2_score(self) -> int:
        return sum([self.s2_q1, self.s2_q2, self.s2_q3, self.s2_q4])

    def set_s3_stability(self, val: str): self.s3_stability = val
    def set_s3_timeline(self, val: str): self.s3_timeline = val

    @rx.var
    def s3_recommendation(self) -> str:
        if self.s3_stability == "Completely Fixed & Policy-governed" and self.s3_timeline == "Generous/Quality-focused":
            return "Waterfall Model (Sequential, document-driven)"
        elif self.s3_stability == "Iterative/Requires User Feedback" or self.s3_timeline == "Extremely urgent/Need immediate working prototype":
            return "Prototyping / Agile Model (Feedback-driven loops)"
        else:
            return "Spiral Model (Iterative risk audit frameworks)"

    def set_s4_chip(self, val: str): self.s4_chip = val
    def set_s4_cloud(self, val: str): self.s4_cloud = val
    def set_s4_users(self, val: list[int]): self.s4_users = int(val[0])

    @rx.var
    def s4_bottleneck(self) -> bool:
        return self.s4_chip == "Standard Core CPU (Low Overhead)" and self.s4_users > 100000

    def set_s5_benefit(self, val: list[int]): self.s5_benefit = int(val[0])
    def set_s5_cost(self, val: list[int]): self.s5_cost = int(val[0])

    @rx.var
    def s5_priority(self) -> int:
        return self.s5_benefit - self.s5_cost

    def set_s6_has_devs(self, val: bool): self.s6_has_devs = val
    def set_s6_need_diff(self, val: bool): self.s6_need_diff = val
    def set_s6_tight_time(self, val: bool): self.s6_tight_time = val

    @rx.var
    def s6_verdict(self) -> str:
        if self.s6_tight_time:
            return "Buy SaaS Product (Custom build takes too long)"
        elif self.s6_has_devs and self.s6_need_diff:
            return "Build Custom System (Maintain strategic competitive edge)"
        else:
            return "Buy and Customize (Leverage standard platforms)"

    def set_s7_freq(self, val: str): self.s7_freq = val
    def set_s7_zones(self, val: str): self.s7_zones = val

    @rx.var
    def s7_rpo(self) -> float:
        if self.s7_freq == "Hourly": return 1.0
        elif self.s7_freq == "Daily": return 24.0
        return 168.0

    @rx.var
    def s7_rto(self) -> float:
        return 2.0 if "Multi-Region" in self.s7_zones else 24.0

    @rx.var
    def s7_cost(self) -> int:
        backup = 5000 if self.s7_freq == "Hourly" else (1000 if self.s7_freq == "Daily" else 200)
        infra = 4000 if "Multi-Region" in self.s7_zones else 500
        return backup + infra

    @rx.var
    def current_session_quiz_len(self) -> int:
        return len(QUIZZES[self.active_session_idx])

    @rx.var
    def current_quiz_submitted(self) -> bool:
        return self.quiz_submitted.get(f"session_{self.active_session_idx}", False)

    @rx.var
    def current_quiz_score_pct(self) -> float:
        correct = 0
        questions = QUIZZES[self.active_session_idx]
        for idx, q in enumerate(questions):
            ans = self.quiz_user_answers.get(f"{self.active_session_idx}_{idx}")
            if ans == q["correct"]:
                correct += 1
        return (correct / len(questions)) * 100.0 if len(questions) > 0 else 0.0

    @rx.var
    def current_quiz_score_raw(self) -> str:
        correct = 0
        questions = QUIZZES[self.active_session_idx]
        for idx, q in enumerate(questions):
            ans = self.quiz_user_answers.get(f"{self.active_session_idx}_{idx}")
            if ans == q["correct"]:
                correct += 1
        return f"{correct} / {len(questions)}"


# Styles
NAV_BTN_STYLE = {
    "padding": "12px 24px",
    "font_weight": "600",
    "border_radius": "8px",
    "cursor": "pointer",
    "transition": "all 0.2s ease-in-out",
}

CONTENT_CONTAINER = {
    "background_color": "#ffffff",
    "border_radius": "12px",
    "padding": "24px",
    "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)",
    "width": "100%",
}


def syllabus_tab_button(name: str):
    is_active = (SubjectState.current_tab == name)
    return rx.button(
        name,
        on_click=lambda: SubjectState.set_tab(name),
        background_color=rx.cond(is_active, "#1e3a8a", "transparent"),
        color=rx.cond(is_active, "#ffffff", "#475569"),
        border=rx.cond(is_active, "1px solid #1e3a8a", "1px solid #cbd5e1"),
        _hover={"background_color": rx.cond(is_active, "#1e3a8a", "#f1f5f9")},
        style=NAV_BTN_STYLE,
    )


def mis_week_button(name: str):
    is_active = (SubjectState.mis_active_week == name)
    return rx.button(
        name,
        on_click=lambda: SubjectState.set_mis_week(name),
        background_color=rx.cond(is_active, "#3b82f6", "#f8fafc"),
        color=rx.cond(is_active, "#ffffff", "#1e293b"),
        border=rx.cond(is_active, "1px solid #3b82f6", "1px solid #e2e8f0"),
        _hover={"background_color": rx.cond(is_active, "#2563eb", "#f1f5f9")},
        padding="8px 16px",
        font_size="13px",
        cursor="pointer",
    )


def render_operating_systems():
    return rx.vstack(
        rx.heading("🖥️ Operating Systems (OS)", size="6", color="#1e3a8a"),
        rx.text("Study of computer system architectures, process scheduling, memory management, and file systems operations.", color="#475569"),
        rx.divider(border_color="#e2e8f0"),
        rx.vstack(
            rx.heading("Key Learning Modules", size="4", color="#0f172a"),
            rx.markdown("""
            * **Process Management:** CPU scheduling algorithms (FIFO, Round Robin, Shortest Job First).
            * **Memory Management:** Virtual memory, paging, segmentation, and thrashing processes.
            * **Storage & File Systems:** Disk allocation methods, directory structures, and journal file recovery (ext4, NTFS).
            * **Concurrency Control:** Deadlocks detection, prevention strategies, and thread synchronization.
            """),
            align="start",
            spacing="3",
        ),
        style=CONTENT_CONTAINER,
        spacing="4",
    )


def render_mis_it():
    return rx.vstack(
        rx.heading("📊 Management Information Systems (MIS/IT)", size="6", color="#1e3a8a"),
        rx.text("Integrating foundational systems operations, IT infrastructure configuration, and disaster coordination planning.", color="#475569"),
        rx.divider(border_color="#e2e8f0"),
        
        # Sub-navigation for Weeks 1-3
        rx.hstack(
            mis_week_button("Week 1: Virtualization"),
            mis_week_button("Week 2: Bootable USB & Hardware"),
            mis_week_button("Week 3: Survival Scenario"),
            spacing="3",
            width="100%",
            wrap="wrap",
        ),
        
        # Dynamic Week Contents
        rx.match(
            SubjectState.mis_active_week,
            ("Week 1: Virtualization", rx.vstack(
                rx.heading("Week 1: Virtualization & Hypervisors", size="5", color="#1e3a8a"),
                rx.markdown("""
                Virtualization uses software to create an abstraction layer over physical computer hardware. This allows a single physical machine to host multiple isolated **Virtual Machines (VMs)**.
                
                ##### Why Virtualize in MIS?
                * **Server Consolidation:** Running multiple OS workloads on one physical computer, reducing hardware footprint.
                * **Disaster Recovery:** Encapsulating environments inside single transportable virtual disk files.
                * **Sandbox Security:** Safely launching unverified programs in isolated systems.
                
                ##### 📦 Curated ISO File Library
                The following bootable operating system files are recommended for weekly labs:
                """),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("OS"),
                            rx.table.column_header_cell("Edition"),
                            rx.table.column_header_cell("RAM Recommend"),
                            rx.table.column_header_cell("Primary Sandbox Purpose"),
                        )
                    ),
                    rx.table.body(
                        rx.table.row(
                            rx.table.cell("Ubuntu Desktop 24.04"), rx.table.cell("LTS (Standard)"), rx.table.cell("4 GB"), rx.table.cell("CLI & Desktop lab operations"),
                        ),
                        rx.table.row(
                            rx.table.cell("Ubuntu Server 24.04"), rx.table.cell("LTS (Headless)"), rx.table.cell("2 GB"), rx.table.cell("DBMS and lightweight hosting labs"),
                        ),
                        rx.table.row(
                            rx.table.cell("Debian 12"), rx.table.cell("Netinst Installer"), rx.table.cell("1 GB"), rx.table.cell("High-security, custom system setup"),
                        ),
                        rx.table.row(
                            rx.table.cell("Alpine Linux"), rx.table.cell("Extended ISO"), rx.table.cell("256 MB"), rx.table.cell("Minimal, low-resource environment testing"),
                        ),
                    ),
                    width="100%",
                ),
                rx.divider(border_color="#f1f5f9"),
                rx.heading("Hypervisor Performance Trade-Off Simulator", size="4", color="#0f172a"),
                rx.select(
                    ["Type 1: Bare-Metal", "Type 2: Hosted"],
                    value=SubjectState.week1_hypervisor_type,
                    on_change=SubjectState.set_hypervisor_type,
                ),
                rx.callout(
                    SubjectState.week1_simulation_result,
                    icon="info",
                    color_scheme="blue",
                    width="100%",
                ),
                align="start",
                spacing="4",
                width="100%",
            )),
            ("Week 2: Bootable USB & Hardware", rx.vstack(
                rx.heading("Week 2: Bootable USBs & Computer Hardware", size="5", color="#1e3a8a"),
                rx.markdown("""
                To successfully install virtual machine platforms or carry out disaster recoveries, technicians must understand system hardware layout and the creation of live installation media.
                
                ##### 💾 Bootable Media Creation
                1. **Download the Target ISO:** Obtain an installation image from official repositories.
                2. **Choose the Utility:** Rufus (Windows), BalenaEtcher (Cross-platform), or Ventoy (Multiboot support).
                3. **Select Boot Scheme:** Configure partitions for modern **UEFI** (GPT) or Legacy **BIOS** (MBR) systems.
                
                ##### 🖥️ IT Hardware Foundations
                * **CPU:** Process execution cores versus clock frequencies. Core counts are optimized for database operations.
                * **RAM:** Volatile work registers that dictate the active running capacity of hosted VM environments.
                * **Storage:** Solid State Drives (NVMe SSD) versus Hard Disk Drives (SATA HDD). NVMe avoids structural database write bottleneck constraints.
                """),
                rx.divider(border_color="#f1f5f9"),
                rx.heading("Flashing Duration Estimator", size="4", color="#0f172a"),
                rx.text("ISO Image Size (GB):"),
                rx.slider(
                    min=0.5,
                    max=32.0,
                    step=0.1,
                    value=[SubjectState.week2_iso_size],
                    on_change=SubjectState.set_iso_size,
                ),
                rx.text(SubjectState.week2_iso_size.to_string() + " GB"),
                rx.text("USB Write Speed (MB/s):"),
                rx.slider(
                    min=5,
                    max=150,
                    step=5,
                    value=[SubjectState.week2_usb_speed],
                    on_change=SubjectState.set_usb_speed,
                ),
                rx.text(SubjectState.week2_usb_speed.to_string() + " MB/s"),
                rx.hstack(
                    rx.text("Estimated Flashing Duration: ", font_weight="600"),
                    rx.badge(SubjectState.week2_flash_duration, color_scheme="green"),
                ),
                align="start",
                spacing="3",
                width="100%",
            )),
            ("Week 3: Survival Scenario", rx.vstack(
                rx.heading("Week 3: Scenario Launch — Post-Apocalyptic Grid Collapse", size="5", color="#ef4444"),
                rx.callout(
                    "EMERGENCY SCENARIO ACTIVE: Year 2028. Global grid is completely offline. A cohort of 5.0M to 5.5M survivors has gathered near clean water basins. Systems administrators must build decentralized LANs, manage resource allocations, and ensure coordination systems operate under severe resource deficits.",
                    icon="alert_triangle",
                    color_scheme="red",
                ),
                rx.markdown("""
                ##### Objective:
                Apply standard IT infrastructure concepts (databases, network topologies, memory constraints) under the simulation constraints of a low-energy, hardware-scavenged society.
                """),
                rx.divider(border_color="#f1f5f9"),
                rx.heading("Scenario Resource Calculator", size="4", color="#0f172a"),
                rx.hstack(
                    rx.vstack(
                        rx.text("Solar Panels Scavenged (100W units):"),
                        rx.slider(
                            min=100,
                            max=10000,
                            step=100,
                            value=[SubjectState.week3_solar_panels],
                            on_change=SubjectState.set_solar_panels,
                        ),
                        rx.text(SubjectState.week3_solar_panels.to_string()),
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("Water Purification (Liters/Hour):"),
                        rx.slider(
                            min=1000,
                            max=50000,
                            step=1000,
                            value=[SubjectState.week3_water_flow],
                            on_change=SubjectState.set_water_flow,
                        ),
                        rx.text(SubjectState.week3_water_flow.to_string()),
                        align="start",
                    ),
                    spacing="6",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Continuous Solar Power Output: ", font_weight="600"),
                        rx.text(SubjectState.week3_power_available),
                    ),
                    rx.hstack(
                        rx.text("Community Hydration Capability: ", font_weight="600"),
                        rx.text(SubjectState.week3_water_capacity),
                    ),
                    align="start",
                    spacing="1",
                ),
                align="start",
                spacing="4",
                width="100%",
            )),
        ),
        style=CONTENT_CONTAINER,
        spacing="4",
        width="100%",
    )


def render_intro_ai():
    return rx.vstack(
        rx.heading("🤖 Introduction to Artificial Intelligence", size="6", color="#1e3a8a"),
        rx.text("Fundamental structures of machine intelligence, problem-solving, logic, search spaces, and modern machine learning frameworks.", color="#475569"),
        rx.divider(border_color="#e2e8f0"),
        rx.vstack(
            rx.heading("Key Learning Modules", size="4", color="#0f172a"),
            rx.markdown("""
            * **Search Algorithms:** Uninformed (BFS, DFS) and informed heuristics (A* Search).
            * **Knowledge Representation:** Propositional logic, inference rules, and semantic webs.
            * **Machine Learning Baselines:** Regression, classification trees, and neural network basics.
            * **Ethics in AI:** Transparency, bias detection, and societal implications of automated systems.
            """),
            align="start",
            spacing="3",
        ),
        style=CONTENT_CONTAINER,
        spacing="4",
    )


def render_quiz_question(q, q_idx):
    options_buttons = rx.vstack(
        rx.foreach(
            q["options"],
            lambda opt: rx.button(
                opt,
                width="100%",
                background_color=rx.cond(
                    SubjectState.quiz_user_answers.get(f"{SubjectState.active_session_idx}_{q_idx}") == opt,
                    "#10b981",
                    "#1e293b"
                ),
                color="#f8fafc",
                border="1px solid #334155",
                _hover={"background_color": "#0d9488"},
                on_click=lambda: SubjectState.select_quiz_answer(q_idx, opt),
                padding="12px",
                justify_content="start",
            )
        ),
        spacing="2",
        width="100%",
    )
    
    selected_answer = SubjectState.quiz_user_answers.get(f"{SubjectState.active_session_idx}_{q_idx}")
    is_correct = selected_answer == q["correct"]
    
    study_mode_feedback = rx.cond(
        selected_answer,
        rx.vstack(
            rx.cond(
                is_correct,
                rx.text("✅ Correct!", color="#10b981", font_weight="bold"),
                rx.text(f"❌ Incorrect. Correct: {q['correct']}", color="#ef4444", font_weight="bold")
            ),
            rx.vstack(
                rx.text("💡 Explanation:", font_weight="bold", color="#f8fafc"),
                rx.text(q["explanation"], color="#94a3b8", font_size="13px"),
                align_items="start",
                padding="12px",
                background_color="#0f172a",
                border_radius="6px",
                width="100%",
            ),
            spacing="2",
            width="100%",
            align_items="start",
            margin_top="8px",
        )
    )
    
    exam_mode_feedback = rx.cond(
        SubjectState.current_quiz_submitted,
        rx.vstack(
            rx.cond(
                is_correct,
                rx.text("✅ Correct", color="#10b981", font_weight="bold"),
                rx.text(f"❌ Incorrect (Correct: {q['correct']})", color="#ef4444", font_weight="bold")
            ),
            rx.vstack(
                rx.text("Explanation:", font_weight="bold", color="#f8fafc"),
                rx.text(q["explanation"], color="#94a3b8", font_size="13px"),
                align_items="start",
                padding="12px",
                background_color="#0f172a",
                border_radius="6px",
                width="100%",
            ),
            spacing="2",
            width="100%",
            align_items="start",
            margin_top="8px",
        )
    )

    return rx.vstack(
        rx.heading(f"❓ Question {q_idx + 1}: {q['text']}", size="3", color="#f8fafc", margin_bottom="8px"),
        options_buttons,
        rx.cond(
            SubjectState.quiz_mode == "Study Mode (Instant Feedback & Reveal)",
            study_mode_feedback,
            exam_mode_feedback
        ),
        padding="16px",
        background_color="#111827",
        border="1px solid #1f2937",
        border_radius="8px",
        width="100%",
        align_items="start",
        margin_bottom="16px",
    )


def render_quiz_tab():
    questions = rx.match(
        SubjectState.active_session_idx,
        (0, rx.vstack(rx.foreach(SESSION_1_QUIZ, lambda q, idx: render_quiz_question(q, idx)), width="100%")),
        (1, rx.vstack(rx.foreach(SESSION_2_QUIZ, lambda q, idx: render_quiz_question(q, idx)), width="100%")),
        (2, rx.vstack(rx.foreach(SESSION_3_QUIZ, lambda q, idx: render_quiz_question(q, idx)), width="100%")),
        (3, rx.vstack(rx.foreach(SESSION_4_QUIZ, lambda q, idx: render_quiz_question(q, idx)), width="100%")),
        (4, rx.vstack(rx.foreach(SESSION_5_QUIZ, lambda q, idx: render_quiz_question(q, idx)), width="100%")),
        (5, rx.vstack(rx.foreach(SESSION_6_QUIZ, lambda q, idx: render_quiz_question(q, idx)), width="100%")),
        (6, rx.vstack(rx.foreach(SESSION_7_QUIZ, lambda q, idx: render_quiz_question(q, idx)), width="100%")),
        rx.text("No quiz loaded.")
    )

    return rx.vstack(
        rx.heading("📝 Practice Quiz Panel", size="4", color="#38bdf8", margin_bottom="8px"),
        
        rx.hstack(
            rx.vstack(
                rx.text("Select Quiz Mode:", font_size="13px", font_weight="600", color="#f8fafc"),
                rx.radio(
                    ["Study Mode (Instant Feedback & Reveal)", "Exam Mode (Submit to Score)"],
                    value=SubjectState.quiz_mode,
                    on_change=SubjectState.set_quiz_mode,
                ),
                align_items="start",
            ),
            rx.text("💡 Study Mode gives you instant feedback and detailed explanations as soon as you select an answer.", color="#38bdf8", font_size="13px", width="60%"),
            justify_content="space-between",
            width="100%",
            padding="16px",
            background_color="#1e293b",
            border_radius="10px",
            margin_bottom="20px",
        ),
        
        questions,
        
        rx.cond(
            SubjectState.quiz_mode == "Exam Mode (Submit to Score)",
            rx.vstack(
                rx.cond(
                    ~SubjectState.current_quiz_submitted,
                    rx.button("Submit Quiz", color_scheme="green", size="3", on_click=SubjectState.submit_quiz),
                    rx.vstack(
                        rx.heading(f"📊 Final Score: {SubjectState.current_quiz_score_raw} ({SubjectState.current_quiz_score_pct}%)", size="4", color="#f8fafc"),
                        rx.button("Retake Quiz", color_scheme="gray", size="2", on_click=SubjectState.retake_quiz),
                        align_items="start",
                        spacing="2",
                    )
                ),
                padding="20px",
                background_color="#1e293b",
                border_radius="8px",
                width="100%",
                align_items="start",
                margin_top="12px",
            )
        ),
        width="100%",
        align_items="start",
    )


def render_mot():
    return rx.vstack(
        rx.heading("📈 Management of Technology (MOT) - MBA Focus", size="6", color="#1e3a8a"),
        rx.text("Syllabus modules, interactive frameworks, and practice quizzes for MBA-Management of Technology (COM 573).", color="#475569"),
        rx.divider(border_color="#e2e8f0"),
        
        # MOT MBA Portal View integrated natively in the tab!
        rx.vstack(
            # Scrollable session title selector
            rx.scroll_area(
                rx.hstack(
                    rx.foreach(
                        SESSION_TITLES,
                        lambda title, idx: rx.button(
                            title,
                            on_click=lambda: SubjectState.set_session_idx(idx),
                            background_color=rx.cond(SubjectState.active_session_idx == idx, "#1e3a8a", "transparent"),
                            color=rx.cond(SubjectState.active_session_idx == idx, "#ffffff", "#475569"),
                            border=rx.cond(SubjectState.active_session_idx == idx, "1px solid #1e3a8a", "1px solid #cbd5e1"),
                            _hover={"background_color": rx.cond(SubjectState.active_session_idx == idx, "#1e3a8a", "#f1f5f9")},
                            cursor="pointer",
                            size="2",
                        )
                    ),
                    spacing="3",
                    margin_bottom="16px",
                ),
                width="100%",
            ),
            
            # Sub-navigation within selected session: Notes vs Quiz
            rx.hstack(
                rx.button(
                    "📖 Lecture Notes & Sandbox",
                    on_click=lambda: SubjectState.set_sub_tab("notes"),
                    background_color=rx.cond(SubjectState.active_sub_tab == "notes", "#3b82f6", "transparent"),
                    color=rx.cond(SubjectState.active_sub_tab == "notes", "#ffffff", "#475569"),
                    border=rx.cond(SubjectState.active_sub_tab == "notes", "1px solid #3b82f6", "1px solid #cbd5e1"),
                    cursor="pointer",
                    size="2",
                ),
                rx.button(
                    "📝 Practice Quiz",
                    on_click=lambda: SubjectState.set_sub_tab("quiz"),
                    background_color=rx.cond(SubjectState.active_sub_tab == "quiz", "#3b82f6", "transparent"),
                    color=rx.cond(SubjectState.active_sub_tab == "quiz", "#ffffff", "#475569"),
                    border=rx.cond(SubjectState.active_sub_tab == "quiz", "1px solid #3b82f6", "1px solid #cbd5e1"),
                    cursor="pointer",
                    size="2",
                ),
                spacing="3",
                margin_bottom="24px",
            ),
            
            # Display contents based on sub-tab Selection
            rx.cond(
                SubjectState.active_sub_tab == "notes",
                rx.match(
                    SubjectState.active_session_idx,
                    (0, render_session_1(SubjectState)),
                    (1, render_session_2(SubjectState)),
                    (2, render_session_3(SubjectState)),
                    (3, render_session_4(SubjectState)),
                    (4, render_session_5(SubjectState)),
                    (5, render_session_6(SubjectState)),
                    (6, render_session_7(SubjectState)),
                    rx.text("No session selected.")
                ),
                render_quiz_tab()
            ),
            width="100%",
        ),
        width="100%",
        spacing="4",
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Page Title / Rebrand header
            rx.vstack(
                rx.heading("🎓 Professor Max's Curriculum Portal", size="8", color="#1e3a8a"),
                rx.text("Interactive Academic Syllabus and Laboratory Hub", color="#475569", font_size="16px"),
                align="center",
                spacing="1",
                margin_bottom="12px",
            ),
            
            # Nav bar for subjects
            rx.hstack(
                syllabus_tab_button("Operating Systems"),
                syllabus_tab_button("MIS/IT"),
                syllabus_tab_button("Introduction to AI"),
                syllabus_tab_button("MOT"),
                spacing="3",
                justify="center",
                width="100%",
                margin_bottom="16px",
            ),
            
            # Dynamic tab container
            rx.match(
                SubjectState.current_tab,
                ("Operating Systems", render_operating_systems()),
                ("MIS/IT", render_mis_it()),
                ("Introduction to AI", render_intro_ai()),
                ("MOT", render_mot()),
            ),
            
            width="100%",
            max_width="1000px",
            padding="24px",
            spacing="4",
        ),
        background_color="#f1f5f9",
        min_height="100vh",
        width="100%",
    )


app = rx.App()
app.add_page(index, title="Curriculum Portal")
