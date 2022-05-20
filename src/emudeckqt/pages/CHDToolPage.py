from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QComboBox


class CHDToolPage(QWizardPage):
    def __init__(self, parent=None):
        super(CHDToolPage, self).__init__(parent)

        self.setTitle(self.tr("CHD Tool"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("Do you want to install our tool to convert iso, gdi and cue to CHD format?\n\n The "
                                  "CHD format allows to have one single file insted of multiple and the final file "
                                  "takes up to 50%% less space"))
        topLabel.setWordWrap(True)

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
                main.CONF.InstallCHD = False
                return EmuDeckWizard.PagePowertools
            case "Yes":
                main.CONF.InstallCHD = True
                return EmuDeckWizard.PagePowertools
