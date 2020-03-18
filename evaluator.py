from tensorflow.keras.models import model_from_json
import numpy as np

def position_parser(position_string):
    piece_map = {'K': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'Q': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'R': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'B': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 'N': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 'P': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 'k': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 'q': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                 'r': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 'b': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 'n': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 'p': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}

    position_array = []

    ps = position_string.replace('/', '')

    for char in ps:
        position_array += 12 * int(char) * [0] if char.isdigit() else piece_map[char]

    # print("position_parser =>  position_array: {}".format(asizeof.asizeof(position_array)))

    return position_array


def fen_to_binary_vector(fen):
    # counter += 1
    # clear_output(wait=True)
    # print(str(counter)+"\n")

    fen_infos = fen.split()

    pieces_ = 0
    turn_ = 1
    castling_rights_ = 2
    en_passant_ = 3
    half_moves_ = 4
    moves_ = 5

    binary_vector = []

    binary_vector += ([1 if fen_infos[turn_] == 'w' else 0]
                      + [1 if 'K' in fen_infos[castling_rights_] else 0]
                      + [1 if 'Q' in fen_infos[castling_rights_] else 0]
                      + [1 if 'k' in fen_infos[castling_rights_] else 0]
                      + [1 if 'q' in fen_infos[castling_rights_] else 0]
                      + position_parser(fen_infos[pieces_])
                      )

    # print("fen_to_binary_vector =>  binary_vector: {}".format(asizeof.asizeof(binary_vector)))
    # clear_output(wait=True)

    return binary_vector

def evaluate_position(model, fen):

    v = fen_to_binary_vector(fen)
    return model.predict(np.array(v).reshape(1,-1))[0][0]

def evaluate_legal_moves(board):

    json_file = open('models/model2.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    move_evaluation = {}
    for move in board.legal_moves:
        next_board = board.copy()
        next_board.push(move)
        move_evaluation[move] = evaluate_position(loaded_model, next_board.fen())

    return move_evaluation


