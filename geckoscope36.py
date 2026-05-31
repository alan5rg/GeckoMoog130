import sys, numpy as np, sounddevice as sd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QProgressBar, QPushButton,
                             QWidget, QComboBox, QLabel, QSlider, QCheckBox, QFrame, QButtonGroup, QDial)
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
#import qdarkstyle
#from qdarkstyle import DarkPalette

from controls.precisiondial2 import PrecisionDial

from radarspok35 import RadarScreen

appversion = "3.6" # - Full Instrumentation TimeWAtherFAll's" #Ei2 & Alan R.G.Systemas
'''
import sounddevice as sd

def list_monitors():
    try:
        devices = sd.query_devices()
        input_devices = [
            (i, device['name'])
            for i, device in enumerate(devices)
            if device['max_input_channels'] > 0 or device['name'] == 'default'
        ]
        names = [name for _, name in input_devices]
        indices = [index for index, _ in input_devices]
        return names, indices
    except Exception as e:
        print("⚠️ Error listando dispositivos:", e)
        return ["default"], [0]
'''
#import sounddevice as sd

def list_monitors():
    """
    Lista dispositivos de entrada de audio disponibles en el sistema.

    Returns:
        tuple:
            - names (list[str]): nombres formateados de dispositivos (incluye hostapi)
            - indices (list[int]): índices correspondientes para usar en sounddevice.InputStream

    Notas:
        - Se filtran únicamente dispositivos con canales de entrada (> 0).
        - Se incluye el hostapi para facilitar debugging multiplataforma.
        - Los índices devueltos corresponden al índice global de sounddevice.query_devices().
    """
    try:
        devices = sd.query_devices()
        hostapis = sd.query_hostapis()

        input_devices = []

        for i, device in enumerate(devices):
            if device["max_input_channels"] > 0:
                hostapi_index = device["hostapi"]
                hostapi_name = hostapis[hostapi_index]["name"]

                name = f"{device['name']} ({hostapi_name})"
                input_devices.append((i, name))

        names = [name for _, name in input_devices]
        indices = [index for index, _ in input_devices]

        return names, indices

    except Exception as e:
        print("⚠️ Error listando dispositivos:", e)
        return ["default"], [0]
    
class GeckoScope(QMainWindow):
    """
        Osciloscopio y analizador de espectro en tiempo real basado en sounddevice + NumPy + PyQtGraph.

        Permite:
            - Seleccionar dispositivos de entrada de audio
            - Visualizar la señal en dominio temporal (osciloscopio)
            - Visualizar el espectro mediante FFT

        Arquitectura:
            - Captura de audio mediante InputStream (callback)
            - Buffer compartido actualizado en tiempo real
            - Renderizado periódico mediante QTimer
    """
    def __init__(self, samplerate=44100, blocksize=1024, mode="large"):
        super().__init__()
        self.setWindowTitle(f"🦎 GeckoScopeAlone v{appversion}")
        self.resize(760, 300)
        
        # --- Parámetros de Control ---
        self.mode = mode
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.gain = 1.0
        self.persistence = 0.5  # Suavizado de FFT
        self.timebase = 1.0 # Factor de zoom X para el osciloscopio
        self.data = np.zeros(self.blocksize)
        self.fft_smooth = np.zeros(self.blocksize // 2 + 1)
        
        # --- Parámetros Waterfall ---
        self.waterfall_depth = 100  # Cuántas líneas de historia guardar
        self.cascada_mode_on = True # FFF (Future Feature Future)
        # Matriz de datos (inicializada en negro/cero)
        self.waterfall_data = np.zeros((self.waterfall_depth, self.blocksize // 2 + 1))
        self.color_maps = [
            ("VI", "viridis"),  # El estándar científico (Azul -> Verde -> Amarillo). Muy limpio.
            ("MA", "magma"),    # Más oscuro que el inferno, tonos púrpura profundos. Muy elegante.
            ("IN", "inferno"),  # Las llamas te rodean, es momento de pagar por tus pecados!
            ("PL", "plasma"),   # Tonos violetas y rosados neón. Bien futurista.
            ("CI", "cividis")   # Escala de azules y amarillos (optimizado para daltonismo y alto contraste).
        ]
        self.colormap = "viridis"

        # --- Parámetros VUMeter ---
        self.vulevel = 0.0

        # Audio Setup
        self.monitors, self.monitor_indices = list_monitors()
        #self.current_device_index = self.monitor_indices[0] if self.monitor_indices else None

        # Buscar dispositivo "default"
        default_index = next(
            (idx for name, idx in zip(self.monitors, self.monitor_indices) 
            if "default" in name.lower()),
            self.monitor_indices if self.monitor_indices else None
        )
        self.current_device_index = default_index

        # Encontrar el índice del dispositivo "default" en la lista de nombres
        self.default_index_in_list = next(
            (i for i, name in enumerate(self.monitors) if "default" in name.lower()),
            0  # Si no se encuentra, usar el primer elemento
        )

        self.init_ui()
        self.start_stream()
        
        # Timer para UI (~60 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(16)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # -----------------------------------------------------------
        # --- PANEL LATERAL IZQUIERDO (Instrumentación Geckonica) ---
        # -----------------------------------------------------------
        panel_left = QFrame()
        #panel_left.setFixedWidth(73)
        #panel_left.setStyleSheet("border-right: 1px solid #1A1A1A;") #background-color: #0A0A0A; #dejamos que el fondo lo maneje GeckoMoog
               
        layout_left = QVBoxLayout(panel_left)
        layout_left.setContentsMargins(0, 0, 0, 0) #Widget sin Bordes (Máxima ocupación de espacio disponible!!!)
        #layout_left.addSpacing(100)
        #'''
        # Selector de Dispositivo
        self.selector = QComboBox()
        self.selector.setFixedWidth(30)
        self.selector.addItems(self.monitors)
        self.selector.setCurrentIndex(self.default_index_in_list)  # Seleccionar "default" si existe
        self.selector.currentIndexChanged.connect(self.change_device)
        #layout_center.addWidget(QLabel("🎧 Audio Source:"))
        layout_left.addWidget(self.selector)
        #'''
        lbl_info = QLabel(f"v.{appversion}") # 🦎 GeckoScope v{appversion}  🦎  Rate: {self.samplerate}Hz  🦎")
        lbl_info.setStyleSheet("color: #3F8") #; font-size: 16px;")
        layout_left.addWidget(lbl_info, alignment=Qt.AlignTop)
        layout_left.addWidget(QLabel("🌊 OSC"))

        layout_left.addWidget(QLabel("⏳"))
        self.sld_time = PrecisionDial() #QDial()
        self.sld_time.setFixedSize(30,30)
        self.sld_time.setRange(1, 100)
        self.sld_time.setValue(100)
        self.sld_time.valueChanged.connect(lambda v: setattr(self, 'timebase', v/100.0))
        layout_left.addWidget(self.sld_time)

        layout_left.addStretch()

        if self.mode == "large":
            self.wf_grid = QCheckBox("#WF")
            self.wf_grid.setChecked(False)
            self.wf_grid.stateChanged.connect(self.toggle_grid_WF)
            layout_left.addWidget(self.wf_grid)

        self.chk_freeze = QCheckBox("[❄️]")
        layout_left.addWidget(self.chk_freeze)
        
        layout_principal.addWidget(panel_left)

        # -----------------------------------------------------------------------
        # --- CUERPO CENTRAL (Gráficos Osciloscopio y Analizador de Espectro) ---
        # -----------------------------------------------------------------------
        layout_center = QVBoxLayout()
        '''
        # Selector de Dispositivo
        self.selector = QComboBox()
        self.selector.addItems(self.monitors)
        self.selector.currentIndexChanged.connect(self.change_device)
        #layout_center.addWidget(QLabel("🎧 Audio Source:"))
        layout_center.addWidget(self.selector)
        '''
        # Osciloscopio Plot
        self.osc_plot = pg.PlotWidget(title="Osciloscopio Geckoniano")
        self.osc_plot.setBackground("#19232d")
        self.osc_plot.setBaseSize(770,250)
        self.osc_plot.setMinimumWidth(290)
        self.osc_plot.showGrid(x=True, y=True, alpha=0.3)
        self.osc_curve = self.osc_plot.plot(pen=pg.mkPen("#00ffaa", width=1.5))
        self.osc_plot.setYRange(-1, 1)

        layout_center.addWidget(self.osc_plot)

        # FFT Plot
        self.fft_plot = pg.PlotWidget(title="Espectro Geckoniano")
        self.fft_plot.setBackground("#19232d")
        self.fft_plot.setBaseSize(770,250)
        self.fft_plot.setMinimumWidth(290)
        self.fft_plot.showGrid(x=True, y=True, alpha=0.3)
        self.fft_curve = self.fft_plot.plot(pen=pg.mkPen("#00d4ff", width=1.5), fillLevel=0, brush=(0, 212, 255, 40))

        layout_center.addWidget(self.fft_plot)

        layout_principal.addLayout(layout_center, stretch=4)

        # ----------------------------------------------------------
        # --- PANEL LATERAL DERECHO (Instrumentación Large Mode) ---
        # ----------------------------------------------------------
        panel_right = QFrame()
        #panel_right.setFixedWidth(73)
        #panel_right.setStyleSheet("border-left: 1px solid #1A1A1A;") #background-color: #0A0A0A; #dejamos que el fondo lo maneje GeckoMoog
        layout_right = QVBoxLayout(panel_right)
        layout_right.setContentsMargins(0, 0, 0, 0)

        #layout_right.addStretch()
        #layout_right.addSpacing(100)
        layout_right.addWidget(QLabel("🌊 OSC"))
        
        # Gain Dial
        layout_right.addWidget(QLabel("△"))
        self.sld_gain = PrecisionDial()
        self.sld_gain.setFixedSize(30,30)
        self.sld_gain.setRange(1, 200) # 0.1x a 20x
        self.sld_gain.setValue(25)
        self.sld_gain.valueChanged.connect(lambda v: setattr(self, 'gain', v/10.0))
        layout_right.addWidget(self.sld_gain)

        # Grid Toggle
        self.osc_grid = QCheckBox("#")
        self.osc_grid.setChecked(True)
        self.osc_grid.stateChanged.connect(self.toggle_grid_OSC)
        layout_right.addWidget(self.osc_grid)

        layout_right.addWidget(QLabel("📊 FFT"))

        # Persistence Dial
        layout_right.addWidget(QLabel("PSTC"))
        self.sld_persist = PrecisionDial()
        self.sld_persist.setFixedSize(30,30)
        self.sld_persist.setRange(0, 95)
        self.sld_persist.setValue(45)
        self.sld_persist.valueChanged.connect(lambda v: setattr(self, 'persistence', v/100.0))
        layout_right.addWidget(self.sld_persist)

        # Log Scale Toggle
        self.chk_log = QCheckBox("Log")
        self.chk_log.stateChanged.connect(self.toggle_log)
        layout_right.addWidget(self.chk_log)

        self.fft_grid = QCheckBox("#")
        self.fft_grid.setChecked(True)
        self.fft_grid.stateChanged.connect(self.toggle_grid_FFT)
        layout_right.addWidget(self.fft_grid)

        layout_principal.addWidget(panel_right)

        if self.mode == "large":
            # --- VUMETROS GECKONICOS
            # GeckoVolumeter Channel A
            self.vu_barA = QProgressBar()
            self.vu_barA.setOrientation(Qt.Vertical)
            self.vu_barA.setRange(0, 100)
            self.vu_barA.setTextVisible(False)
            # Estilo CSS para que parezca un LED meter
            self.vu_barA.setStyleSheet("QProgressBar::chunk { background-color: #3F8; }")
            layout_principal.addWidget(self.vu_barA)

            # GeckoVolumeter Channel B
            self.vu_barB = QProgressBar()
            self.vu_barB.setOrientation(Qt.Vertical)
            self.vu_barB.setRange(0, 100)
            self.vu_barB.setTextVisible(False)
            # Estilo CSS para que parezca un LED meter
            self.vu_barB.setStyleSheet("QProgressBar::chunk { background-color: #3F8; }")
            layout_principal.addWidget(self.vu_barB)

            # --- Gecko WAtherFAlls TM ---
            self.wf_plot = pg.PlotWidget()
            self.wf_plot.setBackground("#19232d")
            #self.wf_plot.showGrid(x=True, y=True)
            self.wf_plot.setMinimumWidth(137)
            self.wf_plot.setMaximumWidth(173)
            #self.wf_plot.setMaximumWidth(440)
            self.wf_plot.setXRange(0,37)
            self.wf_plot.setYRange(0,100)
            # Bloqueamos la interacción para que no se descuadre al clickear
            #self.wf_plot.setMouseEnabled(x=False, y=False)
            #self.wf_plot.setMenuEnabled(False)        
            self.wf_img = pg.ImageItem()
            self.wf_plot.addItem(self.wf_img)
            # Mapa de colores 
            colormap = pg.colormap.get(self.colormap) 
            self.wf_img.setLookupTable(colormap.getLookupTable())
            layout_principal.addWidget(self.wf_plot)

            # Botones Toogle Colormap WAterfalls
            # --- NAV MODES TOOLBAR: MOdos de NAvegación Geckonica by NOva DulceKAli & Alan R.G.Systemas
            nav_layout = QVBoxLayout()
            nav_layout.setSpacing(37)
            nav_layout.setContentsMargins(0, 0, 0, 0)
            self.nav_group = QButtonGroup(self)
            self.nav_group.setExclusive(True)
            
            #nav_layout.addSpacing(17)
            #nav_layout.addStretch()    

            for label, mode in self.color_maps:
                btn = QPushButton(label)
                btn.setFixedSize(22, 22)
                btn.setCheckable(True)
                self.nav_group.addButton(btn)
                btn.clicked.connect(lambda checked, m=mode: self.toogle_colormap(m))
                nav_layout.addWidget(btn, alignment=Qt.AlignTop)
            
            self.nav_group.buttons()[0].setChecked(True)
            layout_principal.addLayout(nav_layout)

    def toogle_colormap(self, mode):
        self.colormap = mode
        colormap = pg.colormap.get(self.colormap)
        self.wf_img.setLookupTable(colormap.getLookupTable())
        ''' Evaluar como actualizar el cristal de RadarSpok en su clase RadarScreen
        if mode=="viridis": # El estándar científico (Azul -> Verde -> Amarillo). Muy limpio.
            self.radarscreen.cristal = "esmeralda"
            self.radarscreen.update()
        elif mode=="magma":  # Más oscuro que el inferno, tonos púrpura profundos. Muy elegante.
            self.radarscreen.cristal = "zafiro azul"
            self.radarscreen.update()
        elif mode=="inferno":  # Las llamas te rodean, es momento de pagar por tus pecados!
            self.radarscreen.cristal = "rubi"
            self.radarscreen.update()
        elif mode=="plasma":   # Tonos violetas y rosados neón. Bien futurista.
            self.radarscreen.cristal = "tanzanita"
            self.radarscreen.update()
        elif mode=="cividis":   # Escala de azules y amarillos (optimizado para daltonismo y alto contraste).
            self.radarscreen.cristal = "zafiro amarillo"
            self.radarscreen.update()
        '''

    def toggle_grid_OSC(self, state):
        self.osc_plot.showGrid(x=state, y=state)

    def toggle_grid_FFT(self, state):
        self.fft_plot.showGrid(x=state, y=state)

    def toggle_grid_WF(self, state):
        if self.mode == "large":
            self.wf_plot.showGrid(x=state, y=state)

    def toggle_log(self, state):
        self.fft_plot.setLogMode(x=(state == Qt.Checked), y=False)

    def start_stream(self):
        """
        Inicia el stream de captura de audio con el dispositivo seleccionado.

        Maneja reinicio seguro del stream previo si existiera.
        """
        try:
            if hasattr(self, "stream"):
                self.stream.stop(); self.stream.close()
            self.stream = sd.InputStream(
                device=self.current_device_index,
                channels=1,
                samplerate=self.samplerate,
                blocksize=self.blocksize,
                callback=self.audio_callback
            )
            self.stream.start()
        except Exception as e:
            print("⚠️ Error Stream:", e)

    def change_device(self, idx):
        """
        Cambia el dispositivo de entrada activo según la selección del usuario.

        Args:
            idx (int): índice del dispositivo seleccionado en el QComboBox.
        """
        self.current_device_index = self.monitor_indices[idx]
        self.start_stream()

    def audio_callback(self, indata, frames, time, status):
        """
        Callback de audio ejecutado en tiempo real por sounddevice.

        Args:
            indata (np.ndarray): buffer de entrada de audio.
            frames (int): cantidad de frames en el buffer.
            time (CData): timestamps del stream.
            status (CallbackFlags): estado del stream (overflow, underflow, etc).

        Notas:
            - Se realiza copia explícita del buffer para evitar corrupción de datos.
            - Se normaliza a float32 para procesamiento posterior.
        """
        # Testing
        #if status:
        #    print("⚠️ audio_callback status:", status)

        # Aplicamos la ganancia directamente al buffer de entrada
        #self.data = indata[:, 0] * self.gain

        if not self.chk_freeze.isChecked():
            #self.data = indata[:, 0] * self.gain
            # Limpieza y Normalizado en mejores practicas por NOva DulceKALi
            #data = indata[:, 0].astype(np.float32) # normaliza el audio

            # Creo que NOva, te Olvidaste la Ganancia
            data = indata[:, 0].astype(np.float32) # normaliza el audio
            data_gain = data * self.gain # Aplicamos Ganancia
            self.data = data_gain.copy() # trabaja con una "copia" por .copy()

    def update_plots(self):
        """
        Actualiza las visualizaciones de osciloscopio y espectro (FFT).

        Se ejecuta periódicamente mediante QTimer (~50 FPS).
        """
        # Update Osciloscopio
        # Timebase: Ajustamos el rango visible de datos
        visible_samples = int(self.blocksize * self.timebase)
        display_data = self.data[:visible_samples]
        self.osc_curve.setData(display_data)
        
        # Update FFT con suavizado (Persistence)
        #raw_fft = np.abs(np.fft.rfft(self.data)) / self.blocksize

        # Filtro anti Lag Spectral NOva DUlceKali
        window = np.hanning(len(self.data))
        data_windowed = self.data * window

        raw_fft = np.abs(np.fft.rfft(data_windowed)) / self.blocksize

        # Formula de persistencia: smooth = (anterior * factor) + (nuevo * (1-factor))
        self.fft_smooth = (self.fft_smooth * self.persistence) + (raw_fft * (1 - self.persistence))
        
        freqs = np.fft.rfftfreq(self.blocksize, 1.0 / self.samplerate)
        self.fft_curve.setData(freqs, self.fft_smooth)

        if self.mode == "large":
            # LÓGICA VUMETER
            # Calculamos el valor RMS o el pico máximo del bloque actual
            rms = np.sqrt(np.mean(self.data**2))
            # Convertimos a una escala 0-100 (ajustable según sensibilidad)
            target_vu = min(int(rms * 500), 100) 
            # Suavizado básico del medidor para que no sea tan "nervioso"
            self.vulevel = (self.vulevel * 0.7) + (target_vu * 0.3)
            
            if target_vu >= 80:
                # ALerta de Saturacion extrema 
                self.vu_barA.setStyleSheet("QProgressBar::chunk { background-color: #ff0000; }")
                self.vu_barB.setStyleSheet("QProgressBar::chunk { background-color: #ff0000; }")
            elif target_vu >= 73 and target_vu < 86:
                # Precaución Limite del Espacio Sonoro
                self.vu_barA.setStyleSheet("QProgressBar::chunk { background-color: #fffa00; }")
                self.vu_barB.setStyleSheet("QProgressBar::chunk { background-color: #fffa00; }")
            elif target_vu > 27 and target_vu < 73:
                self.vu_barA.setStyleSheet("QProgressBar::chunk { background-color: #3f8; }")                
                self.vu_barB.setStyleSheet("QProgressBar::chunk { background-color: #3f8; }")                
            else:
                # demasiado bajo se pierde en el oscuro frio del espacio azul
                self.vu_barA.setStyleSheet("QProgressBar::chunk { background-color: #000ad2; }")                
                self.vu_barB.setStyleSheet("QProgressBar::chunk { background-color: #000ad2; }")                

            self.vu_barA.setValue(int(self.vulevel))
            # implementar logica estereo, por ahora copia
            self.vu_barB.setValue(int(self.vulevel))

            # LÓGICA WATERFALL
            # Desplazamos la matriz hacia abajo una fila
            self.waterfall_data = np.roll(self.waterfall_data, -1, axis=0)
            # Insertamos la nueva fila de la FFT (en la última posición)
            self.waterfall_data[-1, :] = self.fft_smooth

            # Actualizamos la imagen
            if self.cascada_mode_on:
                # Transpuesta == Cascada de Sonido
                self.wf_plot.setXRange(0,37)
                self.wf_plot.setYRange(0,100)
                self.wf_img.setImage(self.waterfall_data.T, autoLevels=True) # .T porque ImageItem usa (x, y)
            else:
                # No Transpuesta == Cascada Temporal en X 
                self.wf_plot.setXRange(0,100)
                self.wf_plot.setYRange(0,37)
                self.wf_img.setImage(self.waterfall_data, autoLevels=True)

    def closeEvent(self, event):
        if hasattr(self, "stream"):
            self.stream.stop(); self.stream.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Aplicamos el estilo Dark para que todo combine
    #app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
    ventana = GeckoScope()
    ventana.show()
    sys.exit(app.exec_())