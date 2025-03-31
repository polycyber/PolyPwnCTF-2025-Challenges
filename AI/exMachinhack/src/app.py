import sys
from bg_board import BGBoard
from game_state_connect4 import GameStateConnect4
from master import Master
from my_player_bg import MyPlayerBG

def play(player1, player2, log_level, port, address) :

    list_players = [player1, player2]
    init_scores = {player1.get_id(): 0, player2.get_id(): 0}
    dim = [6, 7]
    init_rep = BGBoard(env={}, dim=dim)
    initial_game_state = GameStateConnect4(
        scores=init_scores, next_player=player1, players=list_players, rep=init_rep, step=1
        )

    master = Master(
        name="connect_4", initial_game_state=initial_game_state, players_iterator=list_players, log_level=log_level, port=port, hostname=address
    )

    master.record_game(listeners=[])
    
    return master.winner


if __name__=="__main__":

    # get port, its the first argv
    port = int(sys.argv[1])

    flag = "polycyber{C0nn3cT_4_15_50lV3D}"

    game_type = 'human_vs_computer' # 'local'

    player1 = MyPlayerBG("W", name="AVA", strategy="2", interactive=False)
    player2 = MyPlayerBG("B", name="Hacking Enthusiast", strategy="2", interactive=game_type != 'local')

    winner = play(player1=player1, player2=player2, log_level="INFO", port=port, address="localhost")

    if winner and len(winner) == 1 and winner[0].get_name() != "AVA":
        print("Congratulations, you won!")
        print(f"The flag is: {flag}")
    else:
        print("You lost, try again!")