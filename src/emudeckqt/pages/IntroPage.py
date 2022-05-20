import os.path
import subprocess

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QLabel, QComboBox, QVBoxLayout, QWizard


class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(self.tr("Introduction"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("<b>Hi!</b>\nDo you want to run EmuDeck on Easy or Expert mode?\n\n<b>Easy Mode</b> takes care of everything for you, it is an unattended installation.\n\n<b>Expert mode</b> gives you a bit more of control on how EmuDeck configures your system like giving you the option to install PowerTools or keep your custom configurations per Emulator"))
        topLabel.setWordWrap(True)

        combo = QComboBox()
        self.combo = combo
        combo.addItems(["Easy", "Expert"])

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(combo)
        self.setLayout(layout)

    def nextId(self):
        from emudeckqt import app as main
        from emudeckqt.EmuDeckWizard import EmuDeckWizard
        subprocess.getstatusoutput("rm ~/emudek.log &>> /dev/null")
        subprocess.getstatusoutput("rm -rf ~/dragoonDoriseTools")
        subprocess.getstatusoutput("mkdir -p ~/emudeck")
        subprocess.getstatusoutput("echo \"\" > ~/emudeck/emudeck.log")
        if os.path.exists("~/.var/app/io.github.shiiion.primehack/config_bak"):
            subprocess.getstatusoutput("echo "" > ~/emudeck/.finished")
        match self.combo.currentText():
            case "Easy":
                main.CONF.expert = False
                return EmuDeckWizard.PageDestination
            case "Expert":
                main.CONF.expert = True
                return EmuDeckWizard.PageDestination
