import math
import random
import time  # Import time module to handle time limits
from typing import Callable

from bg_player import BGPlayer
from seahorse.game.light_action import LightAction
from seahorse.game.game_state import GameState
from game_state_connect4 import GameStateConnect4

class TimeOutException(Exception):
    """Custom exception to handle timeouts in the search."""
    pass

class Node:
    def __init__(self, state :GameStateConnect4=None, parent=None, action=None):
        self.parent = parent
        self.state = state
        self.action = action
        self.children : list[Node] = []
        self.visits = 0
        self.score = 0

class MyPlayerBG(BGPlayer):
    """
    A player class for Connect4 that limits computation time per turn to 5 seconds.
    """

    def __init__(self, piece_type: str, name: str = "bob", strategy="1", interactive=False) -> None:
        """
        Initializes a new instance of the MyPlayerBG class.

        Args:
            piece_type (str): The type of the player's game piece.
            name (str): The name of the player.
            strategy (str): The strategy to use ("1" for average heuristic, "2" for strong heuristic).
            interactive (bool): Whether the player is interactive.
        """
        super().__init__(piece_type, name)
        self.strategy = strategy
        self.interactive = interactive

    def random_strategy(self, currentState: GameState):
        """
        Chooses a random valid action.
        """
        return random.choice(currentState.get_possible_light_actions())
    
    def halpha_beta_strategy(self, currentState: GameState, heuristic: Callable, time_limit: float):
        """
        Performs iterative deepening alpha-beta pruning with a time limit.

        Args:
            currentState (GameState): The current game state.
            heuristic (Callable): The heuristic function to use.
            time_limit (float): The time limit as a timestamp.
        """
        best_action = None
        depth = 1

        while True:
            try:
                # Start the alpha-beta search at the current depth
                v, action = self._halpha_beta_search(currentState, heuristic, time_limit, depth)
                if action is not None:
                    best_action = action  # Update the best action found so far
                depth += 1  # Increase the depth for the next iteration
            except TimeOutException:
                # Time limit reached; break out of the loop
                break
            except Exception as e:
                # Handle any unexpected exceptions
                print(f"An error occurred: {e}")
                break
        
        print(f"Depth reached: {depth - 1}")
        if best_action is None:
            # If no action was found (time limit reached immediately), return a random valid action
            return self.random_strategy(currentState)
        return best_action

    def _halpha_beta_search(self, currentState: GameState, heuristic: Callable, time_limit: float, depth_limit: int):
        """
        Helper function to perform alpha-beta search up to a certain depth.

        Args:
            currentState (GameState): The current game state.
            heuristic (Callable): The heuristic function to use.
            time_limit (float): The time limit as a timestamp.
            depth_limit (int): The maximum depth to search.
        """
        def max_value(state: GameState, alpha, beta, depth):
            if time.time() > time_limit:
                raise TimeOutException()
            if state.is_done() or depth == 0:
                return heuristic(state), None
            v_star = -math.inf
            m_star = None
            for a in state.get_possible_light_actions():
                next_state = state.apply_action(a)
                v, _ = min_value(next_state, alpha, beta, depth - 1)
                if v > v_star:
                    v_star = v
                    m_star = a
                alpha = max(alpha, v_star)
                if v_star >= beta:
                    break  # Beta cutoff
            return v_star, m_star

        def min_value(state: GameState, alpha, beta, depth):
            if time.time() > time_limit:
                raise TimeOutException()
            if state.is_done() or depth == 0:
                return heuristic(state), None
            v_star = math.inf
            m_star = None
            for a in state.get_possible_light_actions():
                next_state = state.apply_action(a)
                v, _ = max_value(next_state, alpha, beta, depth - 1)
                if v < v_star:
                    v_star = v
                    m_star = a
                beta = min(beta, v_star)
                if v_star <= alpha:
                    break  # Alpha cutoff
            return v_star, m_star

        # Start the search with the max player
        return max_value(currentState, -math.inf, math.inf, depth_limit)

    def average_heuristic(self, state: GameState):
        """
        A heuristic function that counts the number of potential winning lines for the player.
        """
        player_id = self.get_id()
        opponent_id = next(iter(set(state.get_players()) - {self})).get_id()
        env = state.get_rep().get_env()
        rows, cols = state.get_rep().get_dimensions()
        
        score = 0
        
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # vertical, horizontal, diagonals
        
        for row in range(rows):
            for col in range(cols):
                for dx, dy in directions:
                    line_cells = []
                    for i in range(4):
                        x = row + i * dx
                        y = col + i * dy
                        if 0 <= x < rows and 0 <= y < cols:
                            line_cells.append((x, y))
                        else:
                            break
                    if len(line_cells) == 4:
                        player_pieces = sum(
                            1 for x, y in line_cells if env.get((x, y)) and env[(x, y)].get_owner_id() == player_id
                        )
                        opponent_pieces = sum(
                            1 for x, y in line_cells if env.get((x, y)) and env[(x, y)].get_owner_id() == opponent_id
                        )
                        if opponent_pieces == 0 and player_pieces > 0:
                            # This is a potential line for the player
                            score += player_pieces
        return score
    
    def strong_heuristic(self, state: GameState):
        """
        A strong heuristic that evaluates both player's and opponent's potential winning lines,
        giving higher weight to lines with more pieces and penalizing opponent's threats.
        """
        player_id = self.get_id()
        opponent = next(iter(set(state.get_players()) - {self}))
        opponent_id = opponent.get_id()
        env = state.get_rep().get_env()
        rows, cols = state.get_rep().get_dimensions()
        
        score = 0
        
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # vertical, horizontal, diagonals
        
        # Check for immediate win or loss
        if state.get_player_score(self) > state.get_player_score(opponent):
            return float('inf')
        elif state.get_player_score(self) < state.get_player_score(opponent):
            return float('-inf')

        for row in range(rows):
            for col in range(cols):
                for dx, dy in directions:
                    line_cells = []
                    for i in range(4):
                        x = row + i * dx
                        y = col + i * dy
                        if 0 <= x < rows and 0 <= y < cols:
                            line_cells.append((x, y))
                        else:
                            break
                    if len(line_cells) == 4:
                        player_pieces = sum(
                            1 for x, y in line_cells if env.get((x, y)) and env[(x, y)].get_owner_id() == player_id
                        )
                        opponent_pieces = sum(
                            1 for x, y in line_cells if env.get((x, y)) and env[(x, y)].get_owner_id() == opponent_id
                        )
                        if player_pieces > 0 and opponent_pieces == 0:
                            if player_pieces == 4:
                                return float('inf')  # Winning move
                            score += 10 ** player_pieces
                        elif opponent_pieces > 0 and player_pieces == 0:
                            if opponent_pieces == 4:
                                return float('-inf')  # Losing move
                            score -= 10 ** opponent_pieces
        return score

    # def MCTS(self, current_state: GameState, max_time: int = 1e9):
    #     """
    #     Use the mcts algorithm to choose the best action based on the heuristic evaluation of game states.

    #     Args:
    #         current_state (GameState): The current game state.

    #     Returns:
    #         Action: The best action as determined by mcts.
    #     """
        
    #     init_time = time.time()
    #     root = Node(current_state)
    #     while time.time() - init_time < max_time:
    #         node = self.select(root)
    #         if node.visits > 0:
    #             node = self.expand(node)
    #         score = self.simulate(node)
    #         self.backpropagate(node, score)

    #     best_action = self.best_action(root).action
    #     return best_action
    

    # def select(self, root: Node):
    #     node = root
    #     depth = 0
    #     while len(node.children) != 0:
    #         # if depth > self.max_depth:
    #             # self.max_depth = depth
    #             # print("Max depth: ", self.max_depth)
    #         # depth += 1
    #         node = self.best_child(node)
    #     return node
    
    # def best_action(self, node: Node):
    #     best = None
    #     best_score = float('-inf')
    #     for child in node.children:
    #         score = child.visits
    #         if score > best_score:
    #             best_score = score
    #             best = child
    #     return best
    
    # def best_child(self, node: Node):
    #     best = None
    #     best_score = float('-inf')
    #     for child in node.children:
    #         if child.visits == 0:
    #             return child
    #         score = child.score / child.visits + math.sqrt(2 * math.log(node.visits) / child.visits)
    #         if score > best_score:
    #             best_score = score
    #             best = child
    #     return best
    
    # def expand(self, node: Node):
    #     actions = node.state.generate_possible_light_actions()
    #     for action in actions:
    #         child = Node(node.state.apply_action(action), node, action)
    #         node.children.append(child)

    #     if len(node.children) == 0:
    #         return node
    #     return random.choice(node.children)

    # def simulate(self, node: Node):
    #     state = node.state
    #     while not state.is_done():
    #         actions = state.generate_possible_light_actions()
    #         action = random.choice(list(actions))
    #         state = state.apply_action(action)
    #     score = state.scores[self.get_id()] - state.scores[next(iter([x for x in state.players if x != self.get_id()])).get_id()]
    #     return score


    # def backpropagate(self, node: Node, score: float):
    #     while node is not None:
    #         node.visits += 1
    #         node.score += score
    #         node = node.parent
    #     return

    def check_column(self, gs, column, check=True):
        """
        Checks if a move in the specified column is valid.

        Args:
            gs (GameState): The current game state.
            column (int): The column number (1-based indexing).
            check (bool): If True, returns whether the move is valid. If False, returns the action.
        """
        chosen_action = None
        for action in gs.get_possible_light_actions():
            if action.data["position"][1] == column - 1:
                chosen_action = action
                break
        if check:
            return chosen_action is not None
        return chosen_action
        
    def compute_action(self, current_state: GameState, **kwargs) -> LightAction:
        """
        Implements the logic of the player according to the strategy,
        ensuring the computation time does not exceed 5 seconds.

        Args:
            current_state (GameState): The current game state.
            **kwargs: Additional keyword arguments.
        """
        if self.interactive:
            column = input("Enter the column number: ")

            while not column.isdigit() or \
                  int(column) not in range(1, current_state.get_rep().get_dimensions()[1] + 1) or \
                  not self.check_column(current_state, int(column)):
                column = input("Enter a valid column number: ")
            
            column = int(column)
            return self.check_column(current_state, column, check=False)
        else:
            time_limit = time.time() + 4.0
            if self.strategy == "1":
                return self.halpha_beta_strategy(
                    current_state, heuristic=self.average_heuristic, time_limit=time_limit
                )
            elif self.strategy == "2":
                possible_actions = current_state.get_possible_light_actions()
                for action in possible_actions:
                    if current_state.step == 1 and action.data["position"][1] == 3:
                        return action
                    
                    next_state = current_state.apply_action(action)
                    opponent = next(iter(set(next_state.get_players()) - {self}))
                    if next_state.get_player_score(self) > next_state.get_player_score(opponent):
                        return action

                # return self.MCTS(current_state=current_state, max_time=4)
                return self.halpha_beta_strategy(
                    current_state, heuristic=self.strong_heuristic, time_limit=time_limit
                )
            else:
                return self.random_strategy(current_state)
