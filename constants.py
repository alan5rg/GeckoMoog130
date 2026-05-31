# constants.py

from PyQt5.QtCore import Qt

# ─── FRECUENCIAS DE NOTAS ────────────────────────────────────────────────────

# Sistema de Octavas NOva DulceKali
NOTE_FREQ = {
    # OCTAVA 4
    'DO4': 261.63, 'DO#4': 277.18, 'RE4': 293.66, 'RE#4': 311.13,
    'MI4': 329.63, 'FA4': 349.23, 'FA#4': 369.99, 'SOL4': 392.00,
    'SOL#4': 415.30, 'LA4': 440.00, 'LA#4': 466.16, 'SI4': 493.88,

    # OCTAVA 5
    'DO5': 523.25, 'DO#5': 554.37, 'RE5': 587.33, 'RE#5': 622.25,
    'MI5': 659.25, 'FA5': 698.46, 'FA#5': 739.99, 'SOL5': 783.99,
    'SOL#5': 830.61, 'LA5': 880.00, 'LA#5': 932.33, 'SI5': 987.77,
}

# ─── MAPEO QWERTY DE NOTAS ────────────────────────────────────────────────────

# Sistema de Mapeo de Teclado Fisico QWERTY
KEY_MAP = {
        # OCTAVA 4
        Qt.Key_Z: 'DO4',
        Qt.Key_S: 'DO#4',
        Qt.Key_X: 'RE4',
        Qt.Key_D: 'RE#4',
        Qt.Key_C: 'MI4',
        Qt.Key_V: 'FA4',
        Qt.Key_G: 'FA#4',
        Qt.Key_B: 'SOL4',
        Qt.Key_H: 'SOL#4',
        Qt.Key_N: 'LA4',
        Qt.Key_J: 'LA#4',
        Qt.Key_M: 'SI4',
        # OCTAVA 5
        Qt.Key_Q: 'DO5',
        Qt.Key_2: 'DO#5',
        Qt.Key_W: 'RE5',
        Qt.Key_3: 'RE#5',
        Qt.Key_E: 'MI5',
        Qt.Key_R: 'FA5',
        Qt.Key_5: 'FA#5',
        Qt.Key_T: 'SOL5',
        Qt.Key_6: 'SOL#5',
        Qt.Key_Y: 'LA5',
        Qt.Key_7: 'LA#5',
        Qt.Key_U: 'SI5',
        }

# ─── COLORES DE LAS NOTAS ────────────────────────────────────────────────────

def mix_colors(c1, c2):
    r = (int(c1[1:3],16) + int(c2[1:3],16)) // 2
    g = (int(c1[3:5],16) + int(c2[3:5],16)) // 2
    b = (int(c1[5:7],16) + int(c2[5:7],16)) // 2
    return f'#{r:02X}{g:02X}{b:02X}'

NOTA_COLORESZ = {
    'DO': '#FF0000',
    'RE': '#FF7F00',
    'MI': '#FFFF00',
    'FA': '#00FF00',
    'SOL': '#0000FF',
    'LA': '#4B0082',
    'SI': '#8B00FF',
}

NOTA_COLORES = {
    'DO': '#FF0000',
    'DO#': mix_colors(NOTA_COLORESZ['DO'], NOTA_COLORESZ['RE']),
    'RE': '#FF7F00',
    'RE#': mix_colors(NOTA_COLORESZ['RE'], NOTA_COLORESZ['MI']),
    'MI': '#FFFF00',
    'FA': '#00FF00',
    'FA#': mix_colors(NOTA_COLORESZ['FA'], NOTA_COLORESZ['SOL']),
    'SOL': '#0000FF',
    'SOL#': mix_colors(NOTA_COLORESZ['SOL'], NOTA_COLORESZ['LA']),
    'LA': '#4B0082',
    'LA#': mix_colors(NOTA_COLORESZ['LA'], NOTA_COLORESZ['SI']),
    'SI': '#8B00FF',
}

