#a1.py
#John (Junseong) Kim
#301262540
#jka157@sfu.ca

#Citation:
#TA - Mohammad
#https://www.w3schools.com/python/ref_random_shuffle.asp
#https://www.stechies.com/python-print-without-newline/
#https://www.tutorialspoint.com/How-to-measure-elapsed-time-in-python
#https://www.youtube.com/watch?v=GuCzYxHa7iA&t=144s
#https://cs.stackexchange.com/questions/37795/why-is-manhattan-distance-a-better-heuristic-for-15-puzzle-than-number-of-til
#http://www.cs.toronto.edu/~edelisle/384/f14/Lectures/384slides-sep18.pdf

from search import *
import random
import time

#Question 1: Helper Functions

class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """
        #Modified so that it doesn't include zero.
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

#return new instance of EightPuzzle problem with random initial state that is solvable
def make_rand_8puzzle():

    import numpy as np

    #initialize state before using random shuffle to randomize
    state = tuple(np.random.permutation(9))
    eight_puzzle = EightPuzzle(tuple(state))

    #check for solvability from search.py
    while eight_puzzle.check_solvability(state) == False:
        state = tuple(np.random.permutation(9))
        eight_puzzle = EightPuzzle(initial=state)


    #return the randomized 8-puzzle
    return eight_puzzle

#This function is used to display the randomized 8-puzzle
def display(state):
    j = 0
    temp = 0
    #Up until j = 9:
    while j != 9:
        #0 is replaced with *
        if state[j] == 0:
            state[j] == "*"
            print("*" + " ", end='')
        #Prints the number in its rightful place
        else:
            temp = state[j]
            print(str(temp) + " ", end='')

        j += 1
        #Only output 3 on one row before printing to the next line
        if j % 3 == 0:
            print("\n", end='')


#Question 2: Comparing Algorithms

def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    removed_nodes = 0
    while frontier:
        node = frontier.pop()
        # Counting how many nodes are removed from the frontier
        removed_nodes = removed_nodes + 1
        if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                return node, removed_nodes
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, removed_nodes

def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def manh_dist_search(node):

    state = node.state

    end_goal = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 0: [2, 2]}

    index = [
        [0, 0], [0, 1], [0, 2],
        [1, 0], [1, 1], [1, 2],
        [2, 0], [2, 1], [2, 2]]

    index_state = {}

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    dist = 0

    for i in range(1, 9):
        for j in range(2):
            dist = abs(end_goal[i][j] - index_state[i][j]) + dist

    return dist


def max_h(node):
    incorrect_h = EightPuzzle(node.state)
    manh_h = manh_dist_search(node)
    return max(incorrect_h.h(node), manh_h)


#Need to create 10 8-puzzles:
def repeat_Eight():
    i = 0
    for i in range(0, 10):
        #Display the randomized 8-puzzle before solving it:
        print("This is puzzle #" + str(i +1))
        Puzzle = make_rand_8puzzle()
        display(Puzzle.initial)

        #A*-search - Doesn't keep track of h(n)
        start_time = time.time()
        astar, removed_nodes = astar_search(Puzzle, False)
        elapsed_time = time.time() - start_time
        print("\n")
        print("A*-search using the misplaced tile heuristic")
        print(astar.solution())
        print("The number of steps taken are: " + str(len(astar.solution())))
        print("The total number of removed nodes are: " + str(removed_nodes))
        print(f'The elapsed time (in seconds): {elapsed_time}')
        print("\n")


        #Manhattan distance heuristic - Pass in the h(n) value using manhattan distance
        start_time_manh = time.time()
        manh_dist_heur, removed_nodes_manh = astar_search(Puzzle, h=manh_dist_search)
        elapsed_time_manh = time.time() - start_time_manh
        print("A*-search using the Manhattan distance heuristic")
        print(manh_dist_heur.solution())
        print("The number of steps taken are: " + str(len(manh_dist_heur.solution())))
        print("The total number of removed nodes are: ", removed_nodes_manh)
        print(f'The elapsed time (in seconds): {elapsed_time_manh}')
        print("\n")

        #A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic
        start_time_max = time.time()
        max_heur, removed_nodes_max = astar_search(Puzzle, h=max_h)
        elapsed_time_max = time.time() - start_time_max
        print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")
        print(max_heur.solution())
        print("The number of steps taken are: " + str(len(max_heur.solution())))
        print("The total number of removed nodes are: ", removed_nodes_max)
        print(f'The elapsed time (in seconds): {elapsed_time_max}')
        print("\n")


#Modify Problem class and its functions for DuckPuzzle


class DuckPuzzle(Problem):

    # Different Problem to original EightPuzzle, the new board shape is the following:
    # 0 1
    # 2 3 4 5
    #   6 7 8

    # Changed the actions, result for the new puzzle

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square == 0 or index_blank_square == 1 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square == 6 or index_blank_square == 7 or index_blank_square == 8 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        #list of new results

        if blank == 0:
            delta_0 = {'DOWN': 2, 'RIGHT': 1}
            neighbor = blank + delta_0[action]
        if blank == 1:
            delta_1 = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta_1[action]
        if blank == 2:
            delta_2 = {'UP': -2, 'RIGHT': 1}
            neighbor = blank + delta_2[action]
        if blank == 3:
            delta_3 = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta_3[action]
        if blank == 4:
            delta_4 = {'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta_4[action]
        if blank == 5:
            delta_5 = {'DOWN': 3, 'LEFT': -1}
            neighbor = blank + delta_5[action]
        if blank == 6:
            delta_6 = {'UP': -3, 'RIGHT': 1}
            neighbor = blank + delta_6[action]
        if blank == 7:
            delta_7 = {'UP': -3,'LEFT': -1, 'RIGHT': 1}
            neighbor = blank + delta_7[action]
        if blank == 8:
            delta_8 = {'UP': -3, 'LEFT': -1}
            neighbor = blank + delta_8[action]

        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        #print(new_state)
        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

        # Modified so that it doesn't include zero.
        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))

def make_rand_Duck():

    state = [1,2,3,4,5,6,7,8,0]

    temp_state = 0

    #Repeat for 10 times to get 10 different puzzles
    for j in range(0,9):

        #Randomly Shuffle the possible moves (U = Up, D = Down, R = Right, L = Left)
        directions = ["U","D","R","L","U","L","D","R","U","R","L","D"]
        random.shuffle(directions)

        #Get the index of where the 0 is
        min_index = state.index(min(state))

        #Make the appropriate actions for each possible moves based on location
        for i in range(len(directions)):

            if min_index == 0:
                if directions[i] == "R":
                    temp_state = state[min_index+1]
                    state[min_index+1] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "D":
                    temp_state = state[min_index+2]
                    state[min_index+2] = state[min_index]
                    state[min_index] = temp_state
                else:
                    pass

            if min_index == 1:
                if directions[i] == "L":
                    temp_state = state[min_index-1]
                    state[min_index-1] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "D":
                    temp_state = state[min_index+2]
                    state[min_index+2] = state[min_index]
                    state[min_index] = temp_state
                else:
                    pass

            if min_index == 2:
                if directions[i] == "R":
                    temp_state = state[min_index+1]
                    state[min_index+1] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "U":
                    temp_state = state[min_index-2]
                    state[min_index-2] = state[min_index]
                    state[min_index] = temp_state
                else:
                    pass

            if min_index == 3:
                if directions[i] == "L":
                    temp_state = state[min_index - 1]
                    state[min_index - 1] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "D":
                    temp_state = state[min_index + 3]
                    state[min_index + 3] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "U":
                    temp_state = state[min_index - 2]
                    state[min_index - 2] = state[min_index]
                    state[min_index] = temp_state
                else:
                    temp_state = state[min_index + 1]
                    state[min_index + 1] = state[min_index]
                    state[min_index] = temp_state

            if min_index == 4:
                if directions[i] == "L":
                    temp_state = state[min_index - 1]
                    state[min_index - 1] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "D":
                    temp_state = state[min_index + 3]
                    state[min_index + 3] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "R":
                    temp_state = state[min_index+1]
                    state[min_index+1] = state[min_index]
                    state[min_index] = temp_state
                else:
                    pass

            if min_index == 5:
                if directions[i] == "L":
                    temp_state = state[min_index - 1]
                    state[min_index - 1] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "D":
                    temp_state = state[min_index + 3]
                    state[min_index + 3] = state[min_index]
                    state[min_index] = temp_state
                else:
                    pass

            if min_index == 6:
                if directions[i] == "R":
                    temp_state = state[min_index+1]
                    state[min_index+1] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "U":
                    temp_state = state[min_index-3]
                    state[min_index-3] = state[min_index]
                    state[min_index] = temp_state
                else:
                    pass

            if min_index == 7:
                if directions[i] == "L":
                    temp_state = state[min_index - 1]
                    state[min_index - 1] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "U":
                    temp_state = state[min_index-3]
                    state[min_index-3] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "R":
                    temp_state = state[min_index+1]
                    state[min_index+1] = state[min_index]
                    state[min_index] = temp_state
                else:
                    pass

            if min_index == 8:
                if directions[i] == "L":
                    temp_state = state[min_index - 1]
                    state[min_index - 1] = state[min_index]
                    state[min_index] = temp_state
                elif directions[i] == "U":
                    temp_state = state[min_index-3]
                    state[min_index-3] = state[min_index]
                    state[min_index] = temp_state
                else:
                    pass

    duck_puzzle = DuckPuzzle(tuple(state))

    # return the randomized 8-puzzle
    return duck_puzzle

def display_Duck(state):
    # 0 1
    # 2 3 4 5
    #   6 7 8


    # Up until j = 9:
    for j in range(0,9):
        # 0 is replaced with *

        if state[j] == 0:
            print("*", " ", end="")

        else:
            print(state[j], " ", end="")

        if j == 1:
            print('\n', end='')

        elif j == 5:
            print('\n'+ "   ", end='')


def manh_dist_Duck(node):

    state = node.state

    #new end goal and new index for Duck Puzzle
    end_goal = {
        1: [0, 0], 2: [0, 1],
        3: [1, 0], 4: [1, 1], 5: [1, 2], 6: [1, 3],
                   7: [2, 1], 8: [2, 2], 0: [2, 3]}

    index = [
        [0, 0], [0, 1],
        [1, 0], [1, 1], [1, 2], [1, 3],
                [2, 1], [2, 2], [2, 3]]

    index_state = {}

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    dist = 0

    # Don't include zero.
    for i in range(1, 9):
        for j in range(2):
            dist = abs(end_goal[i][j] - index_state[i][j]) + dist

    return dist

def max_h_Duck(node):
    incorrect_h = DuckPuzzle(node.state)
    manh_h = manh_dist_Duck(node)
    return max(incorrect_h.h(node), manh_h)

def repeat_Duck():
    for i in range(0, 10):
        # Display the randomized Duck puzzle before solving it:
        print("This is puzzle #" + str(i + 1))
        Duck_Puzzle = make_rand_Duck()
        display_Duck(Duck_Puzzle.initial)

        # A*-search - Doesn't keep track of h(n)
        start_time = time.time()
        astar, removed_nodes = astar_search(Duck_Puzzle, False)
        elapsed_time = time.time() - start_time
        print("\n")
        print("A*-search using the misplaced tile heuristic")
        print(astar.solution())
        print("The number of steps taken are: " + str(len(astar.solution())))
        print("The total number of removed nodes are: " + str(removed_nodes))
        print(f'The elapsed time (in seconds): {elapsed_time}')
        print("\n")

        # Manhattan distance heuristic - Pass in the h(n) value using manhattan distance
        start_time_manh = time.time()
        manh_dist_heur, removed_nodes_manh = astar_search(Duck_Puzzle, h=manh_dist_Duck)
        elapsed_time_manh = time.time() - start_time_manh
        print("A*-search using the Manhattan distance heuristic")
        print(manh_dist_heur.solution())
        print("The number of steps taken are: " + str(len(manh_dist_heur.solution())))
        print("The total number of removed nodes are: ", removed_nodes_manh)
        print(f'The elapsed time (in seconds): {elapsed_time_manh}')
        print("\n")

        # A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic
        start_time_max = time.time()
        max_heur, removed_nodes_max = astar_search(Duck_Puzzle, h=max_h_Duck)
        elapsed_time_max = time.time() - start_time_max
        print("A*-search using the max of the misplaced tile heuristic and the Manhattan distance heuristic")
        print(max_heur.solution())
        print("The number of steps taken are: " + str(len(max_heur.solution())))
        print("The total number of removed nodes are: ", removed_nodes_max)
        print(f'The elapsed time (in seconds): {elapsed_time_max}')
        print("\n")



#______________________________________________________________________________________________________________________________________________________#

#Main Function:

#This makes 10 random 8-puzzles using make_rand_8puzzle() and uses three search methods on each random 8 puzzle generated.
repeat_Eight()

#This makes 10 random Duckpuzzles using make_rand_Duck() and uses three search methods on each randomly generated puzzles
repeat_Duck()

