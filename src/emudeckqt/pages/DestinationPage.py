import os.path
import subprocess

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizard, QLabel, QWizardPage, QComboBox, QVBoxLayout, QFileDialog


def testLocationValid(name: str, path: str, simulate: bool = False) -> bool:
    from emudeckqt import app as main
    subprocess.getstatusoutput(F"touch {path}/testwrite")
    if not os.path.exists(F"{path}/testwrite"):
        ret = False
    else:
        subprocess.getstatusoutput(F"ln -s {path}/testwrite {path}/testwrite.link")
        if not os.path.exists(F"{path}/testwrite.link"):
            ret = False
        else:
            ret = True
            if not simulate: main.CONF.destinations[name] = path
    subprocess.getstatusoutput(F"rm -f \"{path}/testwrite\" \"{path}/testwrite.link\"")
    return ret


class DestinationPage(QWizardPage):
    def __init__(self, parent=None):
        from emudeckqt import app as main
        super(DestinationPage, self).__init__(parent)

        self.setTitle(self.tr("Destination"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("Where would you like Emudeck to be installed?"))
        topLabel.setWordWrap(True)

        combo = QComboBox()
        self.combo = combo
        combo.addItems(main.CONF.destinations.keys())

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(combo)
        self.setLayout(layout)

    def initializePage(self) -> None:
        from emudeckqt import app as main
        self.setCommitPage(not main.CONF.expert)
        if os.path.exists("/dev/mmcblk0p1"):
            sdCardFull = subprocess.getoutput("findmnt -n --raw --evaluate --output=target -S /dev/mmcblk0p1")
            testLocationValid("SD", sdCardFull)
            self.combo.addItem("SD")
        if main.CONF.expert:
            main.CONF.destinations["Custom"] = "CUSTOM"
            self.combo.addItem("Custom")

    def nextId(self):
        from emudeckqt import app as main
        from emudeckqt.EmuDeckWizard import EmuDeckWizard

        if main.CONF.destinations[self.combo.currentText()] == "CUSTOM":
            main.CONF.destination = QFileDialog.getExistingDirectory(self, "Select a destination for the "
                                                                                     "Emulation directory.")
            if main.CONF.destination != "CUSTOM":
                if not testLocationValid("Custom", main.CONF.destination, True):
                    return EmuDeckWizard.PageDestinationNotFoundError
            else:
                return EmuDeckWizard.PageDestinationNotFoundError
        else:
            main.CONF.destination = main.CONF.destinations[self.combo.currentText()]
        main.CONF.emulationPath = F"{main.CONF.destination}/Emulation/"
        main.CONF.romsPath = F"{main.CONF.destination}/Emulation/roms/"
        main.CONF.toolsPath = F"{main.CONF.destination}/Emulation/tools/"
        main.CONF.biosPath = F"{main.CONF.destination}/Emulation/bios/"
        main.CONF.savesPath = F"{main.CONF.destination}/Emulation/saves/"
        main.CONF.ESDEscrapData = F"{main.CONF.destination}/Emulation/tools/downloaded_media"

        subprocess.getstatusoutput(F"mkdir -p \"{main.CONF.emulationPath}\"")
        subprocess.getstatusoutput(F"mkdir -p \"{main.CONF.toolsPath}\"launchers")
        subprocess.getstatusoutput(F"mkdir -p \"{main.CONF.savesPath}\"")
        subprocess.getstatusoutput(F"find \"{main.CONF.romsPath}\" -name \"readme.md\" -type f -delete &>> "
                                   F"~/emudeck/emudeck.log")
        if main.CONF.expert:
            return EmuDeckWizard.PageCHDTool
        else:
            return EmuDeckWizard.PageInstall
