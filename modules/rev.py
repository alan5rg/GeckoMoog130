# modules/rev.py
import numpy as np

class REVModule:
    def __init__(self):
        self.name = "REV"
        self.is_connected = False
        self.mix = 0.4
        self.decay = 0.7
        self.sample_rate = 44100

        self.comb_delays = [1557, 1617, 1491, 1422]
        self.comb_buffers = [np.zeros(d) for d in self.comb_delays]
        self.comb_pos = [0 for _ in range(len(self.comb_delays))]

        self.ap_delays = [225, 556]
        self.ap_buffers = [np.zeros(d) for d in self.ap_delays]
        self.ap_pos = [0 for _ in range(len(self.ap_delays))]

    def _comb(self, idx, sample):
        buf = self.comb_buffers[idx]
        pos = self.comb_pos[idx]
        out = buf[pos]
        buf[pos] = sample + out * self.decay
        self.comb_pos[idx] = (pos + 1) % len(buf)
        return out

    def _allpass(self, idx, sample):
        buf = self.ap_buffers[idx]
        pos = self.ap_pos[idx]
        buf_out = buf[pos]
        buf[pos] = sample + buf_out * 0.5
        self.ap_pos[idx] = (pos + 1) % len(buf)
        return buf_out - sample

    def process_audio(self, buffer):
        out = buffer.copy()
        for i in range(len(out)):
            mono = (out[i, 0] + out[i, 1]) * 0.5
            verb = sum(self._comb(j, mono) for j in range(len(self.comb_delays)))
            verb /= len(self.comb_delays)
            for j in range(len(self.ap_delays)):
                verb = self._allpass(j, verb)
            out[i, 0] = out[i, 0] * (1 - self.mix) + verb * self.mix
            out[i, 1] = out[i, 1] * (1 - self.mix) + verb * self.mix
        return out

rev = REVModule()

