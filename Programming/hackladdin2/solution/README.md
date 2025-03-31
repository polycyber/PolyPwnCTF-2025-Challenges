# Hackladdin 2

## Write-up FR

Stratégie mise en œuvre
La solution repose sur une approche en deux phases :

- Phase de découverte d'information :
Durant les 19 premières tentatives, des suppositions aléatoires (peut-être amélioré) sont envoyées au serveur pour récolter des indices. Chaque tentative retourne un feedback sous forme de positions correctes, ce qui permet d'affiner les possibilités pour le mot de passe.

- Phase de résolution par programmation par contraintes :
À la dernière tentative, les informations accumulées sont exploitées à l'aide de MiniZinc (ou tout autre outil) et du solveur Gecode pour générer une solution exacte en se basant sur les feedbacks précédents.

## Write-up EN

Strategy implemented
The solution relies on a two-phase approach:

- Information gathering phase:
During the first 19 attempts, random guesses (may be improved) are sent to the server to gather hints. Each attempt returns feedback in the form of correct positions, which helps refine the possibilities for the password.

- Constraint programming resolution phase:
At the last attempt, the accumulated information is exploited using MiniZinc (or any other tool) and the Gecode solver to generate an exact solution based on the previous feedbacks.

## Flag

`polycyber{V1v3l4Pr0Gr4m4m710nP4rC0nTr41nT3}`