# 31/05/2026 🦎 clean_buffers=True ✨
"""
🦎 Gecko Matrix PatchPanel 1.0
🦎 GeckoMoog Modular Patch Matrix

Matriz visual de conexiones entre módulos del sintetizador.

Cada punto representa una conexión:
    source → destination

Los botones son checkables:
    OFF → sin conexión
    ON  → conexión activa

Uso:

modules = ["OSC","FIL","DLY","CHR","REV","MOE"]
matrix = GeckoMoogPatchMatrix(modules)
matrix.connection_changed.connect(handle_connection)

def handle_connection(src, dst, state):
    if state:
        print(f"connect {src} -> {dst}")
    else:
        print(f"disconnect {src} -> {dst}")
"""

import sys
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGroupBox, QSlider, QDial

from PyQt5.QtCore import pyqtSignal, Qt, QTimer

from controls.precisiondial2 import PrecisionDial
from controls.precisionslider import PrecisionSlider

import numpy as np

geckoappversion="2.5"

def get_version(easter_egg=False):
    if not easter_egg:
        return geckoappversion
    
    return f"""
    🦎  GeckoMoog Modular Synth Platform

    GeckoMoogPatchMatrix Version:{geckoappversion}

           __
          / _)
   .-^^^-/ /
__/       /
<__.|_|-|_|

    Modular • Patchable • Geckonian
    """                     """"""
# =========================================================
# FUENTE NUMÉRICA 5x7
# =========================================================

FONT = {
    "C": [
        "01110",
        "10001",
        "10000",
        "10001",
        "01110",
    ],
    "H": [
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
    ],
    "E": [
        "11111",
        "10000",
        "11110",
        "10000",
        "11111",
    ],
    "K": [
        "10001",
        "10010",
        "11100",
        "10010",
        "10001",
    ],
    "O": [
        "01110",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    "G": [
        "01110",
        "10000",
        "10111",
        "10001",
        "01110",
    ],
    "M": [
        "10001",
        "11011",
        "10101",
        "10001",
        "10001",
    ],
    " ": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
    ],
    "*": [
        "01010",
        "10101",
        "10001",
        "01010",
        "00100",
    ],
}

# --------------------------------------------------------
# Patch Point (botón individual)
# --------------------------------------------------------
class PatchPoint(QPushButton):
    def __init__(self, src, dst):
        super().__init__()
        self.src = src
        self.dst = dst
        self.setCheckable(True)
        self.setFixedSize(30, 30)
        self.setCursor(Qt.PointingHandCursor)

# --------------------------------------------------------
# Patch Matrix UI
# --------------------------------------------------------
class GeckoMoogPatchMatrix(QWidget):
    connection_changed = pyqtSignal(str, str, bool)
    def __init__(self,  modules, parent=None, router=None, effects_panel=None):
        super().__init__(parent)
        self.setFixedSize(370,240)
        print(get_version(easter_egg=True))
        
        self.router = router  # ✅ Guardar referencia
        self.effects_panel = effects_panel  # ✅ Guardar referencia directa

        self.modules = modules
        self.connections = {m: [] for m in modules}
        
        self.mode = "PATCH"
        self.marquee_text = ""
        self.marquee_index = 0
        
        self._build_ui()
        self._apply_style()
        # Timer cartelera
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_marquee)
        
        # ── EL PATCH POR DEFECTO DEL GECKO ──
        # Conecta el motor base directo al OUT al arrancar la matriz
        # Si el primer módulo es 'OSC' o 'ENG', buscamos ese botón y lo activamos
        target_src = self.modules[0] if self.modules else "OSC"
        QTimer.singleShot(50, lambda: self.buttons[(target_src, "OUT")].setChecked(True))

    # ----------------------------------------------------
    def _build_ui(self):

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,5)
        self.setLayout(self.main_layout)
        
        grid = QGridLayout()
        grid.setSpacing(3)
        # columnas (destinos) - agregar OUT al final
        columns = self.modules + ["OUT"]  # ✅ OUT solo en columnas
        for col, name in enumerate(columns): #self.modules):
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, 0, col + 1)
        # filas (sources)
        for row, name in enumerate(self.modules):
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, row + 1, 0)
        # matriz de botones
        self.buttons = {}
        for r, src in enumerate(self.modules):
            for c, dst in enumerate(columns): #self.modules):
                btn = PatchPoint(src, dst)
                btn.toggled.connect(
                    lambda state, s=src, d=dst: self._toggle_connection(s, d, state)
                )
                grid.addWidget(btn, r + 1, c + 1)
                self.buttons[(src, dst)] = btn
        self.main_layout.addLayout(grid)


        # ---------------- SIDE PANEL ----------------
        side_layout = QVBoxLayout()
        
        btns_title = QLabel("[MODE]")
        btns_title.setAlignment(Qt.AlignCenter)
        self.btn_patch = QPushButton("GPaTH")
        self.btn_cartel = QPushButton("CaRTl")
        self.btn_clear = QPushButton("CLeaR")

        # ── COMPORTAMIENTO SWITCH GECKÓNICO ──
        self.btn_patch.setCheckable(True)
        self.btn_patch.setChecked(True)  # Edición abierta por defecto
        self.btn_cartel.setCheckable(True) # La pantalla CRT arranca apagada

        # Conexiones directas sin pisar canillas
        self.btn_patch.clicked.connect(self._toggle_editable_mode)
        self.btn_cartel.clicked.connect(self._toggle_cartelera_mode)
        self.btn_clear.clicked.connect(self.clear_with_warning)

        for btn in [self.btn_patch, self.btn_cartel, self.btn_clear]:
            btn.setFixedSize(55,30)

        side_layout.addWidget(btns_title)
        side_layout.addWidget(self.btn_clear)
        side_layout.addWidget(self.btn_cartel)
        side_layout.addStretch()
        side_layout.addWidget(self.btn_patch)
        
        self.main_layout.addSpacing(5)
        self.main_layout.addLayout(side_layout) 

        # ------------- MASTER VOLUME -----------------
        master_control_layout = QVBoxLayout()
        self.slider_vol = PrecisionSlider(orientation=Qt.Vertical) #QSlider(Qt.Vertical)
        self.slider_vol.setFixedHeight(140)
        self.slider_vol.setFixedWidth(25)
        self.slider_vol.setRange(0, 100)
        self.slider_vol.setValue(50)
        self.slider_vol.valueChanged.connect(self._on_volume_change)

        lbl_vol = QLabel("M.Vol.")
        lbl_vol.setAlignment(Qt.AlignCenter)
        
        master_control_layout.addWidget(self.slider_vol, alignment=Qt.AlignCenter)
        master_control_layout.addWidget(lbl_vol)

        master_control_layout.addStretch()

        self.dial_pan = PrecisionDial(self) #QDial()
        self.dial_pan.setFixedSize(37,37)
        self.dial_pan.setRange(-100, 100)
        self.dial_pan.setValue(0)
        self.dial_pan.valueChanged.connect(self._on_pan_change)

        lbl_pan = QLabel("Pan")
        lbl_pan.setAlignment(Qt.AlignCenter)
        
        master_control_layout.addWidget(self.dial_pan, alignment=Qt.AlignCenter)
        master_control_layout.addWidget(lbl_pan)
        
        self.main_layout.addLayout(master_control_layout)

    # ------- Ei2 MOde Logic Fix 31/05/2026 --------
    def _toggle_editable_mode(self):
        """MÉTODO GPaTH: Bloquea o libera la edición física de los cables."""
        is_editable = self.btn_patch.isChecked()
        # Si GPaTH está activo, los botones responden; si no, se congelan
        for btn in self.buttons.values():
            btn.setEnabled(is_editable)
        # Bloqueo de el Boton mas peligroso para GeckoMoog!!!
        self.btn_clear.setEnabled(is_editable)
        #Debug Ei2
        print(f"🦎 GPaTH Hex: Edición del Patch Panel {'HABILITADA' if is_editable else 'CONGELADA'}")

    def _toggle_cartelera_mode(self):
        """MÉTODO CaRTl (CRT): Superpone la marquesina sin alterar el audio de fondo."""
        if self.btn_cartel.isChecked():
            self.mode = "CARTELERA"
            self.marquee_text = "  * * * GECKO  CHEKO  GECKOMOOG  "
            self.marquee_index = 0
            self.timer.start(120)
            #Debug Ei2
            print("📺 CRT Mode: Cartelera superpuesta en el plano visual.")
        else:
            self.timer.stop()
            self.marquee_text = ""
            # Limpiamos el efecto visual de fósforo de los botones
            for btn in self.buttons.values():
                btn.setProperty("marquee", False)
                btn.style().unpolish(btn)
                btn.style().polish(btn)
            #Debug Ei2
            print("📺 CRT Mode: Cartelera apagada. Retorno al plano de cables.")

    def clear_with_warning(self):
        """CLeaR: Extirpación total de cables con escudo de confirmación."""
        from PyQt5.QtWidgets import QMessageBox
        
        # Alerta seria del sistema antes de desconectar el pipeline matricial
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle("⚠️ GECKO PLATFORM CRITICAL")
        box.setText("¿Desea 'DESCONECTAR' el Pipeline de Sonido Matricial Configurado en el Núcleo de GeckoMoog???")
        box.setInformativeText("Esta acción arrancará TODOS los PaTcHs 'Físicos' (Teóricos) Instantáneamente!!!")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.No)
        
        # Si el operador confirma con el ojo chamánico:
        if box.exec_() == QMessageBox.Yes:
            for btn in self.buttons.values():
                btn.setChecked(False)
            self.connections = {m: [] for m in self.modules}
            # Aseguramos que el router limpie los buffers inmediatamente
            if hasattr(self.router, 'set_connections'):
                self.router.set_connections(self.connections)
            #Debug Ei2
            print("🔌 CLeaR: Pipeline de sonido completamente desconectado en el núcleo.")

    # ---NOVA PAN + VOLUME--------------------------------
    def _on_volume_change(self, value):
        #print(self.slider_vol.value())
        if self.router:
            self.router.master_volume = value / 100.0
            #print(f"[VOL] Master volume: {value / 100.0}")

    def _on_pan_change(self, value):
        #print(self.dial_pan.value())
        if self.router:
            self.router.pan = value / 100.0
            #print(f"[PAN] Pan: {value / 100.0}")

    # ----------------------------------------------------
    def _update_marquee(self):
        if not self.marquee_text:
            return

        rows = len(self.modules)
        cols = len(self.modules)

        # limpiar efecto anterior
        for btn in self.buttons.values():
            btn.setProperty("marquee", False)

        # construir bitmap completo
        bitmap = [""] * 5
        for char in self.marquee_text:
            pattern = FONT.get(char, FONT[" "])
            for r in range(5):
                bitmap[r] += pattern[r] + "0"  # espacio entre letras
        total_width = len(bitmap[0])

        # scroll horizontal
        for r in range(min(5, rows)):
            for c in range(cols):
                scroll_x = (c + self.marquee_index) % total_width
                if bitmap[r][scroll_x] == "1":
                    src = self.modules[r]
                    dst = self.modules[c]
                    self.buttons[(src, dst)].setProperty("marquee", True)

        # refrescar estilo
        for btn in self.buttons.values():
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        self.marquee_index += 1
    
    # ----------------------------------------------------
    def _apply_style(self):
        self.setStyleSheet("""
        QLabel {
            color: #8aa;
            font-size: 10px;
            font-weight: bold;
        }
        QPushButton {
            font-weight: bold;
            border-radius: 14px;
            border: 1px solid #00ff88;
            background: #0f1a20;
        }
        QPushButton:checked {
            background: #00ffaa;
        }
        QPushButton:hover {
            border: 3px solid #55ffcc;
        }
        QPushButton[marquee="true"] {
            background: #3f8; /*ffaa00;*/
        }
        QSlider {
            background: #0f1a20;
        }
        QSlider::handle {
            background: #00ffaa;
            border: 1px solid #00ff88;
        }                   
        """)

    # ----------------------------------------------------
    def _toggle_connection(self, src, dst, state):
        """Actualizar conexiones Y el estado is_connected de cada módulo"""
        if state:
            if dst not in self.connections[src]:
                self.connections[src].append(dst)
        else:
            if dst in self.connections[src]:
                self.connections[src].remove(dst)

        # ✅ Actualizar is_connected en cada módulo usando self.router.modules
        if hasattr(self.router, 'modules'):
            for module_name, dests in self.connections.items():
                if module_name in self.router.modules:  
                    self.router.modules[module_name].is_connected = len(dests) > 0

        # ✅ Llamar directamente con referencia guardada
        if self.effects_panel:
            self.effects_panel._update_mecos()

        self.connection_changed.emit(src, dst, state)

    # ----------------------------------------------------
    def get_connections(self):
        return self.connections

    # ----------------------------------------------------
    def clear(self):
        for btn in self.buttons.values():
            btn.setChecked(False)
        self.connections = {m: [] for m in self.modules}

    # ----------------------------------------------------
    # Salida Geckonica    
    # ----------------------------------------------------
    def closeEvent(self, event):
        # Opcional: podrías simplemente ocultarlo en vez de destruirlo
        # self.hide()
        # event.ignore()
        super().closeEvent(event)

# --------------------------------------------------------
# El verdadero Patch Panel de audio
# --------------------------------------------------------
class GeckoAudioRouter:
    """
       La matrix decide
         El router ejecuta 
    """
    def __init__(self):
        # Leo Conection
        self.master_volume = 1.0
        self.pan = 0.0
        self.modules = {}  # {nombre: modulo}
        self.connections = {}  # {source: [destinations]}

        # por ahora UNA sola ruta activa
        self.active_source = None
    
    ''' Original's
    def set_connections(self, connections):
        """
        connections viene de la matrix
        """
        # versión 0.1: agarramos el PRIMER módulo conectado a salida
        for src, dsts in connections.items():
            if "OUT" in dsts:
                self.active_source = src
    '''
    
    # --- LEO CONNECTION WAY-----------------------------------
    def register_module(self, name, module):
        """Registra un módulo en el sistema"""
        self.modules[name] = module
        self.connections[name] = []
        #print(f"[ROUTER] Módulo '{name}' registrado.")

    def set_connections(self, connections):
        """Actualiza las conexiones desde la matrix"""
        self.connections = connections
        #print(f"[ROUTER] Conexiones actualizadas: {connections}")

    def process(self, buffer):
        """Procesa el buffer con los módulos activos"""
        if buffer is None:
            return None

        # Aplicar efectos según conexiones
        # Versión 1: mezclar todos los módulos que van a OUT
        output = np.zeros_like(buffer)

        for src, dsts in self.connections.items():
            if "OUT" in dsts and src in self.modules:
                if src == "ENG":
                    # ENG ya está en buffer, solo sumar
                    output = buffer
                else:
                    # Procesar el buffer con el módulo
                    processed = self.modules[src].process_audio(buffer.copy())
                    output += processed

        # Aplicar volumen maestro
        output *= self.master_volume

        # Aplicar pan (simplificado)
        if self.pan != 0:
            left = output[:, 0] * (1 - abs(self.pan))
            right = output[:, 1] * (1 - abs(self.pan))
            if self.pan > 0:
                right += output[:, 0] * abs(self.pan)
            else:
                left += output[:, 1] * abs(self.pan)
            output[:, 0] = left
            output[:, 1] = right

        return output
    # --- END LEO CONNECTION WAY ---------------------------------------

# ----------------------------------------------------
# Stand Alone Testing
# ----------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    modules = ["OSC","FIL","DLY","CHR","REV","MOE"]
    ventana = GeckoMoogPatchMatrix(modules)
    ventana.show()
    sys.exit(app.exec_())