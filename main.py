from flask import Flask, render_template, request
import os
import random

app = Flask(__name__)
tic_board = [""] * 9
four_board = [["" for _ in range(6)] for _ in range(7)]

def sub_list(list1,list2):
    value = 0
    for item in list1:
        if item in list2:
            value += 1
    if value == len(list1):
        return True
    return False

def return_end_spot(position_list, empty_list):
    combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for combination in combinations:
        for i in range(3):
            filled_spots = combination.copy()
            empty_spot = filled_spots.pop(i)
            if empty_spot in empty_list and filled_spots[0] in position_list and filled_spots[1] in position_list:
                return empty_spot
    return None

def return_feasible_spots(position_list,empty_list):
    combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    single_spots = []
    critical_spot = None
    for i in range(len(combinations)):
        for j in range(3):
            empty_spots = combinations[i].copy()
            filled_spot = empty_spots.pop(j)

            if empty_spots[0] in empty_list and empty_spots[1] in empty_list and filled_spot in position_list:
                new_combinations = combinations.copy()
                new_combinations.remove(combinations[i])

                for the_combination in new_combinations:
                    for k in range(2):
                       if empty_spots[k] in the_combination:
                           possible_filled_spots = the_combination.copy()
                           possible_filled_spots.remove(empty_spots[k])
                           if possible_filled_spots[0] in position_list or possible_filled_spots[1] in position_list:
                               if not critical_spot:
                                   critical_spot = empty_spots[k]

                if empty_spots[0] != critical_spot and empty_spots[0] not in single_spots:
                    single_spots.append(empty_spots[0])
                if empty_spots[1] != critical_spot and empty_spots[1] not in single_spots:
                    single_spots.append(empty_spots[1])

    return critical_spot,single_spots


def return_strategic_spots(empty_list):
    combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    empty_combinations = [combination for combination in combinations if sub_list(combination,empty_list)]
    appearances = [0 for _ in range(9)]
    indexes = [i for i in range(9)]
    for combination in empty_combinations:
        for i in range(3):
            appearances[combination[i]] += 1

    index_order = sorted(indexes,key=lambda x:appearances[x],reverse=True)
    return index_order



def tic_computer_fill(b):
    user_positions = []
    computer_positions = []
    empty_positions = []
    for i in range(len(b)):
        if b[i] == "X":
            user_positions.append(i)
        if b[i] == "O":
            computer_positions.append(i)
        if b[i] == "":
            empty_positions.append(i)

    computer_spot = return_end_spot(computer_positions,empty_positions)
    if computer_spot != None:
        b[computer_spot] = "O"
        print(1)
    else:
        user_spot = return_end_spot(user_positions,empty_positions)
        if user_spot != None:
            b[user_spot] = "O"
            print(2)
        else:
            computer_feasible_spots = return_feasible_spots(computer_positions,empty_positions)
            user_feasible_spots = return_feasible_spots(user_positions,empty_positions)
            if computer_feasible_spots[0]:
                b[computer_feasible_spots[0]] = "O"
            elif user_feasible_spots[0]:
                b[user_feasible_spots[0]] = "O"
            else:
                value = 0
                strategic_spots = return_strategic_spots(empty_positions)
                for spot in strategic_spots:
                    if spot in computer_feasible_spots[1]:
                        value += 1
                        b[spot] = "O"
                        break
                if not value:
                    for spot in strategic_spots:
                        if spot in user_feasible_spots[1]:
                            value += 1
                            b[spot] = "O"
                            break
                    if not value:
                        b[strategic_spots[0]] = "O"

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


# @app.route("/connect-four", methods = ["GET", "POST"])
# def connect_four():
#     if request.method == "GET":
#         global four_board
#         four_board = [["" for _ in range(6)] for _ in range(7)]
#
#     if request.method == "POST":
#         col = int(request.form.get("col"))
#         four_user_fill(four_board,col)
#
#         status = four_check_status(four_board)
#         if status == None:
#             four_computer_fill(four_board)
#             status = four_check_status(four_board)
#
#         return render_template("connect-four.html", board=four_board,status=status)
#
#     if random.randint(0,1) == 0:
#         four_computer_fill(four_board)
#
#     return render_template("connect-four.html",board=four_board,status=None)

@app.route("/snake")
def snake():
    return render_template("snake.html")

@app.route("/pong")
def pong():
    return render_template("pong.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
