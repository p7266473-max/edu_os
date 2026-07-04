import reflex as rx

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
                    value=SubjectState.week2_iso_size,
                    on_change=SubjectState.set_iso_size,
                ),
                rx.text(SubjectState.week2_iso_size.to_string() + " GB"),
                rx.text("USB Write Speed (MB/s):"),
                rx.slider(
                    min=5,
                    max=150,
                    step=5,
                    value=SubjectState.week2_usb_speed,
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
                            value=SubjectState.week3_solar_panels,
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
                            value=SubjectState.week3_water_flow,
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


def render_mot():
    return rx.vstack(
        rx.heading("📈 Management of Technology (MOT)", size="6", color="#1e3a8a"),
        rx.text("Frameworks for evaluating, acquiring, deploying, and optimizing emerging technology infrastructures in modern firms.", color="#475569"),
        rx.divider(border_color="#e2e8f0"),
        rx.vstack(
            rx.heading("Key Learning Modules", size="4", color="#0f172a"),
            rx.markdown("""
            * **Technology Life Cycles:** S-curves, diffusion theories, and disruptive technology models.
            * **Innovation Strategy:** Research & development management, design thinking, and intellectual property.
            * **Tech Acquisition:** Make-or-buy analysis, cloud migrations vs. on-premises architectures, and vendor audits.
            * **Change Management:** Overcoming organizational friction during enterprise system integrations.
            """),
            align="start",
            spacing="3",
        ),
        style=CONTENT_CONTAINER,
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
