"""
QT port for EmuDeck
"""
import argparse

from PyQt5 import QtWidgets

from emudeckqt import EmuDeckWizard
from emudeckqt.Conf import Conf
from pathlib import Path

CONF: Conf = Conf()

app: QtWidgets.QApplication
exitcode: int = 0


def getResourcesDir():
    Path(__file__).joinpath("resources")


def main():
    global app
    global exitcode
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Dev Mode (BETA/DEV/MAIN)", nargs='?', type=str, const="MAIN", default="MAIN")
    args = parser.parse_args()
    match args.mode:
        case "MAIN":
            CONF.branch = "main"
        case "BETA":
            CONF.branch = "beta"
        case "DEV":
            CONF.branch = "dev"
    app = QtWidgets.QApplication(sys.argv)
    wizard = EmuDeckWizard.EmuDeckWizard()
    wizard.show()
    ret = app.exec_()
    if exitcode > 0:
        ret = exitcode
    sys.exit(ret)
