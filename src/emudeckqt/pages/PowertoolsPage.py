from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QComboBox


class PowertoolsPage(QWizardPage):
    def __init__(self, parent=None):
        super(PowertoolsPage, self).__init__(parent)

        self.setTitle(self.tr("Powertools"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("Do you want to install Powertools? This can improve Emulators like Yuzu or "
                                  "Dolphin. You will need to create a password for your deck linux desktop user. "
                                  "PowerTools only has touch support, you can control it using the "
                                  "controller\n\n<b>Do not use this if you do not have basic Linux Terminal "
                                  "knowledge</b>"))
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
                main.CONF.InstallPowertools = False
                return EmuDeckWizard.PageSRM
            case "Yes":
                main.CONF.InstallPowertools = True
                return EmuDeckWizard.PageSRM
