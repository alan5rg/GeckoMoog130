# main.py
# 04/04/2026 👉 “Si Orion va a la Luna, tocaste el routing y no rompiste el M.I.R…
#                entonces no fue suerte… fue arquitectura.”  🦎💙GeckoMoog
# The Basic
import sys
from PyQt5.QtWidgets import QApplication

# GeckoMoog Platform
# “Los Synths y los nilxs primerxs.”
from geckomoog127TT import PiaNOS  # toda la lógica de octava, pad y sequencer incluida de regalo!!!

# MIT Dark Style
import qdarkstyle
from qdarkstyle import DarkPalette

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))

    # Creamos el synth principal PiaNO(va)S(inth) en GeckoMoog Platform
    voices = 8
    synth = PiaNOS(voices)  
    synth.show()

    sys.exit(app.exec_())