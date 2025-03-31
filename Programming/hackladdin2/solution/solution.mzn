include "alldifferent.mzn";

int: n;  % Longueur du mot de passe
int: n_attemps;  % Nombre de tentatives
% Liste des tentatives précédentes sous forme d’un tableau de caractères
array[1..n_attemps, 1..n] of 1..26: essais;
% Feedback : [correct_place, incorrect_place]
array[1..n_attemps, 1..2] of int: feedback;

array[1..n] of var 1..26: password;  % Mot de passe à deviner

constraint alldifferent(password);
constraint
    forall(e in 1..n_attemps) (
        let {
            int: correct_place = feedback[e, 1],
            int: incorrect_place = feedback[e, 2]
        } in
        % Contraintes sur le nombre de lettres correctes bien placées
        correct_place = sum([if essais[e, i] = password[i] then 1 else 0 endif | i in 1..n])
        /\
        % Contraintes sur le nombre de lettres correctes mal placées
        incorrect_place = sum([if (essais[e, i] != password[i]) /\ (essais[e, i] in password) then 1 else 0 endif | i in 1..n])
    );