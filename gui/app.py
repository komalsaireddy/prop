import sys
import os
import re
from datetime import datetime
from tkinter import colorchooser

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox, ttk

from dsl.parser import compile_rule, BehaviorLanguageError
from intent.engine import get_intent_from_ir
from simulator.context import get_context
from safety.kernel import evaluate
from logs.decision_log import log_decision

from adapter.command_adapter import (
    send_command,
    send_simulated_command,
    get_adapter_status
)


class GDBLCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GDBL Compiler – Governed Drone Platform")
        self.root.geometry("1000x760")

        self.compiled_ir = None
        self.editor_font_size = 12

        self.simulator_enabled = tk.BooleanVar(value=False)
        self.sim_running = False

        self.keyword_color = "#569CD6"

        self._build_ui()
        self._auto_refresh_hardware()

    # ================= UI =================

    def _build_ui(self):
        self._build_toolbar()
        self._build_hardware_status()
        self._build_tabs()
        self._build_editor()
        self._build_logs()
        self._build_controls()
        self._build_status()

    def _build_toolbar(self):
        bar = tk.Frame(self.root, bg="#dddddd")
        bar.pack(fill=tk.X)

        tk.Checkbutton(
            bar,
            text="Simulator Mode (Practice)",
            variable=self.simulator_enabled,
            bg="#dddddd"
        ).pack(side=tk.RIGHT, padx=10)

        tk.Button(bar, text="Keyword Color", command=self.pick_keyword_color).pack(side=tk.LEFT, padx=5)
        tk.Button(bar, text="+ Font", command=self.increase_font).pack(side=tk.LEFT, padx=5)
        tk.Button(bar, text="- Font", command=self.decrease_font).pack(side=tk.LEFT, padx=5)

    # ================= HARDWARE =================

    def _build_hardware_status(self):
        frame = tk.Frame(self.root, bg="#202020", padx=10, pady=6)
        frame.pack(fill=tk.X)

        self.hw_status = tk.StringVar(value="NOT CONNECTED")

        tk.Label(frame, text="Hardware:", fg="white", bg="#202020").pack(side=tk.LEFT)
        self.hw_label = tk.Label(frame, textvariable=self.hw_status, fg="red", bg="#202020")
        self.hw_label.pack(side=tk.LEFT, padx=12)

    def _auto_refresh_hardware(self):
        status = get_adapter_status()

        if status["connected"]:
            self.hw_status.set("CONNECTED (REAL DRONE)")
            self.hw_label.config(fg="lime")
            self.run_btn.config(state=tk.NORMAL)
        else:
            self.hw_status.set("NOT CONNECTED")
            self.hw_label.config(fg="red")
            if not self.simulator_enabled.get():
                self.run_btn.config(state=tk.DISABLED)

        self.root.after(1000, self._auto_refresh_hardware)

    # ================= TABS =================

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.editor_tab = tk.Frame(self.notebook)
        self.logs_tab = tk.Frame(self.notebook)

        self.notebook.add(self.editor_tab, text="Editor")
        self.notebook.add(self.logs_tab, text="Action Logs")

    # ================= EDITOR =================

    def _build_editor(self):
        frame = tk.Frame(self.editor_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.editor = tk.Text(
            frame,
            font=("Consolas", self.editor_font_size),
            bg="#1e1e1e",
            fg="#dcdcdc",
            insertbackground="white"
        )
        self.editor.pack(fill=tk.BOTH, expand=True)

        self.editor.insert(
            tk.END,
            "RULE avoid_risk\nWHEN anomaly_detected\nIF confidence > 0.7\nDO RETURN_HOME"
        )

        self.editor.bind("<KeyRelease>", self.apply_syntax_highlighting)

        self.console = tk.Text(
            frame,
            height=7,
            state=tk.DISABLED,
            bg="#111111",
            fg="#e0e0e0",
            font=("Consolas", 10)
        )
        self.console.pack(fill=tk.X, pady=8)

    # ================= LOGS =================

    def _build_logs(self):
        self.logs = tk.Text(
            self.logs_tab,
            state=tk.DISABLED,
            bg="#0d0d0d",
            fg="#e0e0e0",
            font=("Consolas", 10)
        )
        self.logs.pack(fill=tk.BOTH, expand=True)

    # ================= CONTROLS =================

    def _build_controls(self):
        controls = tk.Frame(self.root)
        controls.pack(pady=10)

        btn = dict(width=16, height=2)

        tk.Button(controls, text="COMPILE", command=self.compile_code, **btn).pack(side=tk.LEFT, padx=8)

        self.run_btn = tk.Button(
            controls, text="RUN", command=self.run_code, state=tk.DISABLED, **btn
        )
        self.run_btn.pack(side=tk.LEFT, padx=8)

        tk.Button(controls, text="ABORT", command=self.abort, **btn).pack(side=tk.LEFT, padx=8)
        tk.Button(controls, text="CLEAR", command=self.clear_console, **btn).pack(side=tk.LEFT, padx=8)

    # ================= STATUS =================

    def _build_status(self):
        self.status = tk.StringVar(value="Status: Not compiled")
        tk.Label(self.root, textvariable=self.status, fg="cyan").pack(fill=tk.X)

    # ================= CORE =================

    def compile_code(self):
        try:
            self.compiled_ir = compile_rule(self.editor.get("1.0", tk.END))
            self.status.set("Compiled successfully")
            self.log_console("Compile successful")
            self.run_btn.config(state=tk.NORMAL)
        except BehaviorLanguageError as e:
            self.status.set("Compile error")
            messagebox.showerror("Compile Error", str(e))

    def run_code(self):
        if not self.compiled_ir:
            self.log_console("ERROR: Compile first")
            return

        if self.simulator_enabled.get():
            if self.sim_running:
                return
            self.sim_running = True
            self.log_console("[SIMULATION STARTED]")
            self._sim_loop()
            return

        status = get_adapter_status()
        if not status["connected"]:
            self.log_console("ERROR: No real drone connected")
            return

        intent, ai_signal = get_intent_from_ir(self.compiled_ir)
        context = get_context()
        decision, action, reason = evaluate(intent, context)
        log_decision(intent, decision, action, reason)
        send_command(action)

        self.log_console(f"AI SIGNAL: {ai_signal}")
        self.log_console(f"INTENT: {intent}")
        self.log_console(f"DECISION: {decision}")
        self.log_console(f"ACTION: {action}")
        self.log_console(f"REASON: {reason}")
        self.log_console("-" * 40)

    def _sim_loop(self):
        if not self.sim_running:
            return

        intent, ai_signal = get_intent_from_ir(self.compiled_ir)
        context = get_context()
        decision, action, reason = evaluate(intent, context)

        log_decision(intent, decision, action, reason)
        send_simulated_command(action)

        # Console output (restored)
        self.log_console(f"AI SIGNAL: {ai_signal}")
        self.log_console(f"INTENT: {intent}")
        self.log_console(f"DECISION: {decision}")
        self.log_console(f"ACTION: {action}")
        self.log_console(f"REASON: {reason}")
        self.log_console("-" * 40)

        # Action logs tab (restored)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.config(state=tk.NORMAL)
        self.logs.insert(
            tk.END,
            f"[{ts}] SIM | INTENT={intent} | DECISION={decision} | ACTION={action} | REASON={reason}\n"
        )
        self.logs.see(tk.END)
        self.logs.config(state=tk.DISABLED)

        self.root.after(1000, self._sim_loop)

    def abort(self):
        self.sim_running = False
        if self.simulator_enabled.get():
            send_simulated_command("ABORT")
        else:
            send_command("ABORT")
        self.log_console("ABORT sent")

    # ================= UTIL =================

    def log_console(self, text):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)

    def clear_console(self):
        self.console.config(state=tk.NORMAL)
        self.console.delete("1.0", tk.END)
        self.console.config(state=tk.DISABLED)

    def apply_syntax_highlighting(self, event=None):
        text = self.editor.get("1.0", tk.END)
        self.editor.tag_remove("kw", "1.0", tk.END)
        for m in re.finditer(r"\b(RULE|WHEN|IF|DO)\b", text):
            self.editor.tag_add("kw", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        self.editor.tag_config("kw", foreground=self.keyword_color)

    def pick_keyword_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.keyword_color = c
            self.apply_syntax_highlighting()

    def increase_font(self):
        self.editor_font_size += 1
        self.editor.config(font=("Consolas", self.editor_font_size))

    def decrease_font(self):
        if self.editor_font_size > 8:
            self.editor_font_size -= 1
            self.editor.config(font=("Consolas", self.editor_font_size))


if __name__ == "__main__":
    root = tk.Tk()
    GDBLCompilerGUI(root)
    root.mainloop()
