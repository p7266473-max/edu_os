import reflex as rx
from typing import List, Dict, Any

# Define a custom React draggable wrapper component using React-Draggable
class Draggable(rx.Component):
    library = "react-draggable"
    tag = "Draggable"
    is_default = True
    handle: rx.Var[str] = ".window-header"

    @classmethod
    def create(cls, *children, **props):
        return super().create(*children, **props)


class OSState(rx.State):
    # CENTRALIZED SYSTEM STATE DRIVERS
    active_windows: list[dict] = []
    processes: dict[str, int] = {}
    next_pid: int = 1010
    system_status: str = "nominal"
    status_message: str = "System status: Nominal"

    file_system: dict[str, list[str]] = {
        "C_Drive": ["System32", "Users", "Program_Files", "kernel.sys", "config.json"],
        "D_Drive": ["Documents", "Downloads", "SPM_Project", "edu_os_specs.md", "notes.txt"],
    }

    current_drive: str = "C_Drive"
    selected_file: str = ""
    file_content: str = ""

    calc_input: str = ""
    calc_result: str = "0"

    terminal_logs: list[str] = [
        "Welcome to EduOS v2 (CasaOS Edition)",
        "Type 'help' to see available commands.",
        "user@eduos:~$ ",
    ]

    notepad_text: str = "EduOS — running inside CasaOS.\nClick any desktop icon to open an app."

    start_menu_open: bool = False

    # ── Process Lifecycle ──────────────────────────────────────────────────────
    def open_app(self, name: str):
        self.system_status = "loading"
        if name not in [w["title"] for w in self.active_windows]:
            pid = self.next_pid
            self.next_pid += 1
            self.active_windows.append({"title": name, "minimized": False, "z": len(self.active_windows) + 10})
            self.processes[name] = pid
        self.system_status = "nominal"
        self.status_message = f"Launched {name} (PID {self.processes.get(name, '?')})"

    def close_app(self, name: str):
        self.active_windows = [w for w in self.active_windows if w["title"] != name]
        self.processes.pop(name, None)
        self.status_message = f"Closed {name}"

    def toggle_start_menu(self):
        self.start_menu_open = not self.start_menu_open

    def close_start_menu(self):
        self.start_menu_open = False

    # ── File Explorer ──────────────────────────────────────────────────────────
    def select_drive(self, drive: str):
        self.current_drive = drive

    def select_file(self, filename: str):
        self.selected_file = filename
        self.file_content = f"[Simulated content of {filename}]\nThis file lives on {self.current_drive}.\nIn a full deployment, real files from /app/data appear here."

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
    terminal_input: str = ""

    def set_terminal_input(self, val: str):
        self.terminal_input = val

    def run_command(self):
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


# ── Styles ────────────────────────────────────────────────────────────────────
DESKTOP_STYLE = {
    "width": "100vw",
    "height": "100vh",
    "background": "linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
    "position": "relative",
    "overflow": "hidden",
    "font_family": "'Inter', sans-serif",
}

WINDOW_STYLE = {
    "position": "absolute",
    "top": "80px",
    "left": "120px",
    "min_width": "480px",
    "min_height": "320px",
    "background": "rgba(15,15,30,0.85)",
    "backdrop_filter": "blur(20px)",
    "border": "1px solid rgba(255,255,255,0.12)",
    "border_radius": "12px",
    "box_shadow": "0 24px 64px rgba(0,0,0,0.7)",
    "z_index": "20",
    "overflow": "hidden",
}

HEADER_STYLE = {
    "background": "rgba(255,255,255,0.06)",
    "padding": "10px 16px",
    "display": "flex",
    "align_items": "center",
    "justify_content": "space-between",
    "cursor": "move",
    "border_bottom": "1px solid rgba(255,255,255,0.08)",
    "class_name": "window-header",
}

ICON_STYLE = {
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

TASKBAR_STYLE = {
    "position": "fixed",
    "bottom": "0",
    "left": "0",
    "right": "0",
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

DESKTOP_APPS = [
    ("folder", "File Explorer"),
    ("calculator", "Calculator"),
    ("terminal", "Terminal"),
    ("file-text", "Notepad"),
    ("activity", "System Monitor"),
]


# ── Window contents ───────────────────────────────────────────────────────────
def file_explorer_content():
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
                OSState.file_system[OSState.current_drive],
                lambda f: rx.hstack(
                    rx.icon(tag="file", size=14, color="#a78bfa"),
                    rx.text(f, color="white", font_size="13px",
                            cursor="pointer",
                            on_click=OSState.select_file(f)),
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
                background="rgba(0,0,0,0.3)", padding="10px",
                border_radius="6px", margin_top="8px",
            )
        ),
        align="start", padding="16px", spacing="3", width="100%",
    )


def calculator_content():
    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
        ["C"],
    ]
    return rx.vstack(
        rx.box(
            rx.text(OSState.calc_input, color="#94a3b8", font_size="13px",
                    text_align="right"),
            rx.text(OSState.calc_result, color="white", font_size="28px",
                    font_weight="700", text_align="right"),
            background="rgba(0,0,0,0.3)", padding="12px",
            border_radius="8px", width="100%",
        ),
        rx.vstack(
            *[
                rx.hstack(
                    *[
                        rx.button(
                            btn,
                            on_click=OSState.calc_press(btn),
                            width="60px", height="44px",
                            color_scheme="violet" if btn in ["=", "C"] else "gray",
                            size="2",
                        )
                        for btn in row
                    ],
                    spacing="2",
                )
                for row in buttons
            ],
            spacing="2",
        ),
        align="center", padding="16px", spacing="3",
    )


def terminal_content():
    return rx.vstack(
        rx.box(
            rx.foreach(
                OSState.terminal_logs,
                lambda line: rx.text(line, color="#4ade80",
                                     font_family="monospace", font_size="13px"),
            ),
            background="rgba(0,0,0,0.5)", padding="12px",
            border_radius="6px", height="200px", overflow_y="auto",
            width="100%",
        ),
        rx.hstack(
            rx.text("$ ", color="#4ade80", font_family="monospace"),
            rx.input(
                value=OSState.terminal_input,
                on_change=OSState.set_terminal_input,
                on_key_down=lambda k: OSState.run_command() if k == "Enter" else None,
                placeholder="type a command...",
                background="transparent",
                border="none",
                color="#4ade80",
                font_family="monospace",
                width="100%",
                _focus={"outline": "none"},
            ),
            width="100%",
        ),
        align="start", padding="16px", spacing="3", width="100%",
    )


def notepad_content():
    return rx.vstack(
        rx.text_area(
            value=OSState.notepad_text,
            on_change=OSState.set_notepad_text,
            height="240px",
            width="100%",
            background="rgba(0,0,0,0.3)",
            color="white",
            border="1px solid rgba(255,255,255,0.1)",
            border_radius="6px",
            padding="10px",
            font_family="monospace",
            font_size="13px",
            resize="none",
        ),
        align="start", padding="16px", width="100%",
    )


def sysmon_content():
    return rx.vstack(
        rx.text("Active Processes", color="#a78bfa", font_weight="600"),
        rx.foreach(
            OSState.active_windows,
            lambda w: rx.hstack(
                rx.icon(tag="cpu", size=14, color="#4ade80"),
                rx.text(w["title"], color="white", font_size="13px"),
                rx.text(f"PID: {OSState.processes.get(w['title'], '?')}",
                        color="#94a3b8", font_size="12px"),
                spacing="2",
            )
        ),
        rx.divider(color="rgba(255,255,255,0.1)"),
        rx.text(f"Status: {OSState.system_status}",
                color=rx.cond(OSState.system_status == "nominal", "#4ade80", "#f87171"),
                font_size="13px"),
        rx.text(OSState.status_message, color="#94a3b8", font_size="12px"),
        align="start", padding="16px", spacing="2",
    )


def window_body(title: str):
    return rx.cond(title == "File Explorer", file_explorer_content(),
           rx.cond(title == "Calculator",    calculator_content(),
           rx.cond(title == "Terminal",      terminal_content(),
           rx.cond(title == "Notepad",       notepad_content(),
                                             sysmon_content()))))


def render_window(window: dict):
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon(tag="monitor", size=14, color="#a78bfa"),
                rx.text(window["title"], color="white",
                        font_size="13px", font_weight="600"),
                spacing="2",
            ),
            rx.button(
                rx.icon(tag="x", size=12),
                on_click=OSState.close_app(window["title"]),
                size="1", color_scheme="ruby",
                border_radius="50%", width="20px", height="20px",
            ),
            justify="between", width="100%",
            **{k: v for k, v in HEADER_STYLE.items() if k != "class_name"},
            class_name="window-header",
        ),
        window_body(window["title"]),
        **WINDOW_STYLE,
    )


# ── Taskbar ───────────────────────────────────────────────────────────────────
def taskbar():
    return rx.box(
        # Start button
        rx.button(
            rx.icon(tag="grid-2x2", size=16),
            rx.text("EduOS", font_weight="700", font_size="13px"),
            on_click=OSState.toggle_start_menu,
            background="linear-gradient(135deg,#7c3aed,#4f46e5)",
            color="white",
            border="none",
            border_radius="8px",
            padding="0 14px",
            height="32px",
            cursor="pointer",
            spacing="2",
            display="flex",
            align_items="center",
            gap="6px",
        ),
        # Divider
        rx.divider(orientation="vertical", height="28px",
                   color="rgba(255,255,255,0.15)"),
        # Open windows chips
        rx.foreach(
            OSState.active_windows,
            lambda w: rx.box(
                rx.text(w["title"], color="white", font_size="12px"),
                background="rgba(255,255,255,0.08)",
                border="1px solid rgba(255,255,255,0.12)",
                border_radius="6px",
                padding="4px 12px",
                cursor="pointer",
            )
        ),
        # Clock spacer
        rx.spacer(),
        rx.text("EduOS on CasaOS", color="#94a3b8", font_size="11px"),
        **TASKBAR_STYLE,
    )


# ── Start Menu ────────────────────────────────────────────────────────────────
STUDY_SUBJECTS = {
    "Mathematics": ["Algebra", "Calculus", "Statistics"],
    "Science": ["Physics", "Chemistry", "Biology"],
    "Technology": ["Programming", "Networks", "AI/ML"],
    "Languages": ["English Grammar", "Essay Writing"],
}

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
                        *[rx.text(f"  • {item}", color="#cbd5e1",
                                  font_size="12px", cursor="pointer",
                                  _hover={"color": "white"})
                          for item in items],
                        align="start", spacing="1",
                    )
                    for subject, items in STUDY_SUBJECTS.items()
                ],
                align="start", spacing="3", width="100%",
            ),
            position="fixed",
            bottom="52px",
            left="16px",
            width="220px",
            background="rgba(15,15,30,0.95)",
            backdrop_filter="blur(20px)",
            border="1px solid rgba(255,255,255,0.12)",
            border_radius="12px",
            padding="16px",
            z_index="200",
        ),
    )


# ── Desktop Icons ─────────────────────────────────────────────────────────────
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
                **ICON_STYLE,
            )
            for icon, label in DESKTOP_APPS
        ],
        position="absolute",
        top="24px",
        left="24px",
        spacing="2",
    )


# ── Index page ────────────────────────────────────────────────────────────────
def index():
    return rx.box(
        # Background
        rx.box(
            position="absolute", top="0", left="0",
            right="0", bottom="0",
            background="radial-gradient(ellipse at 20% 50%, rgba(124,58,237,0.15) 0%, transparent 60%), "
                       "radial-gradient(ellipse at 80% 20%, rgba(79,70,229,0.1) 0%, transparent 50%)",
            pointer_events="none",
        ),
        # Desktop icons
        desktop_icons(),
        # Open windows
        rx.foreach(OSState.active_windows, render_window),
        # Start menu
        start_menu(),
        # Taskbar
        taskbar(),
        **DESKTOP_STYLE,
    )


app = rx.App(
    stylesheets=["https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"],
)
app.add_page(index, title="EduOS — CasaOS Edition")
