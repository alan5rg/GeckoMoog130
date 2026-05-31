from PyQt5.QtWidgets import QDial
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QRadialGradient
import math

# ──────────────────────────────────────────────────────────────────────────
# NOva Micro Ajust Parameters Control for Qdials
# ──────────────────────────────────────────────────────────────────────────
class PrecisionDial(QDial):
    """
        Uso:
        dial = PrecisionDial(parent)
        dial.setMinimum(0)
        dial.setMaximum(100)
        dial.setValue(50)    
    """
    def __init__(self, parent=None):
        super().__init__(parent)
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
        else:
            self.setSingleStep(5)
            self.setPageStep(5)
        super().mouseMoveEvent(event)

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
            painter.drawText(0, self.height(), "o")

        else:
            # Modo apagado: anillo sutil gris
            painter.setPen(QPen(QColor("#00ffaa"), 1))
            painter.drawText(0, self.height(), ".")
            painter.setPen(QPen(QColor("#444"), 4))

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

