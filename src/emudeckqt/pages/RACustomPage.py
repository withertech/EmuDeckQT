import os.path
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QComboBox


class RACustomPage(QWizardPage):
    def __init__(self, parent=None):
        super(RACustomPage, self).__init__(parent)

        self.setTitle(self.tr("RetroArch Custom Config"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("Do you want to use your previous RetroArch customization?"))
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
                subprocess.getstatusoutput("echo \"CustomRemain: Yes\" &>> ~/emudeck/emudeck.log")
                main.CONF.RABezels = os.path.exists(main.CONF.BEZELS)
                main.CONF.RAAutoSave = os.path.exists(main.CONF.SAVE)
            case "No":
                subprocess.getstatusoutput("echo \"CustomRemain: No\" &>> ~/emudeck/emudeck.log")
                subprocess.getstatusoutput("rm ~/emudeck/.custom &>> /dev/null")
                subprocess.getstatusoutput("rm ~/emudeck/.bezels &>> /dev/null")
                subprocess.getstatusoutput("rm ~/emudeck/.autosave &>> /dev/null")
        if (not os.path.exists(main.CONF.CUSTOM)) and (not os.path.exists(main.CONF.BEZELS)):
            return EmuDeckWizard.PageRABezels
        elif (not os.path.exists(main.CONF.CUSTOM)) and (not os.path.exists(main.CONF.SAVE)):
            return EmuDeckWizard.PageRAAutoSave
        else:
            return EmuDeckWizard.PageConclusion
