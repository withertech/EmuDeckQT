from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QComboBox


class SNESARPage(QWizardPage):
    def __init__(self, parent=None):
        super(SNESARPage, self).__init__(parent)

        self.setTitle(self.tr("SNES Aspect Ratio"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("What SNES Aspect ratio do you want to use?\n\n<b>4:3</b> Classic CRT "
                                  "TV\n\n<b>8:7</b> Real SNES Internal resolution"))
        topLabel.setWordWrap(True)
        topLabel.setTextFormat(Qt.RichText)

        combo = QComboBox()
        self.combo = combo
        combo.addItems(["4:3", "8:7"])

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(combo)
        self.setLayout(layout)

    def nextId(self):
        from emudeckqt import app as main
        from emudeckqt.EmuDeckWizard import EmuDeckWizard
        match self.combo.currentText():
            case "4:3":
                main.CONF.SNESAR = "43"
            case "8:7":
                main.CONF.SNESAR = "87"
        return EmuDeckWizard.PageWidescreenSelect
