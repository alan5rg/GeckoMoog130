# modules/moe.py
import numpy as np

class MOEModule:
    """MOE: Moog Overdrive Engine — saturación analógica suave"""
    def __init__(self):
        self.name = "MOE"
        self.is_connected = False
        self.drive = 1.5            # 1.0 = suave, 3.0 = agresivo
        self.mix = 0.6              # dry/wet

    def process_audio(self, buffer):
        out = buffer.copy()
        # Saturación suave tipo tanh (analógica)
        driven = np.tanh(out * self.drive)
        out = out * (1 - self.mix) + driven * self.mix
        return out

# ✅ Instancia
moe = MOEModule()

