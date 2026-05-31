
from PyQt5.QtCore import Qt, QTimer

# Reutilizamos el PrecisionDial del Team Cangurera (simulado aquí para ejecución independiente)
from PyQt5.QtWidgets import QDial
from PyQt5.QtGui import QPainter, QPen, QColor, QRadialGradient
from PyQt5.QtCore import QRect
import math


# ────────────────────────────────────────────────────────────────
# 🎛️ Dial de Precisión Geckónico (Inyectado para independencia)
# ────────────────────────────────────────────────────────────────
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

        if self.precision_mode:
            painter.setPen(QPen(QColor("#00ffaa"), 5))
        else:
            painter.setPen(QPen(QColor("#444"), 4))

        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(rect.adjusted(-2, -2, 2, 2))

        # Marcador de valor 
        value_angle = 225 - (self.value() - self.minimum()) * 270 / (self.maximum() - self.minimum())
        angle_rad = math.radians(value_angle)
        
        x = center.x() + int(radius * 0.7 * math.cos(angle_rad))
        y = center.y() - int(radius * 0.7 * math.sin(angle_rad))  
        
        marker_rect = QRect(x - 4, y - 4, 8, 8)
        painter.setPen(QPen(QColor("#00ffaa"), 1))
        painter.drawEllipse(marker_rect)

