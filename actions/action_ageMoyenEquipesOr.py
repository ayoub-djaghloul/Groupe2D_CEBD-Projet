
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppAgeMoyenEquipesOr(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/window_2_1.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAgeMoyenEquipesOr()

    ####################################################################################################################
    # Méthodes permettant de rafraichir les différentes tables
    ####################################################################################################################

    # Fonction de mise à jour de l'affichage d'une seule table
    def refreshTable(self, label, table, query):
        display.refreshLabel(label, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            table.setRowCount(0)
            display.refreshLabel(label, "Impossible d'afficher les données de la table : " + repr(e))
        else:
            display.refreshGenericData(table, result)


    # Fonction permettant de mettre à jour toutes les tables
    @pyqtSlot()
    def refreshAgeMoyenEquipesOr(self):
        query = "SELECT numEq, AVG(age)" \
                "FROM EstEquipier JOIN Equipe_base USING(numEq) JOIN AgesSportifs USING(numSp)" \
                "WHERE numEq IN (SELECT medaille_or FROM Resultat);"

        self.refreshTable(self.ui.label_ageMoyenEquipesOr, self.ui.tableAgeMoyenEquipesOr, query)
