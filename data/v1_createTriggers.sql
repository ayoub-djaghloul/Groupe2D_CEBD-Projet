-- TODO 3.3 Créer un trigger pertinent
-- Vérifie que chaque médaille a été gagnée par un participant différent
CREATE TRIGGER VerificationVainqueur
BEFORE INSERT ON Resultat
WHEN (NEW.medaille_or == NEW.medaille_argent OR NEW.medaille_argent == NEW.medaille_bronze OR NEW.medaille_or == NEW.medaille_bronze)
BEGIN
    SELECT RAISE(ABORT, 'Deux médailles ont été remportées par le même participant');
END;