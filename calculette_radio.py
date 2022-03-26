#!/usr/bin/python3.8
# -*- encoding: utf-8 -*-
# calculette dédiée au calcul liés à la radio 
# la base est issue de mon cours Python Docstring
# Auteur F5GFE


from functools import partial
from math import sqrt, log10, tan, fabs
from PySide2 import QtWidgets, QtGui
from pathlib import Path

power = []  # variable chaine pour STO

class Calculatrice(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.resize(350, 500)
        self.setWindowTitle("Calculette Radio (Z = 50 " + chr(937) + ") F5GFE")
        self.modify_widgets()
        self.setupUi()
        self.setupRaccourcisClavier()
        self.setupConnections()
        self.show()

    def setupUi(self):
        """ création de l interface graph²ique de la calculatice"""

        # cré les 2 lignes de résultat
        self.le_operation = QtWidgets.QLineEdit()  # ligne du haut ligne édition
        self.le_operation.setFont(QtGui.QFont('Times', 8))
        self.le_resultat = QtWidgets.QLineEdit('')  # 2eme ligne édition
        self.gridLayout = QtWidgets.QGridLayout(self)  # cré une grille de positionnement

        # cré les boutons nombres
        self.btn_0 = QtWidgets.QPushButton('0')
        self.btn_1 = QtWidgets.QPushButton('1')
        self.btn_2 = QtWidgets.QPushButton('2')
        self.btn_3 = QtWidgets.QPushButton('3')
        self.btn_4 = QtWidgets.QPushButton('4')
        self.btn_5 = QtWidgets.QPushButton('5')
        self.btn_6 = QtWidgets.QPushButton('6')
        self.btn_7 = QtWidgets.QPushButton('7')
        self.btn_8 = QtWidgets.QPushButton('8')
        self.btn_9 = QtWidgets.QPushButton('9')

        # cré le boutons oppérations
        self.btn_point = QtWidgets.QPushButton('.')
        self.btn_plus = QtWidgets.QPushButton('+')
        self.btn_moins = QtWidgets.QPushButton('-')
        self.btn_mult = QtWidgets.QPushButton('*')
        self.btn_div = QtWidgets.QPushButton('/')
        self.btn_egal = QtWidgets.QPushButton('=')
        self.btn_c = QtWidgets.QPushButton('C')
        self.btn_sqr = QtWidgets.QPushButton('sqr')
        self.btn_swr = QtWidgets.QPushButton('swr')
        self.btn_sto = QtWidgets.QPushButton('sto')
        self.btn_corr = QtWidgets.QPushButton(chr(9668))
        self.btn_dBmW = QtWidgets.QPushButton('dBm>W')
        self.btn_dBmV = QtWidgets.QPushButton('dBm>V')
        self.btn_WdBm = QtWidgets.QPushButton('W>dBm')
        # self.btn_WV = QtWidgets.QPushButton('W > V')
        self.btn_f4 = QtWidgets.QPushButton(chr(955) + '/4')
        self.btn_A = QtWidgets.QPushButton("valeur\nd'une\nself")
        self.btn_A.setFont(QtGui.QFont('Times', 10))
        self.btn_B = QtWidgets.QPushButton('Fréquence\nrésonnance\ncircuit LC')
        self.btn_B.setFont(QtGui.QFont('Times', 10))
        self.btn_C = QtWidgets.QPushButton('NB tours\nself')
        self.btn_C.setFont(QtGui.QFont('Times', 10))
        self.btn_D = QtWidgets.QPushButton('réglage\nantenne')
        self.btn_D.setFont(QtGui.QFont('Times', 10))
        self.btn_E = QtWidgets.QPushButton('antenne\nraccourcie')
        self.btn_E.setFont(QtGui.QFont('Times', 10))

        # positionne les boutons: colonne, ligne, origine, Nb de cellules
        self.gridLayout.addWidget(self.le_operation, 0, 0, 1, 6)
        self.gridLayout.addWidget(self.le_resultat, 1, 0, 1, 6)
        self.gridLayout.addWidget(self.btn_c, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.btn_sqr, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.btn_corr, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.btn_div, 2, 3, 1, 1)
        self.gridLayout.addWidget(self.btn_7, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.btn_8, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.btn_9, 3, 2, 1, 1)
        self.gridLayout.addWidget(self.btn_mult, 3, 3, 1, 1)
        self.gridLayout.addWidget(self.btn_4, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.btn_5, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.btn_6, 4, 2, 1, 1)
        self.gridLayout.addWidget(self.btn_moins, 4, 3, 1, 1)
        self.gridLayout.addWidget(self.btn_1, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.btn_2, 5, 1, 1, 1)
        self.gridLayout.addWidget(self.btn_3, 5, 2, 1, 1)
        self.gridLayout.addWidget(self.btn_plus, 5, 3, 1, 1)
        self.gridLayout.addWidget(self.btn_sto, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.btn_0, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.btn_point, 6, 2, 1, 1)
        self.gridLayout.addWidget(self.btn_egal, 6, 3, 1, 1)
        self.gridLayout.addWidget(self.btn_swr, 2, 4, 1, 1)
        self.gridLayout.addWidget(self.btn_dBmW, 3, 4, 1, 1)
        self.gridLayout.addWidget(self.btn_dBmV, 4, 4, 1, 1)
        self.gridLayout.addWidget(self.btn_WdBm, 5, 4, 1, 1)
        self.gridLayout.addWidget(self.btn_f4, 6, 4, 1, 1)
        self.gridLayout.addWidget(self.btn_A, 2, 5, 1, 1)
        self.gridLayout.addWidget(self.btn_B, 3, 5, 1, 1)
        self.gridLayout.addWidget(self.btn_C, 4, 5, 1, 1)
        self.gridLayout.addWidget(self.btn_D, 5, 5, 1, 1)
        self.gridLayout.addWidget(self.btn_E, 6, 5, 1, 1)

        # cré une variable contenant le Nb de boutons
        self.btns_nombres = []
        # la boucle va récupérer avec isdigit() que les boutons avec des nombres
        for i in range(self.gridLayout.count()):  # parcourt la liste boutons
            widget = self.gridLayout.itemAt(i).widget()  # charge dans widget le type de layout
            if isinstance(widget, QtWidgets.QPushButton):  # test si c est des QPushButton
                widget.setStyleSheet('QPushButton:hower {color: rgb(100, 200, 130);}')
                widget.setFixedSize(60, 60)  # donne leurs une taille
                # widget.QPushButton.isFlat()
                if widget.text().isdigit():  # test si le texte est un nombre
                    self.btns_nombres.append(widget)  # insert les dans la variable btns_nombres
                elif widget.text() == ".":
                    self.btns_nombres.append(widget)  # ajout du point comme un nombre
        '''
        if widget.text() == "Fréquence résonnance circuit LC" or "NB tours self" or "réglage antenne" or "antenne raccourcie":
            widget.setFixedSize(120, 60)
        if widget.text() == "valeur d'une self":
            widget.setFixedSize(120, 60)
        '''

    def setupConnections(self):
        """ fonction qui va lire le bouton pressé et envoyer le résultat a une autre fonction """
        for btn in self.btns_nombres:
            # partial renvoie en argument la valeur texte du bouton nombres
            btn.clicked.connect(partial(self.btnNombrePressed, str(btn.text())))

        # pour les autres boutons capture le texte en envoie en argument à la fonction
        self.btn_moins.clicked.connect(partial(self.btnNombrePressed, str(self.btn_moins.text())))
        self.btn_plus.clicked.connect(partial(self.btnNombrePressed, str(self.btn_plus.text())))
        self.btn_mult.clicked.connect(partial(self.btnNombrePressed, str(self.btn_mult.text())))
        self.btn_div.clicked.connect(partial(self.btnNombrePressed, str(self.btn_div.text())))

        # boutons gérés individuelement
        self.btn_egal.clicked.connect(self.calculOperation)
        self.btn_corr.clicked.connect(self.corr)
        self.btn_sqr.clicked.connect(self.sqr)
        self.btn_swr.clicked.connect(self.swr)
        self.btn_sto.clicked.connect(self.sto)
        self.btn_dBmW.clicked.connect(self.dBmW)
        self.btn_WdBm.clicked.connect(self.WdBm)
        self.btn_dBmV.clicked.connect(self.dBmV)
        # self.btn_WV.clicked.connect(self.WV)
        self.btn_f4.clicked.connect(self.onde)
        self.btn_c.clicked.connect(self.supprimerResultat)
        self.btn_A.clicked.connect(self.henry)
        self.btn_B.clicked.connect(self.qrg)
        self.btn_C.clicked.connect(self.tours)
        self.btn_D.clicked.connect(self.reglage)
        self.btn_E.clicked.connect(self.mobile)

    def setupRaccourcisClavier(self):
        for btn in range(10):  # trie les btn pressé de 0 à 9
            QtWidgets.QShortcut(QtGui.QKeySequence(str(btn)), self, partial(self.btnNombrePressed, str(btn)))
        # va envoyer le texte de la touche clavier pressée a la fonction btnNommbrePressed
        # rechercher ou est le module QKeySequence QyGui ???

        # envoye les signes oppération du clavier a la fonction buttonPressed
        # self.btnNombrePressed, str(btn.text()
        QtWidgets.QShortcut(QtGui.QKeySequence('+'), self, partial(self.btnNombrePressed, '+'))
        QtWidgets.QShortcut(QtGui.QKeySequence('-'), self, partial(self.btnNombrePressed, '-'))
        QtWidgets.QShortcut(QtGui.QKeySequence('*'), self, partial(self.btnNombrePressed, '*'))
        QtWidgets.QShortcut(QtGui.QKeySequence('/'), self, partial(self.btnNombrePressed, '/'))
        QtWidgets.QShortcut(QtGui.QKeySequence('Enter'), self, self.calculOperation)

        # active l'usage des raccourcis clavier dans l application
        QtWidgets.QShortcut(QtGui.QKeySequence('Del'), self, self.supprimerResultat)
        QtWidgets.QShortcut(QtGui.QKeySequence('Esc'), self, self.close)

    def modify_widgets(self):
        css_file = Path.cwd() /"style.css"
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())


    def btnNombrePressed(self, bouton):
        """Fonction activee quand l'utilisateur appuie sur un numero (0-9)"""

        # On recupere le texte dans le LineEdit resultat
        resultat = str(self.le_resultat.text())

        if resultat == '':
            # Si le resultat est egal a 0 on met le nombre du bouton
            # que l'utilisateur a presse dans le LineEdit resultat
            self.le_resultat.setText(bouton)
        else:
            # Si le resultat contient autre chose que zero,
            # On ajoute le texte du bouton a celui dans le LineEdit resultat
            self.le_resultat.setText(resultat + bouton)

    def btnOperationPressed(self, operation):
        """
        Fonction activee quand l'utilisateur appuie sur
        une touche d'operation (+, -, /, *)
        """

        # On recupere le texte dans le LineEdit operation
        operationText = str(self.le_operation.text())
        # On recupere le texte dans le LineEdit resultat
        resultat = str(self.le_resultat.text())

        # On additionne l'operation en cours avec le texte dans le resultat
        # et on ajoute a la fin le signe de l'operation qu'on a choisie
        self.le_operation.setText(operationText + resultat + " " + operation + " ")
        # On reset le texte du LineEdit resultat
        self.le_resultat.setText('')

    def supprimerResultat(self):
        """On reset le texte des deux LineEdit et vide la liste power et la variable a"""
        self.le_resultat.setText('')
        self.le_operation.setText('')
        while len(power) > 0: power.pop()
        a = 0

    def calculOperation(self):
        """On calcule le resultat de l'operation en cours (quand l'utilisateur appuie sur egal)"""
        # On recupere le texte dans le LineEdit resultat
        resultat = str(self.le_resultat.text())
        # On ajoute le nombre actuel dans le LineEdit resultat
        # au LineEdit operation
        self.le_operation.setText(self.le_operation.text() + resultat)

        # On evalue le resultat de l'operation
        resultatOperation = eval(str(self.le_operation.text()))

        # On met le resultat final dans le LineEdit resultat
        self.le_resultat.setText(str(resultatOperation))

    def sqr(self):
        """ fonction calcule de la racine carré """
        # On recupere le texte dans le LineEdit resultat
        resultat = str(self.le_resultat.text())
        print(resultat)
        if resultat == "":
            QtWidgets.QMessageBox.information(None, "Info", "Donne la racine carrée du nombre saisi.")
        # On evalue le resultat de l'operation
        resultatOperation = sqrt(float(self.le_resultat.text()))
        # On met le resultat final dans le LineEdit resultat
        self.le_resultat.setText(str(resultatOperation))
        self.le_operation.setText("sqr " + '%.3f' % resultat)

    def swr(self):
        """fonction calcul du swr récupère puissance directe et puissance réfléchie dans une liste"""
        entree = len(power)  # compte le nombre de valeurs saisies
        print(entree)

        if entree != 2:
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("CALCULE LE SWR")  # titre de la fentre popup
            message_box.setText(
                "Entrez : \nla puissance directe \npuis la puissance réfléchie \nen mémoire STO avant d'appuyer sur le bouton swr")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # efface tout

        elif float(power[0]) <= float(power[1]):
            self.le_operation.setText(str(""))
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle("Aide Fonction SWR")  # titre de la fentre popup
            message_box.setText(
                "Erreur! La puissance réfléchie ne peux être \n"
                "plus grande que la puissance directe")  # texte d aide
            message_box.exec_()
            self.supprimerResultat()

        else:
            pd = float(power[0])  # lit le premier item de la liste power
            print(pd)
            pr = float(power[1])
            print(pr)
            fi = sqrt(pr / pd)
            swr = ((1 + fi) / (1 - fi))
            swr = float(swr)

            self.le_resultat.setText("swr " + str('%.2f' % swr))
            self.le_operation.setText("P.direct " + str('%.2f' % pd) + " W  P.retour " + str('%.2f' % pr) + "W")

    def sto(self):
        """stocker les valeurs saisies dans une liste"""
        if (str(self.le_resultat.text())) != "":
            power.append(str(self.le_resultat.text()))
            self.le_resultat.setText('')
            self.le_operation.setText(str(power))
        else:
            pass
        print(power)

    def dBmW(self):
        """ fonction qui convertie les dBm en Watt ou mW """
        # On recupere le texte dans le LineEdit resultat
        resultat = str(self.le_resultat.text())
        print(resultat)
        if resultat == "":
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("CONVERTI dBm EN WATT")  # titre de la fentre popup
            message_box.setText(
                "Entrez : \nla puissance en dB milli-watt\nrésultat en watt ou milli-watt")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # efface tout
        # On evalue le resultat de l'operation
        # On met le resultat final dans le LineEdit resultat formaté à 2 décimales
        if float(resultat) > 20:
            resultatOperation = 10 ** ((float(resultat) - 30) / 10)
            self.le_resultat.setText("= " + str('%.2f' % (resultatOperation)) + " W")
            self.le_operation.setText(str(resultat) + " dBm ")
        else:
            resultatOperation = (10 ** ((float(resultat) - 30) / 10) * 1000)
            self.le_resultat.setText("= " + str('%.9f' % (resultatOperation)) + " mW")
            self.le_operation.setText(str(resultat) + " dBm ")

    def WdBm(self):
        """ fonction qui convertie les Watt en dBm"""
        # On recupere le texte dans le LineEdit resultat
        resultat = (self.le_resultat.text())
        print(resultat)
        if resultat == "":
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("CONVERTI DES WATTS EN dBm")  # titre de la fentre popup
            message_box.setText("Entrez : \nla puissance en watts\nsera convertie en dB milli-watt")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # OK efface tout

        resultat = float(self.le_resultat.text())
        resultatOperation = 10*(log10(resultat))+30
        self.le_resultat.setText("= " + str('%.2f' % (resultatOperation)) + " dBm")
        self.le_operation.setText("Une puissance de " + str(resultat) + " Watt ")


    def dBmV(self):
        """ fonction qui convertie les dBm en Volt ou µV """
        # On recupere le texte dans le LineEdit resultat
        resultat = str(self.le_resultat.text())
        print(resultat)
        if resultat == "":
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("CONVERTI dBm EN TENSION")  # titre de la fentre popup
            message_box.setText(
                "Entrez : \nla puissance en dBm\nelle sera convertie en tension Volts ou milli-Volt\npour une charge de 50 Ohms")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # efface tout

        # On evalue le resultat de l'operation
        # On met le resultat final dans le LineEdit resultat formaté à 2 décimales
        if float(resultat) > 20:
            resultatOperation = (10 ** ((float(resultat) - 30) / 10) * 0.2250)
            self.le_resultat.setText("= " + str('%.5f' % (resultatOperation)) + " V")
            self.le_operation.setText(str(resultat) + " dBm ")
        else:
            resultatOperation = (10 ** ((float(resultat) - 30) / 10) * 225000000)
            self.le_resultat.setText("= " + str((resultatOperation)) + " µV")
            self.le_operation.setText(str(resultat) + " dBm ")

    def WV(self):
        """ fonction qui convertie les Watt en Volt """
        # On recupere le texte dans le LineEdit resultat
        resultat = str(self.le_resultat.text())
        print(resultat)
        if resultat == "":
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("TENSION EN FONCTION DE LA PUISSANCE")  # titre de la fentre popup
            message_box.setText(
                "Entrez : \nla puissance HF appliquée à la charge ou à l'antenne\nelle sera convertie en tension\npour une impédance de 50 Ohms")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # efface tout
        resultatOperation = sqrt(float(resultat) * 50)
        self.le_resultat.setText("= " + str('%.2f' % (resultatOperation)) + " Volt")
        self.le_operation.setText(str(resultat) + " Watt ")

    def onde(self):
        """ fonction qui convertie la fréquence en 1/4 onde """
        # On recupere le texte dans le LineEdit resultat
        resultat = str(self.le_resultat.text())
        print(resultat)
        if resultat == "":
            QtWidgets.QMessageBox.information(None, "Info", "Calcul le 1/4 d'onde pour la fréquence donnée en MHz.")
        resultatOperation = 299792.458 / (float(resultat) * 4)
        self.le_resultat.setText("= " + str('%.2f' % (resultatOperation)) + " millimètres")
        self.le_operation.setText("Le quart d'onde de " + (str(resultat) + " MHz "))

    def henry(self):
        """fonction qui calcule la valeur d'une self en micro henry """
        entree = len(power)  # compte le nombre de valeurs saisies en STO
        print(entree)

        if entree != 3:
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("CALCUL DE LA VALEUR D'UNE SELF")  # titre de la fentre popup
            message_box.setText(
                "Entrez :\nle diamètre intérieur en mm \nle nombre de tours \nla longueur totale en mm \nen mémoire STO avant d'appuyer sur le bouton self")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # efface tout

        else:
            diam = float(power[0])  # lit le premier item de la liste power
            print(diam)
            nbt = float(power[1])
            print(nbt)
            lon = float(power[2])
            print(lon)
            henry = (pow(diam, 2)) * (pow(nbt, 2)) / ((460 * diam) + (1000 * lon))

            self.le_resultat.setText("La valeur est " + str('%.2f' % (henry)) + " " + chr(956) + "H")
            self.le_operation.setText(
                "pour " + power[1] + " spires d'un diamètre de " + power[0] + "mm et d'une longueur de " + power[
                    2] + "mm")

    def tours(self):
        """Calcul le nombre de tour d'une self"""
        entree = len(power)  # compte le nombre de valeurs saisies en STO
        print(entree)

        if entree != 3:
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("CALCUL LE NOMBRE DE TOURS D'UNE SELF")  # titre de la fentre popup
            message_box.setText(
                "Entrez :\nle diamètre du support en mm \nle diammètre du fil\nla valeur de la self en µH\nen mémoire STO avant d'appuyer sur le bouton self")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # efface tout

        else:
            diam = float(power[0])  # lit le premier item de la liste power
            print(diam)
            fil = float(power[1])# lit le 2eme item de la liste power
            print(fil)
            henry = float(power[2])# lit le 3eme item de la liste power
            print(henry)

            for nb in range(1, 1000):
                nbt = nb/10# je divise le pas par 10 pour plus de précision
                henry2 = (pow(diam, 2)) * (pow(nbt, 2)) / ((460 * diam) + (1000 * (nbt*fil)))
                if henry2 > henry:# quand on depasse la valeur recherché
                    nbt = str(nbt-0.1)# je reviens au pas précédente
                    henry = str(henry)# je fige la valeur
                    self.le_operation.setText("pour les diamètres " + power[0] + "mm du support et " + power[1] + "mm du fil " )
                    self.le_resultat.setText("il faut " + nbt + " tours pour une valeur de " + henry + " " + chr(956) + "H")
                    break
                else:
                    nb = nb+1

    def qrg(self):
        """ calcule la fréquence de résonnance d'un circuit LC """
        entree = len(power)  # compte le nombre de valeurs saisies en STO
        print(entree)

        if entree != 2:
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("CALCUL DE LA FREQUENCE DE RESONNANCE LC")  # titre de la fentre popup
            message_box.setText(
                "Entrez :\nla valeur de la capa en pF \n la valeur de la self µH \n en mémoire STO avant d'appuyer sur le bouton fréquence")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # efface tout

        else:
            capa = float(power[0])  # lit le premier item de la liste power
            print(capa)
            henry = float(power[1])
            print(henry)

            Flc = (159 / (sqrt((capa * 10e-6) * (henry * 10e-12)))) / 100000000

            self.le_resultat.setText("La fréquence résonnance est de " + str('%.3f' % (Flc)) + " MHz ")
            self.le_operation.setText("pour une capa de " + power[0] + " pF et une self de " + power[1] + " µH ")

    def corr(self):
        """fonction de corection de la saisie"""
        txt = self.le_resultat.text()
        print(txt)
        tct = txt[:-1]
        self.le_resultat.setText(tct)

    def mobile(self):
        """ donne la valeur de la self necessaire au raccourcissement d'une antenne mobile """
        entree = len(power)  # compte le nombre de valeurs saisies en STO
        print(entree)

        if entree != 2:
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("CALCUL SELF POUR ANTENNE MOBILE")  # titre de la fentre popup
            message_box.setText(
                "Entrez : \nla fréquence en MHz de résonnance recherchée  \npuis la longueur de l'antenne désirée en m \nen mémoire STO avant d'appuyer sur le bouton antenne raccourcie")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # efface tout

        else:
            qrg = float(power[0])  # lit le premier item de la liste power
            print(qrg)
            lon = float(power[1])
            print(lon)

            onde = float(299792.458 / qrg)
            henry = ((63 / qrg) * (1 / tan(6.28 * (lon / onde)))) / 4000

            self.le_resultat.setText("La valeur de la self est de " + str('%.3f' % (henry)) + "µH")
            self.le_operation.setText(
                "pour avoir une longueur de " + power[1] + "m à la fréquence de résonance " + chr(955) + "/4 de " +
                power[0] + "MHz ")

    def reglage(self):
        """fonction qui calcule l'écart entre deux longueurs d'antenne par rapport à la qrg """
        entree = len(power)  # compte le nombre de valeurs saisies en STO
        print(entree)

        if entree != 2:
            self.le_operation.setText(str(""))  # vide la ligne opération
            message_box = QtWidgets.QMessageBox()  # lance une fenètre d'info en popup
            message_box.setWindowTitle("AJUSTEMENT DIMENTIONNEL D'UNE ANTENNE")  # titre de la fentre popup
            message_box.setText(
                "Entrez : \nla fréquence en MHz de résonnance mesurée  \npuis la fréquence en MHz désirée \nen mémoire STO avant d'appuyer sur le bouton réglage")  # texte d aide
            message_box.exec_()  # ouvre la boite popup
            self.supprimerResultat()  # efface tout

        else:
            qrgMesuree = float(power[0])  # lit le premier item de la liste power
            print(qrgMesuree)
            qrgRecherchee = float(power[1])
            print(qrgRecherchee)

            lom = float(299792.458 / qrgMesuree)
            lor = float(299792.458 / qrgRecherchee)
            delta = (lor - lom) / 4

            if delta < 0:
                self.le_resultat.setText("Raccourcir chaque éléments de " + str('%.0f' % fabs(delta)) + " mm")
                #fabs renvoie la valeur absolue de delta donc toujours positive.
                
            else:
                self.le_resultat.setText("Rallonger chaque éléments de " + str('%.0f' % (delta)) + " mm")

        self.le_operation.setText(
            "Résonnance mesurée à " + power[0] + "MHz vous recherchez une résonance à " + power[1] + "MHz ")


app = QtWidgets.QApplication([])
fenetre = Calculatrice()
fenetre.show()
app.exec_()

"""dB = decibels (Log10)
m = milli = 10E-3
µ = micro = 10E-6
n = nano = 10E-9
p = pico = 10E-12

dBi = decibels relatif à une antenne isotropic
dBw = decibels relatif à 1 watt
dBm = decibels relatif à 1 milliwatt
dBv = decibels relatif à 1 volt
dBµv = decibels relatif à 1 microvolt



"""
