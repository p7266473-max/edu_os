import reflex as rx


class OSState(rx.State):
    # ── Core state ────────────────────────────────────────────────────────────
    active_windows: list[str] = []          # list of app titles (strings, not dicts)
    processes: dict[str, int] = {}
    next_pid: int = 1010
    system_status: str = "nominal"
    status_message: str = "EduOS v2 — CasaOS Edition"

    # ── File system ───────────────────────────────────────────────────────────
    c_drive_files: list[str] = ["System32", "Users", "Program_Files", "kernel.sys", "config.json"]
    d_drive_files: list[str] = ["Documents", "Downloads", "Study_Materials", "notes.txt"]
    current_drive: str = "C_Drive"
    selected_file: str = ""
    file_content: str = ""

    # ── Calculator ────────────────────────────────────────────────────────────
    calc_input: str = ""
    calc_result: str = "0"

    # ── Terminal ──────────────────────────────────────────────────────────────
    terminal_logs: list[str] = [
        "Welcome to EduOS v2 (CasaOS Edition)",
        "Type 'help' to see available commands.",
        "user@eduos:~$ ",
    ]
    terminal_input: str = ""

    # ── Notepad ───────────────────────────────────────────────────────────────
    notepad_text: str = "EduOS — running inside CasaOS.\nClick any desktop icon to open an app."

    # ── Start menu ────────────────────────────────────────────────────────────
    start_menu_open: bool = False

    # ── Computed vars (safe Var access) ───────────────────────────────────────
    @rx.var
    def current_files(self) -> list[str]:
        if self.current_drive == "D_Drive":
            return self.d_drive_files
        return self.c_drive_files

    @rx.var
    def is_nominal(self) -> bool:
        return self.system_status == "nominal"

    # ── Process lifecycle ─────────────────────────────────────────────────────
    def open_app(self, name: str):
        self.system_status = "loading"
        if name not in self.active_windows:
            pid = self.next_pid
            self.next_pid += 1
            self.active_windows.append(name)
            self.processes[name] = pid
        self.system_status = "nominal"
        self.status_message = f"Launched: {name}"

    def close_app(self, name: str):
        self.active_windows = [w for w in self.active_windows if w != name]
        if name in self.processes:
            del self.processes[name]
        self.status_message = f"Closed: {name}"

    def toggle_start_menu(self):
        self.start_menu_open = not self.start_menu_open

    # ── File Explorer ─────────────────────────────────────────────────────────
    def select_drive(self, drive: str):
        self.current_drive = drive
        self.selected_file = ""
        self.file_content = ""

    def select_file(self, filename: str):
        self.selected_file = filename
        self.file_content = (
            f"[Simulated content of {filename}]\n"
            f"Drive: {self.current_drive}\n"
            "In production, real files from /app/data appear here."
        )

    # ── Calculator ────────────────────────────────────────────────────────────
    def calc_press(self, value: str):
        if value == "=":
            try:
                self.calc_result = str(eval(self.calc_input))
            except Exception:
                self.calc_result = "Error"
            self.calc_input = ""
        elif value == "C":
            self.calc_input = ""
            self.calc_result = "0"
        else:
            self.calc_input += value

    # ── Terminal ──────────────────────────────────────────────────────────────
    def set_terminal_input(self, val: str):
        self.terminal_input = val

    def handle_terminal_key(self, key: str):
        if key == "Enter":
            self.run_terminal_command()

    def run_terminal_command(self):
        cmd = self.terminal_input.strip()
        self.terminal_logs.append(f"user@eduos:~$ {cmd}")
        if cmd == "help":
            self.terminal_logs += ["  ls, pwd, whoami, clear, date, uname -a"]
        elif cmd == "ls":
            self.terminal_logs.append("  Documents  Downloads  Study_Materials  notes.txt")
        elif cmd == "pwd":
            self.terminal_logs.append("  /app/data")
        elif cmd == "whoami":
            self.terminal_logs.append("  edu_user")
        elif cmd == "clear":
            self.terminal_logs = ["user@eduos:~$ "]
        elif cmd == "date":
            self.terminal_logs.append("  Thu Jul  3 2026")
        elif cmd.startswith("uname"):
            self.terminal_logs.append("  Linux eduos-casaos 6.x x86_64 GNU/Linux")
        elif cmd == "":
            pass
        else:
            self.terminal_logs.append(f"  bash: {cmd}: command not found")
        self.terminal_logs.append("user@eduos:~$ ")
        self.terminal_input = ""

    # ── Notepad ───────────────────────────────────────────────────────────────
    def set_notepad_text(self, val: str):
        self.notepad_text = val


# ── Shared styles ─────────────────────────────────────────────────────────────
DESKTOP_BG = {
    "width": "100vw",
    "height": "100vh",
    "background": "linear-gradient(135deg,#0f0c29,#302b63,#24243e)",
    "position": "relative",
    "overflow": "hidden",
    "font_family": "'Inter',sans-serif",
}

WIN_STYLE = {
    "position": "absolute",
    "top": "70px",
    "left": "110px",
    "min_width": "460px",
    "background": "rgba(15,15,30,0.88)",
    "backdrop_filter": "blur(20px)",
    "border": "1px solid rgba(255,255,255,0.12)",
    "border_radius": "12px",
    "box_shadow": "0 24px 60px rgba(0,0,0,0.7)",
    "overflow": "hidden",
    "z_index": "20",
}

HDR_STYLE = {
    "background": "rgba(255,255,255,0.06)",
    "padding": "10px 16px",
    "border_bottom": "1px solid rgba(255,255,255,0.08)",
    "display": "flex",
    "align_items": "center",
    "justify_content": "space-between",
    "cursor": "move",
}

ICO_STYLE = {
    "display": "flex",
    "flex_direction": "column",
    "align_items": "center",
    "gap": "6px",
    "cursor": "pointer",
    "padding": "12px",
    "border_radius": "10px",
    "color": "white",
    "font_size": "12px",
    "_hover": {"background": "rgba(255,255,255,0.1)"},
}

TASKBAR = {
    "position": "fixed",
    "bottom": "0", "left": "0", "right": "0",
    "height": "48px",
    "background": "rgba(10,10,20,0.92)",
    "backdrop_filter": "blur(20px)",
    "border_top": "1px solid rgba(255,255,255,0.1)",
    "display": "flex",
    "align_items": "center",
    "padding": "0 16px",
    "gap": "8px",
    "z_index": "100",
}

APPS = [
    ("folder", "File Explorer"),
    ("calculator", "Calculator"),
    ("terminal", "Terminal"),
    ("file-text", "Notepad"),
    ("activity", "System Monitor"),
]

SUBJECTS = {
    "Mathematics": ["Algebra", "Calculus", "Statistics"],
    "Science":     ["Physics", "Chemistry", "Biology"],
    "Technology":  ["Programming", "Networks", "AI / ML"],
    "Languages":   ["English Grammar", "Essay Writing"],
}


# ── Window bodies ─────────────────────────────────────────────────────────────
def file_explorer_body():
    return rx.vstack(
        rx.hstack(
            rx.button("C: Drive", on_click=OSState.select_drive("C_Drive"),
                      color_scheme="violet", size="1"),
            rx.button("D: Drive", on_click=OSState.select_drive("D_Drive"),
                      color_scheme="violet", size="1"),
        ),
        rx.divider(color="rgba(255,255,255,0.1)"),
        rx.vstack(
            rx.foreach(
                OSState.current_files,
                lambda f: rx.hstack(
                    rx.icon(tag="file", size=14, color="#a78bfa"),
                    rx.text(f, color="white", font_size="13px",
                            cursor="pointer", on_click=OSState.select_file(f)),
                    spacing="2",
                )
            ),
            align="start", spacing="1",
        ),
        rx.cond(
            OSState.selected_file != "",
            rx.box(
                rx.text(OSState.file_content, color="#94a3b8",
                        font_size="12px", white_space="pre-wrap"),
                background="rgba(0,0,0,0.35)", padding="10px",
                border_radius="6px", margin_top="6px",
            )
        ),
        align="start", padding="16px", spacing="3", width="100%",
    )


def calculator_body():
    rows = [
        ["7","8","9","/"],
        ["4","5","6","*"],
        ["1","2","3","-"],
        ["0",".","=","+"],
        ["C"],
    ]
    return rx.vstack(
        rx.box(
            rx.text(OSState.calc_input, color="#94a3b8",
                    font_size="13px", text_align="right"),
            rx.text(OSState.calc_result, color="white",
                    font_size="28px", font_weight="700", text_align="right"),
            background="rgba(0,0,0,0.3)", padding="12px",
            border_radius="8px", width="100%",
        ),
        rx.vstack(
            *[
                rx.hstack(
                    *[
                        rx.button(
                            btn, on_click=OSState.calc_press(btn),
                            width="60px", height="44px", size="2",
                            color_scheme="violet" if btn in ["=","C"] else "gray",
                        )
                        for btn in row
                    ],
                    spacing="2",
                )
                for row in rows
            ],
            spacing="2",
        ),
        align="center", padding="16px", spacing="3",
    )


def terminal_body():
    return rx.vstack(
        rx.box(
            rx.foreach(
                OSState.terminal_logs,
                lambda line: rx.text(line, color="#4ade80",
                                     font_family="monospace", font_size="13px"),
            ),
            background="rgba(0,0,0,0.5)", padding="12px",
            border_radius="6px", height="200px",
            overflow_y="auto", width="100%",
        ),
        rx.hstack(
            rx.text("$ ", color="#4ade80", font_family="monospace"),
            rx.input(
                value=OSState.terminal_input,
                on_change=OSState.set_terminal_input,
                on_key_down=OSState.handle_terminal_key,
                placeholder="type a command…",
                background="transparent", border="none",
                color="#4ade80", font_family="monospace",
                width="100%", _focus={"outline": "none"},
            ),
            width="100%",
        ),
        align="start", padding="16px", spacing="3", width="100%",
    )


def notepad_body():
    return rx.vstack(
        rx.text_area(
            value=OSState.notepad_text,
            on_change=OSState.set_notepad_text,
            height="240px", width="100%",
            background="rgba(0,0,0,0.3)", color="white",
            border="1px solid rgba(255,255,255,0.1)",
            border_radius="6px", padding="10px",
            font_family="monospace", font_size="13px", resize="none",
        ),
        align="start", padding="16px", width="100%",
    )


def sysmon_body():
    return rx.vstack(
        rx.text("Active Processes", color="#a78bfa", font_weight="600"),
        rx.foreach(
            OSState.active_windows,
            lambda title: rx.hstack(
                rx.icon(tag="cpu", size=14, color="#4ade80"),
                rx.text(title, color="white", font_size="13px"),
                spacing="2",
            )
        ),
        rx.divider(color="rgba(255,255,255,0.1)"),
        rx.text(
            rx.cond(OSState.is_nominal, "● Nominal", "● Loading…"),
            color=rx.cond(OSState.is_nominal, "#4ade80", "#facc15"),
            font_size="13px",
        ),
        rx.text(OSState.status_message, color="#94a3b8", font_size="12px"),
        align="start", padding="16px", spacing="2",
    )


def window_body(title: str):
    return rx.cond(title == "File Explorer", file_explorer_body(),
           rx.cond(title == "Calculator",    calculator_body(),
           rx.cond(title == "Terminal",      terminal_body(),
           rx.cond(title == "Notepad",       notepad_body(),
                                             sysmon_body()))))


def render_window(title: str):
    return rx.box(
        # Header
        rx.hstack(
            rx.hstack(
                rx.icon(tag="monitor", size=14, color="#a78bfa"),
                rx.text(title, color="white", font_size="13px", font_weight="600"),
                spacing="2",
            ),
            rx.button(
                rx.icon(tag="x", size=12),
                on_click=OSState.close_app(title),
                size="1", color_scheme="ruby",
                border_radius="50%", width="22px", height="22px",
            ),
            **HDR_STYLE,
            width="100%",
        ),
        window_body(title),
        **WIN_STYLE,
    )


# ── Taskbar ───────────────────────────────────────────────────────────────────
def taskbar():
    return rx.box(
        rx.button(
            rx.icon(tag="grid-2x2", size=16),
            rx.text("EduOS", font_weight="700", font_size="13px"),
            on_click=OSState.toggle_start_menu,
            background="linear-gradient(135deg,#7c3aed,#4f46e5)",
            color="white", border="none", border_radius="8px",
            padding="0 14px", height="32px", cursor="pointer",
            display="flex", align_items="center", gap="6px",
        ),
        rx.divider(orientation="vertical", height="28px",
                   color="rgba(255,255,255,0.15)"),
        rx.foreach(
            OSState.active_windows,
            lambda t: rx.box(
                rx.text(t, color="white", font_size="12px"),
                background="rgba(255,255,255,0.08)",
                border="1px solid rgba(255,255,255,0.12)",
                border_radius="6px", padding="4px 12px", cursor="pointer",
            )
        ),
        rx.spacer(),
        rx.text("EduOS on CasaOS", color="#94a3b8", font_size="11px"),
        **TASKBAR,
    )


# ── Start menu ────────────────────────────────────────────────────────────────
def start_menu():
    return rx.cond(
        OSState.start_menu_open,
        rx.box(
            rx.vstack(
                rx.text("Study Materials", color="white",
                        font_weight="700", font_size="15px",
                        border_bottom="1px solid rgba(255,255,255,0.1)",
                        padding_bottom="8px", width="100%"),
                *[
                    rx.vstack(
                        rx.text(subject, color="#a78bfa",
                                font_size="12px", font_weight="600"),
                        *[
                            rx.text(f"  • {item}", color="#cbd5e1",
                                    font_size="12px", cursor="pointer",
                                    _hover={"color": "white"})
                            for item in items
                        ],
                        align="start", spacing="1",
                    )
                    for subject, items in SUBJECTS.items()
                ],
                align="start", spacing="3", width="100%",
            ),
            position="fixed", bottom="52px", left="16px",
            width="220px",
            background="rgba(15,15,30,0.95)",
            backdrop_filter="blur(20px)",
            border="1px solid rgba(255,255,255,0.12)",
            border_radius="12px", padding="16px", z_index="200",
        ),
    )


# ── Desktop icons ─────────────────────────────────────────────────────────────
def desktop_icons():
    return rx.vstack(
        *[
            rx.box(
                rx.vstack(
                    rx.icon(tag=icon, size=32, color="#a78bfa"),
                    rx.text(label, color="white", font_size="11px",
                            text_align="center"),
                    spacing="1", align="center",
                ),
                on_click=OSState.open_app(label),
                **ICO_STYLE,
            )
            for icon, label in APPS
        ],
        position="absolute", top="24px", left="24px", spacing="2",
    )


# ── Root page ─────────────────────────────────────────────────────────────────
def index():
    return rx.box(
        # Ambient glow
        rx.box(
            position="absolute", top="0", left="0", right="0", bottom="0",
            background=(
                "radial-gradient(ellipse at 20% 50%,rgba(124,58,237,0.15) 0%,transparent 60%),"
                "radial-gradient(ellipse at 80% 20%,rgba(79,70,229,0.1) 0%,transparent 50%)"
            ),
            pointer_events="none",
        ),
        desktop_icons(),
        rx.foreach(OSState.active_windows, render_window),
        start_menu(),
        taskbar(),
        **DESKTOP_BG,
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
    ],
)
app.add_page(index, title="EduOS — CasaOS Edition")
