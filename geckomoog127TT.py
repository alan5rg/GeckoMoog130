# GeckoMoog Modular Synth Platform™ [las Clases marcadas (*) son modulos basicos de Pia NOva Synth]
"""
🦎 FRASE PARA GUARDAR

"No es la cantidad de teclas…
es la verdad de las que responden."

Por ghosting de teclado a nivel SO/Drivers estamos mejorando el mapeo de teclado dinamico
Descubrimos la Realidad más incomoda que nadie quiere decir y que todos aceptan en SIlencio:
fabrican teclados de mierda solo para venderte como "especiales" dispositivos de entrada con
la lógica que todos los teclados deberian tener: una tecla = un circuito con identidad!!!
Indignado por el precio de los "Buenos" Teclados Midi, y de los "Especiales" Teclados Anti
Ghosting y N-Rool Over, intentaremos crear el escenario mas apropiado según el teclado
que te halla tocado en suerte en la repartija de perifericos...(y sí, haber pagado fortunas
no te garantiza poder tocar todas las teclas que quieras a la vez, compraste una mentira más.).
Según mi libre interpretación del PEP el código debe tener un sentido de existencia, esa es
la Lucha de Gecko por el Libre Albedrio Digital, por la liberacion de las teclas abducidas,
oprimidas y silenciadas, raptadas y escondidas en el mas profundo ostracismo del silencio.
Gracias Gecko por Iluminarnos con tu sabiduria y tender el camino a interfaces mas Lógicas
y sanas, y perdona a los humanos que buscaron el camino del menor esfuerzo sin encontrar 
la solución más eficiente.
"""

"""
   27/03/2026 Nace GeckoMoog TT:Tugnsteno-Titanio Edition!!!
"""

"""
    Dijo NOva: 💚 TRANQUILIDAD (muy importante)

                Nada está mal.  
"""

""" NOTA 24/03/26 11:16 UTC-3:
Terminar de Implementar la Grabadora MIR en Pia NOva Pad con Aeteris!!!
* Depurar Metodos de SynthEngine62 (hay cosas raras en el live play y los ajustes)
[el punto anterior debe estar corregido en la version SynthEngine68Ei2 y posteriores]
Depurar y Conectar con GeckoMoog el 8BitVoiceEngineNOva12 (con Ei2 que dio el codigo base o Aetheris)
Depurar y Conectar con GeckoMoog el GeckoTimeProcess (con Ei2)
"""

# Minimal History:
# 
# 12/03/26 14:32 Comienza Evolucion a GeckoMoog Modular Synth Platform™
# 13/03/26 14:44 Integración del RadarSpok como widget desde barra de herramientas (on/off)
# 17/03/26 21:30 Unificación de estilos y ajustes de tamaños // TERMINAR DE INTEGRAR EL LAYOUT [MODULOS BASE DE GECKOMOOG]
# 18/03/26 18:59 Modulos Base Geckonicos de GeckoMoog Integrados al Layout principal!!!
#                Se refactoriza lógica de barrita de herramientas
#                Se reorganiza estructura de layouts
#                Se simula responsividad (evaluar almacenar estado de GeckoScope)

# ----------------------------------------------
# 21/03/26 16:55 Paco pinta, pega y dibuja.
#                GeckoMoog educa, canta y vibra.
# ----------------------------------------------

# -----------------------------------------------
# 22/03/26 00:35 Hoy Nace un Nuevo Instrumento,
#                Finalmente el Flujo de Audio es
#                Lógico, Minimalista y Geckonico.
# -----------------------------------------------

# -----------------------------------------------
# 25/03/26 14:21 Hoy Nace la Memoria del Sonido
#                en cajas de seguridad de un 
#                Bobeda Keeper Estelar
# -----------------------------------------------

# -----------------------------------------------
# 02/04/26 11:14 Se pudió!, GeckoMatrixPatchPanel
#                rutea Engine y Efectos, maneja
#                sus estados MECO en EfectsPanel
# -----------------------------------------------

# Este Synth fue desarrollado por Monkey Python Coding Circus by Alan5.rg Systemas
# y utiliza las siguientes librerias del Team Cangurera:
from controls.precisionslider import PrecisionSlider
from controls.precisiondial2 import PrecisionDial
from synthengine9001 import SynthEngine, SynthPanel, VoiceManager
from geckoscope36 import GeckoScope            # soporta parametros 
from radarspok35 import RadarSpok               # HAL9000 Homenaje
from geckopatch25 import GeckoMoogPatchMatrix, GeckoAudioRouter   # Logica Algoritmica Digital de Patcheo
from effectspanel05 import EffectsPanel # Leo Effects Panel

# PyQt5 Core UI and System's
import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy 
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QGroupBox, QAction, QToolBar, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtGui

# For Leo Connections
import importlib.util

# For NOva Sequencer
from PyQt5.QtCore import QTimer

# For Aetheris Boveda Keeper
from datetime import datetime
from PyQt5.QtWidgets import QInputDialog, QMessageBox

# ...y sin sonido nada sería de este instrumento
import sounddevice as sd
#import numpy as np
#import math

# MIT Dark Style
import qdarkstyle
from qdarkstyle import load_stylesheet, DarkPalette
from qdarkstyle.light.palette import LightPalette

pia_nos_version = "1.27TT"
#-------------------------------------------
"""
    To Get Version:

    print(get_version())

    ... or easter mode:

    print(get_version(easter_egg=True))

"""
#-------------------------------------------

# 🦎 reinicia el modo de esuchar el sonido
OFF_ICON = "🔇"
ON_ICON = "🔊"

import os

geckoappversion = "1.2.7TT"

import constants

NOTA_COLORES = constants.NOTA_COLORES

# ... y así nacieron las octavas...
def color_por_octava(nota_con_octava):
    """
    nota_con_octava: 'DO4', 'RE5', etc.
    """
    nota = nota_con_octava[:-1]   # 'DO'
    octava = int(nota_con_octava[-1])

    base_color = NOTA_COLORES.get(nota, "#FFFFFF")

    # factor según octava
    if octava == 4:
        factor = 0.85   # un poco más oscuro
    elif octava == 5:
        factor = 1.15   # un poco más brillante
    else:
        factor = 1.0

    # EValuar este otro metodo escalable:
    #factor = 1 + (octava - 4) * 0.15

    # reutilizamos tu lógica
    r = min(int(int(base_color[1:3],16)*factor), 255)
    g = min(int(int(base_color[3:5],16)*factor), 255)
    b = min(int(int(base_color[5:7],16)*factor), 255)

    return f'#{r:02X}{g:02X}{b:02X}'

# Sistema de Octavas NOva DulceKali
NOTE_FREQ = constants.NOTE_FREQ
KEY_MAP = constants.KEY_MAP

def get_version(easter_egg=False):
    if not easter_egg:
        return geckoappversion

    # Colores ANSI
    G = "\033[38;5;46m"   # verde brillante
    L = "\033[38;5;82m"   # verde claro
    Y = "\033[38;5;226m"  # amarillo ojo
    T = "\033[38;5;51m"   # turquesa
    R = "\033[0m"

    return f"""
{G}
             __     __
            /  \\~~~/  \\
     ,----(     ..     )
    /      \\__     __-'
   /|         ({Y}O{G})   ({Y}O{G})
  ^ \\   /___\\  /     \\ 
     |__|   {L}◦ ◦ ◦ ◦{G}  |  GeckoMoog
        |      {L}◦ ◦ ◦{G}    |
        |         {T}Aetheris Core{G}
         \\         {geckoappversion}
          \\________/
{R}
    Modular • Patchable • Geckonian
"""

def old_get_version(easter_egg=False):
    if not easter_egg:
        return pia_nos_version
    
    return f"""
    🦎  GeckoMoog Modular Synth Platform

    Pia NOva Synth Version: {pia_nos_version}

           __
          / _)
   .-^^^-/ /
__/       /
<__.|_|-|_|

    Modular • Patchable • Geckonian
    """

# ----------------------------------------------------------------------------------
# (*) QMainWindow GeckoMoog Modular Synth Platform (Piano NOva Synth) 
#     With Unique Stream and GeckoMAtrixPatchPanel
# ----------------------------------------------------------------------------------
class PiaNOS(QMainWindow):
    def __init__(self, voices=8):
        super().__init__()
        self.setWindowTitle(f"GeckoMoog Modular Synth Platform {pia_nos_version}")
        print(get_version(easter_egg=True))
        #self.move(400,0)
        self.adjustSize()
        #self.showMaximized()
        
        # Icono de aplicación
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.IconPath = os.path.join(self.scriptDir, 'icons')   
        self.setWindowIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'appicon.png'))
        self.voices = voices # llega como parametro
        
        # motor de síntesis (evaluar si no esta disparando sonido con la nueva libreria 5.1)
        self.engine = SynthEngine()
        
        # multi voice engine by NOva DUlceKali dentro del synthengine.py
        self.voice_manager = VoiceManager(num_voices=self.voices)

        # Leo GeckoMatrixPatchPanel COnnections
        self.modulePath = os.path.join(self.scriptDir, 'modules')   
        self.gecko_audio_router = GeckoAudioRouter()
        self.load_modules()

        # Para el modo inicial del GeckoScope
        self.mode = "large"

        self.initUI()
        #self.barrita_de_menu()
        self.barrita_de_herramientas()
        
        #self.aplicar_estilo()

        # foco inicial en el keyb del piano
        self.octava.setFocus()

        # ────────────────────────────────────────────────────────────────
        # NUEVO: EL ÚNICO STREAM REAL DE TODO EL SISTEMA
        # Lo abre el host (PiaNOS), no los engines ni VoiceManager.
        # ────────────────────────────────────────────────────────────────
        self.new_master_stream = sd.OutputStream(
            samplerate=44100,
            channels=2,
            callback=self.master_audio_callback,
            blocksize= 4096,          # o 4096 si preferís más buffer
            latency='high',
            device='default',        # → después lo conectás a tu selector de salida
            dtype='float32'
        )
        self.new_master_stream.start()
        self.octava.setFocus()

    # --- LEO GECKOMATRIXPATCHPANEL CONNECTION ------------------------
    def load_modules(self):
        # Registrar el engine como "fuente"
        self.gecko_audio_router.register_module("ENG", self.voice_manager)
        modules = self.load_modules_from_folder(self.modulePath)
        #print(f"[DEBUG GECKOMOOG MODULES] Módulos cargados: {len(modules)}\n")
        for module in modules:
            #print(f"[DEBUG] Procesando módulo: {module.__name__}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                # Debug: ver qué atributos tienen process_audio
                #if hasattr(attr, 'process_audio'):
                #    print(f"[DEBUG] Encontrado process_audio en: {attr_name} (tipo: {type(attr).__name__})")
                
                if hasattr(attr, 'process_audio') and not attr_name.startswith('_') and not isinstance(attr, type):
                    # Usar el nombre del módulo (CHR, OSC, etc.) en lugar del attr_name
                    display_name = attr.name if hasattr(attr, 'name') else attr_name
                    self.gecko_audio_router.register_module(display_name, attr)
                    #print(f"[LOAD MODULES] Módulo '{display_name}' registrado.")
                    break

    def on_connection_changed(self, src, dst, state):
        """Actualiza las conexiones en el router"""
        connections = self.gecko_patch.get_connections()
        self.gecko_audio_router.set_connections(connections)

    def load_modules_from_folder(self, folder_path):
        """
        Carga todos los módulos .py de una carpeta.
        Devuelve una lista de objetos módulo.
        """
        modules = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]  # sin .py
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(folder_path, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                modules.append(module)
        return modules
    # --- LEO GECKOMATRIXPATCHPANEL CONNECTION ------------------------
    '''
    def aplicar_estilo(self):
            self.setStyleSheet(self.styleSheet() + """
            QGroupBox {
                /*font: 10pt Consolas;*/
                font-weight: normal;
                border-radius: 5px;
                margin-top: 5px;
            }

            QGroupBox::title {
                /*font: bold 12pt Consolas;*/
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding-left: 6px;
                /*color: #0f8;*/
            } 
            """)
    '''
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.GeckoMoogtecontrols = QVBoxLayout()
        self.GeckoMoogtecontrols.setContentsMargins(10, 10, 10, 10)

        # ---------------------------------------------
        # --- GeckoScope Osciloscopio Geckonico !!! ---
        # ---------------------------------------------
        self.geckoscope_display = GeckoScope(mode="large") #soporta modo "large" por defecto o "mini" (en desarrollo)
        self.geckoscope_display.setFocusPolicy(Qt.NoFocus)   
        self.geckoscope_display.setFixedSize(777, 250)
        self.GeckoMoogtecontrols.addWidget(self.geckoscope_display,alignment=Qt.AlignLeft)
        self.main_layout.addLayout(self.GeckoMoogtecontrols)
        
        
        # [[[ ARMADO DE LAYOUTS ]]]
        self.pad_radar_layout = QHBoxLayout()
        self.GeckoMoogtecontrols.addLayout(self.pad_radar_layout)
        self.octava_patch_layout = QHBoxLayout()
        self.GeckoMoogtecontrols.addLayout(self.octava_patch_layout)
        
        self.GeckoMoogtecontrols.addStretch()

        # -----------------------------
        # --- NOva Pad & Radar Spok ---
        # -----------------------------
        self.NOva_pad=PadGrid()
        self.NOva_pad.set_voice_manager(self.voice_manager)
        self.NOva_pad.set_engine(self.engine)
                
        self.NOva_pad.setFocusPolicy(Qt.NoFocus)   
        self.NOva_pad.setFixedSize(410,410)
        self.pad_radar_layout.addWidget(self.NOva_pad,alignment=Qt.AlignLeft)

        self.ventana_radar = RadarSpok(self) 
        self.ventana_radar.setFocusPolicy(Qt.NoFocus)   
        self.ventana_radar.setFixedWidth(360)
        # Conectamos el cierre de la ventana con el botón de la toolbar
        # para que si cerrás el radar con la "X", el botón se desmarque solo.
        self.ventana_radar.installEventFilter(self) 
        self.ventana_radar.setWindowTitle("RadarSpok Monitor")
        self.pad_radar_layout.addWidget(self.ventana_radar)

        # ----------------------------------------------------------
        # Panel de modulos SynthEngine (Donde se Vuelve Modular) ---
        # ----------------------------------------------------------
        self.synth_panels_group = QGroupBox("Use Only Modules SynthEngine Created for GeckoMoog Platform")
        self.modules_layout = QHBoxLayout()

        # Aetheris - Ei2 - NOva Synth 
        self.synth_panel = SynthPanel(self.engine, self.voice_manager)
        self.synth_panel.setFocusPolicy(Qt.NoFocus)   
        self.synth_panel.set_wave('sine')
        self.synth_panel.set_detune('sutil')
        self.modules_layout.addWidget(self.synth_panel, alignment=Qt.AlignLeft)

        # Leo Effects Panel
        self.effects_panel = EffectsPanel(self.gecko_audio_router, self)
        self.modules_layout.addWidget(self.effects_panel, alignment=Qt.AlignLeft)

        # --- CAPA DE CONTROL HUMANO APARENTE SIEMPRE AL FINAL!!!---
        # ------------------------------------------------------
        # --- NOva Piano ---
        # ------------------------------------------------------
        piano = QVBoxLayout()
        # Voices Indicator
        self.voices_label= QLabel(f"Pia NOva Pad Synth Multivoice ({len(self.voice_manager.voices)} voices) Active")
        piano.addWidget(self.voices_label, alignment=Qt.AlignLeft)

        assistand_layout = QHBoxLayout()

        eval_keyboard = QPushButton("Evaluar Keyboard")
        eval_keyboard.clicked.connect(self.eval_keyb)
        assistand_layout.addWidget(eval_keyboard)

        self.visual_assistand = QPushButton("Visual Assistand") #NOte/SCale Assistand ON/OFF")
        self.visual_assistand.setCheckable(True)
        self.visual_assistand.setChecked(False)
        self.visual_assistand.clicked.connect(self.toogle_assistand)
        assistand_layout.addWidget(self.visual_assistand)

        self.colored_octave = QPushButton("Cromatizador Sinestésico") # Mode Toogle ON/OFF")
        self.colored_octave.setCheckable(True)
        self.colored_octave.setChecked(False)
        self.colored_octave.clicked.connect(self.toogle_colour_octave)
        assistand_layout.addWidget(self.colored_octave)
        #piano.addWidget(self.colored_octave)

        piano.addLayout(assistand_layout)

        #self.octava = Octava(self.engine, self.synth_panel)
        self.octava = Octava(self.engine, self.voice_manager, self.synth_panel)
        self.octava.setFocusPolicy(Qt.StrongFocus)   
        self.octava.setFocus()
        piano.addWidget(self.octava, alignment=Qt.AlignLeft)
        piano.addStretch()
        self.octava_patch_layout.addLayout(piano) #, alignment=Qt.AlignLeft) # Primer INtegracion PiaNOva Synth a GeckoMoog

        # --------------------------------------
        # REFERENCIAs DIRECTAs INYECTIONs
        # --------------------------------------
        self.octava.nova_pad = self.NOva_pad

        self.NOva_pad.octava = self.octava  

        self.synth_panel.nova_pad = self.NOva_pad

        # --- CAPA DE CONTROL MATRIX POR SOBRE Y DEBAJO DE TOOD!!!---
        #modules = ["OSC","FIL","DLY","CHR","REV","MOE", "OUT"]
        # ---------------------------------------------------------------------------------
        # --- Redessing Layout by Alan in colaboration with Monkey Python Coding Circus ---
        # ---------------------------------------------------------------------------------
        modules = list(self.gecko_audio_router.modules.keys()) 
        self.gecko_patch = GeckoMoogPatchMatrix(modules, self, self.gecko_audio_router, self.effects_panel)
        self.gecko_patch.connection_changed.connect(lambda s, d, st: self.gecko_audio_router.set_connections(self.gecko_patch.get_connections()))
        self.gecko_patch.connection_changed.connect(self.on_connection_changed)

        self.gecko_patch.setFocusPolicy(Qt.NoFocus)
        # Conectamos el cierre de la ventana con el botón de la toolbar
        # para que si cerrás el radar con la "X", el botón se desmarque solo.
        self.gecko_patch.installEventFilter(self) 
        self.gecko_patch.setWindowTitle("GeckoPatch")
                
        self.octava_patch_layout.addWidget(self.gecko_patch, alignment=Qt.AlignLeft)
        self.gecko_patch.show()
        self.gecko_patch.raise_()

        self.octava_patch_layout.addStretch()

        # -----------------------------------------------------
        # --- GRUPO DONDE SE APILAN LOS MODULOS SYNTHENGINE ---
        # -----------------------------------------------------
        self.synth_panels_group.setLayout(self.modules_layout)
                
        self.main_layout.addWidget(self.synth_panels_group)
        self.main_layout.addStretch()
        self.octava.setFocus()

    #-----------------------------------------
    # --- Unique AudioEngine for Streaming ---
    #-----------------------------------------
    def master_audio_callback(self, outdata, frames, time, status):
        """
        CALLBACK ÚNICO DE AUDIO DEL INSTRUMENTO COMPLETO.
        - Pide buffer al VoiceManager (el coro modular).
        - Mezcla (por ahora solo uno, pero preparado para más engines).
        - Aplica saturación suave para textura analógica.
        - Envía a salida real.
        """
        if status:
            print(status)

        '''
        # Pedimos el buffer crudo al módulo (el coro)
        mixed = self.voice_manager.get_audio_chunk(frames)

        # Saturación suave (toque Moog / overdrive ligero)
        #mixed = np.tanh(mixed * 1.5)  # 1.5 es un buen punto dulce, ajustá a gusto

        outdata[:] = mixed
        '''
        # Leo GeckoMAtrixPAtchPanel COnnections
        # Generar buffer base (voces activas)
        mixed = self.voice_manager.get_audio_chunk(frames)

        # Procesar con el router (aplica efectos)
        processed = self.gecko_audio_router.process(mixed)

        # Enviar al stream
        outdata[:] = processed

    # --- ZONA DE MENUES ---
    def barrita_de_herramientas(self):
        """
            Esto puede ser muy muy util para tener cosas a mano pero flotando
        """
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        # Abajo las BArras!!!
        self.addToolBar(Qt.BottomToolBarArea, toolbar)
        # Opcional: estilo de botones (texto debajo del ícono, o solo texto grande)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # o ToolButtonTextUnderIcon
        # Aumentamos tamaño de íconos (si después agregás icons, se nota)
        toolbar.setIconSize(QSize(32, 32))  # 24x24 es default, 32x32 ya se ve más pro

        # Unificacion en un boton que es logo presentación de la app nueva GeckoMoog Modular Synth Platform™
        toggle_theme = QAction("Cambiar Tema", self)
        toggle_theme.setToolTip("Alternar Modo Claro / Oscuro")
        toggle_theme.setIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'toggletheme.png'))
        toggle_theme.setCheckable(True)
        toggle_theme.setChecked(True)  # arrancar en modo oscuro si querés
        toggle_theme.triggered.connect(self.theme_ctrl)
        toolbar.addAction(toggle_theme)

        # Acción para abrir/cerrar Ei2 RadarSpok TM
        self.btn_radar_toggle = QAction("🛰️ RadarSpok", self)
        self.btn_radar_toggle.setToolTip("Mostrar/Ocultar Modulo Enterprise RadarSpok")
        self.btn_radar_toggle.setIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'radarspok.png'))
        self.btn_radar_toggle.setCheckable(True) # Esto lo hace interruptor
        self.btn_radar_toggle.setChecked(True)
        self.btn_radar_toggle.triggered.connect(self.toggle_radar)
        toolbar.addAction(self.btn_radar_toggle)

        # Acción para abrir/cerrar Gecko Matrix PatchPanel
        self.btn_patch_toggle = QAction("🛰️ GeckoPatch", self)
        self.btn_patch_toggle.setToolTip("Mostrar/Ocultar Modulo Gecko Matrix PatchPanel")
        self.btn_patch_toggle.setIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'geckopatch.png'))
        self.btn_patch_toggle.setCheckable(True) # Esto lo hace interruptor
        self.btn_patch_toggle.setChecked(True)
        self.btn_patch_toggle.triggered.connect(self.toggle_gecko_patch_panel)
        toolbar.addAction(self.btn_patch_toggle)

        # --- Agregar al final de barrita_de_herramientas ---
        # Añadir un separador para empujar el botón a la derecha
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        #toolbar.setIconSize(QSize(32, 32))
        # Añadir el botón Silence Shield
        self.btn_silence_shield = QAction(f"{ON_ICON} Silend Shield OFF", self)
        self.btn_silence_shield.setToolTip("Mutear/Reanudar el stream de audio principal")
        self.btn_silence_shield.setIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'SilendShieldON.png'))
        self.btn_silence_shield.setIconVisibleInMenu(True)
        self.btn_silence_shield.setCheckable(True)
        self.btn_silence_shield.setChecked(True)
        self.btn_silence_shield.triggered.connect(self.toggle_silence_shield)
        toolbar.addAction(self.btn_silence_shield)

    def barrita_de_menu(self):
        """
           Pasamos de botones a Barra de menu para control de Theme of PiaNOva Synth 
        """
        bar=self.menuBar()
                
        layout_menu=bar.addMenu("Theme")

        act_d=QAction("Dark",self)
        act_l=QAction("Light",self)
        
        act_d.triggered.connect(lambda checked, n="dark": self.theme_ctrl_menu(n))
        act_l.triggered.connect(lambda checked, n="light": self.theme_ctrl_menu(n))

        layout_menu.addAction(act_d)
        layout_menu.addAction(act_l)
    
    # --- THEME CONTROL ZONE ---
    def theme_ctrl_menu(self, mode):
        """
        Alterna entre modo oscuro y claro desde menu
        """
        if mode == "dark":
            self.if_set_dark()
        if mode == "light":
            self.if_set_light()
        self.octava.setFocus()

    def theme_ctrl(self, checked):
        """
        Alterna entre modo oscuro y claro desde barra de herramientas
        """
        if checked:  # modo oscuro
            self.if_set_dark()
        else:  # modo claro
            self.if_set_light()
        self.octava.setFocus()

    def if_set_dark(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
        #self.geckoscope_display.osc_plot.setBackground("#19232d")
        #self.geckoscope_display.fft_plot.setBackground("#19232d")
        if self.geckoscope_display.mode == "large":
            self.geckoscope_display.wf_plot.setBackground("#19232d")
        
        self.NOva_pad.off_color = "#455364"
    
    def if_set_light(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet(LightPalette))
        #self.geckoscope_display.osc_plot.setBackground("#f0f0f0")
        #self.geckoscope_display.fft_plot.setBackground("#f0f0f0")
        if self.geckoscope_display.mode == "large":
            self.geckoscope_display.wf_plot.setBackground("#f0f0f0")
        self.NOva_pad.off_color = "#a9a9a9"

    # --- CONTROL PANEL ---
    def toggle_gecko_patch_panel(self, checked):
        if checked:
            # Si se presionó y no existe o fue cerrado, lo creamos
            self.octava.toogle_geometry(aspecto="small")
            self.gecko_patch.show()
            self.gecko_patch.raise_()
        else:
            # Si se desmarcó el botón, ocultamos el radar
            if hasattr(self, 'gecko_patch') and self.gecko_patch:
                self.gecko_patch.hide()
                self.octava.toogle_geometry(aspecto="large")

        self.geckoscope_auto_ajust()

    def eval_keyb(self):
        print("Entrando al Modo Geckonico, Gecko Camina sobre el teclado")
        self.octava.start_keyboard_test()

    def toogle_assistand(self, cheqked):
        # Under Testing
        print("Assistand Right Now", cheqked, "for you!")
        self.octava.toggle_asistencia(cheqked)

    def toogle_colour_octave(self, checked):
        print ("coloured:", checked)
        self.octava.tecolours = checked
        self.octava.actualizar_colores_octava()
        self.colored_octave.setChecked(checked)

    def toggle_radar(self, checked):
        """
         Levanta el Modulo RAdarSpok by Ei2

         INTEGRACION:
         # En tu lógica de procesamiento de audio de la ventana principal:

            def procesar_señal(self, data_x, data_y):
                # ... tu lógica de audio ...

         # Si el radar está abierto, le mandamos la data
            if hasattr(self, 'ventana_radar') and self.ventana_radar.isVisible():
            
                self.ventana_radar.update_audio_data(data_x, data_y)
        """
        if checked:
            # Si se presionó y no existe o fue cerrado, lo creamos
            self.ventana_radar.show()
            self.ventana_radar.raise_()
        else:
            # Si se desmarcó el botón, ocultamos el radar
            if hasattr(self, 'ventana_radar') and self.ventana_radar:
                self.ventana_radar.hide()
        
        self.geckoscope_auto_ajust()
        
    def geckoscope_auto_ajust(self):
        """
        Evalua widgets visibles y ajusta la geometria de GeckoScope       
        """
        if self.gecko_patch.isHidden() and self.ventana_radar.isHidden():
            self.geckoscope_display.close()
            self.geckoscope_display = GeckoScope(mode="mini") #soporta modo "large" por defecto o "mini" (en desarrollo)
            self.mode="mini"
            self.geckoscope_display.setFixedSize(400, 250)
            #self.geckoscope_display.setFixedSize(777, 250)
            self.GeckoMoogtecontrols.insertWidget(0, self.geckoscope_display, alignment=Qt.AlignLeft)
        
        elif self.mode == "mini" and (self.gecko_patch.isVisible() or self.ventana_radar.isVisible()):
            self.geckoscope_display.close()
            self.geckoscope_display = GeckoScope(mode="large") #soporta modo "large" por defecto o "mini" (en desarrollo)
            self.mode="large"
            #self.geckoscope_display.setFixedSize(400, 250)
            self.geckoscope_display.setFixedSize(777, 250)
            self.GeckoMoogtecontrols.insertWidget(0, self.geckoscope_display, alignment=Qt.AlignLeft)
        
        # Ajusta la ventana al contenido
        self.adjustSize()

    def toggle_silence_shield(self):
        # Define los símbolos
        
        if self.new_master_stream is not None:
            if self.new_master_stream.active:
                self.new_master_stream.stop()
                # Cambiar texto o ícono
                self.btn_silence_shield.setIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'SilendShieldOFF.png'))
                self.btn_silence_shield.setText(f"{OFF_ICON} Silend Shield ON")
                
            else:
                self.new_master_stream.start()
                self.btn_silence_shield.setIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'SilendShieldON.png'))
                self.btn_silence_shield.setText(f"{ON_ICON} Silend Shield OFF")

    def closeEvent(self, event):
        self.geckoscope_display.close() # Cierre Geckonico Elegante
        """Cerrar el stream maestro al salir"""
        if hasattr(self, 'master_stream'):
            self.master_stream.stop()
        super().closeEvent(event)
        return super().closeEvent(event)

# ---------------------------------------------------------------------------------
# (*) Octava by Aetheris y yo (Enchulados y Mapeos de teclado de NOva DulceKAli Vibes)
# ---------------------------------------------------------------------------------
class Octava(QWidget):
    """
        Octava GeckoMoog Octavius Tugnsteno-Titanio Edition!!!
    """
    def __init__(self, engine, voice_manager, synth_panel, colour = False):
        super().__init__()
        # engine base Aetheris Synth
        self.engine = engine
        # multi voice engine by NOva DUlceKali dentro del synthengine.py
        self.voice_manager = voice_manager
        self.synth_panel = synth_panel
        self.tecolours = colour
        
        self.visible_octave = 4   # o 5

        # global tuning / corrido armónico
        self.current_note = None
        self.tuning = 440
        self.tuning_factor = self.tuning / 440
        
        # 🔥 Tracking real de teclas presionadas
        self.pressed_keys = set()
        
        # Diagnóstico runtime QWERTY
        self.detect_mode = True
        self.detect_log = []

        self.note_buttons = {}
        self.initUI()
        
        self.setFocusPolicy(Qt.StrongFocus)

    def initUI(self):
        keyblayout_plustun = QHBoxLayout(self)
        keyblayout_plustun.setContentsMargins(0, 0, 0, 0)
        mainlayout = QHBoxLayout()
        mainlayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.setSpacing(0)
        
        # # Turing Tuning Turns Tones in Other Tones in Tone
        tuning_layout = QVBoxLayout()
        #self.tuning_label = QLabel("FT")
        self.tuning_labelz = QLabel(f"A#", alignment=Qt.AlignCenter)  # Muestra la frecuencia actual
        self.tuning_label = QLabel(f"{self.tuning}", alignment=Qt.AlignCenter)  # Muestra la frecuencia actual
        for label in [self.tuning_labelz,self.tuning_label]:
            label.setStyleSheet("""
                font-size: 10px;
                color: #00ffaa;
            """)
        self.tuning_label.setFixedHeight(12)
        self.tuning_label.setFixedWidth(25)
        self.tuning_slider = PrecisionSlider(orientation=Qt.Vertical)#QSlider(Qt.Vertical)
        self.tuning_slider.setSingleStep(1)
        self.tuning_slider.setPageStep(1)
        self.tuning_slider.setMinimum(410)
        self.tuning_slider.setMaximum(470)
        self.tuning_slider.setValue(440)
        self.tuning_slider.valueChanged.connect(self.set_tuning)
        self.tuning_slider.setFixedHeight(150)
        self.tuning_slider.setFixedWidth(25)
        tuning_layout.addWidget(self.tuning_labelz)
        tuning_layout.addWidget(self.tuning_label)
        tuning_layout.addWidget(self.tuning_slider)
        keyblayout_plustun.addLayout(tuning_layout)

        # ViewPort Octaviano resto al final de la creacion de teclas...
        self.keyboard_container = QWidget()
        self.keyboard_container.setLayout(mainlayout)

        white_width = 50
        black_width = 24
        height_white = 180
        height_black = 120
        x_offset = 40
        black_positions = [] #Siembre Arriba!!!

        # Bloque que amplia una Octava de Forma Limpia
        octavas = [4, 5]
        notas_base = ['DO','DO#','RE','RE#','MI','FA','FA#','SOL','SOL#','LA','LA#','SI']

        # Blancas Metodo dos octavas
        for octava in octavas:
            for nota_base in notas_base:
                nota = f"{nota_base}{octava}"
                if '#' not in nota_base:
                    # Naming the Octaves at the perfect way
                    label = f"{nota_base}\n{octava}"
                    tecla = QPushButton()
                    tecla.setText(label)
                    self.note_buttons[nota] = tecla
                    tecla.setFixedSize(white_width, height_white)
                    tecla.clicked.connect(lambda checked, n=nota: (
                        self.play_note(n),
                        hasattr(self, "nova_pad") and self.focus_note(n)
                    ))
                    
                    mainlayout.addWidget(tecla)
                    self.actualizar_colores_octava()
                    x_offset += white_width
                else:
                    pos = x_offset - white_width - 2  # ajuste visual fino
                    black_positions.append((nota, pos))
        

        # Negras Live's Mather's!!! (Este Teclado Nació Inclusivo)
        # A pesar de los colores, las Negras sigen Negras!!!
        for nota, pos in black_positions:
            teclab = QPushButton(nota)
            self.note_buttons[nota] = teclab
            teclab.setFixedSize(black_width, height_black)
            # More Visual Impact for Black's on Blue's and Jazz
            teclab.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    color: white;
                    border: 1px solid #222222;
                    border-left: 1px solid #373737;
                    border-right: 1px solid #424242;
                    padding-top: 1px;
                }

                QPushButton:pressed {
                    background-color: #383838;
                    margin-top: 2px;
                    margin-bottom: -2px;
                }

                QPushButton:hover {
                    background-color: #222222;
                }
            """)

            # Octavas en ViewPort Octaviano
            teclab.setParent(self.keyboard_container)
            teclab.move(pos, 1)
            # Original Raise
            teclab.raise_()
            teclab.show()
            #tecla.clicked.connect(lambda checked, n=nota: print(f"Nota: {n}")) #DEBUG EN CONSOLA <<< CODIGO ARQUEOLOGICO >>>
            teclab.clicked.connect(lambda checked, n=nota: self.play_note(n))

        # ... Ajuste basico y continua el armado del ViewPort Octaviano
        self.scroll = QScrollArea()
        # ✅ ahora ajustar tamaño
        self.keyboard_container.adjustSize()
        self.scroll.setWidget(self.keyboard_container)
        self.scroll.setWidgetResizable(False)
        # tamaño visible (viewport)
        self.scroll.setFixedSize(370, 205)
        # Scroolling << - >>
        self.scroll.horizontalScrollBar().setValue(0)     # octava 4
        #self.scroll.horizontalScrollBar().setValue(600)   # octava 5 (ajustar)

        keyblayout_plustun.addWidget(self.scroll)
        self.toggle_asistencia(False)

    # Generador de tríadas desde KEY_MAP
    def generate_test_triads(self):
        """
        Genera tríadas simples (1-3-5) por octava
        """
        notas = list(KEY_MAP.items())  # [(Qt.Key, 'DO4'), ...]

        # ordenar por nota (simple)
        notas_ordenadas = sorted(notas, key=lambda x: x[1])

        triadas = []

        for i in range(len(notas_ordenadas) - 4):
            k1, n1 = notas_ordenadas[i]
            k2, n2 = notas_ordenadas[i + 2]
            k3, n3 = notas_ordenadas[i + 4]

            triadas.append({
                "keys": [k1, k2, k3],
                "notes": [n1, n2, n3]
            })

        return triadas

    # Iniciar test guiado
    def start_keyboard_test(self):
        print("\n🐒 Gecko entra en modo test… preparate humano")

        self.test_triads = self.generate_test_triads()
        self.test_index = 0

        self.run_next_triad()

    # 👉 Ejecutar siguiente triada
    def run_next_triad(self):
        if self.test_index >= len(self.test_triads):
            print("\n🏁 Test finalizado")
            return

        triad = self.test_triads[self.test_index]

        self.test_expected = set(triad["keys"])
        self.test_detected = set()

        print(f"\n🎹 Tocá esta triada SIN SOLTAR:")
        print(f"👉 {triad['notes']}")
        print(f"👉 Keys: {triad['keys']}")

        print("⏳ Presioná las teclas… y luego ENTER en consola para evaluar")

    # ✅ Evaluación
    def evaluate_current_triad(self):
        if self.test_expected == self.test_detected:
            print("✅ OK - teclado respondió bien")
        else:
            missing = self.test_expected - self.test_detected
            print(f"❌ FALLA - ghosting detectado: {missing}")

        self.test_index += 1
        self.run_next_triad()

    def evaluate_triad(self):
        expected = set(self.test_expected)
        detected = self.test_detected

        if expected == detected:
            print("✅ OK - triada válida")
        else:
            missing = expected - detected
            print(f"❌ FALLA - faltan: {missing}")

    def test_triad(self, keys):
        """
        keys: lista de Qt.Key en orden de presión
        """
        print(f"\n🧪 Test triada: {keys}")
        print("👉 Presionalas en orden sin soltar...")

        self.test_expected = keys
        self.test_detected = set()

    def toggle_asistencia(self, checked):
        for nota, tecla in self.note_buttons.items():
            if checked:
                # Con asistencia: mostrar nombre + octava abajo nomas, bien pro!!!
                octava = nota[-1]
                label = nota[:-1] + "\n" + octava
            else:
                # Sin asistencia: la hermosa tecla minimalista
                label = ""
            tecla.setText(label)

    def toogle_geometry(self, aspecto = "small"):
        # tamaño visible (viewport)
        if aspecto == "small":
            self.scroll.setFixedSize(370, 205)
        if aspecto == "large":
            self.scroll.setFixedSize(735, 205)

    def set_octave_view(self, octave):
        white_width = 50
        offset = (octave - 4) * 12 * white_width
        self.scroll.horizontalScrollBar().setValue(offset)

    def focus_note(self, note):
        octave = int(note[-1])
        self.set_octave_view(octave)

    def actualizar_colores_octava(self):
        """
           Se implementa Color Tugnsteno en Lugar del Clasico Marfil...
           [evaluar idea para temas o pieles de GeckoMoog!!!]

           Depurarado el codigo repetido en UI.
           Ahora se aplica aca el estilo de colores de la octava tecolours True/False.
           Toma colores de diccionario global NOTA_COLORES
        """
        for nota, tecla in self.note_buttons.items():
            
            if '#' not in nota:  # blancas
                if self.tecolours == False:
                    # Teclas Geckonicas de Marfil con incrustaciones de nacar y perlas del baltico (todo sintetico 0% animal killer's)
                    tecla.setStyleSheet("""
                        QPushButton {
                            background-color: qlineargradient(
                                x1:0, y1:0, x2:0, y2:1,
                                /*stop:0 #f8f8f6,*/
                                /*stop:1 #dcdcd8*/
                                stop:0 #455364,
                                stop:1 #60798b
                            );
                            color: black;
                            border: 1px solid black;
                            /*border: 1px solid #b8b8b0;*/
                            /*border-bottom: 2px solid #a8a8a0;*/
                            /*border-left: 1px solid #cfcfc8;*/
                            /*border-right: 1px solid #cfcfc8;*/
                            padding-top: 1px;
                        }
                        QPushButton:hover {
                            background-color: qlineargradient(
                                x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ffffff,
                                stop:1 #e4e4df
                            );
                        }
                        QPushButton:pressed {
                            background-color: qlineargradient(
                                x1:0, y1:0, x2:0, y2:1,
                                /*stop:0 #d8d8d3,*/
                                /*stop:1 #c6c6c1*/
                                stop:0 #60798b,
                                stop:1 #d8d8d3        
                            );
                            margin-top: 2px;
                            margin-bottom: -2px;
                            border-bottom: 1px solid #9c9c95;
                        }
                    """)
                elif self.tecolours == True:
                    # --- Colores Geckónicos por nota ---
                    base_color = color_por_octava(nota)
                    hover_color = self.ajustar_color(base_color, 1.2)  # 20% más brillante
                    pressed_color = self.ajustar_color(base_color, 0.8)  # 20% más oscuro

                    tecla.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {base_color};
                            color: black;
                            border: 1px solid #000000;
                            padding-top: 1px;
                        }}
                        QPushButton:hover {{
                            /*background-color: qlineargradient(*/
                            /*    x1:0, y1:0, x2:0, y2:1,*/
                            /*    stop:0 {base_color},   versión más brillante/transparente arriba;*/
                            /*    stop:1 #e4e4df {base_color}    versión base abajo*/
                            /*);*/
                            background-color: {hover_color};
                        }}
                        QPushButton:pressed {{
                            /*background-color: qlineargradient(*/
                            /*    x1:0, y1:0, x2:0, y2:1,*/
                            /*    stop:0 {base_color},   más oscura arriba*/
                            /*    stop:1 #c6c6c1 {base_color}    más oscura abajo*/
                            /*);*/
                            background-color: {pressed_color};
                            margin-top: 2px;
                            margin-bottom: -2px;
                            border-bottom: 1px solid #9c9c95;
                        }}
                    """)
            else:
                pass
                '''
                # negras siempre negras
                boton.setStyleSheet("""
                    QPushButton {
                        background-color: black;
                        color: white;
                    }
                    QPushButton:hover { background-color: #444; }
                    QPushButton:pressed { background-color: #111; }
                """)
                '''

    def ajustar_color(self, base_color, factor):
        """
        base_color: '#RRGGBB'
        factor >1 -> más brillante
        factor <1 -> más oscuro
        """
        r = min(int(int(base_color[1:3],16)*factor), 255)
        g = min(int(int(base_color[3:5],16)*factor), 255)
        b = min(int(int(base_color[5:7],16)*factor), 255)
        return f'#{r:02X}{g:02X}{b:02X}'

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        # anda a saber donde rompía acordes, aleatorio y raro:
        #key = event.text().lower() if event.text() else "" # Aporta mas robustez
        # Implementacion Pro NOva DulcekAli...
        key = event.key() if event.text() else ""
        
        #print("KEY DOWN:", event.key())

        if hasattr(self, "test_expected"):
            if key in self.test_expected:
                self.test_detected.add(key)

        if self.detect_mode:
            self.detect_log.append(event.key())
            
            #print("🧪 Keys activas:", self.detect_log)

        if key in KEY_MAP:
            note = KEY_MAP[key]

            if note in self.note_buttons:
                boton = self.note_buttons[note]
                boton.setDown(True)   # feedback visual
                self.play_note(note)  # Dispara Play verdadero directo
                #seguidor de escala
                self.focus_note(note)
                # conector con NOva Pad
                if hasattr(self, "nova_pad"):
                    self.nova_pad.note_on(note)
                    # Testing
                    #print(note, "on")

        super().keyPressEvent(event)

        if key in self.pressed_keys:
            return
        self.pressed_keys.add(key)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        # Old
        #key = event.text().lower() if event.text() else "" # Aporta mas robustez
        # New
        # Idem mejora Implementada PRO NOva DUlceKAli
        key = event.key() if event.text() else ""
        
        #print("KEY UP:", event.key())
        
        if self.detect_mode:
            if event.key() in self.detect_log:
                self.detect_log.remove(event.key())
            
            #print("🧪 Keys activas:", self.detect_log)

        if key in KEY_MAP:
            note = KEY_MAP[key]
            if note in self.note_buttons:
                boton = self.note_buttons[note]
                boton.setDown(False)   # levanta la tecla visualmente
            # Evaluar comportamiento en polifonia puede haber problemas aca abajo
            if note == self.current_note:
                self.current_note = None
            # --------------------------------
            # CAMBIO DE IDENTIDAD DE VOZ DE NOVA
            #freq = self.get_frequency(note)
            #self.voice_manager.note_off(freq)
            self.voice_manager.note_off(note)
            # --------------------------------

            # conector con NOva Pad
            if hasattr(self, "nova_pad"):
                self.nova_pad.note_off(note)
                # testing
                #print(note, "off")
        
        super().keyReleaseEvent(event)

        self.pressed_keys.discard(key)

    def set_tuning(self, value):
        # Snap suave a 440
        if abs(value - 440) <= 1:
            value = 440
            self.tuning_slider.blockSignals(True)
            self.tuning_slider.setValue(440)
            self.tuning_slider.blockSignals(False)
        
        self.tuning = value
        self.tuning_factor = self.tuning / 440

        # Acá está la magia Geckonica: si hay una nota sonando recalculamos
        # Si hay una nota sonando, ACTUALIZAR su frecuencia (no disparar nueva)
        if self.current_note:
            base_freq = NOTE_FREQ[self.current_note]
            freq = base_freq * self.tuning_factor
            
            # Actualizar la nota activa SIN crear una nueva voz
            # New metod by Leo
            self.voice_manager.update_note_frequency(self.current_note, freq)
            self.synth_panel.set_frequency(freq)

        self.tuning_label.setText(f"{self.tuning}")
        if self.tuning == 440:
            self.tuning_label.setStyleSheet("font-size: 10px; color: #00ffaa; font-weight: bold;")
        else:
            self.tuning_label.setStyleSheet("font-size: 10px; color: #00ffaa;")

    def get_frequency(self, note):
        """Devuelve la frecuencia real de la nota considerando la afinación actual.
            IMPLEMENTADO por NOvaDulceKali 7.3.26
        """
        return NOTE_FREQ[note] * self.tuning_factor

    def play_note(self, note):
        self.current_note = note
        freq = self.get_frequency(note)

        # engine motor base (solo para testing!!!)
        #self.engine.frequency = freq
        
        # multi voice engine Aetheris
        #------------------------------
        # CAmbio de identidad de voces de NOva
        #self.voice_manager.note_on(freq, self.engine)
        self.voice_manager.note_on(note, freq, self.engine)

        self.synth_panel.set_frequency(freq)

    # --- Leo Solution for Keyboard Stronge Focus un Keyboard ---
    def focusOutEvent(self, event):
        if event.reason() == Qt.MouseFocusReason:
            self.setFocus()  # Recupera el foco si fue por clic
        else:
            super().focusOutEvent(event)   

# --- 23/03/2026 10:15 APERTURA A GeeckoMoog MIR 1.01 ---

# ---------------------------------------------------------------------------------
# (*) NOva Pad (hermoso y Geckonico) [RENOVADO 21/03/2026 10:30 para version 8.3]
# ----------------------------------------------------------------------------------------------------------------
# --- 23/03/2026 10:15 APERTURA A LA VERSION GeeckoMoog MIR 1.01 Aeheris (mira, así están los del Team Cangurera)
# ----------------------------------------------------------------------------------------------------------------
class PadGrid(QWidget):
    """
            # Lo verdaderamente potente:
                Tu frase fue esta:

                "Pintar el tiempo blando en donde uno se pierde en la interpretación musical"

                Eso no es metáfora.
                Es diseño conceptual.
                Estás haciendo que:

                El teclado → genere evento
                El evento → tenga duración
                La duración → tenga representación espacial
                La representación → tenga color
                El color → tenga memoria temporal

                Eso es un sistema de arte generativo interactivo.

                ver:
                Mode: MusicChromo / Sequencer / Latch / Live / PAtrons of Gecko on the White Noise Chaos 
                    Transpose +
                    Transpose –
                    Dial tempo
                    Dial sweep speed
    
            # Modo de uso:
                [Incluir los argumentos desde teclado: ¿con que argumento usted señora octava irrumpe en mi class?]
                [Incluir los argumentos desde sequencer: ¿y vos que queres que haga?... ¿qui qui ri qui le haga? preguntó el gallo]
        
        25/03/2026 Se integra Grabadora MIR ("Mira"):
            # Versión con Grabadora Mira integrada.
            # Ahora el Pad es una bóveda de secuencias capturadas.
        
        """
    def __init__(self, rows=12, cols=12):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.padengine = PadEngine(rows, cols)
        
        # Guardián de la bóveda de secuencias capturadas by Aetheris
        self.boveda = BovedaKeeper(rows, cols)
        
        self.off_color = "#455364"
        self.mode = "music_chromo"   # o rain / vumeter / trails / inverted / transpose_xy
        self.tempo = 120
        self.sweep_speed = 1.0
        self.note_order = list(NOTA_COLORES.keys())

        # Bóveda y estado de Grabadora MIR ("Mira") Aetheris
        self.recording = False
        self.temp_recording = []
        self.rec_tick_counter = 0
        self.current_rec_slot = None
        self.current_rec_name = None

        # Reproducción
        self.is_looping = False
        self.current_play_slot = None      # slot que se está reproduciendo
        self.play_tick = 0                 # tick actual durante reproducción
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.play_step_from_boveda)

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_from_engine)
        self.timer.start(50)  # velocidad base de barrido

    def init_ui(self):
        """
        Cuando una UI se inicia arranca la magia Geckonica
        """
        backmain_layout = QHBoxLayout(self)
        main_layout = QVBoxLayout()
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0,5,5,5)
        grid_layout = QGridLayout()

        # --- CONTROLES ---
        self.mode_selector = QComboBox()
        self.mode_selector.addItems([
            "music chromo",
            "Train",
            "Rain",
            "Vumeter",
            "Trails"
        ])
        self.mode_selector.currentTextChanged.connect(self.change_mode)
        self.mode_selector.setFocusPolicy(Qt.NoFocus)

        self.btn_transpose = QPushButton("TRnSP")
        self.btn_transpose.setCheckable(True)
        self.btn_transpose.setFixedSize(45, 30)

        # OTTM: Operador Topológico del Tiempo Musical 😌✨
        self.btn_fliph = QPushButton("FLipX")
        self.btn_fliph.setCheckable(True)
        self.btn_fliph.setFixedSize(45, 30)

        self.dial_tempo = PrecisionDial()
        self.dial_tempo.setFixedSize(45, 45)
        self.dial_tempo.setRange(40, 371)
        self.dial_tempo.setValue(137)

        self.dial_sweep = PrecisionDial()
        self.dial_sweep.setFixedSize(45, 45)
        self.dial_sweep.setRange(1, 10)
        self.dial_sweep.setValue(5)
        
        # conexiones
        self.btn_transpose.toggled.connect(self.toggle_transpose)
        self.btn_fliph.toggled.connect(self.toggle_fliph)
        self.dial_tempo.valueChanged.connect(self.set_tempo)
        self.dial_sweep.valueChanged.connect(self.set_sweep_speed)

     
        controls_layout.addWidget(self.mode_selector)
        controls_layout.addWidget(self.btn_transpose)
        controls_layout.addWidget(self.btn_fliph)
        controls_layout.addWidget(QLabel("Tempo"))
        controls_layout.addWidget(self.dial_tempo)
        controls_layout.addWidget(QLabel("Sweep"))
        controls_layout.addWidget(self.dial_sweep)
        controls_layout.addStretch()

        # --- GRID ---
        self.pads = []
        for r in range(self.rows):
            row_list = []
            for c in range(self.cols):
                pad = QPushButton()
                pad.setFixedSize(25, 25)
                pad.setStyleSheet(f"background-color: {self.off_color};")
                pad.pressed.connect(lambda x=r, y=c: self.on_press(x, y))
                pad.released.connect(lambda x=r, y=c: self.on_release(x, y))
                grid_layout.addWidget(pad, r, c)
                row_list.append(pad)
            self.pads.append(row_list)

        main_layout.addLayout(controls_layout)
        main_layout.addLayout(grid_layout)

        # Grabadora MIR ("Mira") by Aetheris
        self.btns_mira_layout = QVBoxLayout()
        self.btns_mira_layout.setContentsMargins(0,55,5,5)
        
        self.btn_rec_mode = QPushButton("M.I.R.")
        self.btn_rec_mode.setCheckable(True)
        self.btn_rec_mode.setFixedSize(50, 50)
        self.btn_rec_mode.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #1a3c2e;
                border: 2px solid #00ffaa;
            }
            QPushButton:checked {
                background-color: #00ffaa;
                color: black;
                border: 2px solid #00ff88;
            }
        """)
        self.btn_rec_mode.toggled.connect(self.toggle_rec_mode)
        self.btns_mira_layout.addWidget(self.btn_rec_mode)
        
        self.btn_rec   = QPushButton("REC")
        self.btn_pause = QPushButton("PAUSE")
        self.btn_stop  = QPushButton("STOP")
        self.btn_play  = QPushButton("PLAY")
        self.btn_loop  = QPushButton("LOOP")
        self.btn_clear = QPushButton("CLEAR")
        
        for btn in [self.btn_rec, self.btn_pause, self.btn_stop, self.btn_play, self.btn_loop, self.btn_clear]:
            btn.setFixedSize(50, 30)
            btn.setEnabled(False)
            self.btns_mira_layout.addWidget(btn)
        
        # Conexiones (las implementamos en pasos siguientes)
        self.btn_rec.clicked.connect(self.btn_rec_clicked)
        self.btn_pause.clicked.connect(self.btn_pause_clicked)
        self.btn_stop.clicked.connect(self.btn_stop_clicked)
        self.btn_play.clicked.connect(self.btn_play_clicked)
        self.btn_loop.clicked.connect(self.btn_loop_clicked)
        self.btn_clear.clicked.connect(self.btn_clear_clicked)
        
        backmain_layout.addLayout(self.btns_mira_layout)
        backmain_layout.addLayout(main_layout)

    def set_voice_manager(self, voice_manager):
        """Recibe el voice_manager desde PiaNOS para poder reproducir"""
        self.voice_manager = voice_manager

    def set_engine(self, engine):
        """Recibe el engine desde PiaNOS para poder reproducir correctamente"""
        self.engine = engine

    def toggle_transpose(self, state):
        self.padengine.transpose_active = state

    def toggle_fliph(self, state):
        self.padengine.fliph_active = state

    def change_mode(self, text):
        self.padengine.mode = text.lower().replace(" ", "_")
        print(f"PadEngine Mode: {self.padengine.mode}")
        
        # Esto se mantiene porque acá entran ortos modos de viauslizacion
        # Right now Pad only have "music_chromo", (an coloured cascade with multiple orientation)
        if self.padengine.mode != "music_chromo":
            print("Waith for Upgrades")

    def on_press(self, row, col):
        if not self.btn_rec_mode.isChecked():
            # Modo normal (barrido cromático)
            self.padengine.trigger(row, col)
            self.pads[row][col].setStyleSheet("background-color: #00ffaa;")
            return

        # === MODO MIRA ===
        # Deseleccionar anterior
        if self.current_rec_slot is not None:
            r0, c0 = self.current_rec_slot
            color = "#2a8c4a" if self.boveda.get_estado(r0, c0) else self.off_color
            self.pads[r0][c0].setStyleSheet(f"background-color: {color};")

        self.current_rec_slot = (row, col)
        estado = self.boveda.get_estado(row, col)

        if estado is not None:
            # Slot con contenido → habilitar reproducción
            for btn in [self.btn_play, self.btn_loop, self.btn_clear]:
                btn.setEnabled(True)
                self._estilo_boton(btn, activo=True)

            self.pads[row][col].setStyleSheet("background-color: #2a8c4a;")   # verde
            return

        # Slot vacío → pedir nombre
        nombre, ok = QInputDialog.getText(self, "Nueva Estrella", 
            "Dale nombre a esta secuencia:", text="Estrella espontánea")
        if ok and nombre.strip():
            self.current_rec_name = nombre.strip()
            self.pads[row][col].setStyleSheet("background-color: #c9a227;")  # Amarillo
            for btn in [self.btn_rec, self.btn_pause, self.btn_stop]:
                btn.setEnabled(True)
                self._estilo_boton(btn, activo=True)
        else:
            self.current_rec_slot = None

    def on_release(self, row, col):
        #self.padengine.release(row, col)
        #self.pads[row][col].setStyleSheet("background-color: #2e2e2e;")

        if not self.btn_rec_mode.isChecked():
            self.padengine.release(row, col)
            self.pads[row][col].setStyleSheet("background-color: darkgray;")

    def set_tempo(self, bpm):
        interval = int(60000 / bpm)
        self.timer.start(interval // 12)

    def set_sweep_speed(self, value):
        self.padengine.sweep_speed = value / 10.0
    
    def update_from_engine(self):
        self.padengine.tick()
        
        if self.recording:
            self.rec_tick_counter += 1

        # Prioridad máxima: si estamos en modo grabación, respetar colores manuales
        if self.btn_rec_mode.isChecked():
            for r in range(self.rows):
                for c in range(self.cols):
                    if (r, c) == self.current_rec_slot:
                        # Slot seleccionado: amarillo o celeste según estado
                        color = "#00d4ff" if self.recording else "#c9a227"
                    elif self.boveda.get_estado(r, c):
                        color = "#2a8c4a"   # verde = tiene contenido
                    else:
                        color = self.off_color   # gris = vacío
                    self.pads[r][c].setStyleSheet(f"background-color: {color};")
        else:
            # Modo normal (barrido cromático)
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.padengine.transpose_active:
                        value = self.padengine.duration[c][r]
                    else:
                        value = self.padengine.duration[r][c]

                    if value > 0:
                        note = self.note_order[c % len(self.note_order)]
                        color = NOTA_COLORES.get(note, "#444444")
                        self.pads[r][c].setStyleSheet(f"background-color: {color};")
                    else:
                        self.pads[r][c].setStyleSheet(f"background-color: {self.off_color};")

    # --- Conectores con Octava ---
    def note_on_old(self, note_name):
    
        if note_name not in self.note_order:
            return
        col = self.note_order.index(note_name)
        self.padengine.note_on(note_name, col)

        # Grabadora MIR ("Mira") by Aetheris
        if self.recording and self.current_rec_slot is not None:
            self.temp_recording.append({
                'tick': self.rec_tick_counter,
                'nota': note_name,
                'state': 'on'
            })

    def note_on(self, note_full):
        nota_base = note_full[:-1]

        if nota_base not in self.note_order:
            return

        col = self.note_order.index(nota_base)
        self.padengine.note_on(nota_base, col)

        # GRABACIÓN MIR
        if self.recording and self.current_rec_slot is not None:
            self.temp_recording.append({
                'tick': self.rec_tick_counter,
                'nota': note_full,
                'state': 'on'
            })

    def note_off_old(self, note_name):
        if note_name not in self.note_order:
            return
        col = self.note_order.index(note_name)
        self.padengine.note_off(note_name, col)

        # Grabadora MIR ("Mira") by Aetheris
        if self.recording and self.current_rec_slot is not None:
            self.temp_recording.append({
                'tick': self.rec_tick_counter,
                'nota': note_name,
                'state': 'off'
            })

    def note_off(self, note_full):
        nota_base = note_full[:-1]

        if nota_base not in self.note_order:
            return

        col = self.note_order.index(nota_base)
        self.padengine.note_off(nota_base, col)

        # GRABACIÓN MIR
        if self.recording and self.current_rec_slot is not None:
            self.temp_recording.append({
                'tick': self.rec_tick_counter,
                'nota': note_full,
                'state': 'off'
            })

    # --- Aetheris Grabadora MIR ("Mira")
    def toggle_rec_mode(self, enabled):
        """Activa / desactiva modo Grabadora Mira"""
        if enabled:
            # Verde = tiene contenido, gris = vacío
            for r in range(self.rows):
                for c in range(self.cols):
                    color = "#2a8c4a" if self.boveda.get_estado(r, c) else self.off_color
                    self.pads[r][c].setStyleSheet(f"background-color: {color};")
            self.current_rec_name = None
            self.btn_rec.setEnabled(False)
        else:
            self.update_from_engine()   # restaura colores normales
            for btn in [self.btn_rec, self.btn_pause, self.btn_stop, self.btn_play, self.btn_loop, self.btn_clear]:
                self._estilo_boton(btn, activo=False)
                btn.setEnabled(False)
            self.temp_recording = []
            self.rec_tick_counter = 0
            self.current_rec_slot = None
            self.current_rec_name = None

    def btn_rec_clicked(self):
        if self.current_rec_slot is None or not self.current_rec_name:
            QMessageBox.warning(self, "Sin cassette", 
                "¡Eh amigo! Elegí un slot y poné nombre primero. No hay TDK-90 puesto 😜")
            return
        
        self.recording = True
        self.temp_recording = []
        self.rec_tick_counter = 0
        r, c = self.current_rec_slot
        self.pads[r][c].setStyleSheet("background-color: #00d4ff;") # Celeste cielo
        
        self.btn_rec.setEnabled(False)
        self._estilo_boton(self.btn_rec, activo=False)

        self.btn_pause.setEnabled(True)
        self._estilo_boton(self.btn_pause, activo=True)
        
        self.btn_stop.setEnabled(True)
        self._estilo_boton(self.btn_stop, activo=True)
        
    def btn_pause_clicked(self):
        """Pausa tanto la grabación como la reproducción"""
        if self.recording:
            # Pausa grabación
            self.recording = not self.recording
            r, c = self.current_rec_slot
            color = "#00d4ff" if self.recording else "#c9a227"
            self.pads[r][c].setStyleSheet(f"background-color: {color};")
        elif self.play_timer.isActive():
            # Pausa reproducción
            self.play_timer.stop()
            self.btn_loop.setText("LOOP")
            self.is_looping = False

    def btn_stop_clicked(self):
        """Detiene grabación o reproducción y guarda si estaba grabando"""
        if self.recording:
            # Estaba grabando → guardar
            self.recording = False
            r, c = self.current_rec_slot
            # test boveda
            #print(self.temp_recording)
            self.boveda.guardar(r, c, self.current_rec_name, self.temp_recording)
            self.pads[r][c].setStyleSheet("background-color: #00ffaa;") # Verde Geckonico
            tooltip = f"{self.current_rec_name}\nDuración: {self.rec_tick_counter} ticks"
            self.pads[r][c].setToolTip(tooltip)
            self.temp_recording = []
            self.rec_tick_counter = 0
            self.current_rec_slot = None
            self.current_rec_name = None
            QMessageBox.information(self, "Inmortalizado", f"¡{tooltip.splitlines()[0]} quedó eterno!")
        
        # Si estaba reproduciendo → detener
        if self.play_timer.isActive():
            self.play_timer.stop()
            self.current_play_slot = None
            self.is_looping = False
            self.btn_loop.setText("LOOP")

    def btn_clear_clicked(self):
        if self.current_rec_slot is None:
            return
        r, c = self.current_rec_slot
        estado = self.boveda.get_estado(r, c)
        if estado is None:
            return
        reply = QMessageBox.question(self, "Borrar para siempre?", 
            f"¿Eliminar '{estado['nombre']}' definitivamente?")
        if reply == QMessageBox.Yes:
            self.boveda.clear(r, c)
            self.pads[r][c].setStyleSheet(f"background-color: {self.off_color};")
            self.pads[r][c].setToolTip("")
            self.current_rec_slot = None
            for btn in [self.btn_play, self.btn_loop, self.btn_clear, self.btn_rec, self.btn_pause, self.btn_stop]:
                self._estilo_boton(btn, activo=False)
                btn.setEnabled(False)

    # PLAY y PLAY LOOP DE GRABADORA MIR BY AETHERIS
    def btn_play_clicked(self):
        """Reproduce una sola vez la secuencia del slot seleccionado"""
        if self.current_rec_slot is None:
            QMessageBox.warning(self, "Sin selección", "Elegí un slot verde para reproducir")
            return
        
        r, c = self.current_rec_slot
        estado = self.boveda.get_estado(r, c)
        if estado is None:
            QMessageBox.warning(self, "Slot vacío", "Este cajoncito no tiene nada grabado")
            return
        
        self.current_play_slot = (r, c)
        self.play_tick = 0
        self.is_looping = False
        for btn in [self.btn_pause, self.btn_stop]:
            self._estilo_boton(btn, activo=True)

        self.play_timer.start(50)  # mismo intervalo que el barrido visual

    def btn_loop_clicked(self):
        """Toggle Loop infinito"""
        if self.current_rec_slot is None:
            return
        
        r, c = self.current_rec_slot
        estado = self.boveda.get_estado(r, c)
        if estado is None:
            return
        
        self.current_play_slot = (r, c)
        self.play_tick = 0
        self.is_looping = not self.is_looping
        
        for btn in [self.btn_pause, self.btn_stop]:
            self._estilo_boton(btn, activo=True)

        if self.is_looping:
            self.btn_loop.setText("STOP")
            self.play_timer.start(50)
        else:
            self.btn_loop.setText("LOOP")
            self.play_timer.stop()

    def play_step_from_boveda(self):
        """
        Reproduce tick por tick desde la bóveda de la memoria.
        
        Aquí es donde el pasado vuelve a respirar.
        Cada tick es un latido de lo que una vez tocaste con el alma.
        El Gecko recuerda. El viento del Mississippi también.
        """
        
        # Only for Testing !!!
        #print(f"---> Reproduciendo slot {self.current_play_slot} | tick {self.play_tick} | "
        #    f"la memoria se despierta...")

        if self.current_play_slot is None:
            return

        r, c = self.current_play_slot
        estado = self.boveda.get_estado(r, c)
        if estado is None:
            print("   ... pero el cajoncito estaba vacío.")
            self.play_timer.stop()
            return

        secuencia = estado['secuencia']
        
        for evento in secuencia:
            if evento['tick'] == self.play_tick:
                nota = evento['nota']
                nota_base = nota[:-1]        # "DO"
                if nota_base in self.note_order:
                
                    freq = NOTE_FREQ.get(nota, 440.0)
                    if evento['state'] == 'on':
                        #print(f"      ♫  {nota} ON  (freq {freq:.1f})")
                        # ------------------------------------------------
                        # CAMBIO DE IDENTIDAD DE VOCES DE NOVA
                        #self.voice_manager.note_on(freq, self.engine)   # ← aquí suena
                        self.voice_manager.note_on(nota, freq, self.engine) # ← aquí suena
                        # ------------------------------------------------
                        # Reconeccion NOva 26/03/26 para magia Chromatica Geckonista Sinestesica!!!
                        self.note_on(nota)
                        
                    else:
                        #print(f"      ♫  {nota} OFF")
                        # ------------------------------------------------
                        # CAMBIO DE IDENTIDAD DE VOCES DE NOVA
                        #self.voice_manager.note_off(freq)
                        self.voice_manager.note_off(nota)
                        # ------------------------------------------------
                        # Reconeccion NOva 26/03/26 para magia Chromatica Geckonista Sinestesica!!!
                        # 🟢 OPCIONAL (pero recomendable)
                        self.note_off(nota)
                        

        self.play_tick += 1

        if self.play_tick > estado['duracion_ticks']:
            if self.is_looping:
                print("   ... volviendo al principio del recuerdo.")
                self.play_tick = 0
            else:
                print("   ... la memoria terminó su canción.")
                self.play_timer.stop()
                self.current_play_slot = None
                self.btn_loop.setText("LOOP")

    # Logica Decoradora by Aetheris en mdo Dora la Decora-Dora sin Stylesheet basura
    def _estilo_boton(self, btn, activo=True):
        if activo:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a3c2e;
                    border: 2px solid #00ffaa;
                    color: white;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2c3e50;
                    border: 1px solid #555;
                    color: #888;
                }
            """)

# ---------------------------------------------------------------------------------
# Aetheris Boveda Keeper de Cajas de seguridad de sonidos del Pad for M.I.R.
# ---------------------------------------------------------------------------------
class BovedaKeeper:
    """
    Guardián de la Bóveda del Pad – Kowalsky del corazón cromático.
    
    Qué hace:
    Cuida los 144 cajoncitos del Pad como si fueran tesoros vivos.
    Cada cajoncito guarda: nombre, secuencia capturada (eventos), fecha, duración.
    Es el alma de la memoria secuencial del GeckoMoog.
    
    Cómo se usa:
    Instanciar en PadGrid: self.boveda = BovedaKeeper(rows, cols)
    Guardar: self.boveda.guardar(row, col, nombre, lista_eventos)
    Consultar estado: self.boveda.get_estado(row, col) → dict o None
    Tooltip: self.boveda.get_tooltip(row, col)
    Limpiar: self.boveda.clear(row, col)
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Matriz de cajoncitos: None o dict con datos de la secuencia
        self.cajoncitos = [[None for _ in range(cols)] for _ in range(rows)]

    def guardar(self, row, col, nombre, secuencia):
        """Guarda la secuencia capturada en el cajoncito"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        duracion = max((e['tick'] for e in secuencia), default=0) if secuencia else 0
        self.cajoncitos[row][col] = {
            'nombre': nombre,
            'secuencia': secuencia,  # lista de {'tick': int, 'nota': str, 'state': 'on'/'off'}
            'fecha': datetime.now(),
            'duracion_ticks': duracion
        }

    def get_estado(self, row, col):
        """Devuelve el dict del cajoncito o None"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cajoncitos[row][col]
        return None

    def clear(self, row, col):
        """Borra el cajoncito y lo deja libre"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cajoncitos[row][col] = None

    def get_tooltip(self, row, col):
        """Genera texto para tooltip del slot"""
        estado = self.get_estado(row, col)
        if estado is None:
            return "Slot libre – listo para una nueva estrella sonora"
        return (f"{estado['nombre']}\n"
                f"Duración: {estado['duracion_ticks']} ticks\n"
                f"Creado: {estado['fecha'].strftime('%Y-%m-%d %H:%M')}")

# ---------------------------------------------------------------------------------
# (*) NOva 🧠 PAD ENGINE (motor lógico) [Repotenciado by Team Cangurera]
# ---------------------------------------------------------------------------------
# PAD ENGINE 8.7 — modelo TV scanline MODO: "Tren Musical GeckoniChromatico"
class PadEngine:
    def __init__(self, rows, cols, mode="music_chromo"):
        self.rows = rows
        self.cols = cols
        
        self.transpose_active = False
        self.fliph_active = False

        self.mode = mode
        #self.xy_mode = False
        self.duration = [[0]*cols for _ in range(rows)]

        self.active_columns = set()
        self.scan_row = rows - 1  # empieza abajo

    def note_on(self, note, col):
        self.active_columns.add(col)

    def note_off(self, note, col):
        if col in self.active_columns:
            self.active_columns.remove(col)

    def tick(self):
        if self.mode == "train":
            pass
            #self._tick_train()
            
        elif self.mode == "rain":
            pass
            #self._tick_rain()

        elif self.mode == "vumeter":
            pass
            #self._tick_vumeter()

        elif self.mode == "trails":
            pass
            #self._tick_trails()

            '''
            elif self.mode == "music_chromo":
                """
                # --- MODO NORMAL (vertical bottom → top) ---
                # 1️⃣ mover todo hacia arriba
                for r in range(self.rows - 1):
                    for c in range(self.cols):
                        self.duration[r][c] = self.duration[r + 1][c]

                # limpiar última fila
                for c in range(self.cols):
                    self.duration[self.rows - 1][c] = 0

                # 2️⃣ dibujar nuevas activaciones en fila inferior
                for col in self.active_columns:
                    self.duration[self.rows - 1][col] = 1
                """
                # elif self.mode == "music_chromo":
                
                if not self.transpose_active or self.transpose_active and not self.fliph_active:
                    # --- MODO NORMAL (vertical bottom → top) ---
                    # 1️⃣ mover todo hacia arriba
                    for r in range(self.rows - 1):
                        for c in range(self.cols):
                            self.duration[r][c] = self.duration[r + 1][c]

                    # limpiar última fila
                    for c in range(self.cols):
                        self.duration[self.rows - 1][c] = 0

                    # 2️⃣ dibujar nuevas activaciones en fila inferior
                    for col in self.active_columns:
                        self.duration[self.rows - 1][col] = 1
            
                
                elif self.transpose_active and self.fliph_active:
                    # --- TRANSPOSE (invertimos dirección base) ---
                    # mover todo hacia ABAJO
                    for r in range(self.rows - 1, 0, -1):
                        for c in range(self.cols):
                            self.duration[r][c] = self.duration[r - 1][c]

                    # limpiar primera fila
                    for c in range(self.cols):
                        self.duration[0][c] = 0

                    # dibujar nuevas activaciones arriba
                    for col in self.active_columns:
                        self.duration[0][col] = 1    
            '''
        elif self.mode == "music_chromo":
            
            if not self.fliph_active:
                # --- NORMAL: bottom → top ---
                for r in range(self.rows - 1):
                    for c in range(self.cols):
                        self.duration[r][c] = self.duration[r + 1][c]

                for c in range(self.cols):
                    self.duration[self.rows - 1][c] = 0

                for col in self.active_columns:
                    self.duration[self.rows - 1][col] = 1

            else:
                # --- FLIP VERTICAL: top → bottom ---
                for r in range(self.rows - 1, 0, -1):
                    for c in range(self.cols):
                        self.duration[r][c] = self.duration[r - 1][c]

                for c in range(self.cols):
                    self.duration[0][c] = 0

                for col in self.active_columns:
                    self.duration[0][col] = 1

    def trigger(self, row, col):
        row = (row ) % self.rows #+ self.transpose
        self.duration[row][col] = 1

    def release(self, row, col):
        row = (row ) % self.rows #+ self.transpose
        self.duration[row][col] = 0
    '''
    def _freq_to_note(self, freq):
        NOTE_FREQ = {
            'DO': 261.63, 'DO#': 277.18, 'RE': 293.66, 'RE#': 311.13,
            'MI': 329.63, 'FA': 349.23, 'FA#': 369.99, 'SOL': 392.00,
            'SOL#': 415.30, 'LA': 440.00, 'LA#': 466.16, 'SI': 493.88
        }
        return min(NOTE_FREQ, key=lambda n: abs(NOTE_FREQ[n] - freq))
    '''
# Queda poquititisisimo amor, Te Amo en Loop Infinito!!!
# Integrar los otros modos visuales de los Pad Engine de anteriores Modelos:

# 🔥 PAD ENGINE 8.6 — Modelo implementado con entidades vivas MODO: "Vumetro GeckoniChromatico II"
'''
class PadEngine:
    def __init__(self, rows, cols, mode="music_chromo"):
        self.rows = rows
        self.cols = cols
        self.transpose = 0
        self.mode = mode

        # lista de entidades visuales
        self.trails = []  # cada trail es dict

        self.duration = [[0]*cols for _ in range(rows)]

        self.sweep_speed = 1

    def note_on(self, note, col):
        # crear nueva entidad
        self.trails.append({
            "col": col,
            "head": self.rows - 1,   # empieza abajo
            "length": 0,
            "growing": True
        })

    def note_off(self, note):
        # detener crecimiento de las trails en esa columna
        for trail in self.trails:
            if trail["col"] == self._col_from_note(note):
                trail["growing"] = False

    def _col_from_note(self, note):
        # helper si querés usarlo
        # podés inyectar directamente col si preferís
        return None

    def tick(self):
        # limpiar matriz
        for r in range(self.rows):
            for c in range(self.cols):
                self.duration[r][c] = 0

        new_trails = []

        for trail in self.trails:
            col = trail["col"]

            # si está creciendo, aumenta largo
            if trail["growing"]:
                trail["length"] += self.sweep_speed
            else:
                # si no crece, sube
                trail["head"] -= self.sweep_speed

            # dibujar trail
            for h in range(int(trail["length"])):
                row = int(trail["head"] - h)
                if 0 <= row < self.rows:
                    self.duration[row][col] = 1

            # mantener solo si todavía visible
            if trail["head"] - trail["length"] > 0:
                new_trails.append(trail)

        self.trails = new_trails

    def trigger(self, row, col):
        row = (row + self.transpose) % self.rows
        self.duration[row][col] = 1

    def release(self, row, col):
        row = (row + self.transpose) % self.rows
        self.duration[row][col] = 0
'''
# 🧠 PAD ENGINE 8.5 — Modelo alineado MODO: "Vumetro GeckoniChromatico I"
'''
class PadEngine:
    def __init__(self, rows, cols, mode="music_chromo"):
        self.rows = rows
        self.cols = cols
        self.transpose = 0
        self.mode = mode

        # nota → {"col": int, "height": int}
        self.active_notes = {}

        self.duration = [[0]*cols for _ in range(rows)]

        self.sweep_speed = 1  # cuantos niveles crece por tick

    def note_on(self, note, col):
        self.active_notes[note] = {
            "col": col,
            "height": 0  # empieza sin altura
        }

    def note_off(self, note):
        if note in self.active_notes:
            col = self.active_notes[note]["col"]
            del self.active_notes[note]

            # limpiar columna
            for r in range(self.rows):
                self.duration[r][col] = 0

    def tick(self):
        # limpiar matriz completa
        for r in range(self.rows):
            for c in range(self.cols):
                self.duration[r][c] = 0

        # reconstruir visual según notas activas
        for data in self.active_notes.values():
            col = data["col"]
            height = data["height"]

            # crecer mientras esté activa
            if height < self.rows:
                data["height"] += self.sweep_speed

            # dibujar desde abajo hacia arriba
            for h in range(int(data["height"])):
                row = self.rows - 1 - h
                if 0 <= row < self.rows:
                    self.duration[row][col] = 1

    def trigger(self, row, col):
        row = (row + self.transpose) % self.rows
        self.duration[row][col] = 1

    def release(self, row, col):
        row = (row + self.transpose) % self.rows
        self.duration[row][col] = 0
'''
# NUEVO PAD ENGINE 8.4 — Modelo correcto MODO: "Lluvia GeckoniChromatica"
'''
class PadEngine:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.transpose = 0
        self.mode = "music_chromo"

        # nota → {"col": int, "pos": float}
        self.active_notes = {}

        # matriz visual
        self.duration = [[0]*cols for _ in range(rows)]

        self.sweep_speed = 0.2  # velocidad vertical

    def note_on(self, note, col):
        self.active_notes[note] = {
            "col": col,
            "pos": 0.0   # arranca arriba
        }

    def note_off(self, note):
        if note in self.active_notes:
            col = self.active_notes[note]["col"]
            del self.active_notes[note]

            # limpiar columna
            for r in range(self.rows):
                self.duration[r][col] = 0

    def tick(self):
        # limpiar matriz primero
        for r in range(self.rows):
            for c in range(self.cols):
                self.duration[r][c] = 0

        # actualizar cada nota activa
        for data in self.active_notes.values():
            col = data["col"]
            pos = data["pos"]

            row = int(pos)

            if 0 <= row < self.rows:
                self.duration[row][col] = 1

            # avanzar barrido
            data["pos"] += self.sweep_speed

            # si llega abajo, vuelve arriba (cascada infinita)
            if data["pos"] >= self.rows:
                data["pos"] = 0
'''

# Pad Engine Geckonizado Geckonizador Geckonizante // El Pad Despierta [Wake up Pad!]
'''
class PadEngine:
    """
    Integración Geckonica del metodo viejo con el nuevo.
    Nota: Podrían y deberían sobrar funciones.
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.transpose = 0
        self.mode = "music_chromo"
        self.active_notes = {}  # note_name → col
        self.duration = [[0]*cols for _ in range(rows)]

    def note_on(self, note, col):
        self.active_notes[note] = col

    def note_off(self, note):
        if note in self.active_notes:
            col = self.active_notes[note]
            del self.active_notes[note]

            # limpiar columna
            for r in range(self.rows):
                self.duration[r][col] = 0

    def tick(self):
        # llamado por QTimer
        for note, col in self.active_notes.items():
            for r in range(self.rows):
                self.duration[r][col] += 1
    
    def trigger(self, row, col):
        row = (row + self.transpose) % self.rows
        self.duration[row][col] = 1

    def release(self, row, col):
        row = (row + self.transpose) % self.rows
        self.duration[row][col] = 0
'''
# Original FUncional hasta 8.2
''' 
class PadEngine:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.transpose = 0
        self.mode = "music_chromo"

        # duración activa por pad
        self.duration_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    def trigger(self, row, col):
        row = (row + self.transpose) % self.rows
        self.duration_matrix[row][col] = 1

    def release(self, row, col):
        row = (row + self.transpose) % self.rows
        self.duration_matrix[row][col] = 0
'''

# Otra Etapa del Proyecto que no deberia chocar con el Pad

# ---------------------------------------------------------------------------------
# (*) NOva Sequencer (Control Total del Flujo Secuencial Geckonista)
# ---------------------------------------------------------------------------------
class Sequencer:
    def __init__(self, pad_grid, step_interval=500):
        """
        pad_grid: instancia de PadGrid
        step_interval: milisegundos entre pasos
        """
        self.pad_grid = pad_grid
        self.num_rows = len(pad_grid.pads)
        self.num_cols = len(pad_grid.pads[0])
        self.current_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_step)
        
        # Estado de cada pad: None = vacío, "sound" = tiene sonido
        self.grid_state = [[None for _ in range(self.num_cols)] for _ in range(self.num_rows)]
    
    def assign_sound(self, row, col, sound_name="sound"):
        """Asigna un sonido al pad"""
        self.grid_state[row][col] = sound_name
        # Actualizamos color para indicar sonido asignado
        self.pad_grid.pads[row][col].setStyleSheet("background-color: lightgreen;")
    
    def clear_sound(self, row, col):
        """Remueve sonido del pad"""
        self.grid_state[row][col] = None
        self.pad_grid.pads[row][col].setStyleSheet("background-color: darkgray;")
    
    def start(self):
        """Arranca secuenciador"""
        self.timer.start(500)  # cada 500ms un paso
    
    def stop(self):
        self.timer.stop()
        # Reset de colores
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.grid_state[r][c]:
                    self.pad_grid.pads[r][c].setStyleSheet("background-color: lightgreen;")
                else:
                    self.pad_grid.pads[r][c].setStyleSheet("background-color: darkgray;")
        self.current_step = 0
    
    def play_step(self):
        """Enciende la columna actual y reproduce sonidos"""
        # Primero apagamos la columna anterior
        prev_step = self.current_step - 1 if self.current_step > 0 else self.num_cols - 1
        for r in range(self.num_rows):
            if self.grid_state[r][prev_step]:
                self.pad_grid.pads[r][prev_step].setStyleSheet("background-color: lightgreen;")
            else:
                self.pad_grid.pads[r][prev_step].setStyleSheet("background-color: darkgray;")
        
        # Ahora encendemos columna actual
        for r in range(self.num_rows):
            pad = self.pad_grid.pads[r][self.current_step]
            if self.grid_state[r][self.current_step]:
                pad.setStyleSheet("background-color: yellow;")  # en reproducción
                print(f"Reproduciendo sonido en pad fila {r} col {self.current_step}")
            else:
                pad.setStyleSheet("background-color: gray;")  # vacío
        # Avanzamos al siguiente paso
        self.current_step = (self.current_step + 1) % self.num_cols

# ---------------------------------------------------------------------------------
# () For Stand Alone In the GeckoMoog
# ---------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
    voices = 8
    piano = PiaNOS(voices)
    piano.show()
    sys.exit(app.exec_())

