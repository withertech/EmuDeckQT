import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QComboBox


class RAAutoSavePage(QWizardPage):
    def __init__(self, parent=None):
        super(RAAutoSavePage, self).__init__(parent)

        self.setTitle(self.tr("RetroArch Auto Save"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("Do you want to use auto save and auto load for RetroArch systems?"))
        topLabel.setWordWrap(True)
        topLabel.setTextFormat(Qt.RichText)

        combo = QComboBox()
        self.combo = combo
        combo.addItems(["No", "Yes"])

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(combo)
        self.setLayout(layout)

    def nextId(self):
        from emudeckqt import app as main
        from emudeckqt.EmuDeckWizard import EmuDeckWizard
        match self.combo.currentText():
            case "No":
                subprocess.getstatusoutput("echo \"AutoSaveLoad: No\" &>> ~/emudeck/emudeck.log")
                main.CONF.RAAutoSave = False
            case "Yes":
                subprocess.getstatusoutput("echo \"AutoSaveLoad: Yes\" &>> ~/emudeck/emudeck.log")
                main.CONF.RAAutoSave = True
                subprocess.getstatusoutput("echo \"\" > ~/emudeck/.autosave")
        return EmuDeckWizard.PageSNESAR
