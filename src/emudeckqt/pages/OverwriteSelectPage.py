from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QListWidget, QListWidgetItem


def itemChanged(item: QListWidgetItem):
    from emudeckqt import app as main
    main.CONF.overwrite[item.text()] = item.checkState() == Qt.Unchecked


class OverwriteSelectPage(QWizardPage):
    def __init__(self, parent=None):
        super(OverwriteSelectPage, self).__init__(parent)
        from emudeckqt import app as main

        self.setCommitPage(True)
        self.setTitle(self.tr("Select Emulators to Overwrite"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("<b>EmuDeck will overwrite the following Emulators configurations</b> \nWhich "
                                  "systems do you want me to keep its current configuration <b>untouched</b>?\nWe "
                                  "recomend to keep all of them unchecked so everything gets updated so any possible "
                                  "bug can be fixed.\n If you want to mantain any custom configuration on some "
                                  "emulator select its name on this list"))
        topLabel.setWordWrap(True)

        listWidget = QListWidget()
        listWidget.addItems(main.CONF.overwrite.keys())
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
        return EmuDeckWizard.PageInstall
