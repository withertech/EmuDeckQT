import os.path
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QListWidget, QListWidgetItem


def itemChanged(item: QListWidgetItem):
    from src.emudeckqt import app as main
    main.CONF.widescreens[item.text()] = item.checkState() == Qt.Unchecked


class WidescreenSelectPage(QWizardPage):
    def __init__(self, parent=None):
        super(WidescreenSelectPage, self).__init__(parent)
        from emudeckqt import app as main

        self.setTitle(self.tr("Select Widescreen Hacks to Disable"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("We use 16:9 widescreen hacks on some emulators, if you want them to have the "
                                  "original 4:3 aspect ratio please select them on the following list"))
        topLabel.setWordWrap(True)

        listWidget = QListWidget()
        listWidget.addItems(main.CONF.widescreens.keys())
        for i in range(listWidget.count()):
            item = listWidget.item(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

        listWidget.itemChanged.connect(itemChanged)

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(listWidget)
        self.setLayout(layout)

    def initializePage(self) -> None:
        from emudeckqt import app as main
        self.setCommitPage(not os.path.exists(main.CONF.SECOND_TIME))

    def nextId(self):
        from emudeckqt import app as main
        from emudeckqt.EmuDeckWizard import EmuDeckWizard
        if os.path.exists(main.CONF.SECOND_TIME):
            subprocess.getstatusoutput("flatpak override io.github.shiiion.primehack --filesystem=host --user")
            subprocess.getstatusoutput("flatpak override net.rpcs3.RPCS3 --filesystem=host --user")
            subprocess.getstatusoutput("flatpak override org.citra_emu.citra --filesystem=host --user")
            subprocess.getstatusoutput("flatpak override org.DolphinEmu.dolphin-emu --filesystem=host --user")
            subprocess.getstatusoutput("flatpak override org.yuzu_emu.yuzu --filesystem=host --user")
            subprocess.getstatusoutput("flatpak override app.xemu.xemu --filesystem=/run/media:rw --user")
            return EmuDeckWizard.PageOverwriteSelect
        else:
            return EmuDeckWizard.PageInstall
