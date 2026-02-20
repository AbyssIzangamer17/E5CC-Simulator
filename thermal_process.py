import time

class ThermalProcess:
    def __init__(self, initial_temp=25.0, ambient_temp=25.0, gain=0.1, tau=300.0, lag=5.0):
        self.true_temperature = initial_temp
        self.displayed_temperature = initial_temp
        self.ambient_temp = ambient_temp
        self.k = gain  # Extreme low gain for industrial stability
        self.tau = tau  # Increased mass (300s)
        self.lag_tau = lag # High-fidelity sensor lag
        self.last_time = time.time()

    def update(self, power, disturbance=0.0):
        now = time.time()
        dt = now - self.last_time
        if dt <= 0: return self.displayed_temperature
        self.last_time = now

        # Heat applied by the electric heater
        # Power is 0.0 to 1.0. Max heat output is 100 * k.
        heat_input = power * 100.0 * self.k
        
        # Heat lost to the environment (Increased for faster natural cooling)
        effective_ambient = self.ambient_temp + disturbance
        temp_diff = self.true_temperature - effective_ambient
        
        # Non-linear cooling (Convection simulation)
        # Hotter objects lose heat faster
        cooling_factor = 1.0 + (abs(temp_diff) / 100.0) 
        heat_loss = temp_diff * cooling_factor * 1.5 # Increased multiplier
        
        # Temperature change
        delta_temp = (heat_input - heat_loss) * (dt / self.tau)
        self.true_temperature += delta_temp

        # Sensor Lag (PV doesn't follow Heater instantly)
        lag_alpha = dt / (self.lag_tau + dt)
        self.displayed_temperature += lag_alpha * (self.true_temperature - self.displayed_temperature)
        
        import random
        noise = random.uniform(-0.01, 0.01)
        
        return self.displayed_temperature + noise

    def reset(self, temp=25.0):
        self.true_temperature = temp
        self.displayed_temperature = temp
        self.last_time = time.time()
