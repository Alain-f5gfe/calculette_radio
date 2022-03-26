#!/usr/bin/python3.6
# -*- encoding: utf-8 -*-
# module bulles info de la calculette radio
import sys
import threading
import time
from PySide2 import QtCore, QtWidgets

class Bulle_info(QtWidgets.QDialog):
	### fonction qui va ouvrir une bulle d'aide au survol d'un bouton ###
    started = QtCore.Signal()# je cré 2 variables qui sont déclencheur d'une action
    finished = QtCore.Signal()

    def __init__(self, parent=None):
        super(Bulle_info, self).__init__(parent)
        self.button = QtWidgets.QPushButton("Click Moi")# je cré un bouton
        layout = QtWidgets.QVBoxLayout(self)#que j organise en verticale
        layout.addWidget(self.button)
        # j'execute la fonction on_clicled a l appui
        self.button.clicked.connect(self.on_clicled)

        self._message_box = QtWidgets.QMessageBox()# je créer la fenetre du message ,j ecrit le message
        self._message_box.setText(str('lire info, On attend Que vous ayez tout lu \net assimilé les bases du concept blabla..'))
        self._message_box.setStandardButtons(QtWidgets.QMessageBox.NoButton)# j'invalide le click manuel avec NoButton
        self.started.connect(self._message_box.show)# affiche la bulle
        self.finished.connect(self._message_box.accept)# ferme la bulle

    @QtCore.Slot() #decorateur qui renvoie les paramètres passé a la fonction sans affecter la fonction
    def on_clicled(self):
    	### lance en tache de fond la fonction dowork ###
        thread = threading.Thread(target=self.dowork, daemon=True)
        thread.start()

    def dowork(self):
    	### gere le temps d affichage ###
        delay = 2.5
        self.started.emit() # emets le dowork
        while delay:
           sys.stdout.write('Working...\n') #suivie dans la console
           time.sleep(0.5)  # faites un truc qui prend du temps...
           delay -= 0.5
        self.finished.emit()# arret dowork

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    bulle = Bulle_info()
    print('starting app...')
    bulle.show()
    sys.exit(app.exec_())