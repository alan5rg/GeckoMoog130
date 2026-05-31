
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


# ──────────────────────────────────────────────────────────────────────────
# Leo Micro Ajust Parameters Control for QSlider // Alan5 Tunning Desing
# ──────────────────────────────────────────────────────────────────────────
class PrecisionSlider(QSlider):
    """
        Uso:
    
        app = QApplication(sys.argv)
        window = QWidget()
        layout = QVBoxLayout()

        slider = PrecisionSlider(parent, orientation=Qt.Vertical)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)

        layout.addWidget(slider)
        window.setLayout(layout)
        window.show()

        sys.exit(app.exec_())
    
    """
    def __init__(self, parent=None, orientation=Qt.Horizontal):
        super().__init__(orientation, parent)
        self.precision_mode = False
        self.setSingleStep(1)
        self.setPageStep(5)
        self._setup_style()

    def _setup_style(self):
        # Estilo base (modo apagado)
        self._base_style = """
        QSlider::groove:vertical {
            border: 1px solid #222;
            width: 5px;
            background: #222;
            border-radius: 3px;
        }
        QSlider::handle:vertical {
            background: qradialgradient(
                cx: 0.5, cy: 0.5,
                fx: 0.5, fy: 0.5,
                radius: 2,
                stop: 0 #000,
                stop: 1 #00ffaa
            );
            border: 2px solid #00ffaa;
            width: 10px;
            height: 5px;
            border-radius: 0px;
        }

        QSlider::handle:vertical:hover {
            background: qradialgradient(
                cx: 0.5, cy: 0.5,
                fx: 0.5, fy: 0.5,
                radius: 2,
                stop: 0 #000,
                stop: 1 #00ffaa
            );
            border: 3px solid #00ffaa;
            width: 12px;
            height: 6px;
            border-radius: 0px;
        }

        QSlider::sub-page:vertical {
            background: #1a1a1a;
            border-radius: 4px;
        }

        QSlider::add-page:vertical {
            background: #00ffaa;
            border-radius: 4px;
        }

        QSlider::tick {
            background: #444;
            width: 3px;
            height: 3px;
        }
        """

        # Estilo activo (modo precisión)
        self._precision_style = """
        QSlider::groove:vertical {
            border: 2px solid #222;
            width: 5px;
            background: #222;
            border-radius: 3px;
        }

        QSlider::handle:vertical {
            background: qradialgradient(
                cx: 0.5, cy: 0.5,
                fx: 0.5, fy: 0.5,
                radius: 2,
                stop: 0 #00ffaa,
                stop: 1 #000
            );
            border: 2px solid #00ffaa;
            width: 10px;
            height: 5px;
            border-radius: 0px;
        }

        QSlider::handle:vertical:hover {
            background: qradialgradient(
                cx: 0.5, cy: 0.5,
                fx: 0.5, fy: 0.5,
                radius: 2,
                stop: 0 #00ffaa,
                stop: 1 #000
            );
            border: 3px solid #00ffaa;
            width: 12px;
            height: 6px;
            border-radius: 0px;
        }

        QSlider::sub-page:vertical {
            background: #1a1a1a;
            border-radius: 4px;
        }

        QSlider::add-page:vertical {
            background: #00ffaa;
            border-radius: 4px;
        }

        QSlider::tick {
            background: #00ffaa;
            width: 4px;
            height: 4px;
        }
        """

        # Aplicar estilo base
        self.setStyleSheet(self._base_style)

    def mouseMoveEvent(self, event):
        # Detectar si Shift está presionado
        precision_now = bool(event.modifiers() & Qt.ShiftModifier)
        if precision_now != self.precision_mode:
            self.precision_mode = precision_now
            self._update_style()
        super().mouseMoveEvent(event)

    def _update_style(self):
        if self.precision_mode:
            self.setSingleStep(1)
            self.setPageStep(1)
            self.setStyleSheet(self._precision_style)
        else:
            self.setSingleStep(1)
            self.setPageStep(5)
            self.setStyleSheet(self._base_style)

    def mousePressEvent(self, event):
        # Añadir efecto de presión (opcional)
        if event.modifiers() & Qt.ShiftModifier:
            self._update_style()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Volver al estilo base si no se mantiene Shift
        if not (event.modifiers() & Qt.ShiftModifier):
            self._update_style()
        super().mouseReleaseEvent(event)  