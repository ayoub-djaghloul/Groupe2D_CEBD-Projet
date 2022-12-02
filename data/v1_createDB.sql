-- TODO 1.3a : Créer les tables manquantes et modifier celles ci-dessous

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

    FOREIGN KEY (numSp) REFERENCES Participant(numPart) ON DELETE CASCADE
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
    gold INTEGER,
    silver INTEGER,
    bronze INTEGER,

    FOREIGN KEY (numEp) REFERENCES Epreuve(numEp) ON DELETE CASCADE,
    FOREIGN KEY (gold) REFERENCES Participant(numPart),
    FOREIGN KEY (silver) REFERENCES Participant(numPart),
    FOREIGN KEY (bronze) REFERENCES Participant(numPart)
);

CREATE TABLE Participant
(
    numPart INTEGER PRIMARY KEY,

    CONSTRAINT PA_CK1 CHECK ((numPart > 0 and numPart < 100) or (numPart > 1000 and numPart < 1500))
);

CREATE TABLE Equipe_base
(
    numEq INTEGER PRIMARY KEY,

    FOREIGN KEY (numEq) REFERENCES Participant(numPart) ON DELETE CASCADE
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
    numPart INTEGER,
    numEp INTEGER,

    CONSTRAINT INS_PK PRIMARY KEY (numPart, numEp),

    FOREIGN KEY (numPart) REFERENCES Participant(numPart) ON DELETE CASCADE,
    FOREIGN KEY (numEp) REFERENCES Epreuve(numEp) ON DELETE CASCADE
);

CREATE TABLE Discipline
(
    nomDi VARCHAR(50) PRIMARY KEY
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
