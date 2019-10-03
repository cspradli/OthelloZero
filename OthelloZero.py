import math
import numpy as np

class OthelloZeroConfig(object):
    def __init__(self):
        self.num_actors = 5000
        self.num_sampling_moves = 30
        self.max_moves = 8*8+1
        self.num_simulations = 800
        self.root_diralecht_alpha = 0.3
        self.root_exploration_fraction = 0.25

        self.pb_c_base = 19652
        self.pb_c_base = 1.25

        self.training_steps = int(7000e3)
        self.checkpoint_interval = int(1e3)
        self.window_size = int(1e6)
        self.batch_size = 4096

        self.weight_decay = 1e-4
        self.momentum = 0.9
        self.learning_rate_schedule = {
            0: 2e-1,
            100e3: 2e-2,
            300e3: 2e-3,
            500e3: 2e-4
        }

class Node(object):

    def __init__(self, prior: float):
        self.visit_count = 0
        self.to_play = -1
        self.prior = prior
        self.value_sum = 0
        self.children = {}

        def expanded(self):
            return len(self.children) > 0
        
        def value(self):
            if self.visit_count == 0:
                return 0
            return self.value_sum / self.visit_count


class Game(object):

    def __init__(self, history=None):
        self.history = history or []
        self.child_visits = []
        self.num_actions = 8*8+1

    def terminal(self):
        #Game specific termination rules
        pass

    def terminal_value(self, to_play):
        #game specific value
        pass

    def legal_actions(self):
        #get legal moves for othello
        return []
        
    def clone(self):
        return Game(list(self.history))
        
    def apply(self, action):
        self.history.append(action)

    def store_search_stats(self, root):
        sum_visits = sum(child.visit_count for child in root.children.iterValues())
        self.child_visits.append([root.children[a].visit_count / sum_visits if a in root.children else 0 for a in range(self.num_actions)])

    def make_image(self, state_index: int):
        return []

    def make_target(self, state_index: int):
        return (self.terminal_value(state_index % 2), 
        self.child_visits[state_index])

    def to_play(self):
        return len(self.history) % 2

class ReplayBuffer(object):
    
    def __init__(self, config: OthelloZeroConfig):
        self.window_size = config.window_size
        self.batch_size = config.batch_size
        self.buffer = []

    def save_game(self, game):
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)
        self.buffer.append(game)

    def sample_batch(self):
        move_sum = float(sum(len(g.history) for g in self.buffer))
        games = np.random.choice(
            self.buffer,
            size = self.batch_size,
            p = [len(g.history) / move_sum for g in self.buffer])
        game_pos = [(g, np.randint(len(g.history))) for g in games]
        return [(g.make_image(i), g.make_target(i)) for (g,i) in game_pos]
        

