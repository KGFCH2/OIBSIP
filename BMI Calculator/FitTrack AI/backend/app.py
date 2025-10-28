"""
Interactive GUI BMI Calculator using Tkinter

This file contains a self-contained Tkinter application that:
 - Shows a particle background
 - Provides weight and height inputs
 - Calculates BMI using `bmi.calculate_bmi`
 - Shows result on a flip-card style container
 - Supports dark/light themes with persistence
 - Implements simple hover/glow effects and a soft click sound on Windows

Note: The flip animation is simulated by shrinking the card width to 0 then expanding
while swapping the front/back content. This approach works with Tkinter geometry.
"""
import json
import os
import sys
import threading
import time
from pathlib import Path
from typing import List, Dict

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except Exception as e:
    print("Tkinter import failed:", e)
    raise

# Import BMI helpers in a way that works when the module is executed as a package
# (python -m backend.app) and when run directly (python backend/app.py).
try:
    from backend.bmi import calculate_bmi, categorize_bmi
except ModuleNotFoundError:
    try:
        # If executing the script directly from the backend folder, import the sibling module
        from bmi import calculate_bmi, categorize_bmi
    except Exception:
        # As a last resort, add the parent folder to sys.path and import by package name
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from backend.bmi import calculate_bmi, categorize_bmi

CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config():
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    return {"theme": "dark"}


def save_config(cfg: dict):
    try:
        CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
    except Exception:
        pass


class Particle:
    def __init__(self, canvas: tk.Canvas, w: int, h: int, theme: str = "dark"):
        import random

        self.canvas = canvas
        self.w = w
        self.h = h
        self.r = random.randint(2, 6)
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        self.dx = random.uniform(-0.5, 0.5)
        self.dy = random.uniform(-0.2, 0.7)
        base = "#9b59b6" if theme == "dark" else "#95a5a6"
        self.color = base
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color, outline="")

    def step(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < -10:
            self.x = self.w + 10
        if self.x > self.w + 10:
            self.x = -10
        if self.y > self.h + 10:
            self.y = -10
        self.canvas.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)


class BMIGUI:
    WIDTH = 500
    HEIGHT = 400

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)

        self.cfg = load_config()
        self.theme = self.cfg.get("theme", "dark")

        # Main canvas for background and particles
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.particles: List[Particle] = []
        self._make_particles()

        # Card container (center)
        self.card_width = 380
        self.card_height = 260
        self.card_x = (self.WIDTH - self.card_width) // 2
        self.card_y = (self.HEIGHT - self.card_height) // 2

        # A frame to hold front/back; we'll place with absolute coords
        self.card_container = tk.Frame(self.canvas, bg=self._bg_color())
        self.card_window = self.canvas.create_window(self.WIDTH // 2, self.HEIGHT // 2, window=self.card_container, width=self.card_width, height=self.card_height)

        # Build front and back
        self.front = tk.Frame(self.card_container, bg=self._card_bg())
        self.back = tk.Frame(self.card_container, bg=self._card_bg())

        self._build_front()
        self._build_back()

        self.front.pack(fill=tk.BOTH, expand=True)

        # Controls
        self.is_flipped = False

        # Start animation loops
        self._animate_particles()

    def _bg_color(self):
        return "#0f0f0f" if self.theme == "dark" else "#F7F9FB"

    def _card_bg(self):
        return "#121212" if self.theme == "dark" else "#FFFFFF"

    def _fg_color(self):
        return "#FFFFFF" if self.theme == "dark" else "#222222"

    def _make_particles(self):
        # Create a few particles
        self.canvas.configure(bg=self._bg_color())
        for _ in range(40):
            p = Particle(self.canvas, self.WIDTH, self.HEIGHT, theme=self.theme)
            self.particles.append(p)

    def _animate_particles(self):
        for p in self.particles:
            p.step()
        self.root.after(40, self._animate_particles)

    def _build_front(self):
        # Title with neon-like label
        title = tk.Label(self.front, text="BMI Calculator", font=("Segoe UI", 18, "bold"), bg=self._card_bg(), fg=self._fg_color())
        title.pack(pady=(16, 6))

        # Inputs
        inputs = tk.Frame(self.front, bg=self._card_bg())
        inputs.pack(pady=6)

        tk.Label(inputs, text="Weight (kg)", bg=self._card_bg(), fg=self._fg_color()).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(inputs, textvariable=self.weight_var, width=18)
        self.weight_entry.grid(row=0, column=1, padx=8, pady=6)

        tk.Label(inputs, text="Height (m)", bg=self._card_bg(), fg=self._fg_color()).grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.height_var = tk.StringVar()
        self.height_entry = ttk.Entry(inputs, textvariable=self.height_var, width=18)
        self.height_entry.grid(row=1, column=1, padx=8, pady=6)

        # Buttons
        btn_row = tk.Frame(self.front, bg=self._card_bg())
        btn_row.pack(pady=(12, 6))

        self.calc_btn = tk.Button(btn_row, text="Calculate BMI", command=self.on_calculate, relief=tk.FLAT, bg="#2c3e50", fg="#fff", padx=12, pady=6)
        self.calc_btn.grid(row=0, column=0, padx=8)
        self._bind_button_hover(self.calc_btn)

        reset_btn = tk.Button(btn_row, text="Reset", command=self.on_reset, relief=tk.FLAT, bg="#7f8c8d", fg="#fff", padx=12, pady=6)
        reset_btn.grid(row=0, column=1, padx=8)
        self._bind_button_hover(reset_btn)

        # Theme toggle
        theme_row = tk.Frame(self.front, bg=self._card_bg())
        theme_row.pack(pady=(6, 0))
        self.theme_btn = tk.Button(theme_row, text=("Light Mode" if self.theme == "dark" else "Dark Mode"), command=self.toggle_theme, relief=tk.FLAT, bg="#34495e", fg="#fff")
        self.theme_btn.pack()
        self._bind_button_hover(self.theme_btn)

    def _build_back(self):
        # Back side: result summary
        self.result_title = tk.Label(self.back, text="Result", font=("Segoe UI", 16, "bold"), bg=self._card_bg(), fg=self._fg_color())
        self.result_title.pack(pady=(20, 8))

        self.bmi_value_label = tk.Label(self.back, text="", font=("Segoe UI", 28, "bold"), bg=self._card_bg(), fg=self._fg_color())
        self.bmi_value_label.pack(pady=6)

        self.bmi_cat_label = tk.Label(self.back, text="", font=("Segoe UI", 14), bg=self._card_bg(), fg=self._fg_color())
        self.bmi_cat_label.pack(pady=6)

        back_btn = tk.Button(self.back, text="Back", command=self.flip_back, relief=tk.FLAT, bg="#95a5a6", fg="#fff", padx=10)
        back_btn.pack(pady=12)
        self._bind_button_hover(back_btn)

    def _bind_button_hover(self, w: tk.Widget):
        # Simple hover glow animation
        def on_enter(e):
            w.configure(bg="#1abc9c")

        def on_leave(e):
            # reset based on text
            txt = getattr(w, "cget", lambda k: "")("text")
            if txt == "Calculate BMI":
                w.configure(bg="#2c3e50")
            elif txt == "Reset":
                w.configure(bg="#7f8c8d")
            else:
                w.configure(bg="#95a5a6")

        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)

    def on_reset(self):
        self.weight_var.set("")
        self.height_var.set("")

    def _play_click(self):
        # Soft click on Windows if available
        if sys.platform.startswith("win"):
            try:
                import winsound

                winsound.MessageBeep(winsound.MB_OK)
            except Exception:
                pass

    def on_calculate(self):
        # Validate inputs
        w = self.weight_var.get().strip()
        h = self.height_var.get().strip()
        try:
            if not w or not h:
                messagebox.showwarning("Missing data", "Please enter both weight and height.")
                return
            weight = float(w)
            height = float(h)
            if weight <= 0 or height <= 0:
                messagebox.showerror("Invalid data", "Weight and height must be positive numbers.")
                return
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter numeric values for weight and height.")
            return

        try:
            bmi_val = calculate_bmi(weight, height)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
            return

        cat, color = categorize_bmi(bmi_val)
        self.bmi_value_label.configure(text=str(bmi_val), fg=color)
        self.bmi_cat_label.configure(text=cat, fg=color)

        # Play click and animate
        threading.Thread(target=self._play_click, daemon=True).start()
        self.flip_card()

    def flip_card(self):
        # Simulate flip by shrinking container width to 10, swap, then expand
        if self.is_flipped:
            return

        steps = 12
        orig = self.card_width

        def anim_shrink(i=0):
            if i >= steps:
                # swap
                self.front.pack_forget()
                self.back.pack(fill=tk.BOTH, expand=True)
                self.is_flipped = True
                anim_expand(0)
                return
            w = int(orig * (1 - (i + 1) / steps))
            if w < 8:
                w = 8
            self.canvas.itemconfigure(self.card_window, width=w)
            self.root.after(16, lambda: anim_shrink(i + 1))

        def anim_expand(i=0):
            if i >= steps:
                self.canvas.itemconfigure(self.card_window, width=orig)
                return
            w = int(orig * ((i + 1) / steps))
            if w < 8:
                w = 8
            self.canvas.itemconfigure(self.card_window, width=w)
            self.root.after(16, lambda: anim_expand(i + 1))

        anim_shrink()

    def flip_back(self):
        if not self.is_flipped:
            return
        steps = 12
        orig = self.card_width

        def anim_shrink(i=0):
            if i >= steps:
                self.back.pack_forget()
                self.front.pack(fill=tk.BOTH, expand=True)
                self.is_flipped = False
                anim_expand(0)
                return
            w = int(orig * (1 - (i + 1) / steps))
            if w < 8:
                w = 8
            self.canvas.itemconfigure(self.card_window, width=w)
            self.root.after(16, lambda: anim_shrink(i + 1))

        def anim_expand(i=0):
            if i >= steps:
                self.canvas.itemconfigure(self.card_window, width=orig)
                return
            w = int(orig * ((i + 1) / steps))
            if w < 8:
                w = 8
            self.canvas.itemconfigure(self.card_window, width=w)
            self.root.after(16, lambda: anim_expand(i + 1))

        anim_shrink()

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.cfg["theme"] = self.theme
        save_config(self.cfg)
        # Simple restart of UI colors
        self.canvas.configure(bg=self._bg_color())
        self.front.configure(bg=self._card_bg())
        self.back.configure(bg=self._card_bg())
        for widget in self.front.winfo_children():
            try:
                widget.configure(bg=self._card_bg(), fg=self._fg_color())
            except Exception:
                pass
        for widget in self.back.winfo_children():
            try:
                widget.configure(bg=self._card_bg(), fg=self._fg_color())
            except Exception:
                pass
        self.theme_btn.configure(text=("Light Mode" if self.theme == "dark" else "Dark Mode"))


def main():
    root = tk.Tk()
    app = BMIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
