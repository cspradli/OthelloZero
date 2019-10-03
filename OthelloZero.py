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

class Network(object):
    
    def inference(self, image):
        return(-1, {})
    
    def get_weights(self):
        return []

class SharedStorage(object):

    def __init__(self):
        self.__networks = {}

    def latest_network(self) -> Network:
        if self.__networks:
            return self.__networks[max(self.__networks.iterkeys())]
        else:
            return make_uniform_network()

    def save_network(self, step: int, network: Network):
        self.__networks[step] = network

### END HELPER FUNCTIONS ###

def OthelloZero(config: OthelloZeroConfig):
    storage = SharedStorage()
    replay_buffer = ReplayBuffer(config)

    for i in range(config.num_actors):
        launch_job(run_selfplay, config, storage, replay_buffer)

    train_network(config, storage, replay_buffer)

    return storage.latest_network()

### SELF PLAY ###

def run_selfplay(config: OthelloZeroConfig, storage: SharedStorage, replay_buffer: ReplayBuffer):
    while True:
        network = storage.latest_network
        game = play_game(config, network)
        replay_buffer.save_game(game)

def play_game(config: OthelloZeroConfig, network: Network):
    game = Game()
    while not game.terminal() and len(game.history) < config.max_moves:
        action, root = run_mcts(config, game, network)
        game.apply(action)
        game.store_search_stats(root)
    return game

def run_mcts(config: OthelloZeroConfig, game: Game, network: Network):
    root = Node(0)
    evaluate(root, game, network)
    add_exploration_noise(config, root)

    for i in range(config.num_simulations):
        node = root
        scratch_game = game.clone()
        search_path = [node]

        while node.expanded():
            action, node = select_child(config, node)
            scratch_game.apply(action)
            search_path.append(node)

        value = evaluate(node, scratch_game, network)
        backpropagate(search_path, value, scratch_game.to_play())

    return select_action(config, game, root), root

def select_action(config: OthelloZeroConfig, game: Game, root: Node):
    visit_counts = [(child.visit_count, action) for action, child in root.children.iteritems()]
    if len(game.history) < config.num_sampling_moves:
        _, action = softmax_sample(visit_counts)
    else:
        _, action = max(visit_counts)
    return action



