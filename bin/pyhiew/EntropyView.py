"""
EntropyView.py - Visual entropy analysis using PyQt5

Features:
- Color-coded entropy visualization
- Double-click to seek in Hiew and close
- Caches results for fast re-open

Requires: pip install PyQt5 (32-bit Python)
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass
from typing import ClassVar

import hiew

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout,
        QHBoxLayout, QLabel
    )
    from PyQt5.QtGui import QPainter, QColor, QPen
    from PyQt5.QtCore import Qt
except ImportError:
    hiew.Message("Error", "PyQt5 not installed.\npip install PyQt5")
    raise SystemExit


# ---------------------------------------------------------------------------
# Entropy calculation
# ---------------------------------------------------------------------------

def calculate_entropy(data: bytes) -> float:
    """Calculate Shannon entropy (0.0 - 8.0 for bytes)."""
    if not data:
        return 0.0

    freq = [0] * 256
    for b in data:
        freq[b] += 1

    length = len(data)
    entropy = 0.0
    for count in freq:
        if count:
            p = count / length
            entropy -= p * math.log2(p)

    return entropy


@dataclass
class EntropyData:
    """Cached entropy data for a file."""
    filename: str
    file_size: int
    chunk_size: int
    entropies: list[float]


class EntropyCache:
    """Module-level cache for entropy data."""
    _cache: ClassVar[dict[tuple[str, int], EntropyData]] = {}

    @classmethod
    def get(cls, filename: str, size: int) -> EntropyData | None:
        return cls._cache.get((filename, size))

    @classmethod
    def store(cls, data: EntropyData) -> None:
        cls._cache[(data.filename, data.file_size)] = data


def compute_entropy(chunk_size: int = 512) -> EntropyData | None:
    """Compute file entropy, using cache if available."""
    data = hiew.GetData()
    filename = data.filename
    file_size = data.filelength

    if not filename or file_size == 0:
        return None

    cached = EntropyCache.get(filename, file_size)
    if cached:
        return cached

    entropies = []
    offset = 0

    while offset < file_size:
        size = min(chunk_size, file_size - offset)
        ret, chunk = hiew.FileRead(offset, size)
        if ret > 0 and chunk:
            entropies.append(calculate_entropy(chunk))
        else:
            entropies.append(0.0)
        offset += chunk_size

    result = EntropyData(
        filename=filename,
        file_size=file_size,
        chunk_size=chunk_size,
        entropies=entropies
    )

    EntropyCache.store(result)
    return result


# ---------------------------------------------------------------------------
# Qt Widgets
# ---------------------------------------------------------------------------

class EntropyWidget(QWidget):
    """Custom widget to draw entropy graph."""

    def __init__(self, entropy_data: EntropyData, parent: 'EntropyWindow'):
        super().__init__()
        self.entropy_data = entropy_data
        self.parent_window = parent
        self.hover_idx = -1
        self.selected_idx = -1
        self.setMouseTracking(True)
        self.setMinimumSize(600, 200)
        self.setFocusPolicy(Qt.StrongFocus)

    @property
    def entropies(self) -> list[float]:
        return self.entropy_data.entropies

    def idx_to_offset(self, idx: int) -> int:
        return idx * self.entropy_data.chunk_size

    def x_to_idx(self, x: int) -> int:
        margin = 40
        graph_w = self.width() - margin * 2
        n = len(self.entropies)

        if n and margin <= x <= self.width() - margin:
            idx = int((x - margin) * n / graph_w)
            return max(0, min(n - 1, idx))
        return -1

    def paintEvent(self, event):
        if not self.entropies:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        margin = 40
        graph_w = w - margin * 2
        graph_h = h - margin * 2

        painter.fillRect(0, 0, w, h, QColor(30, 30, 30))

        painter.setPen(QPen(QColor(60, 60, 60), 1))
        for i in range(9):
            y = margin + (graph_h * i) // 8
            painter.drawLine(margin, y, w - margin, y)

        painter.setPen(QColor(150, 150, 150))
        for i in range(9):
            y = margin + (graph_h * i) // 8
            painter.drawText(5, y + 4, f"{8 - i}")

        n = len(self.entropies)
        bar_w = max(1, graph_w / n)

        for i, ent in enumerate(self.entropies):
            x = margin + (i * graph_w) // n
            bar_h = int((ent / 8.0) * graph_h)
            y = margin + graph_h - bar_h

            if ent < 3:
                color = QColor(80, 200, 80)
            elif ent < 6:
                color = QColor(200, 200, 80)
            else:
                color = QColor(200, 80, 80)

            if i == self.selected_idx:
                color = QColor(100, 150, 255)
            elif i == self.hover_idx:
                color = color.lighter(140)

            painter.fillRect(int(x), y, max(1, int(bar_w) - 1), bar_h, color)

        info_y = h - 10
        painter.setPen(QColor(255, 255, 255))

        if 0 <= self.hover_idx < n:
            offset = self.idx_to_offset(self.hover_idx)
            ent = self.entropies[self.hover_idx]
            text = f"Offset: 0x{offset:08X}  Entropy: {ent:.3f}  [Double-click to jump]"
            painter.drawText(margin, info_y, text)
        else:
            painter.drawText(margin, info_y, "Hover over graph | Double-click to jump in Hiew")

    def mouseMoveEvent(self, event):
        self.hover_idx = self.x_to_idx(event.x())
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected_idx = self.x_to_idx(event.x())
            self.update()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            idx = self.x_to_idx(event.x())
            if idx >= 0:
                offset = self.idx_to_offset(idx)
                self.parent_window.jump_and_close(offset)

    def leaveEvent(self, event):
        self.hover_idx = -1
        self.update()


class EntropyWindow(QMainWindow):
    """Main window for entropy visualization."""

    def __init__(self, entropy_data: EntropyData):
        super().__init__()
        self.entropy_data = entropy_data
        self.jump_offset: int | None = None

        filename = os.path.basename(entropy_data.filename)
        self.setWindowTitle(f"Entropy: {filename}")
        self.setMinimumSize(800, 350)
        self.setStyleSheet("background-color: #1e1e1e; color: #ccc;")

        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Info bar
        info = QHBoxLayout()
        info.addWidget(QLabel(f"<b>File:</b> {filename}"))
        info.addWidget(QLabel(f"<b>Size:</b> {entropy_data.file_size:,} bytes"))

        avg_ent = sum(entropy_data.entropies) / len(entropy_data.entropies)
        info.addWidget(QLabel(f"<b>Avg:</b> {avg_ent:.2f}"))
        info.addStretch()
        layout.addLayout(info)

        # Graph
        self.graph = EntropyWidget(entropy_data, self)
        layout.addWidget(self.graph)

        # Legend
        legend = QHBoxLayout()
        for label, color in [
            ("Low <3 (text/code)", "#50c850"),
            ("Medium 3-6", "#c8c850"),
            ("High >6 (packed)", "#c85050"),
            ("Selected", "#6496ff"),
        ]:
            lbl = QLabel(f"<font color='{color}'>&#9632;</font> {label}")
            legend.addWidget(lbl)
        legend.addStretch()
        layout.addLayout(legend)

        # Instructions
        instr = QLabel("<i>Double-click to jump | Esc to close</i>")
        instr.setStyleSheet("color: #888;")
        layout.addWidget(instr)

    def jump_and_close(self, offset: int):
        """Set jump offset and close window."""
        self.jump_offset = offset
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


def main():
    data = hiew.GetData()
    if not data.filename:
        hiew.Message("Error", "No file open")
        return

    entropy_data = compute_entropy(chunk_size=512)

    if not entropy_data or not entropy_data.entropies:
        hiew.Message("Error", "Could not read file")
        return

    app = QApplication.instance() or QApplication(sys.argv)

    window = EntropyWindow(entropy_data)
    window.show()
    app.exec_()

    if window.jump_offset is not None:
        hiew.ReturnOffset(window.jump_offset)


main()
