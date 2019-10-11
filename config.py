class config(object):

    num_iterations = 4
    num_channels = 10
    num_games = 30
    num_mcts_sims = 30
    c_puct = 1
    val = 0.0001
    momentum = 0.9
    learn_rate = 0.01
    polict_val = 0.0001
    temp_init = 1
    temp_final = 0.001
    temp_thresh = 10
    epochs = 10
    batch_size = 128
    dirilecht_alpha = 0.3
    epsilon = 0.25
    models_direc = "./models/"
    num_eval_games: 12
    eval_win_rate = 0.55
    load_model = 1
    