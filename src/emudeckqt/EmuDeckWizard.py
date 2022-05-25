from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizard, QMessageBox


class EmuDeckWizard(QWizard):
    NUM_PAGES = 17

    (
        PageIntro, PageDestination, PageCHDTool, PagePowertools, PageSRM, PageESDE, PageEmuSelect, PageRACustom,
        PageRABezels, PageRAAutoSave, PageSNESAR, PageWidescreenSelect, PageOverwriteSelect, PageInstall,
        PagePasswordIncorrect, PageDestinationNotFoundError,
        PageConclusion
    ) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(EmuDeckWizard, self).__init__(parent)

        from emudeckqt.pages import IntroPage, DestinationPage, CHDToolPage, PowertoolsPage, SRMPage, ESDEPage, \
            EmuSelectPage, RACustomPage, RABezelsPage, RAAutoSavePage, SNESARPage, WidescreenSelectPage, \
            OverwriteSelectPage, InstallPage, ErrorPage
        self.setPage(self.PageIntro, IntroPage.IntroPage(self))

        self.setPage(self.PageDestination, DestinationPage.DestinationPage())
        self.setPage(self.PageCHDTool, CHDToolPage.CHDToolPage())
        self.setPage(self.PagePowertools, PowertoolsPage.PowertoolsPage())
        self.setPage(self.PageSRM, SRMPage.SRMPage())
        self.setPage(self.PageESDE, ESDEPage.ESDEPage())
        self.setPage(self.PageEmuSelect, EmuSelectPage.EmuSelectPage())
        self.setPage(self.PageRACustom, RACustomPage.RACustomPage())
        self.setPage(self.PageRABezels, RABezelsPage.RABezelsPage())
        self.setPage(self.PageRAAutoSave, RAAutoSavePage.RAAutoSavePage())
        self.setPage(self.PageSNESAR, SNESARPage.SNESARPage())
        self.setPage(self.PageWidescreenSelect, WidescreenSelectPage.WidescreenSelectPage())
        self.setPage(self.PageOverwriteSelect, OverwriteSelectPage.OverwriteSelectPage())
        self.setPage(self.PageInstall, InstallPage.InstallPage())
        # self.setPage(self.PageRegister, RegisterPage())
        # self.setPage(self.PageDetails, DetailsPage())

        self.setPage(self.PagePasswordIncorrect, ErrorPage.PasswordIncorrectErrorPage())
        self.setPage(self.PageDestinationNotFoundError, ErrorPage.DestinationNotFoundErrorPage())
        # self.setPage(self.PageConclusion, ConclusionPage())

        self.setStartId(self.PageIntro)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)
        self.setPixmap(QWizard.LogoPixmap, QPixmap(":/images/logo.png"))
        self.setButtonText(QWizard.CommitButton, "Install")

        # set up help messages
        self._lastHelpMsg = ''
        self._helpMsgs = self._createHelpMsgs()
        self.helpRequested.connect(self._showHelp)

        self.setWindowTitle(self.tr("EmuDeckQT"))

    def _createHelpMsgs(self):
        msgs = {}
        msgs[self.PageIntro] = self.tr(
            "The decision you make here will affect which page you "
            "get to see next.")
        msgs[self.PageDestination] = self.tr(
            "Make sure to provide a valid email address, such as "
            "toni.buddenbrook@example.de.")
        # msgs[self.PageRegister] = self.tr(
        #     "If you don't provide an upgrade key, you will be "
        #     "asked to fill in your details.")
        # msgs[self.PageDetails] = self.tr(
        #     "Make sure to provide a valid email address, such as "
        #     "thomas.gradgrind@example.co.uk.")
        msgs[self.PageConclusion] = self.tr(
            "You must accept the terms and conditions of the "
            "license to proceed.")
        msgs[self.NUM_PAGES + 1] = self.tr("Sorry, I already gave what help I could. "
                                           "\nMaybe you should try asking a human?")
        return msgs

    @pyqtSlot()
    def _showHelp(self):
        # get the help message for the current page
        msg = self._helpMsgs[self.currentId()]

        # if same as last message, display alternate message
        if msg == self._lastHelpMsg:
            msg = self._helpMsgs[self.NUM_PAGES + 1]

        QMessageBox.information(self,
                                self.tr("License Wizard Help"),
                                msg)
        self._lastHelpMsg = msg
