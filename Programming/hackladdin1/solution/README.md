# Hackladdin 1

## Write-up FR

Le script Python suivant utilise la bibliothèque `pwntools` pour interagir avec le serveur et implémente une stratégie basée sur le maintien d'une "connaissance" actualisée à chaque tentative.

- reset_knowledge : Initialise une "connaissance" pour chaque lettre, supposant qu'elle peut apparaître à n'importe quelle position.

- update_knowledge : Met à jour la "connaissance" après chaque tentative, en supprimant les positions impossibles pour chaque lettre.

- get_guess : Génère une supposition basée sur les lettres avec le moins de possibilités, puis complète aléatoirement les autres positions.

- Interaction avec le serveur :
Le script envoie des suppositions au serveur.
Il reçoit des indices sur les lettres bien/mal placées.
Le script affine ses prochaines suppositions jusqu'à trouver le passcode.

## Write-up EN

The following Python script uses the `pwntools` library to interact with the server and implements a strategy based on maintaining "knowledge" updated at each attempt.

- reset_knowledge: Initializes "knowledge" for each letter, assuming it can appear at any position.

- update_knowledge: Updates "knowledge" after each attempt, removing impossible positions for each letter.

- get_guess: Generates a guess based on the letters with the fewest possibilities, then randomly fills the other positions.

- Interaction with the server:
The script sends guesses to the server.
It receives hints on the letters well/placed.
The script refines its next guesses until finding the passcode.

## Flag

`polycyber{C357UnM4573Rm1nD3nf417}`

