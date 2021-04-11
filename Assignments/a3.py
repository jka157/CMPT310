# John (Junseong) Kim
# 301262540
# jka157@sfu.ca

# References:

# TA - Mohammad's Tutorials
# https://www.tutorialspoint.com/python/python_dictionary.htm
# https://pyformat.info/
# https://pynative.com/python-input-function-get-user-input/
# https://www.programiz.com/python-programming/methods

import random
import copy

# Display the board with moves
def display(state):

    print("*---*---*---*")
    print(f"| {state[0]} | {state[1]} | {state[2]} |")
    print("*---*---*---*")
    print(f"| {state[3]} | {state[4]} | {state[5]} |")
    print("*---*---*---*")
    print(f"| {state[6]} | {state[7]} | {state[8]} |")
    print("*---*---*---*")

def checkGame(state, num_plays):

    # Check Status of game:
    if num_plays >= 5:


        # Case 1:
        if state[0] == state[1] == state[2] != " ":
            print("This is case 1")
            if state[0] == "X":
                return 1
            else:
                return 2

        # Case 2:
        if state[3] == state[4] == state[5] != " ":
            print("This is case 2")
            if state[3] == "X":
                return 1
            else:
                return 2

        # Case 3:
        if state[6] == state[7] == state[8] != " ":
            print("This is case 3")
            if state[6] == "X":
                return 1
            else:
                return 2

        #  Case 4:
        if state[0] == state[3] == state[6] != " ":
            print("This is case 4")
            if state[0] == "X":
                return 1
            else:
                return 2

        #  Case 5:
        if state[1] == state[4] == state[7] != " ":
            print("This is case 5")
            if state[1] == "X":
                return 1
            else:
                return 2

        #  Case 6:
        if state[2] == state[5] == state[8] != " ":
            print("This is case 6")
            if state[2] == "X":
                return 1
            else:
                return 2

        #  Case 7:
        if state[0] == state[4] == state[8] != " ":
            print("This is case 7")
            if state[0] == "X":
                return 1
            else:
                return 2

        #  Case 8:
        if state[2] == state[4] == state[6] != " ":
            print("This is case 8")
            if state[2] == "X":
                return 1
            else:
                return 2

        # If the board is all filled up it is a draw
    if num_plays == 9:
        return 3

    return 0

# Recursion function:

def recursion(state, next_move, available_Moves, temp, size):
    lose = 0
    draw = 0
    win = 0
    right_move = []

    for p in range(size):
        if p % 2 == 0:
            temp += 1
            choice = random.choice(next_move)
            print("The player chose:", choice)
            state[choice] = "X"
            available_Moves[choice] = temp
            next_move.remove(choice)
            right_move.append(choice)
            # print(next_move)
            # print("Player:")
            # print(state)
            # print(available_Moves)
            # print(temp)
        else:
            temp += 1
            choice = random.choice(next_move)
            print("The computer chose:", choice)
            state[choice] = "O"
            available_Moves[choice] = temp
            next_move.remove(choice)
            right_move.append(choice)
            # print(next_move)
            # print("Computer:")
            # print(state)
            # print(available_Moves)
            # print(temp)
        display(state)
        finish = checkGame(state, temp)
        if finish == 3:
            print("Game is a draw")
            draw += 1
            return draw, lose, win
        elif finish == 1:
            print("Player wins")
            lose += 1
            return draw, lose, win
        elif finish == 2:
            print("Computer wins")
            win += 1
            return draw, lose, win
            # return 2, right_move

# Recursive function for simulation
def simulation(state, temp, next_move, available_Moves):
    size = len(next_move)
    total_win = 0
    total_lose = 0
    total_draw = 0

    default_state = state.copy()
    default_move = next_move.copy()
    default_avail = available_Moves.copy()
    default_temp = temp

    for q in range(100):
        state = default_state.copy()
        next_move = default_move.copy()
        available_Moves = default_avail.copy()
        temp = default_temp
        finish = 0
        print("Simulation #", q+1)
        print("\n")
        draw, lose, win = recursion(state, next_move, available_Moves, temp, size)
        print("Draw: ", draw)
        print("Win: ", win)
        print("Lose: ", lose)
        print("\n")

        total_win = total_win + win
        total_lose = total_lose + lose
        total_draw = total_draw + draw
        # print(total_win)
        # print(total_lose)
        # print(total_draw)
        # print(q)
        # lose = 0
        # draw = 0
        # win = 0


    return total_draw, total_win, total_lose

# Random simulation for Computer using Monte-Carlo Tree Search (MCTS)
def monte_simulation(state, steps, available_Moves):
    next_move = []
    win_count = []
    draw_count = []
    lose_count = []
    temp = steps

    finish = False
    # count = 0

    for k in range(len(state)):
        if state[k] == " ":
            next_move.append(k)
            # count += 1
    print(next_move)

    original_move = next_move.copy()
    original_state = state.copy()
    original_available = available_Moves.copy()

    print(state)
    print(original_state)

    for n in range(len(original_move)):
        print("Move #", n+1)
        state = original_state.copy()
        next_move = original_move.copy()
        available_Moves = original_available.copy()
        print(state)
        print(next_move)
        state[next_move[n]] = "O"
        available_Moves[next_move[n]] = temp
        print("The computer will test the simulation for move:", next_move[n])
        next_move.pop(n)
        print("These are the possible moves that can be chosen:", next_move)
        print("\n")
        draw, win, lose = simulation(state, temp, next_move, available_Moves)
        # result, correct_moves = simulation(state, temp, next_move, available_Moves)
        print("This is the total number of wins")
        win_count.append(win)
        draw_count.append(draw)
        lose_count.append(lose)
        print(win)
        print("\n")

    for z in range(len(win_count)):
        win_count[z] = (win_count[z] * 100) + (draw_count[z] * 10) - (lose_count[z] * 1000)

    # print(win_count)
    # print(max(win_count))
    # print(win_count.index(max(win_count)))

    state = original_state.copy()
    next_move = original_move.copy()
    available_Moves = original_available.copy()
    index = win_count.index(max(win_count))
    # print(index)
    state[next_move[index]] = "O"
    available_Moves[next_move[index]] = temp
    # print(next_move)
    # print(state)
    # print(available_Moves)

    print("With the simulation, the computer chose: ", next_move[index]+1)
    print("\n")


    return state, available_Moves

# The initial state is randomized for simplicity
def initialComp(state):
    num = random.randint(0, 8)
    state[num] = "O"
    # print(num)
    available_Moves[num] = 1

    return state, available_Moves

def getInput(state, index):
    # Making sure the user inputs the correct value between 0 to 9 and a position that has not been filled yet
    validMove = False
    while validMove == False:
        print("Pick a position between 1 and 9")
        player_move = int(input("Please enter your next move: "))
        print("\n")

        if player_move <= 9 and player_move > 0 and available_Moves[player_move - 1] == " ":
            validMove = True
            break

        print("Please enter a valid number that is empty and between 0 to 9")

    state[player_move - 1] = "X"
    available_Moves[player_move - 1] = index

    # print(steps)
    # print(available_Moves)

    return state, available_Moves

def initInput(state):
    # Making sure the user inputs the correct value between 0 to 9 and a position that has not been filled yet
    validMove = False
    while validMove == False:
        print("Pick a position between 1 and 9")
        player_move = int(input("Please enter your next move: "))
        print("\n")

        if player_move <= 9 and player_move > 0 and available_Moves[player_move - 1] == " ":
            validMove = True
            break

        print("Please enter a valid number that is empty and between 0 to 9")
    print(state)
    state[player_move - 1] = "X"
    available_Moves[player_move - 1] = 1

    # print(steps)
    # print(available_Moves)

    return state, available_Moves

# Player moves = X, Computer moves O
def play_a_new_game():
    moves =[]
    for i in range(9):
        moves.append(" ")

    firstTurn = int(input("Decide who wants to go first: 1 - You, 2 - Computer  "))

    while firstTurn != 1 and firstTurn != 2:
        print("Choose either 1 or 2 to decide who goes first")
        firstTurn = int(input("Decide who wants to go first: 1 - You, 2 - Computer"))

    if firstTurn == 1:
        player_turn = True
    else:
        player_turn = False

    gameStatus = 0
    turns = 1

    while gameStatus == 0:
        print("\n")
        print("*---*---*---*")
        print("| 1 | 2 | 3 |")
        print("*---*---*---*")
        print("| 4 | 5 | 6 |")
        print("*---*---*---*")
        print("| 7 | 8 | 9 |")
        print("*---*---*---*")
        print("\n")

        if player_turn == True:
            if turns == 1:
                moves, possibleMoves = initInput(moves)
            else:
                moves, possibleMoves = getInput(moves, turns)
            print("This is turn #" + str(turns))
            player_turn = False

        else:
            if turns == 1:
                moves, possibleMoves = initialComp(moves)
                print("This is turn #" + str(turns))
                player_turn = True
            elif turns == 9:
                final = moves.index(" ")
                moves[final] = "O"
            else:
                moves, possibleMoves = monte_simulation(moves, turns, possibleMoves)
                print("This is turn #" + str(turns))
                player_turn = True

        # print(possibleMoves)
        display(moves)
        gameStatus = checkGame(moves, turns)
        turns += 1

        if gameStatus == 1:
            print("The game has been won by the player!")
        elif gameStatus == 2:
            print("The game has been won by the computer!")
        elif gameStatus == 3:
            print("Game is completed it was a draw")




# turns = 0
moves = []
available_Moves = []
possibleMoves = []

for i in range(9):
    moves.append(" ")
    available_Moves.append(" ")
    possibleMoves.append(" ")

if __name__ == '__main__':
  play_a_new_game()

