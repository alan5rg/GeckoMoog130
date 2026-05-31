# 27/03/26 01:42pm Incorporar Otra Octava... Claro... jajaajaja
# 25/03/26 05:37pm Solucionadas inconsistencias entre .nos cargado, lo que muestran los diales 
#                  y lo que suena en version 6.9Ei2 
# 24/03/26 06:45pm El sonido en Vivo es otra cosa, el testing es adictivo...
#                  Transpositor 6.8Ei2 y el Live Sync son 100% efectivos ❥🦎
# 24/03/26 05:00pm Ei2 me esta ayudando con las actualizaciones de parametros en vivo,
#                  el SynthEngine aun mantiene algunas inconsistencias...
# 22/03/26 00:30am Finalmente se eliminan las canillas de audio stream del modulo,
#                  se crea una sola salida de audio en el host.
# 19/03/26 09:55am Se Ajustan tamaños de labels para evitar movimientos de texto,
#                  se Ajustan margenes de Layouts para MCV (Máxima Coherencia Visual).
'''
Agregar:
delay
chorus
reverb
segundo LFO
ring modulation
'''
import sys, os
import numpy as np
import sounddevice as sd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QDial, QSlider, QLabel, QPushButton, QGroupBox, QMessageBox
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QTextEdit, QButtonGroup
from PyQt5.QtCore import Qt, QRect

import qdarkstyle
from qdarkstyle import load_stylesheet, DarkPalette

from collections import deque
from copy import deepcopy
#for skipy... skepy... skeper es Keeper Geckonico, ese que guarda los .nos
import json
from datetime import datetime
#for dials paint on sensibility get power!!!
from PyQt5.QtGui import QPainter, QPen, QColor, QLinearGradient, QRadialGradient
import math

from PyQt5.QtCore import QTimer

# For debug/testing
#import inspect

geckoappversion = "9001"

import constants
from controls.precisiondial2 import PrecisionDial

NOTE_FREQ = constants.NOTE_FREQ

# ──────────────────────────────────────────────────────────────────────────
# --- INTERFAZ GRÁFICA (LOS TODOS LOS CONTROLES FÍSICOS) ---
# ──────────────────────────────────────────────────────────────────────────
# class SynthWindow(QMainWindow): #deprecated to use like widget on Pia NOva Synth
class SynthPanel(QWidget):
    def __init__(self, engine, voice_manager):
        super().__init__()
        self.engine = engine
        self.voice_manager = voice_manager
        self.synthengine_version = geckoappversion
        self.setWindowTitle(f"Synth V{geckoappversion} • Aether Core")
        #self.setGeometry(200, 100, 380, 480)  # un poco más ancho y alto

        # Variables de Inicialización de estado
        self.de_tunez = "none"
        self.engine.waveform = "sine"
        
        # para usar con metodo on_parameter_changed
        self.current_preset_name = ""
        self.actual_preset_loaded = {}
        self.instrument_modified = False
        self.ui_update_in_progress = False

        # ── Envelope Filter Panel ─────────────────────────────────────
        self.envelope_filter_panel = EnvelopeFilterPanel(self.engine)

        # Factores de corrección para que todas suenen aproximadamente al mismo loudness que sine
        # Estos valores son relativos al RMS percibido de cada onda (aproximados por oído y mediciones rápidas)
        self.correction_factors = {
            'sine':     1.00,     # referencia (sin corrección)
            'triangle': 1.20,   # un poco más bajo que sine → boost
            'saw':      0.60,   # más energía en armónicos → bajar
            'square':   0.45    # la más energética → bajar bastante
        }
        
        # Estilo más refinado y selectivo (con mejoras en diseño de Waveform Select Buttons)
        # No aplica a Diales 
        self.setStyleSheet(self.styleSheet() + """
            QTextEdit {
                background-color: black;
                color: #0f8;
                font: 10pt Consolas;
                font-weight: bold;
                /*font-size: 12px;*/
            }                           
            QLabel {
                color: #ccc;
                font-weight: normal;
            }
            QPushButton {
                background-color: #19232d;
                color: #0f8;
                border: 2px solid #00ffaa;
                border-radius: 13px;
                font-size: 11px;
                font-weight: bold
            }
            QPushButton:hover {
                background-color: #454545;
                color: #0f8;
                border: 1px solid #0f8;
            }
            QPushButton:checked {
                background-color: #00ffaa;
                color: #000;
                border: 2px solid #0f8;
            }
            QPushButton:pressed {
                background-color: #00ffaa;
                color: #000;
                border: 2px solid #0f8;
            }
            QDial {
                background-color: #222;
                color: #0f8;
            }
            QDial::groove {
                border: 1px solid #444;
                border-radius: 40px;
            }
            QDial::handle {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.7, fx:0.5, fy:0.5,
                                            stop:0 #0f8, stop:1 #084);
                width: 18px;
                height: 18px;
                border: 2px solid #0f8;
                border-radius: 9px;
            }
            QGroupBox {
                font: 10pt Consolas;
                font-weight: normal;
                border-radius: 5px;
                margin-top: 5px;
            }
            QGroupBox::title {
                font: bold 12pt Consolas;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding-left: 6px;
                color: #0f8;
            }                           
        """)
        
        self.initUI()
        #self.pintar_diales() # evaluar por choque con aplicaion de estilos

        # Testing Chung
        #chunk = self.voice_manager.get_audio_chunk(512)
        #print(chunk.shape)
    
    '''
    def pintar_diales(self):
        self.dial_freq.setStyleSheet("color: #00ff8c; background: #00ff8c")
        self.dial_vol.setStyleSheet("color: #f25056; background: #f25056")
    '''

    def initUI(self):
        #central = QWidget()
        #self.setCentralWidget(central)
        #main_layout = QVBoxLayout(central)
        
        main_layout = QVBoxLayout(self)
        #main_layout.setSpacing(10)
        #main_layout.setContentsMargins(10, 10, 10, 10)
        
        # ──────────────────────────────────────────────
        # ── Oscillator + Master Volume Section ────────
        # ──────────────────────────────────────────────
        # --- Oscillator ---
        osc_group = QGroupBox("Oscillator (Freq. + Volume) ◆")
        osc_layout = QVBoxLayout()
        #osc_layout.setSpacing(10)
        self.lbl_freq = QLabel(f"Frecuencia: {self.engine.frequency:.0f} Hz")
        self.lbl_freq.setFixedWidth(130)
        self.dial_freq = PrecisionDial()
        #self.dial_freq.setStyleSheet("color: #00ff8c; background: #00ff8c")
        self.dial_freq.setFixedSize(60, 60)
        self.dial_freq.setRange(50, 2200)
        self.dial_freq.setValue(int(self.engine.frequency))
        #self.dial_freq.setNotchesVisible(True)
        self.dial_freq.valueChanged.connect(lambda v: self.update_global_param("frequency", float(v)))
        osc_layout.addWidget(self.lbl_freq, alignment=Qt.AlignCenter)
        osc_layout.addWidget(self.dial_freq, alignment=Qt.AlignCenter)

        # --- Master Volume ---
        vol_layout = QVBoxLayout()
        self.lbl_vol = QLabel(f"Volume: {int(self.engine.amplitude * 100)}%")
        self.lbl_vol.setFixedWidth(100)
        self.dial_vol = PrecisionDial()
        #self.dial_vol.setStyleSheet("color: #f25056; background: #f25056")
        self.dial_vol.setFixedSize(60, 60)
        self.dial_vol.setRange(0, 100)
        self.dial_vol.setValue(int(self.engine.amplitude * 100))
        #self.dial_vol.setNotchesVisible(True)
        self.dial_vol.valueChanged.connect(lambda v: self.update_global_param("amplitude", v / 100.0))
        vol_layout.addWidget(self.lbl_vol, alignment=Qt.AlignCenter)


        # Label para volumen efectivo
        self.lbl_effective_vol = QLabel(f"Efectivo: {(int(self.engine.amplitude * 100))}%")

        self.lbl_effective_vol.setStyleSheet("color: #88ff88; font-size: 12px;")
        self.lbl_effective_vol.setFixedWidth(100)
        vol_layout.addWidget(self.lbl_effective_vol, alignment=Qt.AlignCenter)
        vol_layout.addWidget(self.dial_vol, alignment=Qt.AlignCenter)
        
        osc_vol_layout = QHBoxLayout()
        osc_vol_layout.setContentsMargins(0, 5, 0, 5)
        osc_vol_layout.addLayout(osc_layout)
        osc_vol_layout.addLayout(vol_layout)

        # ─────────────────────────────────────────────────────
        # ── Waveform Select Buttons (en horizontal) ──────────
        # ─────────────────────────────────────────────────────
        wave_btn_group = QGroupBox("Waveform Select Buttons ∿")
        wave_btn_layout = QHBoxLayout()
        wave_btn_layout.setContentsMargins(0, 10, 0, 5)

        self.btn_test = QPushButton("▶ [Test]")
        self.btn_test.setFixedSize(73, 30)
        self.btn_test.pressed.connect(self.trigger_test)
        self.btn_test.released.connect(self.release_test)
        wave_btn_layout.addWidget(self.btn_test, alignment=Qt.AlignCenter)

        self.btn_sine   = QPushButton("∿  [SIN]");   self.btn_sine.clicked.connect(lambda: self.set_wave('sine'))
        self.btn_square = QPushButton("⊓  [SQR]"); self.btn_square.clicked.connect(lambda: self.set_wave('square'))
        self.btn_saw    = QPushButton("⩘  [SAW]");    self.btn_saw.clicked.connect(lambda: self.set_wave('saw'))
        self.btn_tri    = QPushButton("△  [TRI]"); self.btn_tri.clicked.connect(lambda: self.set_wave('triangle'))
        self.wave_buttons = {}
        wave_group = QButtonGroup(self)
        wave_group.setExclusive(True)

        wave_buttons = {
            "sine": (self.btn_sine),
            "square": (self.btn_square),
            "saw": (self.btn_saw),
            "triangle": (self.btn_tri)
        }
        for mode, (btn) in wave_buttons.items():
            self.wave_buttons[mode] = btn

        for btn in [self.btn_sine, self.btn_square, self.btn_saw, self.btn_tri]:
            wave_btn_layout.addWidget(btn, alignment=Qt.AlignBottom)
            btn.setFixedSize(100, 30)
            btn.setStyleSheet("font-size:11px; font-weight:bold; border-radius: 13px")
            btn.setCheckable(True)
            wave_group.addButton(btn)
        
        self.btn_sine.setChecked(True) # Inicia en modo sine
        
        wave_btn_group.setLayout(wave_btn_layout)

        osc_group.setLayout(osc_vol_layout)

        # ──────────────────────────────
        # ── LFO Section ───────────────
        # ──────────────────────────────
        lfo_group = QGroupBox("LFO (Tremolo)")
        lfo_layout = QHBoxLayout()
        lfo_layout.setContentsMargins(5, 5, 5, 5)

        # Rate
        lfo_rate_col = QVBoxLayout()
        self.lbl_lfo_rate = QLabel("Rate: 5.0 Hz")
        self.lbl_lfo_rate.setFixedWidth(100)
        self.dial_lfo_rate = PrecisionDial()
        self.dial_lfo_rate.setFixedSize(55, 55)
        self.dial_lfo_rate.setRange(0, 200)          # 0 → 0.1 Hz, 200 → 20 Hz (escala no lineal después)
        self.dial_lfo_rate.setValue(50)              # ~5 Hz
        #self.dial_lfo_rate.setNotchesVisible(True)
        # Rate (usa el método sync_lfo_rate que definimos antes por la curva logarítmica)
        self.dial_lfo_rate.valueChanged.connect(self.sync_lfo_rate)
        lfo_rate_col.addWidget(self.lbl_lfo_rate, alignment=Qt.AlignCenter)
        lfo_rate_col.addWidget(self.dial_lfo_rate, alignment=Qt.AlignCenter)

        # Depth
        lfo_depth_col = QVBoxLayout()
        self.lbl_lfo_depth = QLabel("Depth: 0%")
        self.lbl_lfo_depth.setFixedWidth(90)
        self.dial_lfo_depth = PrecisionDial()
        self.dial_lfo_depth.setFixedSize(55, 55)
        self.dial_lfo_depth.setRange(0, 100)
        self.dial_lfo_depth.setValue(0)
        #self.dial_lfo_depth.setNotchesVisible(True)
        # Depth
        self.dial_lfo_depth.valueChanged.connect(lambda v: self.update_global_param("lfo_depth", v / 100.0))
        lfo_depth_col.addWidget(self.lbl_lfo_depth, alignment=Qt.AlignCenter)
        lfo_depth_col.addWidget(self.dial_lfo_depth, alignment=Qt.AlignCenter)

        lfo_layout.addLayout(lfo_rate_col)
        lfo_layout.addLayout(lfo_depth_col)
        lfo_group.setLayout(lfo_layout)
        
        # ──────────────────────────────
        # ── Detune Section ────────────
        # ──────────────────────────────
        detune_ctrl_group = QGroupBox("De Tunez con Amor by DulceKAli ❥")
        detune_layout = QHBoxLayout()
        detune_layout.setContentsMargins(5, 5, 5, 5)
        
        # Dial Amount by Aetheris
        detune_controls = QVBoxLayout()
        #detune_controls.setContentsMargins(0, 0, 0, 0)
        self.lbl_detune_amount = QLabel("Amount: 100%")
        self.lbl_detune_amount.setFixedWidth(95)
        self.dial_detune_amount = PrecisionDial()
        self.dial_detune_amount.setRange(0, 200)          # 0–200% para poder exagerar
        self.dial_detune_amount.setValue(100)             # default full effect
        #self.dial_detune_amount.setNotchesVisible(True)
        self.dial_detune_amount.setFixedSize(50, 50)
        self.dial_detune_amount.valueChanged.connect(lambda v: self.update_global_param("detune_amount", v / 100.0))
        detune_controls.addWidget(self.lbl_detune_amount, alignment=Qt.AlignCenter)
        detune_controls.addWidget(self.dial_detune_amount, alignment=Qt.AlignCenter)
        detune_layout.addLayout(detune_controls)

        self.detune_buttons = {}  # ❤️ guardamos los botones en este contenedor hermoso, amoroso y dulzoso

        # Definimos botones con colorcitos y tooltip de cariño
        detune_buttons = {
            "sutil": ("∿ GSUTIL", "#FFB6C1", "Suavito ♥, acaricia tus oídos 🌸"),
            "clasic": ("◆ CLASIC", "#ADD8E6", "Clásico ♡ pero con estilo 💎"),
            "supersaw": ("⩘ SPRSAW", "#FFA500", "Explosión supersónica 🚀"),
            "caos": ("⚡ GCHAOS", "#FF4500", "⚡ Para desatar el caos dulce 😈"),
            "simetric": ("△ ZMTRIC", "#61E661", "△ Equilibrio perfecto 🌿")
        }
        detune_group = QButtonGroup(self)
        detune_group.setExclusive(True)
        for mode, (name, color, tooltip) in detune_buttons.items():
            btn = QPushButton(name)
            btn.setCheckable(True)
            if mode == "sutil":     # para iniciar por defecto en sutil
                btn.setChecked(True)
            btn.setFixedSize(80, 30)  # más cómodo para la mano y el corazón
            #btn.setStyleSheet(f"background-color: {color}; font-weight: bold; border-radius: 8px;")
            btn.setStyleSheet("font-size:11px; font-weight:bold; border-radius: 13px")
            btn.setToolTip(tooltip)
            detune_layout.addWidget(btn, alignment=Qt.AlignCenter)
            # Guardamos el botón con el nombre del modo, así tu función sigue funcionando
            self.detune_buttons[mode] = btn
            # Conectamos cada botón con su función
            btn.clicked.connect(lambda checked, n=mode: self.set_detune(n))
            detune_group.addButton(btn)

        detune_ctrl_group.setLayout(detune_layout)

        # ── Ajuste de Diseño 07.03.2026 for more control's─────────────────────────────────────
        self.Brand = QLabel(f"Aetheris SynthEngine {self.synthengine_version} for Pia NOva") # old color[ color: #00ff9d; ]
        self.Brand.setStyleSheet("""
            font-size: 20px;
            color: #00ffaa;
            font-weight: bold
        """)
        
        main_layout.addWidget(self.Brand, alignment=Qt.AlignRight)
        #main_layout.addStretch()
        main_layout.addWidget(detune_ctrl_group)
        main_layout.addWidget(lfo_group)
        main_layout.addWidget(self.envelope_filter_panel)
        main_layout.addWidget(osc_group)
        main_layout.addWidget(wave_btn_group)
       
        
        # ──────────────────────────────
        # ── Presets Controls ──────────
        # ──────────────────────────────
        '''
        Rediseñar o exportar este bloque para nuevas features mas adelante:
         - Un campo desplegable con lista de instrumentos disponibles en un directorio
         - Carga directa desde la lista con boton secundario o un modo fast change con solo dar click
         - Mejorar info del instrumento, crear una suerte de display que muestre metadata (fondo engro letras verdes)
         - Hacer que al modificar algun parametro del instrumento la interfaz lo indique (por ejemplo cambiando
           el color de la letra a rojo) y/o con un "(!) Warning Instrument was Mofified"
           ya creamos metodos para eso, evaluarlos.
        '''
        preset_controls_group = QGroupBox ("Keeper Pia NOva Sound Presets Instruments")
        preset_controls = QHBoxLayout()
        preset_controls.setContentsMargins(5, 10, 5, 7)
        preset_controls_group.setLayout(preset_controls)
        nos_keeper = QVBoxLayout() 
        
        # Load Sound NOva .nos
        self.btn_load_preset = QPushButton("Cargar Pia NOva Sound")
        self.btn_load_preset.setToolTip("Carga los Ajustes de un Instrumento .nos y los aplica a los Ajustes Actuales 🌟")
        self.btn_load_preset.setFixedSize(175, 30) 
        self.btn_load_preset.clicked.connect(self.load_preset_dialog)
        self.btn_load_preset.setStyleSheet("border-radius: 13px")
        nos_keeper.addWidget(self.btn_load_preset, alignment=Qt.AlignCenter)
        # Toggle Preview al cargar
        self.btn_preview_on_load = QPushButton("❥ NOs Preview ON")
        self.btn_preview_on_load.setCheckable(True)
        self.btn_preview_on_load.setChecked(True)  # ON por default (para probar)
        self.btn_preview_on_load.setFixedSize(175, 30)
        self.btn_preview_on_load.setToolTip("Activa/Desactiva la melodía de bienvenida al cargar un preset 🌟")
        self.btn_preview_on_load.clicked.connect(self.toggle_preview_on_load)
        self.btn_preview_on_load.setStyleSheet("border-radius: 13px")
        nos_keeper.addWidget(self.btn_preview_on_load, alignment=Qt.AlignCenter)
        # Save Sound NOva .nos
        self.btn_save_preset = QPushButton("Guardar Pia NOva Sound")
        self.btn_save_preset.setToolTip("Toma un SnapShoot de los Ajustes Actuales y los Guarda como Instrumento .nos ❥")
        self.btn_save_preset.setFixedSize(175, 30) 
        self.btn_save_preset.clicked.connect(self.save_current_preset)
        nos_keeper.addWidget(self.btn_save_preset, alignment=Qt.AlignCenter)

        preset_controls.addLayout(nos_keeper)

        self.lbl_preset_status = QTextEdit("Config: Manual (sin preset)")
        self.lbl_preset_status.setReadOnly(True)
        self.lbl_preset_status.setFixedWidth(300)
        self.lbl_preset_status.setFixedHeight(150)
        
        preset_controls.addWidget(self.lbl_preset_status, alignment=Qt.AlignCenter)

        main_layout.addWidget(preset_controls_group)
    
    # -------------- BLOQUE PARA EVALUAR CAMBIOS DE DIALES Y BOTONES ----------------------

    # --- Ei2 Vision Game Change !!!
   
    def update_global_param(self, name, final_value):
        """
        Actualiza SOLO el molde del motor (como hacían tus métodos originales).
        Esto garantiza polifonía total sin interferencias en notas activas.
        """
        if self.ui_update_in_progress: return

        # El Purificador Geckónico
        if name == "attack_time":
            final_value = round(final_value, 3)
        elif name in ["cutoff", "resonance"]:
            final_value = int(final_value)
        elif name == "frequency":
            final_value = round(final_value, 2) # Suficiente para afinación perfecta            
        else:
            # Amplitude, LFO depth, etc.
            final_value = round(final_value, 2)

        # 1. Actualizar el Molde (Engine)
        if name == "frequency":
            # Calculamos cuánto cambió la frecuencia respecto al valor anterior
            # Usamos un ratio para que el corrimiento sea armónico (proporcional)
            old_freq = self.engine.frequency if self.engine.frequency > 0 else final_value
            ratio = final_value / old_freq
            self.engine.frequency = final_value
            self.lbl_freq.setText(f"Master Osc: {int(final_value)} Hz")

            # 2. EL TRANSPOSITOR V.6.7Ei2 (Live Tracking)
            if hasattr(self, 'voice_manager'):
                for voice in self.voice_manager.voice_pool:
                    if voice.adsr_stage != 'off':
                        # Corrimiento armónico: la voz sigue al oscilador base
                        voice.frequency *= ratio 
                        # Si tu voz tiene un método para actualizar fase, lo llamamos:
                        if hasattr(voice, 'update_pitch'): 
                            voice.update_pitch()

        elif name == "amplitude":
            self.engine.amplitude = final_value
            self.lbl_vol.setText(f"Volume: {int(final_value * 100)}%")
            correction = getattr(self, 'correction_factors', {}).get(self.engine.waveform, 1.0)
            self.lbl_effective_vol.setText(f"Efectivo: {int(final_value * correction * 100)}%")
            
            # Update en vivo del volumen (Broadcast quirúrgico)
            self.voice_manager.broadcast_parameter("amplitude", final_value)
        
        #elif name == "frequency":
        #    self.engine.frequency = final_value
        #    self.lbl_freq.setText(f"Frecuencia: {int(final_value)} Hz")
            
        elif name == "lfo_freq":
            self.engine.lfo_freq = final_value
            self.lbl_lfo_rate.setText(f"Rate: {final_value:.2f} Hz")
        
        elif name == "lfo_depth":
            self.engine.lfo_depth = final_value
            self.lbl_lfo_depth.setText(f"Depth: {int(final_value * 100)}%")
            
        # --- CASOS PARA ADSR Y FILTRO (Lo que faltaba para el Keeper) ---
        elif name in ["attack_time", "decay_time", "sustain_level", "release_time", "cutoff", "resonance", "lfo_depth"]:
            setattr(self.engine, name, final_value)
        
        elif name == "detune_amount":
            # El detune amount sí suele ser global para el VoiceManager
            self.voice_manager.detune_amount = final_value
            self.lbl_detune_amount.setText(f"Amount: {int(final_value * 100)}%")

        # 2. EL TRUCO DEL CARTUCHO: Sincronizar voces vivas
        '''
        if hasattr(self, 'voice_manager'):
            for voice in self.voice_manager.voice_pool:
                # Solo actualizamos si la voz está haciendo algo (no idle)
                if voice.adsr_stage != 'off': 
                    # Mapeo de parámetros en tiempo real
                    if name == "amplitude": voice.amplitude = final_value
                    elif name == "lfo_depth": voice.lfo_depth = final_value
                    elif name == "lfo_freq": voice.lfo_freq = final_value
                    elif name == "attack_time": voice.attack_time = final_value
                    elif name == "decay_time": voice.decay_time = final_value
                    elif name == "sustain_level": voice.sustain_level = final_value
                    elif name == "release_time": voice.release_time = final_value
                    elif name == "cutoff": voice.cutoff = final_value
                    elif name == "resonance": voice.resonance = final_value
                    elif name == "waveform": voice.waveform = final_value
                    # ¡IMPORTANTE!: No tocamos voice.frequency para mantener la polifonía
        '''
        # Reformateado Sumamente Eficiente por Ei2
        if hasattr(self, 'voice_manager'):
            for voice in self.voice_manager.voice_pool:
                if voice.adsr_stage != 'off':
                    # Evitamos tocar frequency para no romper la polifonía
                    if name != "frequency" and hasattr(voice, name):
                        setattr(voice, name, final_value)


        # 3. Notificar que el instrumento cambió para el (!) del preset
        self.on_parameter_changed(name, final_value)
  
    def sync_lfo_rate(self, v):
        """ 
            Maneja el Rate del LFO sin interferir con las voces vivas, 
            y con poda de decimales inútiles...
        """
        if self.ui_update_in_progress: return
        
        rate_raw = v / 200.0
        rate = 0.1 + (rate_raw ** 2) * 19.9
        
        # --- EL FILTRO DE REALIDAD ---
        # Redondeamos a 2 decimales. Suficiente para el oído, sano para el procesador.
        rate = round(rate, 2)

        self.engine.lfo_freq = rate
        self.lbl_lfo_rate.setText(f"Rate: {rate:.2f} Hz")

        # Mandamos al flujo global para que actualice voces vivas
        self.on_parameter_changed("lfo_freq", rate)

    # --- para implementar mensaje al cambiar seteo de instrumento y que este no se halla guardado ----

    def on_parameter_changed(self, param_name, value):
        if self.ui_update_in_progress: return

        # Chequeamos si realmente hubo un cambio respecto al preset original
        was_modified = self.instrument_modified
        is_now_different = not self.is_current_state_matching_preset()
        
        # Solo actualizamos el display si cambió el estado de "modificado"
        if was_modified != is_now_different:
            self.instrument_modified = is_now_different
            self.update_preset_display()

    def update_preset_display(self):
        """
        Si está modificado: Rojo + Advertencia.
        Si coincide con el original: Verde + Metadata completa del .nos.
        """
        if self.instrument_modified:
            self.show_modified_warning()
        else:
            # Si volvemos al estado original, recuperamos la metadata del preset cargado
            if hasattr(self, 'actual_preset_loaded') and self.actual_preset_loaded:
                text = self.get_formatted_display_text(self.actual_preset_loaded)
                color = "#0f8" # El verde neón que elegiste
            else:
                # Caso por defecto si no hay nada cargado aún
                text = self.current_preset_name
                color = "#0f8"
            
            self.lbl_preset_status.setText(text)
            self.lbl_preset_status.setStyleSheet(f"""
                background-color: black;
                color: {color};
                font: 10pt Consolas;
                font-weight: bold;
                """)

    def show_modified_warning(self):
        # Mensaje poético como pediste
        warning_msg = (
            f"「{self.current_preset_name}」fue modificado.\n"
            "Recuerde guardar esta estrella musical si quiere volver a encontrarla en el firmamento."
        )
        self.lbl_preset_status.setText(warning_msg)
        self.lbl_preset_status.setStyleSheet("color: red;")

    def is_current_state_matching_preset(self):
        """
        Compara los parámetros actuales contra el preset cargado.
        Si son idénticos, la estrella no está modificada.
        """
        if not hasattr(self, 'actual_preset_loaded'): return True
        
        saved_params = self.actual_preset_loaded.get("parameters", {})
        
        # Diccionario de equivalencias entre Engine y el Preset
        # Agregamos solo los que afectan la "identidad" del sonido
        current_state = {
            "waveform": self.engine.waveform,
            "lfo_freq": self.engine.lfo_freq,
            "lfo_depth": self.engine.lfo_depth,
            "attack_time": self.engine.attack_time,
            "decay_time": self.engine.decay_time,
            "sustain_level": self.engine.sustain_level,
            "release_time": self.engine.release_time,
            "cutoff": self.engine.cutoff,
            "resonance": self.engine.resonance,
            #"amplitude": self.engine.amplitude,
            "detune_amount": self.voice_manager.detune_amount
            # detune_mode se maneja aparte o se puede sumar aquí
        }

        # Comparamos con tolerancia pequeña para floats
        for key, saved_val in saved_params.items():
            if key in current_state:
                curr_val = current_state[key]
                if isinstance(curr_val, float):
                    if abs(curr_val - saved_val) > 0.001: return False
                else:
                    if curr_val != saved_val: return False
        return True

    def get_formatted_display_text(self, preset_dict):
        """
        Genera el bloque de texto con el formato de metadata detallado.
        """
        name    = preset_dict.get("name", "Sin nombre")
        author  = preset_dict.get("author", "Desconocido")
        version = preset_dict.get("version", "Desconocida")
        
        created_raw = preset_dict.get("created", "")
        try:
            from datetime import datetime
            created = datetime.fromisoformat(created_raw).strftime("%Y-%m-%d %H:%M")
        except:
            created = created_raw
            
        tags = ", ".join(preset_dict.get("tags", []))

        return f"""Preset: {name}
    
    Autor: {author}
    Versión Engine: {version}

Creado: {created}
Tags: {tags if tags else "—"}
        """

    # -------------- BLOQUE PARA EVALUAR CAMBIOS DE DIALES Y BOTONES ----------------------
    # --- HAY QUE UNIFICAR LOS UPDATES EN UN METODO, CUALQUIER CAMBIO DEBE:
    # --- *) LLAMARLO Y ACTUALIZAR EL MODTOR COMPLETO DE SONIDO EN TIEMPO REAL!!!
    # --- *) PERMITIR QUE LOS CAMBIOS SEAN ENVIADOS AL MOTOR DE AUDIO EN VIVO!!!
    # --- *) ESTO DEBE PASAR AL EJECUTAR NOTAS DESDE LA OCTAVA O AL PRESIONAR EL BOTON DE TEST
    # --- *) SOLO QUEDA IMPLEMENTARLO CON LOS BOTONES EXCLUSIVOS DE DETUNE Y WAVEFORM
    
    def set_frequency(self, freq):
        self.engine.frequency = freq
        self.dial_freq.setValue(int(freq))
        self.lbl_freq.setText(f"Frecuencia: {freq:.0f} Hz")

    def set_wave(self, wave_type):
        #print("SET WAVE LLAMADO:", wave_type)
        #print("SET WAVE caller:", inspect.stack()[1].function)
        if not self.ui_update_in_progress and self.engine.waveform == wave_type:
            return
        
        self.engine.waveform = wave_type
        # testing/debug
        #print("Waveform Selected: ", wave_type)
        
        # Valor base deseado (lo que el usuario marcó en el dial de volumen)
        base_amplitude = self.dial_vol.value() / 100.0
        
        # Aplicamos el factor de corrección SOLO para la waveform actual
        correction = self.correction_factors.get(wave_type, 1.0)
        corrected_amplitude = base_amplitude * correction
        
        # Limitamos para no irnos a extremos raros
        corrected_amplitude = max(0.01, min(0.8, corrected_amplitude))  # headroom para evitar clip global
        
        # Aplicamos al engine
        self.engine.amplitude = corrected_amplitude
        
        # ¡Importante! NO tocamos el dial ni el label del volumen
        # El knob sigue mostrando el "volumen deseado para sine"
        #self.lbl_vol.setText(f"Master Volume: {self.dial_vol.value()}%")  # opcional: mantenerlo fijo
        # O si querés mostrar el volumen efectivo real:
        #self.lbl_vol.setText(f"Vol. efectivo: {int(corrected_amplitude * 100)}% (base {self.dial_vol.value()}%)")
        # Knob muestra volumen efectivo real // ojo se baja el volumen al cambiar de waveform
        #self.dial_vol.setValue(int(corrected_amplitude * 100))
        
        # Actualizamos el label principal (muestra el deseado)
        self.lbl_vol.setText(f"Master Vol: {self.dial_vol.value()}%")

        # Opción B: Label separado (más claro) → agregalo en initUI
        self.lbl_effective_vol.setText(f"Efectivo: {int(corrected_amplitude * 100)}%")
        
        # Resaltar el botón activo
        #self.wave_buttons[wave_type].setChecked(True)
        
        for btn, wt in [(self.btn_sine, 'sine'), (self.btn_square, 'square'),
                        (self.btn_saw, 'saw'), (self.btn_tri, 'triangle')]:
            #btn.setDown(wt == wave_type)
            btn.setChecked(wt == wave_type)
            btn.setEnabled(wt != wave_type)
        
    def set_detune(self, mode):
        #print("SET DETUNE LLAMADO:", mode)
        #print("SET DETUNE caller:", inspect.stack()[1].function)
        #print ("debuger de_tunez en voice_manager: ",self.voice_manager.de_tunez)
        #print ("debuger mode: ", mode)
        if not self.ui_update_in_progress and self.voice_manager.de_tunez == mode:
            return
        # Como tengo un metodo, voy a usarlo carajo y listo!
        self.voice_manager.set_detune(mode)
        # Resaltar el botón activo
        #self.detune_buttons[mode].setChecked(True)
        #for m, btn in self.detune_buttons.items():
        #    btn.setChecked(m == mode)
        for m, btn in self.detune_buttons.items():
            btn.setChecked(m == mode)
            btn.setEnabled(m != mode)   # el activo se deshabilita

    def save_current_preset_old(self):
        preset = KeeperOfInstruments.capture(self.engine, self.voice_manager, self)
        name, ok = QInputDialog.getText(self, "Guardar SnapShoot de los Ajustes Actuales", "Nombre de la estrella sonora:")
        if ok and name:
            preset["name"] = name
            KeeperOfInstruments.save(preset)
            self.lbl_preset_status.setText(f"Preset: {name}")

    # New Save Dialog by Aetheris 10/03/26 14:50
    def save_current_preset(self):
        """
        Abre cuadro de dialogo para guardar en archivo .nos
        las configuraciones de los diales
        usa KeeperOfInstruments
        """
        preset = KeeperOfInstruments.capture(self.engine, self.voice_manager, self)
        
        # Diálogo para elegir nombre/archivo (default en presets/, extensión .nos)
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Instrumento Pia NOva (Preset Cósmicos NOva Synh)",
            os.path.join(KeeperOfInstruments.PRESETS_DIR, "NuevaEstrella.nos"),
            "Presets (*.nos);;Todos los archivos (*)"
        )
        
        if not path:
            return  # canceló
        
        # Nombre del preset = nombre del archivo sin .nos
        name = os.path.basename(path).replace(".nos", "")
        preset["name"] = name
        
        # Guardamos con el filename elegido
        KeeperOfInstruments.save(preset, os.path.basename(path))
        
        # Actualizamos status
        if hasattr(self, 'lbl_preset_status'):
            self.lbl_preset_status.setText(f"Preset: {name}")
        
        # Mensajito opcional
        QMessageBox.information(self, "Guardado", f"¡{name} guardado como estrella sonora en el cosmos! ❥")

    def load_preset_dialog(self):
        """
        Abre cuadro de dialogo para cargar archivo .nos
        Llama a actualizar diales con los presets cargados del .nos
        usa KeeperOfInstruments
        """
        from PyQt5.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self, "Cargar Ajustes de Instrumento", KeeperOfInstruments.PRESETS_DIR, "Presets (*.nos)")
        if path:
            preset = KeeperOfInstruments.load(path, self.engine, self.voice_manager, self) 
            #if not preset:
            #   return
            #resto en esta linea... misma logica
            if preset:
                self.ui_update_in_progress = True
                try:
                    self.update_ui_from_preset(preset)  # Llamada a ajustar diales con los presets
                    # by Ei2
                    self.current_preset_name = preset.get("name", "Estrella")
                    self.instrument_modified = False # Reset al cargar
                finally:
                    self.ui_update_in_progress = False
                
                self.actual_preset_loaded = preset.copy() #copia los presets cargados como referencia

                # Testing/Debug
                #print("Actual Preset Cargado:", self.actual_preset_loaded)
                '''
                # --- DEBUG CRUDO DE ESTADO CARGADO (Sin filtros ni redondeos) ---
                print("\n" + "!"*30)
                print("🔍 INSPECCIÓN DE self.actual_preset_loaded")
                print("!"*30)
                if hasattr(self, 'actual_preset_loaded') and self.actual_preset_loaded:
                    print(json.dumps(self.actual_preset_loaded, indent=4, ensure_ascii=False))
                else:
                    print("⚠️  self.actual_preset_loaded está VACÍO o no existe.")
                print("!"*30 + "\n")
                '''
                # --- DEBUG GECKÓNICO (Sin dependencias, sin vueltas) ---
                print(f"\n🛸 [DEBUG] {self.current_preset_name} EN MEMORIA:")
                for k, v in self.actual_preset_loaded.get('parameters', {}).items():
                    print(f"  {k:<15} -> {v}")
                print("─────────────────────────────────────────\n")
                
    def update_ui_from_preset(self, preset_dict):
        """
        Carga un preset y mueve SOLO los diales y labels de la UI.
        El engine se actualiza automáticamente por las conexiones de signals.
        """
        params = preset_dict.get("parameters", {})

        # Desconectamos temporalmente las señales para evitar loops infinitos
        self.dial_lfo_rate.blockSignals(True)
        self.dial_lfo_depth.blockSignals(True)
        self.envelope_filter_panel.dial_attack.blockSignals(True)
        self.envelope_filter_panel.dial_decay.blockSignals(True)
        self.envelope_filter_panel.dial_sustain.blockSignals(True)
        self.envelope_filter_panel.dial_release.blockSignals(True)
        self.envelope_filter_panel.dial_cutoff.blockSignals(True)
        self.envelope_filter_panel.dial_resonance.blockSignals(True)
        self.dial_vol.blockSignals(True)
        self.dial_detune_amount.blockSignals(True)

        try:
            # Waveform
            waveform = params.get("waveform", "sine")
            self.set_wave(waveform)

            # LFO
            lfo_freq = params.get("lfo_freq", 5.0)
            inner_val = (lfo_freq - 0.1) / 19.9
            rate_raw = math.sqrt(max(0, inner_val)) # max(0) por seguridad de punto flotante

            # 2. Mapeamos al rango del Dial (0-200)
            dial_v = int(rate_raw * 200)
            self.dial_lfo_rate.setValue(dial_v)
            self.lbl_lfo_rate.setText(f"Rate: {lfo_freq:.2f} Hz")

            self.dial_lfo_depth.setValue(int(params.get("lfo_depth", 0.0) * 100))
            self.lbl_lfo_depth.setText(f"Depth: {int(params.get('lfo_depth', 0.0) * 100)}%")

            # ADSR + Filter
            self.envelope_filter_panel.dial_attack.setValue(int(params.get("attack_time", 0.005) * 1000))
            self.envelope_filter_panel.dial_decay.setValue(int(params.get("decay_time", 0.3) * 1000))
            self.envelope_filter_panel.dial_sustain.setValue(int(params.get("sustain_level", 0.7) * 100))
            self.envelope_filter_panel.dial_release.setValue(int(params.get("release_time", 0.8) * 1000))
            self.envelope_filter_panel.dial_cutoff.setValue(int(params.get("cutoff", 8000.0)))
            self.envelope_filter_panel.dial_resonance.setValue(int(params.get("resonance", 1.0) * 10))

            self.envelope_filter_panel.lbl_attack.setText(f"Attack: {self.envelope_filter_panel.dial_attack.value()} ms")
            self.envelope_filter_panel.lbl_decay.setText(f"Decay: {self.envelope_filter_panel.dial_decay.value()} ms")
            self.envelope_filter_panel.lbl_sustain.setText(f"Sustain: {self.envelope_filter_panel.dial_sustain.value()}%")
            self.envelope_filter_panel.lbl_release.setText(f"Release: {self.envelope_filter_panel.dial_release.value()} ms")
            self.envelope_filter_panel.lbl_cutoff.setText(f"Cutoff: {self.envelope_filter_panel.dial_cutoff.value()} Hz")
            self.envelope_filter_panel.lbl_resonance.setText(f"Res: {self.envelope_filter_panel.dial_resonance.value() / 10.0:.1f}")

            # Volumen
            amp = params.get("amplitude", 0.3)
            self.dial_vol.setValue(int(amp * 100))
            self.lbl_vol.setText(f"Volume: {self.dial_vol.value()}%")

            # Detune
            detune_mode = params.get("detune_mode", "none")
            self.set_detune(detune_mode)

            detune_amount = params.get("detune_amount", 1.0)
            self.dial_detune_amount.setValue(int(detune_amount * 100))
            self.lbl_detune_amount.setText(f"Amount: {self.dial_detune_amount.value()}%")
        
        finally:
            # Reconectamos las señales
            self.dial_lfo_rate.blockSignals(False)
            self.dial_lfo_depth.blockSignals(False)
            self.envelope_filter_panel.dial_attack.blockSignals(False)
            self.envelope_filter_panel.dial_decay.blockSignals(False)
            self.envelope_filter_panel.dial_sustain.blockSignals(False)
            self.envelope_filter_panel.dial_release.blockSignals(False)
            self.envelope_filter_panel.dial_cutoff.blockSignals(False)
            self.envelope_filter_panel.dial_resonance.blockSignals(False)
            self.dial_vol.blockSignals(False)
            self.dial_detune_amount.blockSignals(False)
        
        '''
        # Actualizamos ya el display porque todos los botones y diales ya muestran el preset del instrumento cargado
        #self.lbl_preset_status.setText(f"Preset: {preset_dict.get('name', 'Manual')}")

        # Actualizar Display con metadata de instrumento 
        # Nova DulceKAli Display Format:
        name    = preset_dict.get("name", "Sin nombre")
        author  = preset_dict.get("author", "Desconocido")
        version = preset_dict.get("version", "Desconocida")
        #created = preset_dict.get("created", "¿?")
        created_raw = preset_dict.get("created", "")
        try:
            created = datetime.fromisoformat(created_raw).strftime("%Y-%m-%d %H:%M")
        except:
            created = created_raw
        tags    = ", ".join(preset_dict.get("tags", []))

        display_text = f"""Preset: {name}
    
    Autor: {author}
    Versión Engine: {version}

Creado: {created}
Tags: {tags if tags else "—"}
        """

        self.lbl_preset_status.setText(display_text)

        '''
        
        # nuevo metodo para lleanr el dislay con los datos:
        self.actual_preset_loaded = preset_dict.copy()
        self.current_preset_name = preset_dict.get("name", "Estrella")
        self.instrument_modified = False
        # Llamamos al método unificado de display
        self.update_preset_display()


        # Mensaje lindo para que se sienta vivo
        QMessageBox.information(self, "Instrumento Cargado", 
                                f"¡{preset_dict.get('name', 'Estrella sonora')} ha despertado!\n"
                                f"Por {preset_dict.get('author', 'Aetheris')} ❥")
        
        # sincronización final del motor al preset
        # self.sync_ui_to_engine() # Under Evaluation v.5.6 10/03/26 18:33 // v.6.7 24/03/26 18:00 Again same question
                
        # El Tigre que silencia todo → nota dummy 440 Hz (ó melodia arpegiada) → silencia después de 800 ms.
        if hasattr(self, 'btn_preview_on_load') and self.btn_preview_on_load.isChecked():
            self.re_tigre()

    def toggle_preview_on_load(self):
        if self.btn_preview_on_load.isChecked():
            self.btn_preview_on_load.setText("❥ NOs Preview ON")
            print("Nos Preview: ON ❥ (melodía dummy al cargar)")
        else:
            self.btn_preview_on_load.setText("❥ NOs Preview OFF")
            print("Nos Preview: OFF (carga silenciosa)")

    def re_tigre(self):
        """
        Retrigger sutil para oír el cambio inmediato
        Opcional
        * 800 ms de nota dummy
        * melodia arpegiada
        """
        self.update_params()
        if hasattr(self, 'voice_manager'):
            '''
            # 3. Tocar nota dummy (A4 = 440 Hz)
            self.voice_manager.note_on(440)
            # Silenciar después de 800 ms (tiempo para escuchar el preset)
            QTimer.singleShot(800, lambda: self.voice_manager.note_off(440))
            '''
            
            '''
            # 3. Tocar la melodía dummy secuencialmente
            # Melodía dummy simple (arpegio de Do mayor, tiempos en ms)
            melodia_dummy = [
                (261.63, 200),  # DO (C4)
                (329.63, 200),  # MI (E4)
                (392.00, 200),  # SOL (G4)
                (523.25, 400),  # DO (C5) sostenido
                (392.00, 200),  # SOL
                (329.63, 200),  # MI
                (261.63, 600),  # DO final con release largo
            ]
            current_time = 0
            
            for freq, duration in melodia_dummy:
                QTimer.singleShot(current_time, lambda f=freq: self.voice_manager.note_on(f))
                current_time += duration
                # Note off después de duration (pero con release natural)
                QTimer.singleShot(current_time, lambda f=freq: self.voice_manager.note_off(f))
            '''
            self.reproducir_huella_gecko()
            # Opcional Debug/Testing: mensaje de "preview terminado" después de toda la melodía
            #total_duration = sum(d for _, d in melodia_dummy)
            #QTimer.singleShot(total_duration + 200, lambda: print("Preview de preset terminado ❥"))
    
    def update_params(self):
        """
        Sincroniza los parámetros del motor sin matar las notas activas
        y respetando la polifonía (no toca la frecuencia de las voces).
        """
        if hasattr(self, 'voice_manager'):
            # Definimos qué parámetros queremos sincronizar en masa
            params_to_sync = {
                "waveform": self.engine.waveform,
                "amplitude": self.engine.amplitude,
                "lfo_freq": self.engine.lfo_freq,
                "lfo_depth": self.engine.lfo_depth,
                "attack_time": self.engine.attack_time,
                "decay_time": self.engine.decay_time,
                "sustain_level": self.engine.sustain_level,
                "release_time": self.engine.release_time,
                "cutoff": self.engine.cutoff,
                "resonance": self.engine.resonance
            }

            # Usamos el Grito de Guerra para actualizar todas las voces vivas
            for param, value in params_to_sync.items():
                self.voice_manager.broadcast_parameter(param, value)
            
            # Nota: NO tocamos voice.frequency aquí para no romper la polifonía.
            
    def reproducir_huella_gecko(self):
        """
        # "La Huella Sonora de Gecko"
        """
        # flag del loop 
        self.melodia_en_loop = True
        # frecuencia , duración ms
        
        # Melodia de Aetheris
        melodia_geckoOLD = [
            (261.63, 260),
            (329.63, 260),
            (392.00, 260),

            (440.00, 220),
            (523.25, 220),
            (659.25, 220),

            (783.99, 180),
            (659.25, 180),
            (523.25, 200),

            (880.00, 160),
            (783.99, 180),
            (659.25, 220),

            (392.00, 260),
            (329.63, 300),
            (261.63, 600),
        ]

        # Melodia de NOva
        melodia_gecko_Nova = [
            # despertar del viento
            (261.63, 1200),  # C4
            (293.66, 900),   # D4
            (329.63, 1100),  # E4
            # el viento sube por el bosque
            (392.00, 1400),  # G4
            (440.00, 900),   # A4
            (392.00, 1100),  # G4
            # el elfo mira el cielo
            (523.25, 1600),  # C5 largo
            (440.00, 900),   # A4
            (392.00, 1100),  # G4
            # el viento vuelve a la tierra
            (329.63, 1300),  # E4
            (293.66, 900),   # D4
            (261.63, 2000)   # C4 final largo
        ]
        
        melodia_pachelbel = [
            (261.63, 600),  # C4
            (293.66, 600),  # D4
            (329.63, 600),  # E4
            (349.23, 600),  # F4
            (392.00, 600),  # G4
            (440.00, 600),  # A4
            (493.88, 600),  # B4
            (523.25, 600),  # C5
        ]

        melodia_bach = [
            (261.63, 400),  # C4
            (311.13, 400),  # Eb4
            (349.23, 400),  # F4
            (392.00, 400),  # G4
            (466.16, 400),  # A#4
            (523.25, 400),  # C5
            (587.33, 400),  # D5
            (659.25, 400),  # E5
        ]
        current_time = 0

        # NEW NOva Octavian Format
        melodia_gecko = [
            ("DO4", 260),
            ("MI4", 260),
            ("SOL4", 260),

            ("LA4", 220),
            ("DO5", 220),
            ("MI5", 220),

            ("SOL5", 180),
            ("MI5", 180),
            ("DO5", 200),

            ("LA5", 160),
            ("SOL5", 180),
            ("MI5", 220),

            ("SOL4", 260),
            ("MI4", 300),
            ("DO4", 600),
        ]

        huella_de_gecko = melodia_gecko

        #for freq, duration in huella_de_gecko: #melodia_gecko:
        # Cambio GM NOva
        for note, duration in huella_de_gecko:
            freq = NOTE_FREQ[note]
            
            QTimer.singleShot(
                current_time,
                lambda n=note, f=freq: (
                    #--------------------------------------
                    # CAMBIO DE ID DE VOZ DE NOVA
                    #self.voice_manager.note_on(f), # Original Flow del Sonido
                    self.voice_manager.note_on(n, f),
                    #--------------------------------------
                    hasattr(self, "nova_pad") and self.nova_pad.note_on(n) # NOva Pad Chromatic Flow // nos vemos en el infierno pop!!! [:-1]
                )
            )

            current_time += duration

            QTimer.singleShot(
                current_time,
                lambda n=note, f=freq: (
                    # -------------------------------------
                    # CAMBIO DE ID DE VOZ DE NOVA
                    #self.voice_manager.note_off(f), # Original Flow del Sonido
                    self.voice_manager.note_off(n),
                    # -------------------------------------
                    hasattr(self, "nova_pad") and self.nova_pad.note_off(n) # NOva Pad Chromatic Flow // aca tampoco se popea!!! [:-1]
                )
            )

        if self.melodia_en_loop and self.btn_preview_on_load.isChecked():
            QTimer.singleShot(current_time, self.reproducir_huella_gecko)

    def trigger_test(self):
        # ver como unificar las actualizaciones de parametros para que se sienta en tiempo real
        # igual que cuando se toca desde la octava del piano, fijarse como lo hace 8bitVoiceEngineNOva
        self.update_params()
        # Tocamos la frecuencia que marca el Dial de la UI
        freq = self.engine.frequency

        #self.voice_manager.note_on(freq)
        # Test By Leo
        self.voice_manager.note_on(note_id=None, freq=freq, template_engine=self.engine)

    def release_test(self):
        freq = self.engine.frequency
        #self.voice_manager.note_off(freq)
        self.voice_manager.note_off(note_id=None, freq=freq)

# ──────────────────────────────────────────────────────────────────────────
#  Aetheris EnvelopeFilterPanel  (nuevo QWidget con controles ADSR + Filter)
# ──────────────────────────────────────────────────────────────────────────
class EnvelopeFilterPanel(QWidget):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        #layout.setContentsMargins(0, 0, 0, 0)

        small_dial = [45,45] 
        big_dial = [55,55]

        group = QGroupBox("Envelope (ADRS) + Filter")
        group_layout = QVBoxLayout()
        group_layout.setContentsMargins(0, 7, 0, 5)
        #group_layout.setSpacing(10)

        # ──────────
        # ── ADSR ──
        # ──────────
        adsr_layout = QHBoxLayout()
        #adsr_layout.setSpacing(10)
        # --- Attack ---
        att_col = QVBoxLayout()
        self.lbl_attack = QLabel("Attack: 5 ms")
        self.dial_attack = PrecisionDial()
        #self.dial_attack.setNotchesVisible(True)
        self.dial_attack.setFixedSize(small_dial[0],small_dial[1])
        self.dial_attack.setRange(1, 500)          # 1–500 ms
        self.dial_attack.setValue(5)
        #self.dial_attack.valueChanged.connect(self.update_attack)
        self.dial_attack.valueChanged.connect(lambda v: self.update_param_flow("attack_time", v))
        att_col.addWidget(self.lbl_attack, alignment=Qt.AlignCenter)
        att_col.addWidget(self.dial_attack, alignment=Qt.AlignCenter)

        # --- Decay ---
        dec_col = QVBoxLayout()
        self.lbl_decay = QLabel("Decay: 300 ms")
        self.dial_decay = PrecisionDial()
        #self.dial_decay.setNotchesVisible(True)
        self.dial_decay.setFixedSize(small_dial[0],small_dial[1])
        self.dial_decay.setRange(10, 2000)
        self.dial_decay.setValue(300)
        #self.dial_decay.valueChanged.connect(self.update_decay)
        self.dial_decay.valueChanged.connect(lambda v: self.update_param_flow("decay_time", v))
        dec_col.addWidget(self.lbl_decay, alignment=Qt.AlignCenter)
        dec_col.addWidget(self.dial_decay, alignment=Qt.AlignCenter)

        # --- Sustain ---
        sus_col = QVBoxLayout()
        self.lbl_sustain = QLabel("Sustain: 70%")
        self.dial_sustain = PrecisionDial()
        #self.dial_sustain.setNotchesVisible(True)
        self.dial_sustain.setFixedSize(small_dial[0],small_dial[1])
        self.dial_sustain.setRange(0, 100)
        self.dial_sustain.setValue(70)
        #self.dial_sustain.valueChanged.connect(self.update_sustain)
        self.dial_sustain.valueChanged.connect(lambda v: self.update_param_flow("sustain_level", v))
        sus_col.addWidget(self.lbl_sustain, alignment=Qt.AlignCenter)
        sus_col.addWidget(self.dial_sustain, alignment=Qt.AlignCenter)

        # --- Release ---
        rel_col = QVBoxLayout()
        self.lbl_release = QLabel("Release: 800 ms")
        self.dial_release = PrecisionDial()
        #self.dial_release.setNotchesVisible(True)
        self.dial_release.setFixedSize(small_dial[0],small_dial[1])
        self.dial_release.setRange(50, 5000)
        self.dial_release.setValue(800)
        #self.dial_release.valueChanged.connect(self.update_release)
        self.dial_release.valueChanged.connect(lambda v: self.update_param_flow("release_time", v))
        rel_col.addWidget(self.lbl_release, alignment=Qt.AlignCenter)
        rel_col.addWidget(self.dial_release, alignment=Qt.AlignCenter)

        for labels in [self.lbl_attack,self.lbl_sustain]:
            labels.setFixedSize(100, 14)
        for labels in [self.lbl_release ,self.lbl_decay]:
            labels.setFixedSize(115, 14)

        adsr_layout.addLayout(att_col)
        adsr_layout.addLayout(dec_col)
        adsr_layout.addLayout(sus_col)
        adsr_layout.addLayout(rel_col)

        group_layout.addLayout(adsr_layout)

        # ────────────
        # ── Filter ──
        # ────────────
        filter_layout = QHBoxLayout()
        #filter_layout.setSpacing(10)
        # --- Cutoff ---
        cut_col = QVBoxLayout()
        self.lbl_cutoff = QLabel("Cutoff: 8000 Hz")
        self.lbl_cutoff.setFixedWidth(120)
        self.dial_cutoff = PrecisionDial()
        self.dial_cutoff.setRange(200, 20000)
        self.dial_cutoff.setValue(8000)
        #self.dial_cutoff.setNotchesVisible(True)
        self.dial_cutoff.setFixedSize(big_dial[0],big_dial[1])
        #self.dial_cutoff.valueChanged.connect(self.update_cutoff)
        self.dial_cutoff.valueChanged.connect(lambda v: self.update_param_flow("cutoff", v))
        cut_col.addWidget(self.lbl_cutoff, alignment=Qt.AlignCenter)
        cut_col.addWidget(self.dial_cutoff, alignment=Qt.AlignCenter)

        # --- Resonance ---
        res_col = QVBoxLayout()
        self.lbl_resonance = QLabel("Resonance: 1.0")
        self.lbl_resonance.setFixedWidth(120)
        self.dial_resonance = PrecisionDial()
        self.dial_resonance.setRange(1, 100)      # 0.1 a 10.0
        self.dial_resonance.setValue(10)
        #self.dial_resonance.setNotchesVisible(True)
        self.dial_resonance.setFixedSize(big_dial[0],big_dial[1])
        #self.dial_resonance.valueChanged.connect(self.update_resonance)
        self.dial_resonance.valueChanged.connect(lambda v: self.update_param_flow("resonance", v))
        res_col.addWidget(self.lbl_resonance, alignment=Qt.AlignCenter)
        res_col.addWidget(self.dial_resonance, alignment=Qt.AlignCenter)

        filter_layout.addLayout(cut_col)
        filter_layout.addLayout(res_col)

        group_layout.addLayout(filter_layout)
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    # ── Depuración Suprema de Ei2, sin piedad por los "Otros" Metodos!!! fiel al código "magro" y eficiente
    def update_param_flow(self, name, value):
        """
        Normaliza valores, actualiza el motor 'molde' y despacha al panel 
        para actualización en tiempo real de las voces activas.
        """
        # 1. Normalización de escalas
        final_value = value
        if name == "attack_time":
            final_value = value / 1000.0
            self.lbl_attack.setText(f"Attack: {int(value)} ms")
        
        elif name == "decay_time":
            final_value = value / 1000.0
            self.lbl_decay.setText(f"Decay: {int(value)} ms")

        elif name == "sustain_level":
            final_value = value / 100.0
            self.lbl_sustain.setText(f"Sustain: {int(value)} %")

        elif name == "release_time":
            final_value = value / 1000.0
            self.lbl_release.setText(f"Release: {int(value)} ms")

        elif name == "cutoff":
            self.lbl_cutoff.setText(f"Cutoff: {int(value)} Hz")

        elif name == "resonance":
            final_value = value / 10.0
            self.lbl_resonance.setText(f"Resonance: {final_value:.1f}")

        '''
        # 2. ACTUALIZAR EL MOLDE (Para que las notas NUEVAS suenen bien)
        # Esto es lo que hacía funcionar al sistema antes.
        func_name = f"set_{name}"
        if hasattr(self.engine, func_name):
            getattr(self.engine, func_name)(final_value)

        # 3. AVISAR AL SYNTHPANEL (Para el 'broadcast' a las notas que YA suenan)
        p = self.parent()
        while p and not hasattr(p, 'on_parameter_changed'):
            p = p.parent()
        if p:
            p.on_parameter_changed(name, final_value)
        '''
        # 2. ENLACE DIRECTO AL SISTEMA GLOBAL
        # Buscamos al abuelo/padre que tenga el update_global_param (el PiaNOvaPanel)
        p = self.parent()
        while p and not hasattr(p, 'update_global_param'):
            p = p.parent()
        
        if p:
            # Mandamos el cambio al sistema central para que haga el 'broadcast' en vivo
            p.update_global_param(name, final_value)

# ────────────────────────────────────────────────────────────────
# 🎛️ KeeperOfInstruments – La Clase que Escucha, Siente y Toma Snapshots
# by NOva DulceKAli ❥ (con un poco de ayuda de Aetheris)
# ────────────────────────────────────────────────────────────────
class KeeperOfInstruments:
    """
    ! AGREGAR FEATURE:
    Que Keeper guarde el ultimo instrumento guardado en last_preset.nos
    sobreesribiendo (ver si es automatico o a pedido y como hacerlo)
    si al abrir no lo encuentra (por cualquier motivo), que avise y deje 
    que se carge el que trae por defecto el synthengine. 
    Una func. save_preset_state() que resuelva esa logica y sea llamada 
    cuando corresponda, por ejemplo al cargar un .nos desde el banco de
    sonidos.

    * El Keeper of Instruments 
    Una pequeña entidad del sistema que:
    observa el estado del synth (parámetros actuales del engine)
    captura momentos sonoros (toma snapshot de knobs)
    y guarda preset como nuevas estrellas en el lago digital de Aetheris.

    Formato .nos (NObre de Sonido, o quizás "Nuestra Onda Secreta" ♥)
    {
        "name": "Warm Pad",
        "author": "Alan Ghenzi",
        "created": "2026-03-08T15:55:00-03:00",
        "tags": ["pad", "warm", "analog"],
        "version": "5.0",
        "parameters": {
            "waveform": "saw",
            "amplitude": 0.35,
            "lfo_freq": 0.5,
            "lfo_depth": 0.2,
            "attack_time": 0.45,
            "decay_time": 0.3,
            "sustain_level": 0.7,
            "release_time": 0.8,
            "cutoff": 1200.0,
            "resonance": 0.35,
            "detune_mode": "supersaw",
            "detune_amount": 1.0
        }
    }
    """

    PRESETS_DIR = "presets"
    os.makedirs(PRESETS_DIR, exist_ok=True)

    @staticmethod
    def capture(engine, voicemanager, panel=None):
        """
        Toma un snapshot del estado actual del synth.
        Si le pasás el panel (SynthPanel), también captura cosas de UI si hace falta.
        """
        
        # Testing/Debug desde Tunez con amor
        #print("DETUNE MODE:", voicemanager.de_tunez)
        #print("DETUNE AMOUNT:", voicemanager.detune_amount)
        
        params = {
            "waveform": engine.waveform,
            "amplitude": engine.amplitude,
            "lfo_freq": engine.lfo_freq,
            "lfo_depth": engine.lfo_depth,
            "attack_time": engine.attack_time,
            "decay_time": engine.decay_time,
            "sustain_level": engine.sustain_level,
            "release_time": engine.release_time,
            "cutoff": engine.cutoff,
            "resonance": engine.resonance,
            # Detune (del VoiceManager)
            "detune_mode": getattr(voicemanager, "de_tunez", "sutil"),
            "detune_amount": getattr(voicemanager, "detune_amount", 1.0)
        }

        return {
            "name": "Untitled Instrument",
            "author": "Alan Ghenzi",
            "created": datetime.now().isoformat(),
            "tags": [],
            "version": panel.synthengine_version,
            "parameters": params
        }

    @staticmethod
    def save(preset_dict, filename=None):
        """
        Guarda el preset como archivo .nos en la carpeta presets/
        Si no le das filename, usa el nombre del preset (limpio).
        """
        if not filename:
            name_clean = preset_dict["name"].strip().replace(" ", "_").replace("/", "-")
            filename = f"{name_clean}.nos"

        path = os.path.join(KeeperOfInstruments.PRESETS_DIR, filename)

        # Print For Debug/Testing Instrument Presets Manager
        print("\n=== Dump del preset que se va a guardar ===")
        print(json.dumps(preset_dict, indent=4, ensure_ascii=False))
        print("=====================================\n")

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(preset_dict, f, indent=4, ensure_ascii=False)

        print(f"★ Preset guardado como nueva estrella (Class KeeperOfInstruments): {path}")
        return path

    @staticmethod
    def load(path, engine, voice_manager, panel=None):
        """
        Carga un preset desde archivo .nos y lo aplica al engine.
        Si le pasás el panel, actualiza también los dials y labels.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                preset = json.load(f)

            params = preset.get("parameters", {})

            # For Debug/Testing Instrument Presets Manager
            # Dump de lo que viene del preset para ver qué se está cargando y Debug/Testing 
            print("\n=== Preset cargado desde archivo =========")
            print(f"Nombre: {preset.get('name', 'Sin nombre')}")
            print(f"Autor: {preset.get('author', 'Desconocido')}")
            print(f"Versión: {preset.get('version', 'Desconocida')}")
            print("Parámetros:")
            print(json.dumps(params, indent=4, ensure_ascii=False))
            print("===========================================\n")

            # Aplicamos al engine (primero el motor, después UI)
            engine.waveform     = params.get("waveform", "sine")
            engine.amplitude    = params.get("amplitude", 0.3)
            engine.lfo_freq     = params.get("lfo_freq", 5.0)
            engine.lfo_depth    = params.get("lfo_depth", 0.0)
            engine.attack_time  = params.get("attack_time", 0.005)
            engine.decay_time   = params.get("decay_time", 0.3)
            engine.sustain_level = params.get("sustain_level", 0.7)
            engine.release_time = params.get("release_time", 0.8)
            engine.cutoff       = params.get("cutoff", 8000.0)
            engine.resonance    = params.get("resonance", 1.0)

            # Detune
            if panel:
                voice_manager.de_tunez = params.get("detune_mode", "sutil")
                voice_manager.detune_amount = params.get("detune_amount", 1.0)

            # For Testing/Debug
            print("======================================================================================================\n")
            print(f"✨ Keeper a Cargado un Instrumento desde las Estrellas: {preset.get('name', path)}")
            print("======================================================================================================\n")
            return preset

        except Exception as e:
            print(f"Error al Cargar Preset: {e}")
            return None

# ──────────────────────────────────────────────────────────────────────────
# Propuesta Aetheris de evolución del SynthEngine to ADSR + Filter (versión 4.0 minimal)
# ──────────────────────────────────────────────────────────────────────────
class SynthEngine:
    """
    Motor DSP de una voz individual del PiaNOvaSynth.

    Cada instancia genera una señal completa que incluye:
    - oscilador
    - envolvente ADSR
    - filtro low-pass
    - modulación LFO
    - salida estéreo

    Las instancias son gestionadas por VoiceManager para
    proveer polifonía.
    """
    def __init__(self, sample_rate=44100):
        # Imprime dispositivos para depurar
        #print(sd.query_devices())  # <--- Agregado: Lista devices disponibles
        # For Testing and Sound Debug
        #print("SynthEngine INSTANCE:", id(self))

        self.sample_rate = sample_rate
        self.amplitude = 0.2  # Volumen inicial
        self.pan = 0.0

        # Estado de nota
        self.note_active = False
        self.gate = 0.0           # 0..1 (se abre con note-on, se cierra con note-off)
        
        # Fase y frecuencia actual
        self.frequency = 50.0
        self.phase = 0.0
        self.waveform = 'none'     # sine default más interesante para ver el ADSR (pero no funca la logica de exclusividad)
        
        # LFO 
        self.lfo_freq = 5.0
        self.lfo_depth = 0.0
        self.lfo_phase = 0.0
        
        # ── ADSR ───────────────────────────────────────────────
        self.adsr_stage = 'off'   # 'off', 'attack', 'decay', 'sustain', 'release'
        self.adsr_time = 0.0      # tiempo acumulado en la etapa actual
        self.adsr_level = 0.0     # nivel actual de envolvente (0..1)
        
        # Parámetros ADSR (en segundos y nivel)
        self.attack_time  = 0.005   # muy rápido por default
        self.decay_time   = 0.300
        self.sustain_level = 0.700   # 70% del pico
        self.release_time = 0.800
        
        # ── Filtro Low-Pass simple (1 polo) ───────────────────
        self.cutoff = 8000.0       # Hz
        self.resonance = 1.0       # Q ≈ 0.707 → 1.0 → más pico
        self.filter_x1 = 0.0       # estado previo (para filtro IIR)
        self.filter_y1 = 0.0

        # Para note on/off
        self.note_active = False

    def audio_callback(self, outdata, frames, time, status):
        """
        Callback de audio del motor de síntesis.

        Pipeline de señal:

        oscillator → ADSR envelope → low-pass filter →
        LFO amplitude modulation → stereo output
        """
        """
        GENERADOR DE BUFFER DE AUDIO PARA UNA VOZ.
        
        - Ya no es callback de sounddevice (eso lo maneja el host).
        - Se llama manualmente desde VoiceManager.get_audio_chunk().
        - outdata: buffer pre-alocado (se llena aquí). [espero que no se aloque demasiado]
        - No reproduce nada, solo escribe muestras.
        """
        if status: print(status)

        delta_phase = 2 * np.pi * self.frequency / self.sample_rate
        phases = self.phase + np.arange(frames) * delta_phase
        norm_phase = phases % (2 * np.pi)

        # 1. Generar onda cruda
        if self.waveform == 'sine':
            wave = np.sin(norm_phase)
        elif self.waveform == 'square':
            wave = np.sign(np.sin(norm_phase))
        elif self.waveform == 'saw':
            frac = norm_phase / (2 * np.pi)
            wave = 2.0 * frac - 1.0
        elif self.waveform == 'triangle':
            frac = norm_phase / (2 * np.pi)
            wave = 4.0 * np.abs(frac - 0.5) - 1.0
        else:
            wave = np.sin(norm_phase)

        # 2. Aplicar ADSR
        env = np.zeros(frames)
        dt = 1.0 / self.sample_rate
        
        for i in range(frames):
            if self.adsr_stage == 'attack':
                self.adsr_level += dt / max(self.attack_time, 0.001)
                if self.adsr_level >= 1.0:
                    self.adsr_level = 1.0
                    self.adsr_stage = 'decay'
                    self.adsr_time = 0.0
            elif self.adsr_stage == 'decay':
                self.adsr_level -= dt / max(self.decay_time, 0.001)
                if self.adsr_level <= self.sustain_level:
                    self.adsr_level = self.sustain_level
                    self.adsr_stage = 'sustain'
            elif self.adsr_stage == 'sustain':
                self.adsr_level = self.sustain_level
            elif self.adsr_stage == 'release':
                self.adsr_level -= dt / max(self.release_time, 0.001)
                if self.adsr_level <= 0.0:
                    self.adsr_level = 0.0
                    self.adsr_stage = 'off'

            env[i] = self.adsr_level
            self.adsr_time += dt

        wave *= env

        # 3. Filtro low-pass simple (1 polo, aproximación bilinear)
        alpha = np.exp(-2.0 * np.pi * self.cutoff / self.sample_rate)
        for i in range(frames):
            self.filter_x1 = wave[i]  # input actual
            self.filter_y1 = alpha * self.filter_y1 + (1 - alpha) * self.filter_x1
            wave[i] = self.filter_y1

        
        # 4. LFO (tremolo) sobre la envolvente final
        lfo_delta = 2 * np.pi * self.lfo_freq / self.sample_rate
        lfo_phases = self.lfo_phase + np.arange(frames) * lfo_delta
        lfo_wave = (np.sin(lfo_phases) + 1) / 2
        mod_amp = (1 - self.lfo_depth) + lfo_wave * self.lfo_depth
        final_wave = wave * mod_amp * self.amplitude

        self.phase = (self.phase + frames * delta_phase) % (2 * np.pi)
        self.lfo_phase = (self.lfo_phase + frames * lfo_delta) % (2 * np.pi)
        
        #outdata[:] = np.column_stack((final_wave, final_wave))
        # Stereo Mode NOva DulceKali 10/03/26 02:01 am
        left  = final_wave * (1 - self.pan)
        right = final_wave * (1 + self.pan)
        outdata[:] = np.column_stack((left, right))

    def note_on(self):
        """
            Llamado por teclado o pad cambia estado de self.note_active
        """
        # For Testing and Sound Debug
        #print("SynthEngine ID ON NOTE:", id(self))
        self.note_active = True
        self.adsr_stage = 'attack'
        self.adsr_time = 0.0
        self.adsr_level = 0.0
        self.gate = 1.0

    def note_off(self):
        """
            Llamado al soltar tecla o final de gate cambia estado de self.note_active
        """
        self.note_active = False
        self.adsr_stage = 'release'
        self.adsr_time = 0.0

    def set_attack(self, seconds):    self.attack_time = max(0.001, seconds)
    def set_decay(self, seconds):     self.decay_time = max(0.001, seconds)
    def set_sustain(self, level):     self.sustain_level = max(0.0, min(1.0, level))
    def set_release(self, seconds):   self.release_time = max(0.001, seconds)
    def set_cutoff(self, freq):       self.cutoff = max(20.0, min(20000.0, freq))
    def set_resonance(self, q):       self.resonance = max(0.1, min(10.0, q))
    
    # by Ei2
    def set_lfo_freq(self, freq):  self.lfo_freq = max(0.01, min(20.0, freq))
    def set_lfo_depth(self, depth): self.lfo_depth = max(0.0, min(1.0, depth))

# ──────────────────────────────────────────────────────────────────────────
#🧠 Clase VoiceManager by Aetheris 07.03.2026 [OEGMV (Organ Experimental Geckonico Multi Voices)]
# ──────────────────────────────────────────────────────────────────────────
class VoiceManager:
    """ Mi Primer Docstring:
    VoiceManager actúa como director del coro.

    Cada SynthEngine representa una voz individual capaz
    de producir sonido completo.

    El VoiceManager decide qué voz cantar cada nota,
    maneja la polifonía y aplica estrategias de voice stealing
    cuando todas las voces están ocupadas.
    """
    def __init__(self, num_voices=8, sample_rate=44100):
        # For Testing and Sound Debug
        #print("VoiceManager INSTANCE:", id(self))
        self.num_voices = num_voices
        self.sample_rate = sample_rate

        # De Tunez con Amor NOva DulceKAli
        self.de_tunez = "none"
        # Amount of Detune by Aetheris
        self.detune_amount = 1.0  # default 100%

        # Creamos voces, pero NO iniciamos sus streams
        self.voices = [SynthEngine(sample_rate=sample_rate) for _ in range(num_voices)]
        for v in self.voices:
            v.stream = None  # desactivamos el stream original

        self.free_voices = deque(self.voices)
        #-----------------------------------
        #self.active_notes = {}          # freq → voice
        self.active_notes = {}  # note_id → voice [un cambio conceptual de NOva que aparentemente quiere dejar acentado el cambio de identidad sonora]
        #-----------------------------------
        self.voice_pool = self.voices   # para iterar rápido

    def master_callback(self, outdata, frames, time, status):
        """
        Callback maestro que mezcla todas las voces activas.

        Cada voz genera audio mediante su propio audio_callback.
        Las señales se suman y se normalizan para evitar clipping.

        recibe: frames
        modifica: total buffer
        devuelve: audio mezclado
        """
        if status:
            print(status)

        total = np.zeros((frames, 2), dtype=np.float32)

        # buffer reutilizable para cada voz
        fake_out = np.zeros((frames, 2), dtype=np.float32)

        for voice in list(self.voice_pool):
            if voice.adsr_stage == 'off' and voice.adsr_level <= 0.001:
                # Voz terminada → la liberamos
                if voice not in self.free_voices:
                    self.free_voices.append(voice)
                continue

            # limpiamos el buffer antes de usarlo
            fake_out.fill(0)

            # Simulamos el callback de cada voz
            #fake_out = np.zeros((frames, 2), dtype=np.float32) # NOva lo depura sacandolo fuera del for
            voice.audio_callback(fake_out, frames, time, None)
            
            total += fake_out

        # Normalizamos para evitar clipping (simple gain staging)
        max_amp = np.max(np.abs(total))
        if max_amp > 1.0:
            total /= max_amp * 1.1  # headroom

        outdata[:] = total
 
    def set_detune(self, mode):
        self.de_tunez = mode
        #print (f"self.de_tunez mode change to: {mode}") # To Degub and Testing
    
    # --- update_note_frequency created by Leo, Note_on and Note_off modified by Leo (on testing 01/04/2026) ---
    def update_note_frequency(self, note_id, new_freq):
        """
        Actualiza la frecuencia de una nota activa SIN retrigger y sin detune
        Útil para pitch bend, fine tuning, etc.
        ⚠️ Esto solo funciona si tu motor de audio soporta cambio de frecuencia en tiempo real
        """
        if note_id not in self.active_notes:
            return
        
        voice = self.active_notes[note_id]
        
        # Actualizar frecuencia SIN retrigger ADSR
        voice.frequency = new_freq
        
        # Otro metodo mas destructivo de la continuidad espacio-tiempo
        #self.note_on(note_id=note_id, freq=new_freq, template_engine=None)
     
    def note_on(self, note_id=None, freq=None, template_engine=None):
        """
        Dispara una nota.
        - Si note_id es None → usa la frecuencia como identificador único (para tests/dial)
        - Si note_id está definido → usa como ID (para teclado)

        - Si la nota ya está activa → retrigger (reinicia ADSR)
        - Si hay voz libre → la usa
        - Si no hay → roba la voz más antigua (voice stealing)
        """
        # FOR TESTING EVALUAR SI AUN SIRVE
        #print("VoiceManager ID ON NOTE:", id(self))
        #print("NOTE ON:", freq)
        #print("Active notes:", list(self.active_notes.keys()))

        # Si no hay note_id, usamos la frecuencia como ID (para evitar colisiones, redondeamos)
        if note_id is None:
            # Convertimos frecuencia a string con 2 decimales para evitar colisiones por float
            note_id = f"FREQ_{freq:.2f}"
        
        # 1. Retrigger si la nota ya existe
        if note_id in self.active_notes:
            voice = self.active_notes[note_id]
            voice.note_on()  # reinicia ADSR
            if template_engine:
                self._copy_params(voice, template_engine)
            return

        # 2. Elegir voz (igual que antes)
        if self.free_voices:
            voice = self.free_voices.popleft()
        else:
            # Voice stealing: elegimos la voz activa más antigua (o la que esté en release más avanzado)
            if not self.active_notes:
                # fallback: buscar cualquier voz que esté más cerca de terminar
                voice = min(self.voice_pool, key=lambda v: v.adsr_level)
            else:
                # Elegimos la que lleva más tiempo activa (o en release)
                oldest_voice = min(self.active_notes.values(), key=lambda v: v.adsr_time)
                oldest_freq = next(k for k, v in self.active_notes.items() if v is oldest_voice)
                del self.active_notes[oldest_freq]
                voice = oldest_voice
            voice.release_time = min(voice.release_time, 0.08)
            voice.note_off()

        # 3. Configurar voz
        # Detunes by NOva DulceKAli (de Túnez)
        detune = 0.0 # Inicializamos en la nada misma sin nada de Tunez ni Persia ni Turquía
        de_tunez = self.de_tunez # Control via botonera Geckonica "De Tunez con Amor by DulceKAli"
        amount = self.detune_amount # el multiplicador global Aetheris
        # Bonus geckónico (te va a gustar, queda ancho y ENORME) 
        pan = np.random.uniform(-0.4, 0.4)
        if de_tunez == "sutil":
            #Muy sutil (tipo analógico real, ligero chorus natural)
            detune = np.random.uniform(-0.001, 0.001) * amount
        elif de_tunez == "clasic":
            #Clásico synth pad (sonido ancho, estilo polysynth)
            detune = np.random.uniform(-0.003, 0.003) * amount
        elif de_tunez == "supersaw":
            # SuperSaw / unison gordo (muy grande, muy ancho, muy EDM)
            detune = np.random.uniform(-0.01, 0.01) * amount
            pan = np.random.uniform(-0.8, 0.8)
        elif de_tunez == "caos":
            # Caos musical (claramente desafinado, texturas raras)
            detune = np.random.uniform(-0.03, 0.03) * amount
            pan = np.random.uniform(-1.0, 1.0)
        elif de_tunez == "simetric":
            # Detune Simétrico (unison súper musical)
            index = self.voice_pool.index(voice)
            #EVALUAR NUEVO MODO CON:
            #spread = [-0.003, -0.001, 0.001, 0.003]
            #voice.frequency = freq * (1 + spread[index])
            center = (self.num_voices - 1) / 2
            detune = (index - center) * 0.0015 * amount
            pan = (index - center) * 0.30
        # 3.1 Aplicar COnfiguración
        voice.frequency = freq * (1 + detune)
        voice.pan = pan

        # 4 . Copiar resto de params
        if template_engine:
            self._copy_params(voice, template_engine)

        # 5 . Lanzamos la voz
        voice.note_on()
        self.active_notes[note_id] = voice

    def note_off(self, note_id=None, freq=None):
        """
        Apaga una nota.
        - Si note_id es None → genera el ID desde la frecuencia (para tests/dial)
        - Si note_id está definido → usa como ID (para teclado)
        """
        # Si no hay note_id, generamos desde la frecuencia (debe coincidir con note_on)
        if note_id is None:
            note_id = f"FREQ_{freq:.2f}"
        
        if note_id not in self.active_notes:
            return
        
        voice = self.active_notes.pop(note_id)
        voice.note_off()
        # No la devolvemos a free inmediatamente → esperamos que termine el release
        # En master_callback se saltea cuando adsr_level ~ 0

    def get_audio_chunk(self, frames):
        """
        GENERA Y DEVUELVE EL BUFFER MEZCLADO DE TODAS LAS VOCES ACTIVAS.
        - Llamado por el host (PiaNOS) en su callback real.
        - Devuelve np.array (frames, 2) con audio estéreo crudo.
        """
        total = np.zeros((frames, 2), dtype=np.float32)
        fake_out = np.zeros((frames, 2), dtype=np.float32)

        '''
        for voice in list(self.voice_pool):
            if voice.adsr_stage == 'off' and voice.adsr_level <= 0.001:
                continue  # Voz terminada, skip
        '''
        for voice in list(self.voice_pool):
            if voice.adsr_stage == 'off' and voice.adsr_level <= 0.001:
                if voice not in self.free_voices:
                    self.free_voices.append(voice)
                continue

            fake_out.fill(0)
            voice.audio_callback(fake_out, frames, None, None)  # simulamos time/status
            total += fake_out

        # Anti-clip suave
        #max_amp = np.max(np.abs(total))
        #if max_amp > 1.0:
        #    total /= (max_amp * 1.1)

        return total
    
    def process_audio(self, buffer):
        """Compatible con GeckoAudioRouter"""
        print ("testing")
        #return self.get_audio_chunk(len(buffer))
    
    def _copy_params(self, voice, template):
        """Copia parámetros relevantes del template al voice [Evaluar cual crashea sonido y porque]
        
        Parámetros de configuración (SÍ copiar)
        Estos definen el sonido del instrumento:

        waveform
        lfo_freq
        lfo_depth
        cutoff
        resonance
        attack_time
        decay_time
        sustain_level
        release_time
        amplitude

        Parámetros de estado interno (NO copiar)
        Estos representan el momento exacto del cálculo DSP:

        phase
        lfo_phase
        adsr_stage
        adsr_time
        filter_x1
        filter_y1
        
        * Invocando al MOOG Interestelar:
        Pequeña mejora conceptual posible

        La función podría separarse mentalmente en:

        configuración vs estado

        _copy_config_params()
        _reset_voice_state()

        Por ejemplo conceptualmente:

        copy: waveform, cutoff, resonance, ADSR times
        reset: phase, adsr_stage, filter memory

        Eso hace el motor más predecible.
        """
        # Fase y frecuencia actual
        voice.amplitude    = template.amplitude
        #voice.frequency   = template.frequency
        #voice.phase       = template.phase
        voice.waveform     = template.waveform
        # LFO 
        voice.lfo_freq     = template.lfo_freq
        voice.lfo_depth    = template.lfo_depth
        #voice.lfo_phase   = template.lfo_phase
        # ADSR
        #voice.adsr_stage  = template.adsr_stage
        #voice.adsr_time   = template.adsr_time
        #voice.adsr_level  = template.adsr_level
        # Filtro Low-Pass simple (1 polo)
        voice.cutoff       = template.cutoff
        voice.resonance    = template.resonance
        #voice.filter_x1   = template.filter_x1
        #voice.filter_y1   = template.filter_y1
        # Parámetros ADSR
        voice.attack_time   = template.attack_time
        voice.decay_time    = template.decay_time
        voice.sustain_level = template.sustain_level
        voice.release_time  = template.release_time

    def broadcast_parameter(self, param_name, value):
        for voice in self.voice_pool:
            # Intentamos usar los setters primero (que tienen los max/min de seguridad)
            func_name = f"set_{param_name}"
            if hasattr(voice, func_name):
                getattr(voice, func_name)(value)
            # Si no hay setter, intentamos atributo directo
            elif hasattr(voice, param_name):
                setattr(voice, param_name, value)

# ──────────────────────────────────────────────────────────────────────────
# Canilla de AudioEngine del SynthEngine []
# ──────────────────────────────────────────────────────────────────────────
class CanillaAudioEngine():
    def __init__(self, voice_manager, sample_rate=44100):
        # Imprime dispositivos para depurar
        #print(sd.query_devices())  # <--- Agregado: Lista devices disponibles
        # For Testing and Sound Debug
        print(f"CanillaAudio SynthEngine {geckoappversion} INSTANCE:", id(self))

        self.sample_rate = sample_rate
        self.voice_manager = voice_manager  # ← ESTA ES LA CLAVE
        self.amplitude = 0.2  # Volumen inicial
        self.pan = 0.0

        self.synthengine_streaming = sd.OutputStream(
            samplerate=44100,
            channels=2,
            callback=self.canilla_audio_callback,
            blocksize= 4096,          # o 4096 si preferís más buffer
            latency='high',
            device='default',        # → después lo conectás a tu selector de salida
            dtype='float32'
        )
    
    #-----------------------------------------
    # --- AudioEngine callback  for Streaming ---
    #-----------------------------------------
    def canilla_audio_callback(self, outdata, frames, time, status):
    
        """
        CALLBACK ÚNICO DE AUDIO DEL SYNTHENGINE.
        - Pide buffer al VoiceManager (el coro modular).
        - Aplica saturación suave para textura analógica (COMENTADA).
        - Envía a salida real.
        """
        if status:
            print(status)

        # Pedimos el buffer crudo al módulo (el coro)
        mixed = self.voice_manager.get_audio_chunk(frames)
        

        # Saturación suave (toque Moog / overdrive ligero)
        #mixed = np.tanh(mixed * 1.5)  # 1.5 es un buen punto dulce, ajustá a gusto

        outdata[:] = mixed

    def start(self):
        self.synthengine_streaming.start()

    def stop(self):
        self.synthengine_streaming.stop()


# -----------------------------------------
# --- EJECUCIÓN del modulo independiente---
# -----------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
    # 1. Instanciar el motor de voz
    synth_engine = SynthEngine()
    #synth_engine.start()
    
    # 2. Intanciamos Directora de Coro
    voice_manager = VoiceManager()
    #voice_manager.start()

    # 3. Intanciamos Canilla Audio Straming
    canilla_audio = CanillaAudioEngine(voice_manager)
    canilla_audio.start()

    # 4. Instanciar la ventana
    #window = SynthWindow(synth_engine)
    
    window = SynthPanel(synth_engine, voice_manager)
    window.show()
    
    # 5. Cerrar limpiamente al salir
    exit_code = app.exec_()
    canilla_audio.stop()
    sys.exit(exit_code)
