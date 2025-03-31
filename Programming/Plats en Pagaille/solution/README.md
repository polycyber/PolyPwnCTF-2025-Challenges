# Nom du défi

## Write-up FR

Le secret du défi réside dans les couverts et la manière dont ils sont positionnés dans l'assiette. Il y a tout un langage basé sur la façon de positionner ses couverts dans son assiette dans les hautes sphères de la gastronomie. Anton Ego ne s'exprime ainsi que par des "Bon", "Parfait", "Pause", "Bof", "Fini" selon la façon dont il agence ses couverts.

Les plats qui constituent le flag sont donc ceux reconnus comme bons et parfaits. On utilise la première lettre de chaque plat dans l'ordre pour reconstituer le flag.
Une fois la bonne suite de plats donnée, la dernière phrase nous indique la casse : "Le flag se trouve dans ce que j'ai aimé et ADORÉ". 
- Si un plat est "Bon", alors il l'a aimé et la lettre est donc en minuscule. 
- Si un plat a été "Parfait", alors il est ADORÉ et la lettre est donc en majuscule.

Cas particulier : la "Pause". 
Elle dure 3s pendant lesquelles il ne faut surtout rien écrire et attendre le véritable retour sous forme de "Bon", "Bof" ou "Parfait" avant de renvoyer une autre proposition de plat.

Pour arriver à trouver la solution, il faut parcourir la liste menu dans l'ordre Entrée, Plats, Fromages et Desserts tout en respectant les temps de pause aléatoires

## Write-up EN

The secret of the challenge lies in the cutlery and how it is positioned on the plate. There is an entire language based on the way cutlery is arranged on a plate. Anton Ego expresses himself only through "Good", "Perfect", "Pause", "Meh", and "Finished," depending on how he arranges his cutlery.

The dishes that make up the flag are those recognized as "Good" and "Perfect." The first letter of each selected dish, in order, is used to reconstruct the flag.

Once the correct sequence of dishes is found, the last sentence provides a clue about the case sensitivity: "The flag is found in what I liked and LOVED".
- If a dish is rated as "Good", it means he liked it, and the letter should be lowercase.
- If a dish is rated as "Perfect," then he LOVED it, so the letter should be uppercase.

Special case: the "Pause"
It lasts 3 seconds, during which nothing should be written. You must wait for the actual feedback in the form of "Good," "Meh," or "Perfect" before submitting another dish.

To find the solution, you must go through the menu in order: Starters, Main Courses, Cheeses, and Desserts, while respecting the random pause times.


## Flag

`polycyber{UnFLagRAfFinE}`
