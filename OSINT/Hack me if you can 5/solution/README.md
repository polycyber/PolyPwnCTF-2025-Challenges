# Hack me if you can 5/5

## Write-up FR

Dans cet ultime défi, il fallait bien regarder les photos de la perquisition et trouver un indice intéressant, un bout d'url : .gg/vFzZQKjkmY  
En se renseignant en ligne sur ce que cela pouvait être, on tombe sur les invitations discord, qui sont de ce format là.  
On peut aller former l'url complet : https://discord.gg/vFzZQKjkmY  

On arrive alors sur le serveur Discord de Frank Konners, dans lequel il anime une communauté de falsification de chèques.  
On voit alors un message intéressant, il dit à Brenda que si elle veut participer aux activités, elle doit avoir un rôle spécial. 
   
En testant tous les rôles possibles, on peut alors en voir deux qui donnent accès à des canaux supplémentaires :
- Le rôle tampering-enthusiast donne accès à un forum dans lequel Frank dit que le prochain meeting aura lieu le 29 mars dans un lieu caché dans une photo avec un mot de passe. Il précise que le mot de passe a été donné aux "counterfeiters'
- le rôle counterfeiters donne accès à un canal dans lequel il donne le lien vers https://justpaste.it/g4htx, ui contient, écrit en blanc, le mot de passe : uF4dcz15j  

Avec toutes ces informations, on peut alors appliquer la méthode LSB sur l'image pour en extraire des données (avec l'outil steghide par exemple).  
On trouver alors le texte : Rendez-vous at the Beaver lake on March 29 - F Konners / Taylor / Abagnale

## Write-up EN

In this final challenge, the key was to closely examine the photos from the raid and find an interesting clue: a piece of a URL: .gg/vFzZQKjkmY.  
By researching online what this could be, we discover that it corresponds to a Discord invitation, which follows this format.  
We can complete the URL: https://discord.gg/vFzZQKjkmY.  

This leads us to Frank Konners' Discord server, where he runs a community focused on check forgery.  
We then see an interesting message where Frank tells Brenda that if she wants to participate in the activities, she must have a special role.  

By testing all possible roles, we find two that provide access to additional channels:
- The tampering-enthusiast role gives access to a forum where Frank says the next meeting will be on March 29 at a secret location hidden in a photo, along with a password. He mentions that the password has been given to the "counterfeiters."
- The counterfeiters role gives access to a channel where he shares a link to https://justpaste.it/g4htx, which contains the password, written in white text: uF4dcz15j.  
With all this information, we can apply the LSB (Least Significant Bit) method on the image to extract data (using a tool like steghide, for example).  

We will find the text: "Rendez-vous at the Beaver lake on March 29 - F Konners / Taylor / Abagnale."  

## Flag

`polycyber{beaver_lake}` ou `polycyber{lac_aux_castors}`
