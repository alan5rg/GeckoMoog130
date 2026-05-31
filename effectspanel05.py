# effectspanel01.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel
from PyQt5.QtCore import Qt
from controls.precisiondial2 import PrecisionDial

# for Leo MECO Indicator
from PyQt5.QtGui import QPainter, QColor

geckoappversion = "0.5"

# ------------------------------------------------------
# --- MECO (Me Encanta Conectar Obvio)
# ------------------------------------------------------
class MECOIndicator(QWidget):
    """
        Indicador visual MECO: "Me Conecté" (Module Connected)
        Despreocupate Este Code es Negligible 🦎✨
    """
    
    def __init__(self, module_name, parent=None):
        super().__init__(parent)
        self.module_name = module_name
        self.is_connected = False
        
        self.setFixedSize(30, 10)
        self.setToolTip(f"{module_name}: {'Conectado' if self.is_connected else 'Desconectado'}")
    
    def paintEvent(self, event):
        """Dibujar el indicador MECO"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Color según estado: ROJO (desconectado) o VERDE (conectado)
        color = QColor("#00ffaa") if self.is_connected else QColor("#b80000")
        
        # Dibujar círculo
        painter.setBrush(color)
        painter.setPen(QColor("#cccccc"))#00ff88"))
        #painter.drawEllipse(1, 1, 14, 14)
        painter.drawRect(5,1,30,30)
        
        # Brillo interno
        painter.setBrush(color.lighter(150))
        painter.setPen(Qt.NoPen)
        #painter.drawEllipse(3, 3, 10, 10)
        painter.drawRect(8,3,30,30)
    
    def set_connected(self, is_connected):
        """Establecer estado de conexión"""
        self.is_connected = is_connected
        self.update()
        self.setToolTip(f"{self.module_name}: {'Conectado' if is_connected else 'Desconectado'}")

# ------------------------------------------------------
# --- IU EffectsPanel by Leo
# ------------------------------------------------------
class EffectsPanel(QWidget):
    """Panel de efectos con diales para controlar cada módulo"""
    
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self.dials = {}  # {module_name: {param_name: dial}}
        
        self._build_ui()
        self._apply_style()
    
    def _build_ui(self):
        """Construir UI dinámicamente según los módulos"""
        main_layout = QVBoxLayout()
        #main_layout.setContentsMargins(0, 5, 0, 5)

        # Título principal
        self.brand = QLabel(f"GeckoMoog Leo Effects Panel v.{geckoappversion}")
        self.brand.setStyleSheet("""
            font-size: 20px;
            color: #00ffaa;
            font-weight: bold
        """)
        main_layout.addWidget(self.brand, alignment=Qt.AlignRight)
        
        # Crear QGroupBox para cada módulo
        for module_name, module in self.router.modules.items():
            #print("modules in effectspanel:", module_name)
            if module_name != "ENG":
                group_box = self._create_module_group(module_name, module)
                main_layout.addWidget(group_box)
  
        self.setLayout(main_layout)
    
    def _create_module_group(self, module_name, module):
        """Crear QGroupBox para un módulo específico"""
        # Obtener nombre legible del módulo
        display_name = getattr(module, 'name', module_name)
        
        # Mapeo de nombres legibles
        names_map = {
            'VIB': 'Vibrato Geckonico',
            'FIL': 'Filter Paso Bajo',
            'DLY': 'Delay con Feedback',
            'CHO': 'Chorus Geckonico',
            'MOE': 'Moog Overdrive Engine',
            'REV': 'Reverb Schroeder'
        }
        
        full_name = f"{display_name}: {names_map.get(display_name, 'Efecto')}"
        
        # Crear QGroupBox
        group_box = QGroupBox(full_name)
        layout = QHBoxLayout()
        #layout.setSpacing(15)
        
        # Crear diales para cada parámetro del módulo
        self.dials[module_name] = {}

        # MECO Indicator
        meco = MECOIndicator(module_name)
        layout.addWidget(meco, alignment=Qt.AlignTop)
        self.dials[module_name] ['meco'] = meco  # ✅ Guardar en el dict
        
        # Obtener atributos numéricos del módulo (excluyendo privados y métodos)
        for attr_name in dir(module):
            if attr_name.startswith('_') or attr_name in ['name', 'is_connected']:
                continue
            
            attr = getattr(module, attr_name, None)
            
            # Solo crear diales para atributos numéricos
            if isinstance(attr, (int, float)):
                if module_name == "DLY" or module_name == "CHO":
                    dial = self._create_dial(module, attr_name, attr, ancho=50, alto=50)
                else:
                    dial = self._create_dial(module, attr_name, attr, ancho=60, alto=60)
                layout.addWidget(dial)
                self.dials[module_name] [attr_name] = dial
        
        group_box.setLayout(layout)

        group_box.setStyleSheet("""
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
        
        return group_box
    
    def _create_dial(self, module, param_name, current_value, ancho=50, alto=50):
        """Crear un dial para un parámetro"""
        # Contenedor para dial + label
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        #layout.setSpacing(5)
        
        # Crear dial con rangos según el parámetro
        dial = PrecisionDial(self)
        
        dial.setFixedSize(ancho, alto)
       
        # Configurar rangos según el parámetro
        ranges = self._get_dial_range(param_name, current_value)
        dial.setRange(ranges['min'], ranges['max'])
        dial.setValue(int(current_value * ranges['scale']))
        
        # Conectar cambios
        dial.valueChanged.connect(
            lambda value: self._on_dial_changed(module, param_name, value, ranges)
        )
        
        # Label con nombre del parámetro
        label = QLabel(param_name)
        label.setAlignment(Qt.AlignCenter)
        
        #layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(dial, alignment=Qt.AlignCenter)
        container.setLayout(layout)
        
        return container
    
    def _get_dial_range(self, param_name, current_value):
        """Definir rango y escala para cada parámetro"""
        ranges = {
            'rate': {'min': 0, 'max': 100, 'scale': 100},           # 0.0 - 10.0 Hz
            'depth': {'min': 0, 'max': 100, 'scale': 10000},        # 0.0 - 0.01
            'cutoff': {'min': 0, 'max': 100, 'scale': 100},         # 0.0 - 1.0
            'delay_ms': {'min': 10, 'max': 1000, 'scale': 1},       # 10 - 1000 ms
            'feedback': {'min': 0, 'max': 100, 'scale': 100},       # 0.0 - 1.0
            'mix': {'min': 0, 'max': 100, 'scale': 100},            # 0.0 - 1.0
            'drive': {'min': 10, 'max': 300, 'scale': 100},         # 0.1 - 3.0
            'decay': {'min': 10, 'max': 100, 'scale': 100},         # 0.1 - 1.0
        }
        
        return ranges.get(param_name, {'min': 0, 'max': 100, 'scale': 100})
    
    def _on_dial_changed(self, module, param_name, dial_value, ranges):
        """Actualizar parámetro del módulo cuando cambia el dial"""
        # Convertir valor del dial al rango real del parámetro
        real_value = dial_value / ranges['scale']
        
        # Aplicar al módulo
        setattr(module, param_name, real_value)
        
        print(f"[EFFECTS] {module.name}.{param_name} = {real_value:.4f}")

    def _update_mecos(self):
        """Actualizar estado de MECOs (llamado desde GeckoMoogPatchMatrix)"""
        # for Testing Debug 
        #print(f"[MECO UPDATE] Iniciando actualización de MECOs")
        #print(f"[MECO UPDATE] Módulos en router: {list(self.router.modules.keys())}")
        #print(f"[MECO UPDATE] Dials disponibles: {list(self.dials.keys())}")
        for module_name, module in self.router.modules.items():
            if module_name == "ENG":
                continue
            
            # ✅ Leer directamente del módulo
            is_connected = getattr(module, 'is_connected', False)
            #print(f"[MECO UPDATE] {module_name}: is_connected = {is_connected}")
            
            # Actualizar MECO
            if module_name in self.dials:
                #print(f"[MECO UPDATE] {module_name} encontrado en dials")
                if 'meco' in self.dials[module_name]:
                    meco = self.dials[module_name] ['meco']
                    #print(f"[MECO UPDATE] {module_name} MECO encontrado, actualizando a {is_connected}")
                    meco.set_connected(is_connected)
                else:
                    print(f"[MECO UPDATE] ❌ {module_name} NO tiene 'meco' en dials")
                    print(f"[MECO UPDATE] Keys en dials[{module_name}]: {list(self.dials[module_name].keys())}")
            else:
                print(f"[MECO UPDATE] ❌ {module_name} NO encontrado en dials")

    def _apply_style(self):
        """Aplicar estilo general"""
        self.setStyleSheet("""
            QLabel {
                color: #ccc;
                font-size: 9px;
                font-weight: normal;
            }
        """)

        