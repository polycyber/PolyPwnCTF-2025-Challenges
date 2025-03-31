# Nom du défi

## Write-up FR

Il s'agit d'un défi d'analyse de Mémoire RAM. Utiliser volatility 3 pour faire les actions suivantes:
1. volatility3 banners
2. Télécharger les symboles (https://github.com/Abyss-W4tcher/volatility3-symbols/blob/master/Ubuntu/amd64/6.8.0/40/generic/Ubuntu_6.8.0-40-generic_6.8.0-40.40~22.04.3_amd64.json.xz) et déposer les fichiers JSON sous volatility3/symbols/linux
3. volatility3 linux.pslist -> gimp est un éditeur d'image
4. volatility3 linux.lsof --pid "code PID" -> list les fichiers associés au processus gimp. Le fichier n'est pas listé dans le processus mais on obtiens le username (russell)
5. volatility3 linux.pagecache.Files | grep "/home/russell" | less -> tout les fichiers ouverts de l'utilisateur russell. La seule image est au directory /home/russell/Desktop/souvenir.jpeg
6. volatility3 linux.pagecache.InodePages --find "/home/russell/Desktop/souvenir.jpeg" --dump  -> récupérer la photo (flag)
7. Répérer le fichier .dmp qui a du contenu. Valider le type de fichier et renommer en .jpeg
8. Ouvrir la photo et récupérer le flag!

## Write-up EN

This is a RAM analysis challenge. Use Volatility 3 to perform the following actions:

1. volatility3 banners
2. Download the symbols (https://github.com/Abyss-W4tcher/volatility3-symbols/blob/master/Ubuntu/amd64/6.8.0/40/generic/Ubuntu_6.8.0-40-generic_6.8.0-40.40~22.04.3_amd64.json.xz)and place the JSON files under volatility3/symbols/linux.
3. volatility3 linux.pslist -> gimp is an image editor.
4. volatility3 linux.lsof --pid "process PID" -> lists the files associated with the gimp process. The target file is not listed, but we get the username (russell).
5. volatility3 linux.pagecache.Files | grep "/home/russell" | less -> lists all open files for the user russell. The only image is located at /home/russell/Desktop/souvenir.jpeg.
6. volatility3 linux.pagecache.InodePages --find "/home/russell/Desktop/souvenir.jpeg" --dump -> extract the photo (flag).
7. Identify the .dmp file containing data. Verify the file type and rename it to .jpeg.
8. Open the photo and get the flag!

## Flag

`polycyber{Y0u_Sav3d_Russ3ll_f4v_P1c}`
