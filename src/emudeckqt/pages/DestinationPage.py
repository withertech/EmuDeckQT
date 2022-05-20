import os.path
import subprocess

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizard, QLabel, QWizardPage, QComboBox, QVBoxLayout

from emudeckqt.Destination import Destination


class DestinationPage(QWizardPage):
    def __init__(self, parent=None):
        super(DestinationPage, self).__init__(parent)

        self.setTitle(self.tr("Destination"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("Do you want to install your roms on your SD Card or on your Internal Storage?"))
        topLabel.setWordWrap(True)

        combo = QComboBox()
        self.combo = combo
        combo.addItems(["SD", "Internal"])

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(combo)
        self.setLayout(layout)

    def initializePage(self) -> None:
        from emudeckqt import app as main
        self.setCommitPage(not main.CONF.expert)

    def nextId(self):
        from emudeckqt import app as main
        from emudeckqt.EmuDeckWizard import EmuDeckWizard

        def makeDirs():
            subprocess.getstatusoutput(F"mkdir -p \"{main.CONF.emulationPath}\"")
            subprocess.getstatusoutput(F"mkdir -p \"{main.CONF.toolsPath}\"launchers")
            subprocess.getstatusoutput(F"mkdir -p \"{main.CONF.savesPath}\"")

            subprocess.getstatusoutput(F"find \"{main.CONF.romsPath}\" -name \"readme.md\" -type f -delete &>> "
                                       F"~/emudeck/emudeck.log")

        def setOverridesAndReturn():
            if main.CONF.expert:
                return EmuDeckWizard.PageCHDTool
            else:
                return EmuDeckWizard.PageInstall

        match self.combo.currentText():
            case "SD":
                subprocess.getstatusoutput("echo \"Storage: SD\" &>> ~/emudeck/emudeck.log")
                main.destination = Destination.SD
                subprocess.getstatusoutput("echo \"\" > ~/emudeck/.SD")
                if os.path.exists("/dev/mmcblk0p1"):
                    sdCardFull = subprocess.getoutput("findmnt -n --raw --evaluate --output=target -S /dev/mmcblk0p1")
                    subprocess.getstatusoutput(F"touch {sdCardFull}/testwrite")
                    if not os.path.exists(F"{sdCardFull}/testwrite"):
                        return EmuDeckWizard.PageSDNotWritableError
                    subprocess.getstatusoutput(F"ln -s {sdCardFull}/testwrite {sdCardFull}/testwrite.link")
                    if not os.path.exists(F"{sdCardFull}/testwrite.link"):
                        return EmuDeckWizard.PageSDIncompatibleFSError
                    os.remove(F"{sdCardFull}/testwrite.link")
                    os.remove(F"{sdCardFull}/testwrite")
                else:
                    return EmuDeckWizard.PageSDNonexistentError
                main.CONF.emulationPath = F"{sdCardFull}/Emulation/"
                main.CONF.romsPath = F"{sdCardFull}/Emulation/roms/"
                main.CONF.toolsPath = F"{sdCardFull}/Emulation/tools/"
                main.CONF.biosPath = F"{sdCardFull}/Emulation/bios/"
                main.CONF.savesPath = F"{sdCardFull}/Emulation/saves/"
                main.CONF.ESDEscrapData = F"{sdCardFull}/Emulation/tools/downloaded_media"
                makeDirs()
                return setOverridesAndReturn()

            case "Internal":
                subprocess.getstatusoutput("echo \"Storage: INTERNAL\" &>> ~/emudeck/emudeck.log")
                main.CONF.destination = Destination.INTERNAL
                makeDirs()
                return setOverridesAndReturn()
