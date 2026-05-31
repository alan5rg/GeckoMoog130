# modules/dly.py
import numpy as np

class DLYModule:
    """Delay simple con feedback"""
    def __init__(self):
        self.name = "DLY"
        self.is_connected = False
        self.delay_ms = 300
        self.feedback = 0.5
        self.mix = 0.4
        self.sample_rate = 44100
        
        # Buffer circular con NumPy (más simple que deque)
        delay_samples = int(self.sample_rate * self.delay_ms / 1000)
        self.buffer_left = np.zeros(delay_samples, dtype=np.float32)
        self.buffer_right = np.zeros(delay_samples, dtype=np.float32)
        self.write_pos = 0

    def process_audio(self, buffer):
        out = buffer.copy()
        
        for i in range(len(out)):
            # Leer del buffer (posición actual)
            delayed_l = self.buffer_left[self.write_pos]
            delayed_r = self.buffer_right[self.write_pos]
            
            # Escribir en el buffer (con feedback)
            self.buffer_left[self.write_pos] = out[i, 0] + delayed_l * self.feedback
            self.buffer_right[self.write_pos] = out[i, 1] + delayed_r * self.feedback
            
            # Mezclar dry/wet
            out[i, 0] = out[i, 0] * (1 - self.mix) + delayed_l * self.mix
            out[i, 1] = out[i, 1] * (1 - self.mix) + delayed_r * self.mix
            
            # Avanzar posición (circular)
            self.write_pos = (self.write_pos + 1) % len(self.buffer_left)
        
        return out

dly = DLYModule()