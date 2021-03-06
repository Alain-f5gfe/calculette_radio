from PySide2 import QtWidgets, QtGui

CUSTOM_FONT = QtGui.QFont
CUSTOM_FONT.setPiointSize(14)


class BoutonCustom(QtWidgets.QPushButton):

    def __init__(self, texte):
        super(BoutonCustom, self).__init__(texte)

        self.setFont(CUSTOM_FONT)
        self.setStyleSheet('QPushButton:hover {color rgb(100, 200, 130);}')