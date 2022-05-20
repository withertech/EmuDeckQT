import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QListWidget, QListWidgetItem


def itemChanged(item: QListWidgetItem):
    from emudeckqt import app as main
    main.CONF.emus[item.text()] = item.checkState() == Qt.Checked


class EmuSelectPage(QWizardPage):
    def __init__(self, parent=None):
        super(EmuSelectPage, self).__init__(parent)
        from emudeckqt import app as main

        self.setTitle(self.tr("Select Emulators"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("What emulators do you want to install?"))
        topLabel.setWordWrap(True)

        listWidget = QListWidget()
        listWidget.addItems(main.CONF.emus.keys())
        for i in range(listWidget.count()):
            item = listWidget.item(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

        listWidget.itemChanged.connect(itemChanged)

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(listWidget)
        self.setLayout(layout)

    def nextId(self):
        from emudeckqt.EmuDeckWizard import EmuDeckWizard
        from emudeckqt import app as main
        if os.path.exists(F"{main.CONF.romsPath}/wiiu/roms/"):
            main.CONF.emus["Cemu"] = True
        if os.path.exists(
                main.CONF.CUSTOM) and os.path.exists("~/.var/app/org.libretro.RetroArch/config/retroarch"
                                                               "/retroarch.cfg"):
            return EmuDeckWizard.PageRACustom
        return EmuDeckWizard.PageRABezels
