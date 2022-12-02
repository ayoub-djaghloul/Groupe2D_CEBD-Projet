import sqlite3
from sqlite3 import IntegrityError

import pandas

def read_excel_file_V0(data:sqlite3.Connection, file):
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert into V0_LesSportifsEQ values ({},'{}','{}','{}','{}','{}',{})".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'], row['numEq'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Lecture de l'onglet LesEpreuves du fichier excel, en interprétant toutes les colonnes comme des string
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert into V0_LesEpreuves values ({},'{}','{}','{}','{}',{},".format(
                row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'])

            if (row['dateEp'] != 'null'):
                query = query + "'{}')".format(row['dateEp'])
            else:
                query = query + "null)"
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

#TODO 1.3a : modifier la lecture du fichier Excel pour lire l'ensemble des données et les intégrer dans le schéma de la BD V1
def read_excel_file_V1(data:sqlite3.Connection, file):
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            # Insertion d'une nouvelle ligne dans la table Participant
            query = "insert into Participant values ({})".format(row['numSp'])
            cursor.execute(query)

            query = "insert into Sportif_base values ({},'{}','{}','{}','{}','{}')".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'])
            cursor.execute(query)

        except IntegrityError as err:
            print(err)

    num_equipes=[]
    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        if (row['numEq'] != 'null'):
            if (row['numEq'] not in num_equipes):
                num_equipes.append(row['numEq'])
                query = "insert into Participant values ('{}')".format(row['numEq'])
                cursor.execute(query)
                query = "insert into Equipe_base values ('{}')".format(row['numEq'])
                cursor.execute(query)
            query = "insert into EstEquipier values ('{}','{}')".format(row['numEq'], row['numSp'])
            cursor.execute(query)

    # Lecture de l'onglet du fichier excel LesEpreuves, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    disciplines=[]
    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            if (row['nomDi'] not in disciplines):
                query = "insert into Discipline values ('{}')".format(row['nomDi'])
                cursor.execute(query)
                disciplines.append(row['nomDi'])

            query = "insert into Epreuve values ('{}','{}','{}','{}','{}','{}','{}')".format(
                row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'], row['dateEp'] if row['dateEp'] != 'null' else 'null')

            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    # Lecture de l'onglet du fichier excel LesInscriptions  , en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_inscriptions = pandas.read_excel(file, sheet_name='LesInscriptions', dtype=str)
    df_inscriptions = df_inscriptions.where(pandas.notnull(df_inscriptions), 'null')

    cursor = data.cursor()
    for ix, row in df_inscriptions.iterrows():
        try:
            query = "insert into Inscription values ('{}','{}')".format(row['numIn'], row['numEp'])
            cursor.execute(query)
            pass
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    # Lecture de l'onglet du fichier excel LesResultats  , en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_resultats = pandas.read_excel(file, sheet_name='LesResultats', dtype=str)
    df_resultats = df_resultats.where(pandas.notnull(df_resultats), 'null')

    cursor = data.cursor()
    for ix, row in df_resultats.iterrows():
        try:
            query = "insert into Resultat values('{}','{}','{}','{}')".format(
                row['numEp'], row['gold'], row['silver'], row['bronze'], row['numEp'])
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")
