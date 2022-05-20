from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QComboBox


class SRMPage(QWizardPage):
    def __init__(self, parent=None):
        super(SRMPage, self).__init__(parent)

        self.setTitle(self.tr("Steam Rom Manager"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("Do you want to update Steam Rom Manager?"))
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
                main.CONF.InstallSRM = True
                return EmuDeckWizard.PageESDE
            case "No":
                main.CONF.InstallSRM = False
                return EmuDeckWizard.PageESDE
