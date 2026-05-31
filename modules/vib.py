# modules/vib.py
import numpy as np

class VIBModule:
    def __init__(self):
        self.name = "VIB"
        self.is_connected = False
        self.rate = 5 # 5 Hz

    def process_audio(self, buffer):
        """
            Procesa el buffer (ej: añade vibrato)
            Agregar: depth — profundidad del vibrato
        """
        t = np.linspace(0, len(buffer) / 44100, len(buffer))
        osc = np.sin(2 * np.pi * self.rate * t) * 0.1  
        buffer[:, 0] += osc
        buffer[:, 1] += osc
        return buffer

# ✅ Instanciar al final del módulo
vib = VIBModule()

