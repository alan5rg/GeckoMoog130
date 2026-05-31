# modules/fil.py
import numpy as np

class FILModule:
    """Filtro paso bajo simple (IIR de 1 polo)"""
    def __init__(self):
        self.name = "FIL"
        self.is_connected = False
        self.cutoff = 0.3       # 0.0 (cerrado) → 1.0 (abierto)
        self.prev_left = 0.0
        self.prev_right = 0.0

    def process_audio(self, buffer):
        alpha = self.cutoff
        out = buffer.copy()
        for i in range(len(out)):
            self.prev_left  = alpha * out[i, 0] + (1 - alpha) * self.prev_left
            self.prev_right = alpha * out[i, 1] + (1 - alpha) * self.prev_right
            out[i, 0] = self.prev_left
            out[i, 1] = self.prev_right
        return out

# ✅ Instancia
fil = FILModule()

