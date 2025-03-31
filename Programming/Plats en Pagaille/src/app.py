from enum import Enum
import random
import sys
import time
from inputimeout import inputimeout 

class Consignes(Enum):
    BIEN = 4
    MAUVAIS = 1
    PAUSE = 3
    FINI = 0
    EXCELLENT = 2

PAUSE_TIME = 3

COUVERTS = [
    r"""
  _________
 /         \
|  |||  |\  |
|   |   |/  |
|   |   |   |
 \_________/""",
    r"""
  _________
 /         \
|   ///|\   |
|   /   L\  |
|  /      \ |
 \_________/""",
    r"""
  _________
 /         \
|     \\\|\ |
|       \ L\|
|        \  \
 \_________/""",
    r"""
  _________
 /         \
|  ///  |\  |
|  /     L\ |
| /        \|
 \_________/""",
    r"""
  _________
 /         \
|           |
|   ----E   |
|   --==>   |
 \_________/"""
]

with open("menu.txt", "r", encoding="utf-8") as f:
    MENU = {ligne.strip().lower() for ligne in f}

with open("plats_flag.txt", "r", encoding="utf-8") as f:
    PLATS_FLAG = [ligne.strip() for ligne in f]

def main():
    print("> Je ne souhaite que les meilleurs de vos plats\nSurprenez-moi !")

    index_plat = 0
    consigne = Consignes.MAUVAIS
    while(consigne != Consignes.FINI):
        plat = input("\n> ").strip()

        # Cas entrée utilisateur faisant partie du menu
        if (plat.lower() in MENU and plat!="" and plat[0]!='-') :
            if(plat.lower() == PLATS_FLAG[index_plat].lower()):
                if(PLATS_FLAG[index_plat][0].islower() or not PLATS_FLAG[index_plat][0].isupper()):
                    consigne = Consignes.BIEN
                else:
                    consigne = Consignes.EXCELLENT
                index_plat = index_plat+1
            else :
                consigne = Consignes.MAUVAIS
        
        # Cas entrée utilisateur ne faisant pas partie du menu
        else :
            consigne = Consignes.FINI
            print(COUVERTS[consigne.value])
            print("\n> Quel est ce plat ? Préparez-vous à perdre une étoile !")
            return 0
        
        # De manière aléatoire, affiche un couvert marquant une pause
        random_number = random.randint(0, 15)
        if(random_number == 0):
            print(COUVERTS[Consignes.PAUSE.value])
            # L'utilisateur ne doit rien rentrer pendant le temps de pause
            try: 
                inputimeout(prompt='\n> ', timeout=PAUSE_TIME) 
                print("\n> Je ne peux pas manger dans ces conditions, vous allez trop vite !")
                return 0
            
            # Si l'utilisateur ne rentre rien, tout va bien
            except Exception: 
                pass
        
        # Affichage des couverts
        print(COUVERTS[consigne.value])
        if(index_plat == len(PLATS_FLAG)-1):
            consigne = Consignes.FINI
    print(COUVERTS[consigne.value])
    print("\n> Ce soir, j’ai découvert un nouveau talent, un génie en fait, un génie aussi rare qu’imprévisible.\nLe flag se trouve dans ce que j'ai aimé et ADORÉ")
    sys.stdout.flush()
    time.sleep(2)

if __name__ == "__main__":
    main()
        
