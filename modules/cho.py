# modules/cho.py
import numpy as np

class CHRModule:
    """Chorus estéreo clásico (modulación de delay con LFO)"""
    def __init__(self):
        self.name = "CHO"
        self.is_connected = False
        self.rate = 1.5             # Hz del LFO
        self.depth = 0.003          # profundidad de modulación
        self.mix = 0.5              # dry/wet
        self.sample_rate = 44100
        self.max_delay = int(0.03 * self.sample_rate)   # 30ms máx
        self.buf_left  = np.zeros(self.max_delay)
        self.buf_right = np.zeros(self.max_delay)
        self.write_pos = 0
        self.lfo_phase = 0.0

    def process_audio(self, buffer):
        out = buffer.copy()
        lfo_inc = 2 * np.pi * self.rate / self.sample_rate

        for i in range(len(out)):
            # LFO
            lfo = np.sin(self.lfo_phase)
            self.lfo_phase += lfo_inc

            # Delay modulado
            delay_samples = int((0.01 + self.depth * lfo) * self.sample_rate)
            delay_samples = max(1, min(delay_samples, self.max_delay - 1))

            read_pos = (self.write_pos - delay_samples) % self.max_delay

            # Escribir en buffer circular
            self.buf_left[self.write_pos]  = out[i, 0]
            self.buf_right[self.write_pos] = out[i, 1]

            # Mezclar dry/wet
            out[i, 0] = out[i, 0] * (1 - self.mix) + self.buf_left[read_pos]  * self.mix
            out[i, 1] = out[i, 1] * (1 - self.mix) + self.buf_right[read_pos] * self.mix

            self.write_pos = (self.write_pos + 1) % self.max_delay

        return out

# ✅ Instancia
cho = CHRModule()

