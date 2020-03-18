import chess
import numpy as np
from evaluator import *

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

board = chess.Board()

@app.route('/chess_ai', methods=['GET', 'POST'])
def chess_ai():
    if request.args.get("move"):

        #player move
        move_str = request.args.get("move")
        move = chess.Move.from_uci(move_str)
        board.push(move)


        #AI move
        elm = evaluate_legal_moves(board)
        print(elm)
        best_move = min(elm, key=elm.get)
        board.push(best_move)


    legal_moves = [legal_move.uci() for legal_move in board.legal_moves]
    chessboard = np.array(list(str(board).replace(' ','').replace('.',' ').replace("\n",""))).reshape(8,8)

    return render_template('index.html', chessboard = chessboard, legal_moves = legal_moves)

@app.route('/reset_board', methods=['GET', 'POST'])
def reset_board():
    board.reset_board()
    return redirect(url_for('chess_ai'))