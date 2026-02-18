import tkinter as tk
from thermal_process import ThermalProcess
from pid_controller import PIDController
from ui import E5CC_UI
import time
import threading

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        
        # State shared between threads
        # Optimized default parameters for the virtual oven
        self.state = type('obj', (object,), {
            'pv': 25.0,
            'sv': 50.0,
            'p': 25.0,     # Proportional Band (25 degrees)
            'i': 480,      # Integral Time (8 minutes)
            'd': 80,       # Derivative Time
            'in_t': 5,     # K-Thermocouple
            'reverse': True,
            'output': 0.0,
            'p_term': 0.0,
            'i_term': 0.0,
            'd_term': 0.0,
            'at_active': False,
            'at_mode': "OFF", # OFF or AT-2
            'disturbance': 0.0,
            'running': True
        })()

        # Process: gain=1.2, inertia=120s, sensor_lag=2s
        self.process = ThermalProcess(initial_temp=25.0, ambient_temp=25.0, gain=1.2, tau=120.0, lag=2.0)
        
        # PID Controller
        self.pid = PIDController(p=self.state.p, i=self.state.i, d=self.state.d, reverse=self.state.reverse)
        
        self.ui = E5CC_UI(self.root, self.state)
        
        # Start simulation thread
        self.sim_thread = threading.Thread(target=self.simulation_loop, daemon=True)
        self.sim_thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def simulation_loop(self):
        autotuner = None
        last_at_sv = None
        last_at_dist = None
        while self.state.running:
            # Handle Auto-tuning
            if self.state.at_active:
                # Reset tuner if SV or Disturbance changes during tuning
                # Significant disturbance change (>2.0) shifts the baseline too much
                sv_changed = last_at_sv is not None and abs(self.state.sv - last_at_sv) > 0.1
                dist_changed = last_at_dist is not None and abs(self.state.disturbance - last_at_dist) > 2.0
                
                if sv_changed or dist_changed:
                    autotuner = None 
                
                if autotuner is None:
                    from pid_controller import AutoTuner
                    autotuner = AutoTuner(self.state.sv)
                    last_at_sv = self.state.sv
                    last_at_dist = self.state.disturbance
                
                res = autotuner.update(self.state.pv, self.state.sv)
                if res['done']:
                    self.state.p = round(res['p'], 1)
                    self.state.i = int(res['i'])
                    self.state.d = int(res['d'])
                    self.state.at_active = False
                    self.state.at_mode = "OFF"
                    autotuner = None
                else:
                    self.state.output = res['output']
                    # Telemetry while AT
                    self.state.p_term = 100.0 if res['output'] > 0 else 0.0
                    self.state.i_term = 0.0
                    self.state.d_term = 0.0
            else:
                autotuner = None
                # Normal PID Update
                self.pid.setpoint = self.state.sv
                self.pid.set_parameters(self.state.p, self.state.i, self.state.d, self.state.reverse)
                
                # Compute PID output and get telemetry
                telemetry = self.pid.compute(self.state.pv)
                self.state.output = telemetry['output']
                self.state.p_term = telemetry['p_term']
                self.state.i_term = telemetry['i_term']
                self.state.d_term = telemetry['d_term']
            
            # Update physical process
            self.state.pv = self.process.update(self.state.output, disturbance=self.state.disturbance)
            
            time.sleep(0.05)

    def on_close(self):
        self.state.running = False
        self.root.destroy()

if __name__ == "__main__":
    MainApp()
