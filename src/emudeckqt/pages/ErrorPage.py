from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizardPage, QWizard, QLabel, QVBoxLayout


class ErrorPage(QWizardPage):
    def __init__(self, error: str, detail: str, parent=None):
        super(ErrorPage, self).__init__(parent)

        self.setFinalPage(True)
        self.setTitle(self.tr(F"Error: {error}"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        top_label = QLabel(self.tr(detail))
        top_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(top_label)
        self.setLayout(layout)

    def nextId(self) -> int:
        return -1


class PasswordErrorPage(ErrorPage):
    def __init__(self, detail: str, parent=None):
        super(PasswordErrorPage, self).__init__("Password Error", detail, parent)


class PasswordIncorrectErrorPage(PasswordErrorPage):
    def __init__(self, parent=None):
        super(PasswordIncorrectErrorPage, self).__init__("<b>Password incorrect</b>", parent)


class SDErrorPage(ErrorPage):
    def __init__(self, detail: str, parent=None):
        super(SDErrorPage, self).__init__("SDCard Error", detail, parent)


class SDNotWritableErrorPage(SDErrorPage):
    def __init__(self, parent=None):
        super(SDNotWritableErrorPage, self).__init__("<b>SD Card not writable</b>\nMake sure your SD Card is writable",
                                                     parent)


class SDIncompatibleFSErrorPage(SDErrorPage):
    def __init__(self, parent=None):
        super(SDIncompatibleFSErrorPage, self).__init__("<b>Your SD Card is not compatible with EmuDeck.</b>\nMake "
                                                        "sure to use a supported filesystem like EXT4. Formatting "
                                                        "your SD Card from SteamUI will fix this.\n\n Go back to "
                                                        "Gaming Mode, Settings, System and select Format SD Card "
                                                        "there. This will delete all your SD contents.",
                                                        parent)


class SDNonexistentErrorPage(SDErrorPage):
    def __init__(self, parent=None):
        super(SDNonexistentErrorPage, self).__init__("<b>SD Card not detected</b>\nMake sure your SD Card is inserted "
                                                     "and start again the installation",
                                                     parent)
