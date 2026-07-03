import reflex as rx
from typing import List, Dict, Any

# Define a custom React draggable wrapper component using React-Draggable
class Draggable(rx.Component):
    library = "react-draggable"
    tag = "Draggable"
    handle: rx.Var[str] = ".window-header"

class OSState(rx.State):
    # Active windows list: list of dicts with title, minimized, maximized
    active_windows: list[dict] = []
    
    # Simple File System
    file_system: dict[str, list[str]] = {
        "C_Drive": ["System32", "Users", "Program Files", "kernel.sys", "config.json"],
        "D_Drive": ["Documents", "Downloads", "SPM_Project", "edu_os_specs.md", "notes.txt"]
    }
    
    # Drive navigation and selected files
    current_drive: str = "C_Drive"
    selected_file: str = ""
    file_content: str = ""
    
    # Calculator state
    calc_input: str = ""
    calc_result: str = "0"
    
    # Terminal logs
    terminal_logs: list[str] = [
        "EduOS Kernel v1.0.0 (x86_64)",
        "Initializing virtual memory manager...",
        "Mounting file system: C_Drive, D_Drive...",
        "System Ready. Welcome to EduOS!",
        "guest@edu_os:~$ "
    ]
    
    # Text Editor state
    notepad_text: str = "Welcome to EduOS! Double-click on any desktop icon to open the corresponding application. Feel free to explore."

    # App management
    def open_app(self, name: str):
        # If already open, bring to front (by removing and appending to end of list)
        for window in self.active_windows:
            if window["title"] == name:
                self.active_windows.remove(window)
                self.active_windows.append(window)
                return
        
        # Add a new window config
        self.active_windows.append({
            "title": name,
            "minimized": False,
            "maximized": False,
        })

    def close_app(self, name: str):
        self.active_windows = [w for w in self.active_windows if w["title"] != name]

    # File Explorer
    def select_drive(self, drive: str):
        self.current_drive = drive
        self.selected_file = ""
        self.file_content = ""

    def read_file(self, filename: str):
        self.selected_file = filename
        if filename == "edu_os_specs.md":
            self.file_content = "# EduOS System Specifications\n- Kernel: Custom Reflex OSState\n- Architecture: Web-Native\n- UI Framework: Radix UI / Tailwind CSS\n- Project Directory: /KE/SPM"
        elif filename == "notes.txt":
            self.file_content = "This is a simple text note. You can edit notes inside the Notepad app!"
        elif filename == "config.json":
            self.file_content = '{\n  "version": "1.0.0",\n  "theme": "glassmorphism-dark",\n  "dev_mode": true\n}'
        elif filename == "kernel.sys":
            self.file_content = "[BINARY DATA: 0x4A6B9C2D3E4F]"
        else:
            self.file_content = f"Contents of {filename} (Read-Only Mode)"

    # Calculator
    def calc_press(self, key: str):
        if key == "C":
            self.calc_input = ""
            self.calc_result = "0"
        elif key == "=":
            try:
                allowed_chars = "0123456789+-*/. "
                if all(c in allowed_chars for c in self.calc_input):
                    self.calc_result = str(eval(self.calc_input))
                else:
                    self.calc_result = "Error"
            except Exception:
                self.calc_result = "Error"
            self.calc_input = self.calc_result
        else:
            if self.calc_input == "0" or self.calc_result == "Error":
                self.calc_input = key
            else:
                self.calc_input += key

    # Terminal command handler
    def execute_terminal_cmd(self, form_data: dict):
        cmd = form_data.get("terminal_input", "").strip()
        if not cmd:
            return
        
        self.terminal_logs.append(f"guest@edu_os:~$ {cmd}")
        cmd_parts = cmd.split()
        base_cmd = cmd_parts[0].lower()
        
        if base_cmd == "help":
            self.terminal_logs.extend([
                "Available commands:",
                "  help       - Show this message",
                "  ls         - List files in current directory",
                "  cat [file] - Display file content",
                "  clear      - Clear terminal logs",
                "  neofetch   - Display system specs"
            ])
        elif base_cmd == "clear":
            self.terminal_logs = ["guest@edu_os:~$ "]
            return
        elif base_cmd == "ls":
            self.terminal_logs.append("C_Drive/  D_Drive/")
        elif base_cmd == "neofetch":
            self.terminal_logs.extend([
                "   /\\_/\\      OS: EduOS v1.0.0",
                "  ( o.o )     Kernel: Python 3.10 / Reflex",
                "   > ^ <      Uptime: 2 mins",
                "              Shell: Bash-Interactive",
                "              Memory: 256MB / 4096MB"
            ])
        elif base_cmd == "cat":
            if len(cmd_parts) > 1:
                filename = cmd_parts[1]
                found = False
                for drive, files in self.file_system.items():
                    if filename in files:
                        found = True
                        if filename == "edu_os_specs.md":
                            self.terminal_logs.append("Kernel: Custom Reflex OSState")
                        elif filename == "notes.txt":
                            self.terminal_logs.append("This is a simple text note.")
                        else:
                            self.terminal_logs.append(f"[Mock Content of {filename}]")
                if not found:
                    self.terminal_logs.append(f"cat: {filename}: No such file or directory")
            else:
                self.terminal_logs.append("cat: missing file operand")
        else:
            self.terminal_logs.append(f"sh: command not found: {base_cmd}")
            
        self.terminal_logs.append("guest@edu_os:~$ ")


# ------------------- UI COMPONENTS -------------------

def desktop_icon(name: str, icon_tag: str) -> rx.Component:
    """Renders a double-clickable or single-clickable desktop icon."""
    return rx.button(
        rx.vstack(
            rx.icon(
                tag=icon_tag,
                size=32,
                color="rgba(255, 255, 255, 0.95)",
                style={"filter": "drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3))"}
            ),
            rx.text(
                name,
                color="white",
                font_size="xs",
                font_weight="medium",
                style={"text-shadow": "0 2px 4px rgba(0,0,0,0.8)"}
            ),
            spacing="1",
            align="center",
        ),
        on_click=OSState.open_app(name),
        background="transparent",
        _hover={"background": "rgba(255, 255, 255, 0.15)", "transform": "scale(1.05)"},
        border_radius="md",
        padding="3",
        width="20",
        height="20",
        transition="all 0.2s ease",
    )


def render_explorer() -> rx.Component:
    """Renders the file explorer inside a window."""
    return rx.grid(
        # Drive Selector (Left Pane)
        rx.vstack(
            rx.text("Drives", font_size="sm", font_weight="bold", color="gray.300", padding_left="2"),
            rx.button(
                rx.hstack(rx.icon(tag="database", size=16), rx.text("C: Drive", font_size="sm")),
                width="full",
                variant="ghost",
                on_click=OSState.select_drive("C_Drive"),
                color="white" if OSState.current_drive == "C_Drive" else "gray.400",
                background="rgba(255, 255, 255, 0.08)" if OSState.current_drive == "C_Drive" else "transparent",
            ),
            rx.button(
                rx.hstack(rx.icon(tag="database", size=16), rx.text("D: Drive", font_size="sm")),
                width="full",
                variant="ghost",
                on_click=OSState.select_drive("D_Drive"),
                color="white" if OSState.current_drive == "D_Drive" else "gray.400",
                background="rgba(255, 255, 255, 0.08)" if OSState.current_drive == "D_Drive" else "transparent",
            ),
            border_right="1px solid rgba(255, 255, 255, 0.1)",
            padding="2",
            spacing="2",
            height="full",
            align_items="start",
        ),
        
        # Files List (Middle Pane)
        rx.vstack(
            rx.text("Files", font_size="sm", font_weight="bold", color="gray.300", padding_left="2"),
            rx.vstack(
                rx.foreach(
                    OSState.file_system[OSState.current_drive],
                    lambda file: rx.button(
                        rx.hstack(rx.icon(tag="file", size=16), rx.text(file, font_size="sm")),
                        width="full",
                        variant="ghost",
                        color="white" if OSState.selected_file == file else "gray.300",
                        background="rgba(255, 255, 255, 0.08)" if OSState.selected_file == file else "transparent",
                        on_click=OSState.read_file(file),
                    )
                ),
                width="full",
                spacing="1",
            ),
            padding="2",
            spacing="2",
            height="full",
            align_items="start",
        ),
        
        # File Content Viewer (Right Pane)
        rx.vstack(
            rx.text("File Preview", font_size="sm", font_weight="bold", color="gray.300"),
            rx.cond(
                OSState.selected_file,
                rx.vstack(
                    rx.text(OSState.selected_file, font_size="xs", color="teal.300", font_weight="semibold"),
                    rx.scroll_area(
                        rx.text(
                            OSState.file_content,
                            font_size="xs",
                            font_family="monospace",
                            color="gray.200",
                            white_space="pre-wrap",
                        ),
                        height="200px",
                        width="full",
                    ),
                    spacing="2",
                    align_items="start",
                    width="full",
                ),
                rx.text("Select a file to preview its contents.", font_size="xs", color="gray.500")
            ),
            padding="2",
            spacing="2",
            height="full",
            align_items="start",
        ),
        columns="3",
        spacing="2",
        width="full",
        height="300px",
    )


def render_calculator() -> rx.Component:
    """Renders the simple calculator app."""
    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", "=", "+"]
    ]
    return rx.vstack(
        rx.box(
            rx.text(
                OSState.calc_input,
                font_size="lg",
                color="gray.400",
                text_align="right",
                height="6",
                overflow="hidden"
            ),
            rx.text(
                OSState.calc_result,
                font_size="2xl",
                color="white",
                font_weight="bold",
                text_align="right"
            ),
            width="full",
            background="rgba(0,0,0,0.3)",
            padding="3",
            border_radius="md",
            border="1px solid rgba(255, 255, 255, 0.1)",
        ),
        rx.grid(
            rx.foreach(
                buttons,
                lambda row: rx.foreach(
                    row,
                    lambda btn: rx.button(
                        btn,
                        on_click=OSState.calc_press(btn),
                        color="white",
                        background="rgba(255, 255, 255, 0.12)" if btn not in ["+", "-", "*", "/", "=", "C"]
                        else "rgba(20, 110, 190, 0.6)" if btn == "="
                        else "rgba(240, 80, 80, 0.6)" if btn == "C"
                        else "rgba(255, 255, 255, 0.2)",
                        _hover={"background": "rgba(255, 255, 255, 0.25)"},
                        width="full",
                        height="12",
                        font_size="md",
                        font_weight="semibold",
                    )
                )
            ),
            columns="4",
            spacing="2",
            width="full",
        ),
        width="280px",
        spacing="3",
        align="stretch",
    )


def render_terminal() -> rx.Component:
    """Renders the interactive command-line terminal."""
    return rx.vstack(
        rx.scroll_area(
            rx.vstack(
                rx.foreach(
                    OSState.terminal_logs,
                    lambda log: rx.text(
                        log,
                        color="green.300" if "guest@edu_os" in log else "white" if not log.startswith(" ") else "gray.400",
                        font_family="monospace",
                        font_size="xs",
                        white_space="pre-wrap"
                    )
                ),
                align_items="start",
                spacing="1",
            ),
            height="220px",
            width="full",
            background="black",
            border_radius="md",
            padding="3",
            border="1px solid rgba(255, 255, 255, 0.15)",
        ),
        rx.form(
            rx.hstack(
                rx.text("guest@edu_os:~$", color="green.300", font_family="monospace", font_size="xs", align_self="center"),
                rx.input(
                    id="terminal_input",
                    placeholder="Type help...",
                    color="white",
                    background="transparent",
                    border="none",
                    _focus={"border": "none", "outline": "none"},
                    font_family="monospace",
                    font_size="xs",
                    width="full",
                ),
                rx.button("Execute", type="submit", size="1", color_scheme="teal", variant="solid"),
                width="full",
                spacing="2",
            ),
            on_submit=OSState.execute_terminal_cmd,
            reset_on_submit=True,
            width="full",
        ),
        width="full",
        spacing="2",
    )


def render_notepad() -> rx.Component:
    """Renders notepad app."""
    return rx.vstack(
        rx.text_area(
            value=OSState.notepad_text,
            on_change=OSState.set_notepad_text,
            width="full",
            height="220px",
            background="rgba(255,255,255,0.05)",
            color="white",
            border="1px solid rgba(255,255,255,0.1)",
            _focus={"border": "1px solid rgba(0, 150, 255, 0.5)"},
            font_size="sm",
        ),
        rx.text(
            f"Character count: {OSState.notepad_text.length()}",
            font_size="xs",
            color="gray.400",
            align_self="end"
        ),
        width="450px",
        spacing="2",
    )


def render_window(title: str) -> rx.Component:
    """Renders a styled, draggable window frame with specific application contents."""
    # Determine which sub-view to inject inside the window body
    content = rx.cond(
        title == "File Explorer",
        render_explorer(),
        rx.cond(
            title == "Calculator",
            render_calculator(),
            rx.cond(
                title == "Terminal",
                render_terminal(),
                rx.cond(
                    title == "Notepad",
                    render_notepad(),
                    rx.text(f"Welcome to {title}!", color="white")
                )
            )
        )
    )

    return Draggable(
        rx.box(
            # Window Header (Drag Handle)
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        tag="terminal" if title == "Terminal" 
                        else "folder" if title == "File Explorer"
                        else "calculator" if title == "Calculator"
                        else "file-text",
                        size=14,
                        color="gray.300"
                    ),
                    rx.text(
                        title,
                        color="white",
                        font_size="sm",
                        font_weight="bold",
                    ),
                    spacing="2",
                    align="center",
                ),
                # Window Action Buttons
                rx.hstack(
                    rx.button(
                        rx.icon(tag="minus", size=12),
                        variant="ghost",
                        size="1",
                        color="gray.400",
                        _hover={"color": "white", "background": "rgba(255,255,255,0.1)"},
                    ),
                    rx.button(
                        rx.icon(tag="square", size=10),
                        variant="ghost",
                        size="1",
                        color="gray.400",
                        _hover={"color": "white", "background": "rgba(255,255,255,0.1)"},
                    ),
                    rx.button(
                        rx.icon(tag="x", size=14),
                        on_click=OSState.close_app(title),
                        color="gray.400",
                        variant="ghost",
                        size="1",
                        _hover={"color": "white", "background": "rgba(240, 80, 80, 0.8)"},
                    ),
                    spacing="1",
                ),
                class_name="window-header",
                width="full",
                padding_x="3",
                padding_y="2",
                justify="between",
                background="rgba(15, 23, 42, 0.85)",
                border_top_left_radius="12px",
                border_top_right_radius="12px",
                border_bottom="1px solid rgba(255, 255, 255, 0.1)",
                style={"cursor": "move", "user-select": "none"},
            ),
            
            # Window Body
            rx.box(
                content,
                padding="4",
                background="rgba(15, 23, 42, 0.65)",
                backdrop_filter="blur(16px)",
                border_bottom_left_radius="12px",
                border_bottom_right_radius="12px",
            ),
            style={
                "width": "fit-content",
                "box-shadow": "0 20px 50px rgba(0, 0, 0, 0.5)",
                "border": "1px solid rgba(255, 255, 255, 0.15)",
                "border-radius": "12px",
                "z-index": "50",
            },
        ),
    )


def taskbar() -> rx.Component:
    """Renders the desktop bottom taskbar containing open windows."""
    return rx.box(
        rx.hstack(
            # Start button
            rx.button(
                rx.hstack(
                    rx.icon(tag="layers", size=16),
                    rx.text("EduOS", font_size="xs", font_weight="semibold"),
                    spacing="2",
                ),
                color="white",
                background="rgba(255, 255, 255, 0.15)",
                _hover={"background": "rgba(255, 255, 255, 0.25)"},
                border_radius="md",
                size="2",
            ),
            
            # Active tasks indicator
            rx.hstack(
                rx.foreach(
                    OSState.active_windows,
                    lambda w: rx.button(
                        rx.hstack(
                            rx.box(
                                width="2",
                                height="2",
                                border_radius="full",
                                background="teal.400"
                            ),
                            rx.text(w["title"], font_size="xs", font_weight="medium"),
                            spacing="2",
                            align="center",
                        ),
                        variant="solid",
                        background="rgba(255, 255, 255, 0.1)",
                        _hover={"background": "rgba(255, 255, 255, 0.2)"},
                        color="white",
                        size="2",
                    )
                ),
                spacing="2",
            ),
            
            # System Clock and indicators (right-aligned)
            rx.hstack(
                rx.icon(tag="wifi", size=14, color="white"),
                rx.icon(tag="volume-2", size=14, color="white"),
                rx.text("14:24", color="white", font_size="xs", font_weight="bold"),
                spacing="3",
                align="center",
            ),
            justify="between",
            align="center",
            width="full",
            padding_x="4",
            padding_y="2",
        ),
        position="fixed",
        bottom="0",
        left="0",
        right="0",
        height="12",
        background="rgba(15, 23, 42, 0.75)",
        backdrop_filter="blur(20px)",
        border_top="1px solid rgba(255, 255, 255, 0.1)",
        z_index="100",
    )


def index() -> rx.Component:
    """The main desktop view."""
    return rx.box(
        # Beautiful gradient background wallpaper
        style={
            "background": "radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), "
                          "radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), "
                          "radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%), "
                          "radial-gradient(at 0% 100%, hsla(339,49%,30%,1) 0, transparent 50%), "
                          "radial-gradient(at 100% 100%, hsla(256,40%,25%,1) 0, transparent 50%)",
            "background-color": "hsla(253,16%,7%,1)",
            "width": "100vw",
            "height": "100vh",
            "overflow": "hidden",
            "position": "relative",
        },
        
        # Grid of Desktop Icons (Top Left)
        rx.vstack(
            desktop_icon("File Explorer", "folder"),
            desktop_icon("Calculator", "calculator"),
            desktop_icon("Terminal", "terminal"),
            desktop_icon("Notepad", "file-text"),
            position="absolute",
            top="6",
            left="6",
            spacing="4",
        ),
        
        # Render all active app windows
        rx.box(
            rx.foreach(
                OSState.active_windows,
                lambda w: render_window(w["title"])
            ),
            position="absolute",
            top="0",
            left="0",
            width="full",
            height="full",
        ),
        
        # Bottom Taskbar
        taskbar(),
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        accent_color="teal",
    )
)
app.add_page(index, title="EduOS - Virtual reflex Learning Environment")
