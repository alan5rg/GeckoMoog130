# ==============================================================================
# 🛰️ RadarSpok TM - Visualizador de Ondas de Lissajous Vulkono-Geckónico
# VERSION EI2 2.2 13.03.2026 12:00 - STAR NAVIGATION ENABLED
# for GeckoMoog Modular Synth Platform™
# ==============================================================================
appversion = "3.5" # HAL9000 Version // Vulkan Decide the LWS (Logic Way for Sizes)
# 2.7 integra:
#   Definición de población de estrellas en el systema global self.number_stars_in_system
#   Mejora en navegación de campo estelar:
#       val = self.dial_subspacesync.value()
#       self.warp = (abs(val) * val) / (self.submax * 100) 
#   Sensibilidad calibrada de instrumental de detección estelar
#   Perfume Safirus en el Puente
#   Aprovado por el consejo Vulkano como 2.8 aconsejando calibrar el instrumento
#   Llevado a Vulkano por recalibracion y agregado de modos de NAvegacion DulceKAli Geckonicos
#   Coherencia Total del Instrumento con el entorno espacial, subespacial y atómico en power - play/pausa.
#   3.0 "Star Registry" by Ei2 fue implementado se reenvia al consejo reunidos en una luna lejana del systema Vulkano
#   3.1 Nos habilitan a implementar "Visualización de Branas y Espacios Inter-Multiversales"
#   - Es Lógico que GeckoMoog cuente con ello - habría dicho al unisono el Consejo
#   3.2 Certificado de Calibración Lógica. Liberado a Producción.
import sys
import math
import numpy as np
import random # Agregado para el universo aleatorio
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QFrame, QApplication, QDial, QSlider, QButtonGroup, QComboBox
from PyQt5.QtCore import Qt, QTimer, QPointF, QRect, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPolygonF, QFont, QLinearGradient, QRadialGradient, QPainterPath

from controls.precisionslider import PrecisionSlider

# ──────────────────────────────────────────────────────────────────────────
# Ei2 RadarSpok TM
# ──────────────────────────────────────────────────────────────────────────
class RadarSpok(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)
        self.setMidLineWidth(1)
        #self.setFixedSize(345, 420)
        self.setFixedSize(380, 400) #(Esto da margen para la pantalla de 400x400 más los botones de abajo).
        #self.setFixedSize(300, 450) 
        
        self.gemas= [
            "esmeralda",
            "rubi",
            "zafiro amarillo",
            "jade",
            "zafiro azul",
            "tanzanita"
        ]

        self.is_on = True     
        self.is_paused = False
        self.has_signal = True
        self.nav_mode = "starseeker"
        '''
        soporta modos de navegacion:
        starseeker, deriva, transpose, pausa, quantic
        '''
        self.audio_data_x = None
        self.audio_data_y = None
        
        # Colores Compatibles tema MIT
        self.color_fondo_oscuro = QColor("#19232d")
        self.color_fondo_claro = QColor("#fafafa")
        self.color_text_claro = QColor("#fafafa")
        self.color_fondoinstrumento_claro = QColor("#a9a9a9")
        self.color_fondoinstrumento_Oscuro = QColor("#19232d")
        # Colores Tema RadarSpok for GeckoMoog
        self.color_on = QColor("#00FF44")   
        self.color_off = QColor("#A30000")  
        self.color_star = QColor("#FFFFFF") 
        self.color_text = QColor("#00CC33") 
        self.color_btn_on = QColor("#00ffaa") 
        self.color_btn_off = QColor("#B30000") 
        self.color_btn_pause = QColor("#DDB800") 
        self.color_btn_play = QColor("#00ffaa")  

        self.signal_loss_counter = 0
        
        # --- Lógica Vulkana: Universo inicial ---
           
        # Star Registry by Ei2
        self.hovered_star = None  # Estrella bajo el mouse
        self.selected_stars = set() # IDs de estrellas con etiqueta fija 
        
        # Navegación NOva start
        self.max_stars = 2274 # Es 2 x 1137 = 2274 (Evaluar con la NASA)
        self.max_stars_x = 1 # Multiplicador x1, x3 x5 x7 (Alerta: en 7x Navegas entre Branas Multiversales)
        self.stars = self._generate_stars(self.max_stars)
        self.number_stars_in_system = self.max_stars
        
        self.warp = 0.96 # Sync with de subspace frequences
        # Autocalc de rango de instrumento
        self.submin = -(self.number_stars_in_system)
        self.submax = self.number_stars_in_system

        self.lissajous_points = []
        self.lissajous_index = 0
        self.paused_lissajous_points = []

        self._init_ui()

        # Star Registry by Ei2
        self.radar_screen.setMouseTracking(True)

        ''' # DesComentar luego de terminar modificaciones
        # Estilo más refinado y selectivo (con mejoras en diseño de Waveform Select Buttons)
        self.setStyleSheet(self.styleSheet() + """
            QWidget {
                background-color: #19232d; 
            }
            QTextEdit {
                background-color: black;
                color: #fafafa;
                font: 10pt Consolas;
                font-weight: normal;
                /*font-size: 12px;*/
            }                           
            QLabel {
                color: #fafafa;
                font-weight: normal;
            }
            QPushButton {
                /*background-color: #19232d;*/
                color: #000000;
                border: 2px solid #00ffaa;
                border-radius: 35px;
                font-size: 11px;
                font-weight: bold
            }
            QPushButton:hover {
                /*background-color: #454545;*/
                color: #0f8;
                border: 1px solid #0f8;
            }
            QPushButton:checked {
                /*background-color: #00ffaa;*/
                color: #000000;
                border: 2px solid #0f8;
            }
            QPushButton:pressed {
                /*background-color: #00ffaa;*/
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
                border-radius: 13px;
                margin-top: 5px;
            }
            QGroupBox::title {
                font: bold 12pt Consolas;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding-left: 13px;
                color: #0f8;
            }                           
        """)
        ''' # DesComentar luego de terminar modificaciones
        
        '''
        # Estilo del Slider by Ei2
        self.slider_stars.setStyleSheet("""
            QSlider::groove:vertical {
                background: #222;
                width: 6px;
                border-radius: 3px;
            }

            QSlider::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                            stop:0 #00ffaa, stop:1 #008855);
                border: 1px solid #0f8;
                height: 18px;
                margin-left: -6px;
                margin-right: -6px;
                border-radius: 9px;
            }

            QSlider::handle:vertical:hover {
                background: #00ffaa;
                border: 1px solid white;
            }

            QSlider::add-page:vertical {
                background: #004422; /* Color del rastro (lo que queda abajo) */
                border-radius: 3px;
            }

            QSlider::sub-page:vertical {
                background: #333; /* Color de la parte de arriba (vacío) */
                border-radius: 3px;
            }
        """)
        '''
        
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.update_visuals)
        #self.timer.start(20) # 20 normal time

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_visible_stars) # Aquí dentro ya se llama a update_visuals
        self.timer2.start(20) # 20 normal time

    # UI RADARSPOK
    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.radar_screen = RadarScreen(self)
        layout.addWidget(self.radar_screen, stretch=1)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(5)

        self.btn_power = QPushButton("PWR", self)
        self.btn_power.setCheckable(True)
        self.btn_power.setChecked(self.is_on)
        self.btn_power.setFixedSize(70, 70)
        self.btn_power.clicked.connect(self.toggle_power)
        self._set_button_style(self.btn_power, self.color_btn_on if self.is_on else self.color_btn_off)
        button_layout.addWidget(self.btn_power, alignment=Qt.AlignCenter)

        self.dial_subspacesync = PrecisionDial()
        self.dial_subspacesync.setFixedSize(73, 73)
        self.dial_subspacesync.setRange(self.submin,self.submax)
        #self.dial_subspacesync.setValue(96) # Sintonia casi perfecta del Instrumento
        self.dial_subspacesync.setValue(self.submin) # Mejor inciar dessincronizado del mundo [SIEMPRE DESFAZADO]
        self.dial_subspacesync.valueChanged.connect(self.sync_to_subspace)
        #self.warp = self.dial_subspacesync.value()/100
        val = self.dial_subspacesync.value()
        self.warp = (abs(val) * val) / (self.submax * 100)
        self.lbl_freq = QLabel(f"{self.warp:0.2f}", alignment=Qt.AlignRight)#ubspace")#(f"SEF:1.50 W")
        self.lbl_freq.setFixedSize(45,20)
        
        #button_layout.addSpacing(10)
        button_layout.addWidget(self.lbl_freq)
        button_layout.addWidget(self.dial_subspacesync)

        self.btn_pause = QPushButton("P/S", self)
        self.btn_pause.setCheckable(True)
        self.btn_pause.setFixedSize(70, 70)
        self.btn_pause.clicked.connect(self.toggle_pause)
        self._set_button_style(self.btn_pause, self.color_btn_play) 
        button_layout.addWidget(self.btn_pause, alignment=Qt.AlignCenter)

        layout.addLayout(button_layout)

        # --- NAV MODES TOOLBAR: MOdos de NAvegación Geckonica by NOva DulceKAli & Alan R.G.Systemas
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nova_modes = [
            ("+", "starseeker"),
            ("~", "deriva"),
            ("#", "transpose"),
            ("π", "pausa"),
            ("@", "quantic")
        ]
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        nav_layout.addSpacing(0)
        for label, mode in nova_modes:
            btn = QPushButton(label)
            btn.setFixedSize(18, 50)
            btn.setCheckable(True)
            self.nav_group.addButton(btn)
            btn.clicked.connect(lambda checked, m=mode: self.set_nav_mode(m))
            nav_layout.addWidget(btn, alignment=Qt.AlignTop)
        nav_layout.addStretch()    
        self.nav_group.buttons()[0].setChecked(True)
        
        # Selector de Cristal
        self.selec_cristal = QComboBox()
        self.selec_cristal.setFixedWidth(18)
        for value in self.gemas:
            self.selec_cristal.addItem(value)
        self.selec_cristal.currentIndexChanged.connect(self.toggle_cristal)
        nav_layout.addWidget(self.selec_cristal)
        main_layout.addLayout(nav_layout)

        main_layout.addLayout(layout)

        zoom_layout = QVBoxLayout()
        zoom_layout.setContentsMargins(0, 0, 0, 0)

        self.slider_stars = PrecisionSlider(orientation=Qt.Vertical) #QSlider(Qt.Vertical)
        self.slider_stars.setFixedHeight(250)
        self.slider_stars.setFixedWidth(25)
        self.slider_stars.setRange(0,self.submax) # Acoplamiento total
        #self.slider_stars.setValue(137) # Punto de partida equilibrado 1/137 const. de estructura fina
        self.slider_stars.setValue(self.submax) # Punto de partida máximo/(mejor medio) para no perder sensibilidad de instrumento
        self.slider_stars.sliderMoved.connect(self.change_sensibility) # Conectamos para actualizar aun en pausa
        
        zoom_layout.addWidget(self.slider_stars, alignment=Qt.AlignTop)

        self.zoom_group = QButtonGroup()
        self.zoom_group.setExclusive(True)
        self.btn_1x = QPushButton("I") #ixcl
        self.btn_10x = QPushButton("X")
        self.btn_50x = QPushButton("C")
        self.btn_100x = QPushButton("L")
        btns_zoom =[self.btn_1x, self.btn_10x, self.btn_50x, self.btn_100x]
        for btn in btns_zoom:
            btn.setCheckable(True)
            btn.setFixedSize(18, 24)
            self.zoom_group.addButton(btn)
            btn.clicked.connect(self.zoom_select)
            zoom_layout.addWidget(btn,alignment=Qt.AlignBottom)
        self.zoom_group.buttons()[3].setChecked(True)
                
        #main_layout.addWidget(self.slider_stars, alignment=Qt.AlignTop)
        main_layout.addLayout(zoom_layout)

    # EStilo Botones
    def _set_button_style(self, button, color):
        checked_style = f"background-color: {color.name()}; color: black; border: 1px solid white;"
        unchecked_style = f"background-color: #19232d; color: {color.name()}; border: 1px solid {color.name()};"
        style = f"""
            QPushButton {{
                border-radius: 35px;
                font-weight: bold;
                font-size: 12px;
                {unchecked_style}
            }}
            QPushButton:checked {{
                {checked_style}
            }}
            QPushButton:hover {{ 
                border: 2px solid white;
            }}
            /*QWidget {{
                background-color: #19232d;
            }}*/
            QLabel {{
                color: #fafafa;
                font-weight: normal;
            }}
        """
        self.setStyleSheet(style)

    # Controles UI
    def set_nav_mode(self, mode):
        self.nav_mode = mode

    def toggle_cristal(self, idx):
        gema = self.gemas[idx]
        self.radar_screen.cristal = gema
        self.radar_screen.update()

    def toggle_power(self, checked):
        self.is_on = checked
        
        if self.is_on:
            self._set_button_style(self.btn_power, self.color_btn_on if self.is_on else self.color_btn_off)
            self.btn_pause.setCheckable(True)
            self.btn_pause.setEnabled(True)
            self.dial_subspacesync.setEnabled(True)
            self.slider_stars.setEnabled(True)
            for btn in self.nav_group.buttons():
                btn.setEnabled(True)

            #self.update_visuals()
            #self.update_visible_stars() #Mantiene el universo coherente con la session
            #self.stars = self._generate_stars(self.number_stars_in_system) #ver porque tenia un numero bajo
            
        else:
            self.is_paused = False 
            self.btn_pause.setChecked(False)
            self._set_button_style(self.btn_pause, self.color_btn_play)
            self.btn_pause.setCheckable(False)
            self.btn_pause.setDisabled(True)
            self.dial_subspacesync.setDisabled(True)
            self.slider_stars.setDisabled(True)
            for btn in self.nav_group.buttons():
                btn.setDisabled(True)
            #self.radar_screen.update() 

    def sync_to_subspace(self):
        #self.warp = self.dial_subspacesync.value()/100
        
        # Ingeniería  de control
        val = self.dial_subspacesync.value()
        # Función de potencia que mantiene el signo (val^2 * sign) 
        # Normalizada para que el máximo del slider (self.submax) de un warp coherente
        self.warp = (abs(val) * val) / (self.submax * 100)
        
        self.lbl_freq.setText(f"{self.warp:.2f}")

    def toggle_pause(self, checked):
        if not self.is_on: return 
        self.is_paused = checked
        self._set_button_style(self.btn_pause, self.color_btn_pause if self.is_paused else self.color_btn_play)
        if self.is_paused:
            self.paused_lissajous_points = list(self.lissajous_points)
        self.radar_screen.update() 

    def zoom_select(self):
        
        if self.zoom_group.buttons()[3].isChecked():
            #print("1x")
            self.max_stars_x = 1

        elif self.zoom_group.buttons()[2].isChecked():
            self.max_stars_x = 3
            #print("10x")

        elif self.zoom_group.buttons()[1].isChecked():
            self.max_stars_x = 5
            #print("50x")
        else:
            self.max_stars_x = 7
            #print("100x") # Si, más estrellas es menos zoom por eso el orden de los indices está invertido!
        
        #self.max_stars = int(13700 / self.max_stars_x)
        self.number_stars_in_system = int(self.max_stars / self.max_stars_x)
        
        # For Star's Debug at the Universe
        #print (self.max_stars)
        #print (self.number_stars_in_system)
        
        # Don't use these line please!
        #self.stars = self._generate_stars(self.max_stars)
        
        self.submin = -(self.number_stars_in_system)
        self.submax = self.number_stars_in_system
        
        self.slider_stars.setRange(0,self.submax) # Acoplamiento total
        self.slider_stars.setValue(self.submax) # Maximo ZOOM
        
        
        self.change_sensibility()

    def change_sensibility(self):
        self.radar_screen.update()

    # Generators
    ''' ORINIGAL _generate_stars EI2 NOVA
    def _generate_stars(self, num_stars):
        """Genera un universo aleatorio de estrellas con profundidad (velocidad)."""
        stars_list = []
        for _ in range(num_stars):
            stars_list.append({
                'pos': QPointF(random.random() * 300, random.random() * 300),
                'vel': random.uniform(0.5, 3.5), # Diferentes Velocidades (Parallax)
                'size': random.randint(1, 2)     # Algunos píxeles más grandes
            })
        #return stars_list
        # --- LÓGICA VULKANA: Ordenamos por velocidad ('vel') ---
        # Las más lentas (lejanas) quedan primero
        #stars_list.sort(key=lambda x: x['vel'])
        return stars_list
    '''
    
    # for "Star Registry" by Ei2 "Nombrar una estrella es darle vida"
    def _generate_stars(self, num_stars):
        stars_list = []
        letras = "BCDFGHJKLMNPQRSTVWXYZ"
        for i in range(num_stars):
            # Generador de nombres tipo GKO-77
            prefix = "".join(random.choice(letras) for i in range(3))
            name = f"{prefix}-{random.randint(10, 99)}"
            stars_list.append({
                'id': i,
                'pos': QPointF(random.random() * 400, random.random() * 400),
                'vel': random.uniform(0.5, 3.5),
                'size': random.randint(1, 2),
                'name': name
            })
        return stars_list

    def _generate_lissajous_points(self):
        if not self.has_signal: return
        steps = 100
        data_len = len(self.audio_data_x)
        if data_len < steps: steps = data_len
        
        norm_x = (self.audio_data_x[:steps] - np.min(self.audio_data_x)) / (np.max(self.audio_data_x) - np.min(self.audio_data_x) + 1e-6)
        norm_y = (self.audio_data_y[:steps] - np.min(self.audio_data_y)) / (np.max(self.audio_data_y) - np.min(self.audio_data_y) + 1e-6)
        
        screen_points = [QPointF(x * 280, y * 280) for x, y in zip(norm_x, norm_y)]
        self.lissajous_points = screen_points
        self.lissajous_index = 0

    # Visual Data Trigers
    def update_audio_data(self, data_x, data_y):
        self.audio_data_x = data_x
        self.audio_data_y = data_y
        self.has_signal = self.audio_data_x is not None and self.audio_data_y is not None
        if self.has_signal:
            self._generate_lissajous_points()

    def update_visible_stars(self):
        self.number_stars_in_system = self.slider_stars.value()
        if not self.is_paused:
            self.update_visuals()
        #self.radar_screen.update() # evaluar
        #self.stars = self._generate_stars(self.number_stars_in_system) # Generamos el mapa estelar

    def update_visuals(self): # Aca Ocurre la Magía del Chamán Progamador
        
        if not self.is_on: return 
        # --- Lógica de Navegación Estelar ---
        # --- MOVER TODAS LAS ESTRELLAS SIEMPRE AUN EN EL CAMBIO DE SENSIBILIDAD ESTELAR ---
        # Modes Implemented by NOva DulceKAli & Alan R.G.Systemas with MOnkey Python Cooding Circus
        nav_mode = self.nav_mode #"starseker" #"explorers" #"deriva" #"starsekker" cambiar por un nav_mode = self.nav_mode
        for star in self.stars:
            # Universo en Movimiento Ei2
            if nav_mode == "starseeker":
                star['pos'].setX(star['pos'].x() - star['vel'] + self.warp)
            # Modos de Exploración Universal by NOva DulceKAli
            # Deriva Galáctica by NOva DulceKAli
            elif nav_mode == "deriva":
                star['pos'].setY(star['pos'].y() + math.sin(self.warp * 10 + star['vel']) * 0.1)
            elif nav_mode == "transpose":
                star['pos'].setY(star['pos'].y() + math.sin(self.warp * 10 + star['pos'].x()) * 0.1)
            elif nav_mode == "pausa": #implementar para cuando se presione el boton de play/pausa
                star['pos'].setX(star['pos'].x() - (star['vel'] * (1 + abs(self.warp))) + self.warp)
            elif nav_mode == "quantic":
                star['pos'].setX(star['pos'].x() - math.sin(self.warp * 10 + star['vel']))
            else:
                pass
            # Límites de pantalla (usando 400 por el reescalado que hicimos)
            if star['pos'].x() > 400:
                star['pos'].setX(0)
                star['pos'].setY(random.random() * 400)
            elif star['pos'].x() < 0:
                star['pos'].setX(400)
                star['pos'].setY(random.random() * 400)
        
        # --- Logic for lissajous waves ---
        if self.has_signal:
            if not self.is_paused:
                if self.lissajous_index < len(self.lissajous_points):
                    self.lissajous_index += 1
                else:
                    self.lissajous_index = 1 
            self.radar_screen.update()
        else:
            self.signal_loss_counter = (self.signal_loss_counter + 1) % 40 
            if self.signal_loss_counter % 20 == 0: 
                self.radar_screen.update()

    # Salida Geckonica    
    def closeEvent(self, event):
        # Opcional: podrías simplemente ocultarlo en vez de destruirlo
        # self.hide()
        # event.ignore()
        super().closeEvent(event)

# ──────────────────────────────────────────────────────────────────────────
# Instrumento Estelar
# ──────────────────────────────────────────────────────────────────────────
class RadarScreen(QWidget):
    def __init__(self, radar_spok, cristal = "esmeralda"):
        super().__init__(radar_spok)
        self.radar = radar_spok
        self.cristal = cristal
        #self.resize(300,300)
    
    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # --- NUEVA LÍNEA: FONDO DEL CUADRANTE ---
        # Pintamos el fondo de la pantalla (un gris muy oscuro o negro azulado)
        # Esto evita la transparencia y le da cuerpo al instrumento
        #painter.setBrush(QBrush(QColor("#19232d"))) # Ajustá este color a tu gusto
        
        # para distinto color de pantalla on/off
        color_fondo = QColor("#19232d") if self.radar.is_on else QColor("#080808")
        painter.setBrush(QBrush(color_fondo))
        
        #painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect().center(), 137, 137) # Usamos el mismo radio del radar
        # ----------------------------------------

        # 0. Retícula física (Se dibuja siempre sobre el cristal)
        # Usamos un gris más tenue (#404040) para que sea "fina" a la vista
        painter.setPen(QPen(QColor("#474747"), 1, Qt.DotLine)) 
        paso = 30  # Tamaño del cuadrado de la rejilla
        tamano_total = 400
        # Dibujamos líneas verticales y horizontales cada 20px
        for i in range(paso, tamano_total, paso):
            # Líneas Verticales
            painter.drawLine(i, 0, i, tamano_total)
            # Líneas Horizontales
            painter.drawLine(0, i, tamano_total, i)
        
        # MÁSCARA
        # Creamos la Máscara para el encendido (El marco negro con agujero)
        path = QPainterPath()
        path.setFillRule(Qt.OddEvenFill) # Esta es la clave
        # Añadimos el área total
        path.addRect(QRectF(self.rect()))
        # Añadimos el círculo (el "agujero")
        center = self.rect().center()
        radius = 137
        path.addEllipse(center, radius, radius)
        # --- OFF STATE ---
        if not self.radar.is_on:
            # Esto pintará todo el rectángulo EXCEPTO el círculo aun apagado
            painter.setBrush(QColor("#19232d")) # (Qt.black)
            #painter.setPen(Qt.NoPen)
            painter.drawPath(path)
            self.vidrio_cristal_hal()
            self.version_radarpoke()
            return 
        
        # --- GENERACIÓN DEL CAMPO ESTELAR GALACTICO DEL SYSTEMA ---
        # --- CON EQUIP, ENCENDIDO RASTREO DE SYSTEMA ESTELAR ---
        # 1. Dibujar el mapa estelar en navegación
        painter.setPen(Qt.NoPen)
        ''' THE BASIC STAR SISTEM SENSIIBLITY
        for star in self.radar.stars[:self.radar.number_stars_in_system]:
            # Estrellas más rápidas son más brillantes (están más cerca)
            color = QColor(220, 220, 220, int(star['vel'] * 170))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(star['pos'], star['size'], star['size'])
        '''
        # Las más brillantes (las últimas de la lista ordenada) son las primeras en ser detectadas
        # por el RadarSpok en frecuencias subespaciales
        # Tomamos las estrellas desde el final (las más brillantes)
        
        num = self.radar.number_stars_in_system
        # Usamos un slice que tome las últimas N estrellas de la lista ya movida
        estrellas_a_dibujar = self.radar.stars[-num:] if num > 0 else []
        # Brillo dependiente de la sensibilidad (alpha dinámico by NOva DulceKAli)
        sensitivity_factor = num / self.radar.submax
        for star in estrellas_a_dibujar:
            # aplicamos brillo dependiente
            alpha = int(star['vel'] * 170 * sensitivity_factor)
            #alpha = max(15, min(alpha, 255))  # clamp
            alpha = max(40, min(alpha, 255))  # clamp
            # Preparamos el pincel            
            color = QColor(220, 220, 220, int(star['vel'] * 170))
            painter.setBrush(QBrush(color))
            #painter.drawEllipse(star['pos'], star['size'], star['size'])
            # El tamaño ahora escala con la velocidad: las rápidas son más grandes
            size_pro = star['size'] if star['vel'] < 2.5 else star['size'] + 1
            painter.drawEllipse(star['pos'], size_pro, size_pro)
        
            # ¿Dibujamos etiqueta? (Si el mouse está encima O si fue seleccionada con clic)
            # --- ETIQUETAS (Star Registry) ---
            painter.setPen(Qt.NoPen) #para que no se dibujen mil star locker's 
            is_hovered = (self.radar.hovered_star and self.radar.hovered_star['id'] == star['id'])
            is_selected = (star['id'] in self.radar.selected_stars)
            if is_hovered or is_selected:
                painter.setPen(QPen(self.radar.color_text, 1))
                painter.setFont(QFont("Monospace", 8, QFont.Bold))
                painter.drawText(star['pos'] + QPointF(5, -5), star['name'])
                if is_selected:
                    painter.setPen(QPen(Qt.white, 1, Qt.DotLine))
                    painter.drawEllipse(star['pos'], size_pro + 4, size_pro + 4)
        
        # --- lISSAJOUUS WAVES GENERATOR OF [AUDIO X / AUDIO Y]
        # 2. Dibujar Ondas de Lissajous o Pérdida de Señal
        if self.radar.has_signal:
            points_to_draw = self.radar.paused_lissajous_points if self.radar.is_paused else self.radar.lissajous_points[:self.radar.lissajous_index]
            
            if points_to_draw:
                painter.setPen(QPen(self.radar.color_on, 2))
                painter.drawPolyline(QPolygonF(points_to_draw))
                
                if not self.radar.is_paused and self.radar.lissajous_index > 0:
                    current_point = points_to_draw[-1]
                    painter.setBrush(QBrush(self.radar.color_on))
                    painter.drawEllipse(current_point, 4, 4) 
        
        else:
            if self.radar.signal_loss_counter < 20: 
                painter.setPen(QPen(self.radar.color_text))
                painter.setFont(QFont("Monospace", 16, QFont.Bold))
                text = "SIGNAL LOSS"
                text2 ="OUT OF RANGE"
                fm = painter.fontMetrics()
                text_width = fm.width(text)
                text_height = fm.height()
                painter.drawText((345 - text_width) // 2, (270 + text_height) // 2, text)
                painter.drawText((335 - text_width) // 2, (320 + text_height) // 2, text2)
        
        # Esto pintará todo el rectángulo EXCEPTO el círculo aun apagado
        #painter.setBrush(Qt.black)
        painter.setPen(Qt.NoPen)
        #painter.drawPath(path)

        self.vidrio_cristal_hal()
        
        self.version_radarpoke()
    
    def old_vidrio_cristal(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # --- EFECTO CRISTAL (REFLEJO) ---
        # Creamos un gradiente diagonal de blanco a transparente
        reflejo = QLinearGradient(0, 0, self.width(), self.height())
        reflejo.setColorAt(0, QColor(255, 255, 255, 40))  # Blanco muy tenue (40/255 de opacidad)
        reflejo.setColorAt(0.4, QColor(255, 255, 255, 0)) # Desaparece rápido
        reflejo.setColorAt(1, QColor(255, 255, 255, 10))  # Un brillo sutil al final

        painter.setBrush(reflejo)
        painter.setPen(Qt.NoPen)
        
        # Dibujamos un círculo igual al del radar para que el reflejo solo esté en el "vidrio"
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect().center(), 137, 137)

    def vidrio_cristal_hal(self):
        """
            HAL-9000 Homenaje,
            Una Joya en el Firmamento,
            Cristal de Piedras Preciosas...
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        cristal = self.cristal
        
        if cristal == "esmeralda":
            # --- FONDO VERDE ESMERALDA (BRILLO INTERNO TIPO PIEDRA PRECIOSA) ---
            emerald_green = QRadialGradient(self.width() / 2, self.height() / 2, min(self.width(), self.height()) / 2)
            emerald_green.setColorAt(0, QColor(0, 220, 130, 137))     # Verde brillante en el centro
            emerald_green.setColorAt(0.7, QColor(0, 158, 96, 100))    # Verde intenso y profundo
            emerald_green.setColorAt(1, QColor(0, 80, 60, 86))        # Transición oscura al borde
            painter.setBrush(emerald_green)
        
        elif cristal == "rubi":
            # --- FONDO ROJO HAL (BRILLO INTERNO COLOR RUBI) ---
            hal_red = QRadialGradient(self.width() / 2, self.height() / 2, min(self.width(), self.height()) / 2)
            hal_red.setColorAt(0, QColor(255, 30, 0, 117))      # Rojo intenso en el centro // 137
            hal_red.setColorAt(0.7, QColor(200, 0, 0, 86))     # Rojo más oscuro en los bordes //100
            hal_red.setColorAt(1, QColor(100, 0, 0, 73))       # Transición suave al fondo //86
            painter.setBrush(hal_red)
       
        elif cristal == "zafiro amarillo":
            # --- FONDO ZAFIRO AMARILLO (BRILLO INTERNO DE GEMA) ---
            yellow_sapphire = QRadialGradient(self.width() / 2, self.height() / 2, min(self.width(), self.height()) / 2)
            yellow_sapphire.setColorAt(0, QColor(255, 230, 100, 137))   # Amarillo brillante en centro (oro claro)
            yellow_sapphire.setColorAt(0.7, QColor(255, 200, 50, 100))  # Amarillo intenso (tono canario)
            yellow_sapphire.setColorAt(1, QColor(180, 120, 0, 86))      # Transición a dorado oscuro
            painter.setBrush(yellow_sapphire)

        elif cristal == "jade":
            # --- FONDO VERDE JADE (BRILLO INTERNO DE GEMA) ---
            jade_green = QRadialGradient(self.width() / 2, self.height() / 2, min(self.width(), self.height()) / 2)
            jade_green.setColorAt(0, QColor(154, 207, 193, 137))   # Verde jade brillante en centro (#9ACFC1)
            jade_green.setColorAt(0.7, QColor(114, 159, 159, 100))  # Verde azulado profundo (#729F9F)
            jade_green.setColorAt(1, QColor(0, 100, 80, 86))       # Borde oscuro para profundidad
            painter.setBrush(jade_green)

        elif cristal == "zafiro azul":
            # --- FONDO AZUL ZAFIRO (BRILLO INTERNO DE GEMA) ---
            sapphire_blue = QRadialGradient(self.width() / 2, self.height() / 2, min(self.width(), self.height()) / 2)
            sapphire_blue.setColorAt(0, QColor(100, 200, 255, 137))   # Azul brillante en centro (cielo profundo)
            sapphire_blue.setColorAt(0.7, QColor(40, 90, 180, 100))   # Azul intenso (tono zafiro clásico)
            sapphire_blue.setColorAt(1, QColor(0, 30, 80, 86))        # Borde casi negro para profundidad
            painter.setBrush(sapphire_blue)      

        elif cristal == "tanzanita":
            # --- FONDO TANZANITA (BRILLO INTERNO DE GEMA RARA) ---
            tanzanite_gradient = QRadialGradient(self.width() / 2, self.height() / 2, min(self.width(), self.height()) / 2)
            tanzanite_gradient.setColorAt(0, QColor(130, 80, 200, 137))    # Azul-violeta brillante en centro
            tanzanite_gradient.setColorAt(0.7, QColor(90, 50, 160, 100))   # Violeta profundo intenso
            tanzanite_gradient.setColorAt(1, QColor(40, 20, 80, 86))       # Borde casi negro con tono púrpura
            painter.setBrush(tanzanite_gradient)   

        

        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # --- EFECTO CRISTAL (REFLEJO) ---
        reflejo = QLinearGradient(0, 0, self.width(), self.height())
        reflejo.setColorAt(0, QColor(255, 255, 255, 73))
        reflejo.setColorAt(0.4, QColor(255, 255, 255, 0))
        reflejo.setColorAt(1, QColor(255, 255, 255, 10))
        painter.setBrush(reflejo)
        painter.drawRect(self.rect())  

        if self.radar.is_on:
            # --- REFLEJO BLANCO SIMULADO (como en HAL original) ---
            '''
            # Posición del reflejo: cerca del borde superior derecho
            radio_reflejo = max(1, int(min(self.width(), self.height()) * 0.02))  # 2% del tamaño
            centro_x = int(self.width() * 0.75)
            centro_y = int(self.height() * 0.25)
            painter.setBrush(QColor(255, 255, 255, 200))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPoint(centro_x, centro_y), radio_reflejo, radio_reflejo)
            '''
            # --- REFLEJO BLANCO MÁS GRANDE Y TRANSPARENTE ---
            radio_reflejo = max(2, int(min(self.width(), self.height()) * 0.037))  # % del tamaño (más grande)
            centro_x = int(self.width() * 0.43)
            centro_y = int(self.height() * 0.43)
            painter.setBrush(QColor(255, 255, 255, 27))  # Opacidad 
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPoint(centro_x, centro_y), radio_reflejo, radio_reflejo)
            
            radio_reflejo = max(2, int(min(self.width(), self.height()) * 0.17))  # % del tamaño (más grande)    
            centro_x = int(self.width()/2)# * 0.75)
            centro_y = int(self.height()/2)# * 0.25)
            painter.setBrush(QColor(255, 255, 255, 17))  # Opacidad 
            painter.drawEllipse(QPoint(centro_x, centro_y), radio_reflejo, radio_reflejo)

        
        
        # MÁSCARA
        # Creamos la Máscara para el encendido (El marco negro con agujero)
        path = QPainterPath()
        path.setFillRule(Qt.OddEvenFill) # Esta es la clave
        # Añadimos el área total
        path.addRect(QRectF(self.rect()))
        # Añadimos el círculo (el "agujero")
        center = self.rect().center()
        radius = 137
        path.addEllipse(center, radius, radius)
        # --- OFF STATE ---
        #if not self.radar.is_on:
        # Esto pintará todo el rectángulo EXCEPTO el círculo aun apagado
        painter.setBrush(QColor("#19232d")) # (Qt.black)
        #painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        #self.version_radarpoke()
                       
        
        # Aro de Titanio-Molibdeno-Rubinio Anodizado
        # --- MARCO EXTERIOR PLATEADO (ARO DE HAL) ---
        diametro_interno = min(self.width(), self.height()) * 0.90
        diametro_externo = min(self.width(), self.height()) * 0.98
        centro_x, centro_y = self.width() / 2, self.height() / 2

        # Gradiente radial para efecto metálico plateado
        metal = QRadialGradient(centro_x - diametro_externo * 0.1, centro_y - diametro_externo * 0.1,
                                diametro_externo)
        metal.setColorAt(0, QColor(220, 220, 245))
        metal.setColorAt(0.5, QColor(160, 160, 160))
        metal.setColorAt(1, QColor(180, 180, 200))

        painter.setBrush(metal)
        painter.setPen(Qt.NoPen)
        # Dibujar aro (donut) con QPainterPath
        path = QPainterPath()
        path.addEllipse(int(centro_x - diametro_externo / 2),
                        int(centro_y - diametro_externo / 2),
                        int(diametro_externo), int(diametro_externo))
        inner_circle = QPainterPath()
        inner_circle.addEllipse(int(centro_x - diametro_interno / 2),
                                int(centro_y - diametro_interno / 2),
                                int(diametro_interno), int(diametro_interno))
        path = path.subtracted(inner_circle)
        painter.drawPath(path)   

        return 

    def version_radarpoke(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # --- VERSIÓN DE APP (Esquina superior derecha) ---
        painter.setPen(QPen(self.radar.color_btn_on))
        fuente_version = QFont("Monospace", 8, QFont.Bold)
        painter.setFont(fuente_version)
        
        # El texto que definiste
        texto_ver = f"RadarSpok {appversion}"
        '''
        # Calculamos la posición para que no se pegue al borde del círculo
        # Ajustamos x restando el ancho del texto y un margen
        margin = 5 
        x_pos = self.width() - painter.fontMetrics().width(texto_ver) - margin
        y_pos = margin + 10
        painter.drawText(x_pos, y_pos, texto_ver)
        '''
        painter.drawText(200, 12, texto_ver)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        found = None
        # Sincronizamos con la población real dibujada (las últimas N estrellas)
        num = self.radar.number_stars_in_system
        estrellas_en_pantalla = self.radar.stars[-num:] if num > 0 else []
        
        for star in estrellas_en_pantalla:
            # El sensor ahora coincide con el ojo
            diff = star['pos'] - QPointF(pos)
            if math.hypot(diff.x(), diff.y()) < 15: # Radio de captura de 15px
                found = star
                break

        if self.radar.hovered_star != found:
            self.radar.hovered_star = found
            self.update()

    def mousePressEvent(self, event):
        if self.radar.hovered_star:
            s_id = self.radar.hovered_star['id']
            if s_id in self.radar.selected_stars:
                self.radar.selected_stars.remove(s_id)
            else:
                self.radar.selected_stars.add(s_id)
        self.update()

# ──────────────────────────────────────────────────────────────────────────
# NOva Micro Ajust Parameters Control for Qdials
# ──────────────────────────────────────────────────────────────────────────
class PrecisionDial(QDial):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.precision_mode = False
        
    def mouseMoveEvent(self, event):
        # solo redibuja cuando cambia el estado
        # y detecta Shift aunque haya otros modificadores
        precision_now = bool(event.modifiers() & Qt.ShiftModifier)
        if precision_now != self.precision_mode:
            self.precision_mode = precision_now
            self.update()
        
        if self.precision_mode:
            self.setSingleStep(1)
            self.setPageStep(1)
            self.precision_mode = True
        else:
            self.setSingleStep(55)
            self.setPageStep(55)
            self.precision_mode = False
        self.update()
        super().mouseMoveEvent(event)

    # Ei2 More Events Listeners
    
    def wheelEvent(self, event):
        # Detectamos si Shift está presionado durante el scroll
        precision_now = bool(event.modifiers() & Qt.ShiftModifier)
        
        if precision_now:
            # En modo precisión, nos movemos de a 1 unidad
            # El delta de la rueda suele ser 120 por "click", lo normalizamos
            steps = event.angleDelta().y() // 120
            new_value = self.value() + steps
            self.setValue(new_value)
            
            # Forzamos el modo precisión para el paintEvent
            if not self.precision_mode:
                self.precision_mode = True
                self.update()
        else:
            # Comportamiento normal (usando los steps definidos)
            if self.precision_mode:
                self.precision_mode = False
                self.update()
            super().wheelEvent(event)
    
    def enterEvent(self, event):
        # Al entrar con el mouse, chequeamos el estado del teclado de una
        modifiers = QApplication.keyboardModifiers()
        self.precision_mode = bool(modifiers & Qt.ShiftModifier)
        self.update()
        super().enterEvent(event)

    # Esto detecta el Shift si el dial tiene el foco
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.precision_mode = True
            self.update()
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.precision_mode = False
            self.update()
        super().keyReleaseEvent(event)
    
    # Diseño de Dial de Leo
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(6, 6, -6, -6)
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2

        # Fondo oscuro metálico
        gradient_bg = QRadialGradient(center, radius)
        gradient_bg.setColorAt(0, QColor("#2c2c2c"))
        gradient_bg.setColorAt(1, QColor("#1a1a1a"))
        painter.setBrush(gradient_bg)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect)

        # Anillo exterior con efecto de brillo
        if self.precision_mode:
            # Modo activo: anillo brillante (verde cian)
            #pen = QPen(Qt.cyan, 2)
            #pen = QPen(Qt.yellow, 2)
            painter.setPen(QPen(QColor("#00ffaa"), 5))
            #painter.drawText(0, self.height(), "o") # mín
            #painter.drawText(self.height()-8, self.width(), "o") # máx
            painter.drawText(self.height()-8, 8, "o") # Marca en "ZOna "Syncro

        else:
            # Modo apagado: anillo sutil gris
            painter.setPen(QPen(QColor("#00ffaa"), 1))
            #painter.drawText(0, self.height(), ".") # mín
            #painter.drawText(self.height()-8, self.width(), ".") # máx
            #painter.setPen(QPen(QColor("#444"), 4))
            painter.drawText(self.height()-8, 8, ".") # Marca en "ZOna "Syncro

        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(rect.adjusted(-2, -2, 2, 2))

        # Marcador de valor 
        value_angle = 225 - (self.value() - self.minimum()) * 270 / (self.maximum() - self.minimum())
        angle_rad = math.radians(value_angle)  # Usa math.radians en lugar de multiplicar por 3.14159/180
        
        x = center.x() + int(radius * 0.7 * math.cos(angle_rad))
        y = center.y() - int(radius * 0.7 * math.sin(angle_rad))  # Resta para que suba hacia arriba (si no va a subir para abajo!)  
        
        marker_rect = QRect(x - 4, y - 4, 8, 8)
        painter.setPen(QPen(QColor("#00ffaa"), 1))
        painter.drawEllipse(marker_rect)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle(f"RadarSpok TM {appversion}")
    layout = QVBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)
    radar = RadarSpok()
    layout.addWidget(radar, alignment=Qt.AlignCenter)

    def generate_dummy_audio():
        t = np.linspace(0.8 * np.pi, 2048)
        data_x = np.sin(3 * t)
        data_y = np.sin(4 * t + np.pi / 4)
        radar.update_audio_data(data_x, data_y)
       
    btn_signal = QPushButton("Simular Señal de Audio", window)
    btn_signal.clicked.connect(generate_dummy_audio)
    btn_signal.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(btn_signal)

    window.show()
    sys.exit(app.exec_())