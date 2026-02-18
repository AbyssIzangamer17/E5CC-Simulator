import time

class PIDController:
    def __init__(self, p=25.0, i=480.0, d=80.0, reverse=True):
        self.p_band = p
        self.i_time = i
        self.d_time = d
        self.reverse = reverse
        
        self.setpoint = 0.0
        self.integral = 0.0
        self.last_error = 0.0
        self.last_time = time.time()
        self.last_output = 0.0
        
        self.d_filtered = 0.0
        self.N = 8.0 # Filter coeff

    def set_parameters(self, p, i, d, reverse=True):
        self.p_band = p
        self.i_time = i
        self.d_time = d
        self.reverse = reverse

    def compute(self, current_value):
        now = time.time()
        dt = now - self.last_time
        if dt < 0.01: return self.last_output
            
        error = self.setpoint - current_value
        if not self.reverse: error = -error
            
        # P-Term
        if self.p_band <= 0.1: p_term = 100.0 if error > 0 else 0.0
        else: p_term = (error / self.p_band) * 100.0
        
        # Integral Term with Strict Clamping (Anti-Windup)
        # Only integrate if we are not saturated OR if we are integrating in the direction that helps
        i_term = 0.0
        if self.i_time > 0:
            potential_integral = self.integral + error * dt
            # Ki calculation
            i_term = (100.0 / self.p_band) * (potential_integral / self.i_time)
            
            # Anti-windup clamping
            if -100.0 < (p_term + i_term) < 100.0:
                self.integral = potential_integral
            else:
                # If saturated, we only update integral if it helps reduce the saturation
                if (p_term + i_term >= 100.0 and error < 0) or (p_term + i_term <= -100.0 and error > 0):
                    self.integral = potential_integral
        
        # D-Term (Predictive Brake)
        de = (error - self.last_error) / dt
        self.d_filtered += (dt / (dt + (self.d_time / self.N + 0.001))) * (de - self.d_filtered)
        d_term = (100.0 / self.p_band) * (self.d_time * self.d_filtered)
        
        total_output = p_term + i_term + d_term
        
        # Final Clamping for Hardware (0-100%)
        clamped_output = max(0.0, min(100.0, total_output))
            
        self.last_error = error
        self.last_time = now
        self.last_output = clamped_output / 100.0
        
        return {
            'output': self.last_output,
            'p_term': p_term,
            'i_term': i_term,
            'd_term': d_term
        }

class AutoTuner:
    def __init__(self, target_sv):
        self.target_sv = target_sv
        self.cycles = 0
        self.peak_times = []
        self.peak_values = []
        self.going_up = True
        self.has_crossed = False
        self.hysteresis = 0.2 # Small hysteresis for stability

    def update(self, pv, current_sv):
        self.target_sv = current_sv
        now = time.time()
        
        # Determine output based on Relay with Hysteresis
        if self.going_up:
            if pv > (self.target_sv + self.hysteresis):
                # Cycle Top Reached
                self.going_up = False
                if self.has_crossed:
                    self.peak_values.append(pv)
                    self.cycles += 0.5
            output = 1.0
        else:
            if pv < (self.target_sv - self.hysteresis):
                # Cycle Bottom Reached
                self.going_up = True
                self.has_crossed = True # We started the first real cycle
                self.peak_times.append(now)
                self.cycles += 0.5
            output = 0.0

        # Logic for first initialization: if PV >> SV, wait to cool down
        if not self.has_crossed and pv > self.target_sv:
            output = 0.0
            self.going_up = False # Force "cooling" mode until we cross SV
        
        # After 3 complete oscillations
        if self.cycles >= 3.5:
            if len(self.peak_times) >= 2 and len(self.peak_values) >= 2:
                # Tu: Average time between bottom points
                tu = (self.peak_times[-1] - self.peak_times[-2]) / (len(self.peak_times) - 1)
                
                # a: Average amplitude
                # We calculate average peak from SV
                avg_peak = sum(self.peak_values) / len(self.peak_values)
                a = abs(avg_peak - self.target_sv)
                
                if a < 0.1: a = 0.1 # Safety
                
                # Ku = (4 * 1.0) / (pi * a)
                import math
                ku = 4.0 / (math.pi * a)
                
                # Ziegler-Nichols (PID)
                kp = 0.6 * ku
                # Scaling for Omron (PB = 100/Kp)
                p = 100.0 / (kp * 1.5) # Tuning factor for the oven
                i = 0.5 * tu
                d = 0.12 * tu
                
                return {"done": True, "p": p, "i": i, "d": d}
        
        return {"done": False, "output": output}
