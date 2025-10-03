from flask import Flask, render_template, request
import os
import random

app = Flask(__name__)
tic_board = [""] * 9
four_board = [["" for _ in range(6)] for _ in range(7)]


def return_block_spot(empty_list, user_list):
    index_list = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for indexes in index_list:
        for i in range(3):
            new_indexes = indexes.copy()
            block_spot = indexes.pop(i)
            if indexes[0] in user_list and indexes[1] in user_list and block_spot in empty_list:
                return block_spot
            indexes = new_indexes
    return None



def tic_computer_fill(b):
    empty_indexes = [i for i in range(9) if b[i] == ""]
    computer_indexes = [i for i in range(9) if b[i] == "O"]
    user_indexes = [i for i in range(9) if b[i] == "X"]

    computer_block_spot = return_block_spot(empty_indexes, computer_indexes)
    if computer_block_spot:
        b[computer_block_spot] = "O"
    else:
        user_block_spot = return_block_spot(empty_indexes, user_indexes)
        if user_block_spot:
            b[user_block_spot] = "O"
        else:
            b[random.choice(empty_indexes)] = "O"


def check_status(b):
    index_list = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for indexes in index_list:
        if [b[i] for i in indexes] == ["O","O","O"]:
            return 0
        if [b[i] for i in indexes] == ["X","X","X"]:
            return 1
    if "" not in b:
        return 2
    
    return None


def four_user_fill(b,col):
    for i in range(6):
        if b[col][i] != "":
            b[col][i-1] = "X"
            break
        if i == 5:
            b[col][i] = "X"


def four_computer_fill(b):
    col = random.randint(0,6)
    while "" not in b[col]:
        col = random.randint(0,6)

    for i in range(6):
        if b[col][i] != "":
            b[col][i - 1] = "O"
            break
        if i == 5:
            b[col][i] = "O"


def sub_list(list1,list2):
    value = 0
    for item in list1:
        if item in list2:
            value += 1
    if value == len(list1):
        return True
    return False

def check_win(spot_list):
    for spot in spot_list:
        print([(spot[0], spot[1] + 1), (spot[0], spot[1] + 2), (spot[0], spot[1] + 3)], spot_list)
        if (sub_list([(spot[0],spot[1]+1),(spot[0],spot[1]+2),(spot[0],spot[1]+3)],spot_list) or
            sub_list([(spot[0],spot[1]-1),(spot[0],spot[1]-2),(spot[0],spot[1]-3)],spot_list) or
            sub_list([(spot[0]+1,spot[1]), (spot[0]+2, spot[1]), (spot[0]+3, spot[1])], spot_list) or
            sub_list([(spot[0]-1, spot[1]), (spot[0]-2, spot[1]), (spot[0]-3, spot[1])], spot_list) or
            sub_list([(spot[0]+1, spot[1]-1), (spot[0]+2, spot[1]-2), (spot[0]+3, spot[1]-3)], spot_list) or
            sub_list([(spot[0]+1, spot[1]+1), (spot[0]+2, spot[1]+2), (spot[0]+3, spot[1]+3)], spot_list) or
            sub_list([(spot[0]-1, spot[1]-1), (spot[0]-2, spot[1]-2), (spot[0]-3, spot[1]-3)], spot_list) or
             sub_list([(spot[0]-1, spot[1]+1), (spot[0]-2, spot[1]+2), (spot[0]-3, spot[1]+3)], spot_list)):
            return True
    return False


def four_check_status(b):               # RECURSION PROBLEM
    user_spots = []
    computer_spots = []
    for col in range(7):
        for row in range(6):
            if b[col][row] == "X":
                user_spots.append((col,row))
            if b[col][row] == "O":
                computer_spots.append((col,row))
    if check_win(user_spots):
        return 1
    if check_win(computer_spots):
        return 0

    index = 0
    for i in range(7):
        if "" not in b[i]:
            index += 1
    if index == 7:
        return 2
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tic", methods = ["GET", "POST"])
def tic():
    if request.method == "GET":
        global tic_board
        tic_board = [""] * 9

    if request.method == "POST":
        position = request.form.get("pos")
        tic_board[int(position)] = "X"     # SET USER MOVE AS CLICKED

        status = check_status(tic_board)   # CHECK GAME STATUS
        if status == None:
            tic_computer_fill(tic_board)       # COMPUTER MOVE
            status = check_status(tic_board)

        return render_template("tic.html", board=tic_board, status=status)


    if random.randint(0, 1) == 0:               # INITIAL COMPUTER MOVE
        tic_computer_fill(tic_board)

    return render_template("tic.html",board=tic_board, status=None)


@app.route("/connect-four", methods = ["GET", "POST"])
def connect_four():
    if request.method == "GET":
        global four_board
        four_board = [["" for _ in range(6)] for _ in range(7)]

    if request.method == "POST":
        col = int(request.form.get("col"))
        four_user_fill(four_board,col)

        status = four_check_status(four_board)
        if status == None:
            four_computer_fill(four_board)
            status = four_check_status(four_board)

        return render_template("connect-four.html", board=four_board,status=status)

    if random.randint(0,1) == 0:
        four_computer_fill(four_board)

    return render_template("connect-four.html",board=four_board,status=None)


if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
