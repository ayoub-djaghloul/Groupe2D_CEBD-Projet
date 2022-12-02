-- TODO 1.3a : Créer les tables manquantes et modifier celles ci-dessous
CREATE TABLE Discipline
(
    nomDi VARCHAR(50) PRIMARY KEY
);

CREATE TABLE Sportif_base
(
    numSp INTEGER PRIMARY KEY,
    nomSp VARCHAR(20) NOT NULL,
    prenomSp VARCHAR(20) NOT NULL,
    pays VARCHAR(20),
    categorieSp VARCHAR(10),
    dateNaisSp DATE,

    CONSTRAINT SP_CK1 CHECK(numSp > 0),
    CONSTRAINT SP_CK2 CHECK(categorieSp IN ('feminin','masculin')),

    FOREIGN KEY (numSp) REFERENCES Participant(numPa) ON DELETE CASCADE
);

CREATE TABLE Epreuve
(
    numEp INTEGER PRIMARY KEY,
    nomEp VARCHAR(30),
    formeEp VARCHAR(15),
    nomDi VARCHAR(50),
    categorieEp VARCHAR(10),
    nbSportifsEp INTEGER,
    dateEp DATE,

    CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
    CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
    CONSTRAINT EP_CK3 CHECK (numEp > 0),
    CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 0),

    FOREIGN KEY (nomDi) REFERENCES Discipline(nomDi) ON DELETE CASCADE
);

CREATE TABLE Resultat
(
    numEp INTEGER PRIMARY KEY,
    medaille_or INTEGER,
    medaille_argent INTEGER,
    medaille_bronze INTEGER,

    FOREIGN KEY (numEp) REFERENCES Epreuve(numEp) ON DELETE CASCADE,
    FOREIGN KEY (medaille_or) REFERENCES Participant(numPa),
    FOREIGN KEY (medaille_argent) REFERENCES Participant(numPa),
    FOREIGN KEY (medaille_bronze) REFERENCES Participant(numPa)
);

CREATE TABLE Participant
(
    numPa INTEGER PRIMARY KEY,

    CONSTRAINT PA_CK1 CHECK ((numPa > 0 and numPa < 100) or (numPa > 1000 and numPa < 1500))
);

CREATE TABLE Equipe_base
(
    numEq INTEGER PRIMARY KEY,

    FOREIGN KEY (numEq) REFERENCES Participant(numPa) ON DELETE CASCADE
);

CREATE TABLE EstEquipier
(
    numEq INTEGER,
    numSp INTEGER,

    CONSTRAINT ESEQ_PK PRIMARY KEY (numEq, numSp),

    FOREIGN KEY (numEq) REFERENCES Equipe_base(numEq) ON DELETE CASCADE,
    FOREIGN KEY (numSp) REFERENCES Sportif_base(numSp) ON DELETE CASCADE
);

CREATE TABLE Inscription
(
    numPa INTEGER,
    numEp INTEGER,

    CONSTRAINT INS_PK PRIMARY KEY (numPa, numEp),

    FOREIGN KEY (numPa) REFERENCES Participant(numPa) ON DELETE CASCADE,
    FOREIGN KEY (numEp) REFERENCES Epreuve(numEp) ON DELETE CASCADE
);

-- TODO 1.4a : ajouter la définition de la vue LesAgesSportifs
CREATE VIEW AgesSportifs(numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, age) AS
    SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, CURRENT_DATE - dateNaisSp AS age
    FROM Sportif_base;

-- TODO 1.5a : ajouter la définition de la vue LesNbsEquipiers
CREATE VIEW LesNbsEquipiers(numEq, nbEquipiers) AS
    SELECT numEq, COUNT(numSp) AS nbEquipiers
    FROM Equipe_base JOIN EstEquipier USING(numEq)
    GROUP BY numEq;
-- TODO 3.3 : ajouter les éléments nécessaires pour créer le trigger (attention, syntaxe SQLite différent qu'Oracle)
