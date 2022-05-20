from emudeckqt.Destination import Destination


class Conf:
    branch: str = "main"
    expert: bool = False
    destination: Destination = Destination.SD
    emulationPath: str = "$HOME/Emulation/"
    romsPath: str = "$HOME/Emulation/roms/"
    toolsPath: str = "$HOME/Emulation/tools/"
    biosPath: str = "$HOME/Emulation/bios/"
    savesPath: str = "$HOME/Emulation/saves/"
    ESDEscrapData: str = ""
    InstallCHD: bool = False
    InstallPowertools: bool = False
    InstallSRM: bool = True
    InstallESDE: bool = True
    emus: dict = {
        "RetroArch": False,
        "PrimeHack": False,
        "PCSX2": False,
        "RPCS3": False,
        "Citra": False,
        "Dolphin": False,
        "DuckStation": False,
        "PPSSPP": False,
        "Yuzu": False,
        "Cemu": False,
        "Xemu": False
    }
    SECOND_TIME: str = "$HOME/emudeck/.finished"
    CUSTOM: str = "$HOME/emudeck/.custom"
    BEZELS: str = "$HOME/emudeck/.bezels"
    SAVE: str = "$HOME/emudeck/.autosave"
    RABezels: bool = True
    RAAutoSave: bool = False
    SNESAR: str = "43"
    widescreens: dict = {
        "Dolphin": True,
        "Duckstation": True,
        "BeetlePSX": True,
        "Dreamcast": True
    }
    overwrite: dict = {
        "RetroArch": True,
        "PrimeHack": True,
        "PCSX2": True,
        "RPCS3": True,
        "Citra": True,
        "Dolphin": True,
        "Duckstation": True,
        "PPSSPP": True,
        "Yuzu": True,
        "Cemu": True,
        "Xemu": True,
        "SRM": True
    }
