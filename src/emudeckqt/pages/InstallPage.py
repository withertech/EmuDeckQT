import crypt
import getpass
import os.path
import re
import spwd
import subprocess
import threading

import pexpect as pexpect
import qtutils
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMutex, QWaitCondition, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout, QProgressBar, QInputDialog, QMessageBox, \
    QLineEdit

from emudeckqt.Destination import Destination


def sudo(password: str, command: str = "") -> str | bool:
    if command == "":
        s = pexpect.spawn("sudo -s")
    else:
        s = pexpect.spawn(F"sudo {command}")
    i = s.expect([".*[$#]", "assword.*: "])
    if i == 0:
        print("didnt need password!")
        pass
    elif i == 1:
        print("sending password")
        s.sendline(password)
        j = s.expect([".*[$#]", "Sorry, try again"])
        if j == 0:
            pass
        elif j == 1:
            return False
    else:
        return False
    return s.after


class InstallPage(QWizardPage):
    def __init__(self, parent=None):
        super(InstallPage, self).__init__(parent)
        self.installer = InstallPage.InstallWorker(self)
        self.complete = False
        self.total = 0
        self.step = 0
        self.setTitle(self.tr("Installing"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        top_label = QLabel(self.tr("Installing EmuDeck"))
        top_label.setWordWrap(True)
        top_label.setTextFormat(Qt.RichText)

        bar = QProgressBar()
        self.bar = bar

        status_label = QLabel(self.tr(""))
        status_label.setWordWrap(True)
        status_label.setTextFormat(Qt.RichText)
        self.statusLabel = status_label

        layout = QVBoxLayout()
        layout.addWidget(top_label)
        layout.addWidget(bar)
        layout.addWidget(status_label)
        self.installer.status_signal.connect(self.statusLabel.setText)
        self.installer.password_signal.connect(self.password)
        self.installer.start_signal.connect(self.start)
        self.installer.next_signal.connect(self.next)
        self.installer.finish_signal.connect(self.finish)
        self.setLayout(layout)

    def password(self):
        from emudeckqt.EmuDeckWizard import EmuDeckWizard
        text, ok = QInputDialog.getText(self, "Hey!", F"Hey! This is not an SteamDeck. EmuDeck can work just fine, "
                                                      F"but you need to have a valid account\n\nWe need your password "
                                                      F"to make sure everything works as expected\n\n"
                                                      F"Password for {getpass.getuser()}:",
                                        QLineEdit.Password)
        if ok and text != "" and sudo(text):
            self.installer.password = text
        else:
            self.wizard().setStartId(EmuDeckWizard.PagePasswordIncorrect)
            self.wizard().restart()
            self.wizard().setStartId(0)

    def finish(self):
        self.statusLabel.setText("<b>Finished</B>")
        self.percentage(self.total)
        self.complete = True
        self.completeChanged.emit()

    def start(self):
        from emudeckqt import app as main

        if not main.CONF.expert:
            main.CONF.emus = {
                "RetroArch": True,
                "PrimeHack": True,
                "PCSX2": True,
                "RPCS3": True,
                "Citra": True,
                "Dolphin": True,
                "DuckStation": True,
                "PPSSPP": True,
                "Yuzu": True,
                "Cemu": True,
                "Xemu": True
            }
        count: int = 0

        # Downloading files
        # count += 1

        # Installing AppImages
        if main.CONF.InstallESDE:
            count += 1
        if main.CONF.destination != "$HOME":
            count += 1
        if main.CONF.InstallESDE:
            count += 1

        # Installing Flatpaks
        for item in main.CONF.emus.values():
            if item:
                count += 1

        self.total = count

    def isComplete(self) -> bool:
        return self.complete

    def initializePage(self) -> None:
        self.installer.install()

    def percentage(self, step: int):
        self.bar.setValue(int((step / self.total) * 100))

    def next(self):
        self.step += 1
        self.percentage(self.step)

    def nextId(self):
        from emudeckqt.EmuDeckWizard import EmuDeckWizard
        return EmuDeckWizard.PageConclusion

    class InstallWorker(QThread):
        start_signal = pyqtSignal()
        next_signal = pyqtSignal()
        finish_signal = pyqtSignal()
        status_signal = pyqtSignal(str)
        password_signal = pyqtSignal()

        def __init__(self, parent=None):
            QThread.__init__(self, parent)
            self.password = ""

        def install(self):
            self.start()

        def set_password(self, password: str):
            self.password = password

        def download_files(self):
            from emudeckqt import app as main
            self.status_signal.emit(F"<b>Downloading files from {main.CONF.branch} channel...</b>")
            subprocess.getstatusoutput("mkdir -p ~/dragoonDoriseTools")
            subprocess.getstatusoutput("mkdir -p ~/dragoonDoriseTools/EmuDeck")
            subprocess.getstatusoutput("git clone https://github.com/dragoonDorise/EmuDeck.git "
                                       "~/dragoonDoriseTools/EmuDeck &>> ~/emudeck/emudeck.log")
            subprocess.getstatusoutput(f"cd ~/dragoonDoriseTools/EmuDeck; git checkout {main.CONF.branch} &>> "
                                       f"~/emudeck/emudeck.log")
            self.next_signal.emit()

        def install_appimages(self):
            from emudeckqt import app as main
            if main.CONF.InstallESDE:
                self.status_signal.emit("<b>Installing EmulationStation Desktop Edition</b>")

                subprocess.getstatusoutput(F"curl https://gitlab.com/es-de/emulationstation-de/-/raw/master/es-app"
                                           F"/assets/latest_steam_deck_appimage.txt --output \"{main.CONF.toolsPath}"
                                           F"latesturl.txt\" >> ~/emudeck/emudeck.log")
                latestURL = subprocess.getoutput(F"grep \"https://gitlab\" \"{main.CONF.toolsPath}latesturl.txt\"")
                subprocess.getstatusoutput(F"curl {latestURL} --output \"{main.CONF.toolsPath}EmulationStation-DE\""
                                           F"-x64_SteamDeck.AppImage >> ~/emudeck/emudeck.log")
                subprocess.getstatusoutput(F"rm \"{main.CONF.toolsPath}latesturl.txt\"")
                subprocess.getstatusoutput(
                    F"chmod +x \"{main.CONF.toolsPath}EmulationStation-DE-x64_SteamDeck.AppImage\"")
                self.next_signal.emit()

            if main.CONF.destination != "$HOME":
                if not os.path.exists(main.CONF.ESDEscrapData):
                    if "SD" in main.CONF.destinations.keys() and main.CONF.destination == main.CONF.destinations.get(
                            "SD"):
                        self.status_signal.emit("<b>Moving EmulationStation downloaded media to the SD Card</b>")
                    else:
                        self.status_signal.emit(
                            F"<b>Moving EmulationStation downloaded media to {main.CONF.destination}</b>")
                    subprocess.getstatusoutput(F"mv ~/.emulationstation/downloaded_media {main.CONF.ESDEscrapData}")
                    subprocess.getstatusoutput(F"rm -rf ~/.emulationstation/downloaded_media")
                    subprocess.getstatusoutput(F"mkdir -p {main.CONF.ESDEscrapData}")
                    subprocess.getstatusoutput(F"ln -s {main.CONF.ESDEscrapData} ~/.emulationstation/downloaded_media")
                    self.next_signal.emit()

            if main.CONF.InstallSRM:
                self.status_signal.emit("<b>Installing Steam Rom Manager</b>")

                subprocess.getstatusoutput(
                    "rm -f ~/Desktop/Steam-ROM-Manager-2.3.29.AppImage &>> ~/emudeck/emudeck.log")
                subprocess.getstatusoutput(
                    "curl -L \"$(curl -s https://api.github.com/repos/SteamGridDB/steam-rom-manager"
                    "/releases/latest | grep -E 'browser_download_url.*AppImage' | grep -ve 'i386' "
                    "| cut -d '\"' -f 4)\" > ~/Desktop/Steam-ROM-Manager.AppImage")
                subprocess.getstatusoutput("chmod +x ~/Desktop/Steam-ROM-Manager.AppImage")
                self.next_signal.emit()

        def install_flatpaks(self):
            from emudeckqt import app as main

            if main.CONF.emus["PCSX2"]:
                self.status_signal.emit("<b>Installing PCSX2</b>")
                subprocess.getstatusoutput("flatpak install flathub net.pcsx2.PCSX2 -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                subprocess.getstatusoutput("flatpak override net.pcsx2.PCSX2 --filesystem=host --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run net.pcsx2.PCSX2\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/pcsx2.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/pcsx2.sh")
                self.next_signal.emit()

            if main.CONF.emus["PrimeHack"]:
                self.status_signal.emit("<b>Installing PrimeHack</b>")
                subprocess.getstatusoutput("flatpak install flathub io.github.shiiion.primehack -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                subprocess.getstatusoutput("flatpak override io.github.shiiion.primehack --filesystem=host --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run io.github.shiiion.primehack\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/primehack.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/primehack.sh")
                self.next_signal.emit()

            if main.CONF.emus["RPCS3"]:
                self.status_signal.emit("<b>Installing RPCS3</b>")
                subprocess.getstatusoutput("flatpak install flathub net.rpcs3.RPCS3 -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                subprocess.getstatusoutput("flatpak override net.rpcs3.RPCS3 --filesystem=host --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run net.rpcs3.RPCS3\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/rpcs3.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/rpcs3.sh")
                self.next_signal.emit()

            if main.CONF.emus["Citra"]:
                self.status_signal.emit("<b>Installing Citra</b>")
                subprocess.getstatusoutput("flatpak install flathub org.citra_emu.citra -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                subprocess.getstatusoutput("flatpak override org.citra_emu.citra --filesystem=host --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run org.citra_emu.citra\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/citra.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/citra.sh")
                self.next_signal.emit()

            if main.CONF.emus["Dolphin"]:
                self.status_signal.emit("<b>Installing Dolphin</b>")
                subprocess.getstatusoutput("flatpak install flathub org.DolphinEmu.dolphin-emu -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                subprocess.getstatusoutput("flatpak override org.DolphinEmu.dolphin-emu --filesystem=host --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run org.DolphinEmu.dolphin-emu\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/dolphin-emu.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/dolphin-emu.sh")
                self.next_signal.emit()

            if main.CONF.emus["DuckStation"]:
                self.status_signal.emit("<b>Installing DuckStation</b>")
                subprocess.getstatusoutput("flatpak install flathub org.duckstation.DuckStation -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                # subprocess.getstatusoutput("flatpak override org.duckstation.DuckStation --filesystem=host --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run org.duckstation.DuckStation\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/duckstation.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/duckstation.sh")
                self.next_signal.emit()

            if main.CONF.emus["RetroArch"]:
                self.status_signal.emit("<b>Installing RetroArch</b>")
                subprocess.getstatusoutput("flatpak install flathub org.libretro.RetroArch -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                # subprocess.getstatusoutput("flatpak override org.libretro.RetroArch --filesystem=host --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run org.libretro.RetroArch\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/RetroArch.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/RetroArch.sh")
                self.next_signal.emit()

            if main.CONF.emus["PPSSPP"]:
                self.status_signal.emit("<b>Installing PPSSPP</b>")
                subprocess.getstatusoutput("flatpak install flathub org.ppsspp.PPSSPP -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                # subprocess.getstatusoutput("flatpak override org.ppsspp.PPSSPP --filesystem=host --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run org.ppsspp.PPSSPP\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/ppsspp.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/ppsspp.sh")
                self.next_signal.emit()

            if main.CONF.emus["Yuzu"]:
                self.status_signal.emit("<b>Installing Yuzu</b>")
                subprocess.getstatusoutput("flatpak install flathub org.yuzu_emu.yuzu -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                subprocess.getstatusoutput("flatpak override org.yuzu_emu.yuzu --filesystem=host --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run org.yuzu_emu.yuzu\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/yuzu.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/yuzu.sh")
                self.next_signal.emit()

            if main.CONF.emus["Xemu"]:
                self.status_signal.emit("<b>Installing Xemu</b>")
                subprocess.getstatusoutput("flatpak install flathub app.xemu.xemu -y --system	&>> "
                                           "~/emudeck/emudeck.log")
                subprocess.getstatusoutput("flatpak override app.xemu.xemu --filesystem=/run/media:rw --user")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run app.xemu.xemu\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/xemu.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/xemu.sh")
                self.next_signal.emit()

            if "SD" in main.CONF.destinations.keys() and main.CONF.destination == main.CONF.destinations.get("SD"):
                self.status_signal.emit("<b>Creating roms folder in your SD Card...</b>")
            elif "Internal" in main.CONF.destinations.keys() and main.CONF.destination == main.CONF.destinations.get(
                    "Internal"):
                self.status_signal.emit("<b>Creating roms folder in your home folder...</b>")
            else:
                self.status_signal.emit(F"<b>Creating roms folder in {main.CONF.destination}...</b>")

            subprocess.getstatusoutput(F"mkdir -p \"{main.CONF.romsPath}\"")
            subprocess.getstatusoutput(F"mkdir -p \"{main.CONF.biosPath}\"")
            subprocess.getstatusoutput(F"mkdir -p \"{main.CONF.biosPath}/yuzu/\"")
            subprocess.getstatusoutput(F"rsync -r {main.getResourcesDir()}/roms/ \"{main.CONF.romsPath}\" "
                                       F"&>> ~/emudeck/emudeck.log")

            if main.CONF.emus["Cemu"]:
                self.status_signal.emit("<b>Installing Cemu</b>")
                subprocess.getstatusoutput("flatpak remote-add --user --if-not-exists withertech "
                                           "https://repo.withertech.com/repository/flatpak/withertech.flatpakrepo &>> "
                                           "~/emudeck/emudeck.log")
                subprocess.getstatusoutput("flatpak install withertech info.cemu.Cemu -y &>> ~/emudeck/emudeck.log")
                subprocess.getstatusoutput("flatpak install flathub org.winehq.Wine -y &>> ~/emudeck/emudeck.log")
                if os.path.exists(F"{main.CONF.romsPath}/wiiu/roms/"):
                    subprocess.getstatusoutput(F"mv {main.CONF.romsPath}wiiu/roms/ {main.CONF.romsPath}wiiutemp &>> "
                                               F"~/emudeck/emudeck.log")
                    subprocess.getstatusoutput(
                        F"mv {main.CONF.romsPath}wiiu/Cemu.exe {main.CONF.romsPath}wiiu/Cemu.bak &>>"
                        F" ~/emudeck/emudeck.log")
                    subprocess.getstatusoutput(F"rsync -ri {main.CONF.romsPath}wiiu/ "
                                               F"~/.var/app/info.cemu.Cemu/data/cemu/ &>> ~/emudeck/emudeck.log")
                    subprocess.getstatusoutput(F"mv {main.CONF.romsPath}wiiu/ {main.CONF.romsPath}wiiu_delete_me &>> "
                                               F"~/emudeck/emudeck.log")
                    subprocess.getstatusoutput(F"mv {main.CONF.romsPath}wiiutemp/ {main.CONF.romsPath}wiiu/ &>> "
                                               F"~/emudeck/emudeck.log")
                subprocess.getstatusoutput(F"echo \"#!/bin/sh\n"
                                           F"/usr/bin/flatpak run info.cemu.Cemu\" > "
                                           F"\"{main.CONF.toolsPath}\"launchers/cemu.sh")
                subprocess.getstatusoutput(F"chmod +x \"{main.CONF.toolsPath}\"launchers/cemu.sh")

        def run(self):
            self.start_signal.emit()

            # self.download_files()

            self.install_appimages()
            if re.search("Jupiter", subprocess.getoutput("cat /sys/devices/virtual/dmi/id/product_name")) is None:
                self.password_signal.emit()
                while self.password == "":
                    self.sleep(1)
                for package in ("packagekit-qt5", "flatpak", "rsync", "unzip"):
                    subprocess.getstatusoutput(F"pacman -Q {package} &>> ~/emudeck/emudeck.log || sudo pacman -Sy "
                                               F"--noconfirm ${package} &>> ~/emudeck/emudeck.log")
                if re.search(getpass.getuser(), subprocess.getoutput("awk '/'${USER}'/ {if ($1 ~ /wheel/) print}' "
                                                                     "/etc/group")) is None:
                    subprocess.getstatusoutput("sudo usermod -a -G wheel ${USER} &>> ~/emudeck/emudeck.log")
                    subprocess.getstatusoutput("newgrp wheel")
                if re.search("root", subprocess.getoutput("stat -c %U ${HOME}/Desktop")):
                    subprocess.getstatusoutput("sudo chown -R ${USER}:${USER} ~/Desktop &>> ~/emudeck/emudeck.log")
            self.install_flatpaks()

            self.finish_signal.emit()
