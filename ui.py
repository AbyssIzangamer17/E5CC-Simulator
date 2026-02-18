import tkinter as tk
from tkinter import ttk
import time
import threading
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

class E5CC_UI:
    def __init__(self, root, simulator):
        self.root = root
        self.simulator = simulator
        self.root.title("Omron E5CC Virtual Simulator")
        self.root.geometry("450x800")
        self.root.configure(bg="#1a1a1a")

        # Premium Design tokens
        self.bg_color = "#1a1a1a"
        self.panel_color = "#333333"
        self.display_bg = "#000000"
        self.pv_color = "#ffffff"
        self.sv_color = "#00ff00"
        self.accent_color = "#ff9900"
        
        self.pv_font = ("Consolas", 54, "bold")
        self.sv_font = ("Consolas", 36, "bold")
        self.label_font = ("Verdana", 9, "bold")

        # State management
        self.level = "Operation" # Operation, Adjustment, Initial
        self.menu_index = 0
        self.update_count = 0
        
        self.setup_ui()
        if HAS_MATPLOTLIB:
            self.setup_graph()
        self.update_loop()

    def setup_ui(self):
        # Front Panel Case
        self.case = tk.Frame(self.root, bg="#222", bd=4, relief="raised")
        self.case.pack(pady=20, padx=20, fill="x")

        # OMRON Logo & Model
        top_bar = tk.Frame(self.case, bg="#222")
        top_bar.pack(fill="x", pady=5, padx=10)
        tk.Label(top_bar, text="OMRON", bg="#222", fg="#005eb8", font=("Arial", 14, "bold")).pack(side="left")
        tk.Label(top_bar, text="E5CC", bg="#222", fg="white", font=("Arial", 12)).pack(side="right")

        # Display Section
        self.screen = tk.Frame(self.case, bg=self.display_bg, bd=8, relief="sunken")
        self.screen.pack(pady=10, padx=10, fill="x")

        # Status Indicators (Left side of screen)
        self.status_panel = tk.Frame(self.screen, bg=self.display_bg, width=60)
        self.status_panel.pack(side="left", fill="y", padx=10)
        
        self.out1_led = tk.Label(self.status_panel, text="OUT1", bg=self.display_bg, fg="#333", font=self.label_font)
        self.out1_led.pack(pady=2)
        
        self.at_led = tk.Label(self.status_panel, text="AT", bg=self.display_bg, fg="#333", font=self.label_font)
        self.at_led.pack(pady=2)

        # Values Vertical Frame
        values_frame = tk.Frame(self.screen, bg=self.display_bg)
        values_frame.pack(side="left", fill="both", expand=True)

        self.pv_display = tk.Label(values_frame, text="25.0", bg=self.display_bg, fg=self.pv_color, font=self.pv_font)
        self.pv_display.pack(anchor="e")

        self.sv_display = tk.Label(values_frame, text="50.0", bg=self.display_bg, fg=self.sv_color, font=self.sv_font)
        self.sv_display.pack(anchor="e")

        # Output Power Bar (Small vertical level)
        self.power_bg = tk.Frame(self.screen, bg="#111", width=12, height=120)
        self.power_bg.pack(side="right", padx=10, pady=10)
        self.power_bar = tk.Frame(self.power_bg, bg="red", width=12, height=0)
        self.power_bar.place(x=0, y=120, anchor="sw")

        # Control Buttons
        btn_container = tk.Frame(self.case, bg="#333", pady=15)
        btn_container.pack(fill="x")

        # Styling for industrial buttons
        btn_style = {"bg": "#555", "fg": "white", "relief": "raised", "bd": 3, "width": 5, "height": 2, "font": ("Arial", 10, "bold")}
        
        self.btn_level = tk.Button(btn_container, text="O", **btn_style)
        self.btn_level.pack(side="left", expand=True)
        self.btn_level.bind("<ButtonPress-1>", self.level_hold_start)
        self.btn_level.bind("<ButtonRelease-1>", self.level_hold_stop)

        self.btn_mode = tk.Button(btn_container, text="M", command=self.on_mode, **btn_style)
        self.btn_mode.pack(side="left", expand=True)

        self.btn_down = tk.Button(btn_container, text="▼", command=self.on_down, **btn_style)
        self.btn_down.pack(side="left", expand=True)

        self.btn_up = tk.Button(btn_container, text="▲", command=self.on_up, **btn_style)
        self.btn_up.pack(side="left", expand=True)

        # Disturbance Simulator Frame
        dist_frame = tk.LabelFrame(self.root, text=" Simulación de Carga / Valor Externo ", bg=self.bg_color, fg="#888", font=("Arial", 9))
        dist_frame.pack(fill="x", padx=20, pady=10)
        
        self.dist_slider = tk.Scale(dist_frame, from_=-40, to=40, orient="horizontal", bg=self.bg_color, fg=self.accent_color, 
                                   highlightthickness=0, troughcolor="#333", command=self.on_dist)
        self.dist_slider.set(0)
        self.dist_slider.pack(fill="x", padx=10, pady=5)
        
        self.dist_info = tk.Label(dist_frame, text="Perturbación térmica: 0.0°C", bg=self.bg_color, fg="#555")
        self.dist_info.pack()

        # Triple Correction Info (PID Telemetry)
        self.pid_frame = tk.Frame(self.root, bg=self.bg_color)
        self.pid_frame.pack(fill="x", padx=20, pady=10)
        
        self.p_label = tk.Label(self.pid_frame, text="P: 0.0%", bg=self.bg_color, fg="#ff4444", font=("Consolas", 9))
        self.p_label.pack(side="left", expand=True)
        
        self.i_label = tk.Label(self.pid_frame, text="I: 0.0%", bg=self.bg_color, fg="#44ff44", font=("Consolas", 9))
        self.i_label.pack(side="left", expand=True)
        
        self.d_label = tk.Label(self.pid_frame, text="D: 0.0%", bg=self.bg_color, fg="#4444ff", font=("Consolas", 9))
        self.d_label.pack(side="left", expand=True)

        # Footer Status
        self.status_bar = tk.Label(self.root, text="System Ready | Closed-Loop 50ms", bg="#000", fg="#444", font=("Arial", 8))
        self.status_bar.pack(side="bottom", fill="x")

    def level_hold_start(self, e): self.hold_time = time.time()
    def level_hold_stop(self, e):
        duration = time.time() - self.hold_time
        if duration > 3.0: self.go_init()
        elif duration > 0.1: self.toggle_adj()

    def toggle_adj(self):
        if self.level == "Operation":
            self.level = "Adjustment"
            self.adjustment_menus = ["L.ADJ", "AT", "P", "I", "D"]
        else:
            self.level = "Operation"
        self.menu_index = 0

    def go_init(self):
        self.level = "Initial"
        self.initial_menus = ["IN-T", "CNTL", "OREV"]
        self.menu_index = 0

    def on_mode(self):
        if self.level == "Adjustment": self.menu_index = (self.menu_index + 1) % len(self.adjustment_menus)
        elif self.level == "Initial": self.menu_index = (self.menu_index + 1) % len(self.initial_menus)

    def on_up(self):
        if self.level == "Operation": self.simulator.sv += 1.0
        elif self.level == "Adjustment":
            m = self.adjustment_menus[self.menu_index]
            if m == "AT":
                self.simulator.at_mode = "AT-2"
                self.simulator.at_active = True
            elif m == "P": self.simulator.p += 1.0
            elif m == "I": self.simulator.i += 10
            elif m == "D": self.simulator.d += 5
        elif self.level == "Initial":
            if self.initial_menus[self.menu_index] == "OREV": self.simulator.reverse = not self.simulator.reverse

    def on_down(self):
        if self.level == "Operation": self.simulator.sv -= 1.0
        elif self.level == "Adjustment":
            m = self.adjustment_menus[self.menu_index]
            if m == "AT":
                self.simulator.at_mode = "OFF"
                self.simulator.at_active = False
            elif m == "P": self.simulator.p = max(0.1, self.simulator.p - 1.0)
            elif m == "I": self.simulator.i = max(0, self.simulator.i - 10)
            elif m == "D": self.simulator.d = max(0, self.simulator.d - 5)
        elif self.level == "Initial":
            if self.initial_menus[self.menu_index] == "OREV": self.simulator.reverse = not self.simulator.reverse

    def on_dist(self, v):
        self.simulator.disturbance = float(v)
        self.dist_info.config(text=f"Perturbación térmica: {float(v):.1f}°C")

    def setup_graph(self):
        self.graph_frame = tk.Frame(self.root, bg=self.bg_color)
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=5)
        self.fig, self.ax = plt.subplots(figsize=(4, 3), facecolor=self.bg_color)
        self.ax.set_facecolor("black")
        self.ax.tick_params(colors="#555", labelsize=8)
        self.pv_data, self.sv_data, self.time_data = [], [], []
        self.pv_line, = self.ax.plot([], [], color="white", linewidth=1.5, label="PV")
        self.sv_line, = self.ax.plot([], [], color=self.sv_color, linewidth=1, linestyle="--", label="SV")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_loop(self):
        # Update Main Display
        if self.level == "Operation":
            self.pv_display.config(text=f"{self.simulator.pv:.1f}", fg=self.pv_color)
            self.sv_display.config(text=f"{self.simulator.sv:.1f}", fg=self.sv_color)
        else:
            menu = self.adjustment_menus[self.menu_index] if self.level == "Adjustment" else self.initial_menus[self.menu_index]
            self.pv_display.config(text=f"{menu}", fg=self.accent_color, font=("Consolas", 40, "bold"))
            val = ""
            if menu == "AT": val = self.simulator.at_mode
            elif menu == "P": val = f"{self.simulator.p:.1f}"
            elif menu == "I": val = f"{self.simulator.i}"
            elif menu == "D": val = f"{self.simulator.d}"
            elif menu == "OREV": val = "OR-R" if self.simulator.reverse else "OR-D"
            self.sv_display.config(text=val, fg=self.accent_color)

        # LEDS
        if self.simulator.at_active:
            self.at_led.config(fg="orange")
        else:
            self.at_led.config(fg="#333")

        # LED OUT1 (Red pulse)
        if self.simulator.output > 0:
            # PWM effect simulation in UI
            if (self.update_count % 10) < (self.simulator.output * 10):
                self.out1_led.config(fg="red")
            else:
                self.out1_led.config(fg="#333")
        else:
            self.out1_led.config(fg="#333")

        # Power Bar
        h = int(self.simulator.output * 120)
        self.power_bar.config(height=h)

        # Update PID telemetry
        self.p_label.config(text=f"P:{self.simulator.p_term:>5.1f}%")
        self.i_label.config(text=f"I:{self.simulator.i_term:>5.1f}%")
        self.d_label.config(text=f"D:{self.simulator.d_term:>5.1f}%")

        # Graph Update (every 500ms to save performance)
        if HAS_MATPLOTLIB and self.update_count % 5 == 0:
            self.time_data.append(time.time())
            self.pv_data.append(self.simulator.pv)
            self.sv_data.append(self.simulator.sv)
            if len(self.time_data) > 100:
                self.time_data.pop(0); self.pv_data.pop(0); self.sv_data.pop(0)
            t_rel = [t - self.time_data[0] for t in self.time_data]
            self.pv_line.set_data(t_rel, self.pv_data)
            self.sv_line.set_data(t_rel, self.sv_data)
            self.ax.relim(); self.ax.autoscale_view()
            self.canvas.draw()

        self.update_count += 1
        self.root.after(100, self.update_loop)

if __name__ == "__main__":
    # Test stub
    class State:
        def __init__(self): self.pv=25.0; self.sv=50.0; self.output=0.5; self.p=25.0; self.i=480; self.d=80; self.reverse=True; self.disturbance=0.0
    root = tk.Tk()
    E5CC_UI(root, State())
    root.mainloop()
