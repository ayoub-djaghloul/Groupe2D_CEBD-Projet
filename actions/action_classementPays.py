
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppClassementPays(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/window_2_2.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshClassementPays()

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
    def refreshClassementPays(self):

        query = """WITH PaysParticipant AS (
                    SELECT pays, numSp as numPa
                    FROM Sportif_base
                    UNION
                    SELECT pays, numEq as numPa
                    FROM Sportif_base JOIN EstEquipier USING (numSp)
                ),
                ParticipantOr AS (
                        SELECT numPa, COUNT(medaille_or) as nbOr
                        FROM Participant LEFT JOIN Resultat ON (numPa == medaille_or)
                        GROUP BY numPa
                ),
                    ParticipantArgent AS (
                        SELECT numPa, COUNT(medaille_argent) as nbArgent
                        FROM Participant LEFT JOIN Resultat ON (numPa == medaille_argent)
                        GROUP BY numPa
                ),
                    ParticipantBronze AS (
                        SELECT numPa, COUNT(medaille_bronze) as nbBronze
                        FROM Participant LEFT JOIN Resultat ON (numPa == medaille_bronze)
                        GROUP BY numPa
                ),
                ParticipantMedaille AS (
                    SELECT numPa, nbOr, nbArgent, nbBronze
                    FROM ParticipantOr JOIN ParticipantArgent USING(numPa)
                                        JOIN ParticipantBronze USING(numPa)
                    WHERE nbOr > 0 or nbArgent > 0 or nbBronze > 0
                )
                SELECT pays, SUM(nbOr), SUM(nbArgent), SUM(nbBronze)
                FROM PaysParticipant JOIN ParticipantMedaille USING(numPa)
                GROUP BY pays
                ORDER BY SUM(nbOr) DESC, SUM(nbArgent) DESC, SUM(nbBronze) DESC;"""

        self.refreshTable(self.ui.labelClassementPays, self.ui.tableClassementPays, query)
