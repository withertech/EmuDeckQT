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


class DestinationErrorPage(ErrorPage):
    def __init__(self, detail: str, parent=None):
        super(DestinationErrorPage, self).__init__("Destination Error", detail, parent)


class DestinationNotFoundErrorPage(DestinationErrorPage):
    def __init__(self, parent=None):
        super(DestinationNotFoundErrorPage, self).__init__("<b>No such file or directory</b>", parent)
