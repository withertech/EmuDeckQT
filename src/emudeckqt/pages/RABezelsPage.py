import os
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QComboBox


class RABezelsPage(QWizardPage):
    def __init__(self, parent=None):
        super(RABezelsPage, self).__init__(parent)

        self.setTitle(self.tr("RetroArch Bezels"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("Do you want to use Bezels (Overlays) on RetroArch systems?"))
        topLabel.setWordWrap(True)
        topLabel.setTextFormat(Qt.RichText)

        combo = QComboBox()
        self.combo = combo
        combo.addItems(["Yes", "No"])

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(combo)
        self.setLayout(layout)

    def nextId(self):
        from emudeckqt import app as main
        from emudeckqt.EmuDeckWizard import EmuDeckWizard
        match self.combo.currentText():
            case "Yes":
                subprocess.getstatusoutput("echo \"Overlays: Yes\" &>> ~/emudeck/emudeck.log")
                main.CONF.RABezels = True
                subprocess.getstatusoutput("echo \"\" > ~/emudeck/.bezels")
            case "No":
                subprocess.getstatusoutput("echo \"Overlays: No\" &>> ~/emudeck/emudeck.log")
                main.CONF.RABezels = False
        if (not os.path.exists(main.CONF.CUSTOM)) and (not os.path.exists(main.CONF.SAVE)):
            return EmuDeckWizard.PageRAAutoSave
        else:
            return EmuDeckWizard.PageSNESAR
