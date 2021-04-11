# John (Junseong) Kim
# 301262540
# jka157@sfu.ca
#
# References:
#
# TA - Mohammad's Tutorials
# https://www.youtube.com/watch?v=ZAtYbC9E6qM
# https://pynative.com/python-random-randrange/#:~:text=Use%20randint()%20when%20you,number%20from%20an%20exclusive%20range.
# https://www.youtube.com/watch?v=KzqSDvzOFNA
#

from csp import *
from a2_q1 import *
import random
import numpy

# csp_sol will be in this format: X = {0:0, 1:1, 2:1, 3:0}
# graph is this form: {0: [2], 1: [2, 4], 2: [0, 1, 4], 3: [], 4: [1, 2]}


# Traverse through the graph to see if there are any friends in the same group

    # If team is inputted for csp_sol:
    # Put it into dictionary form:
    # Ex): If team is
    # X = {0:0, 1:1, 2:1, 3:0}
    # Put 0 and 3 on team 0, and 1 and 2 on on team 1
    # In dictionary form:
    # g = {0: [1,2], 1:[0,3], 2:[0,3], 3:[1,2]}



def check_teams(graph, csp_sol):

    friend_list = {}
    size = len(csp_sol)

    for i in range(size):
        friend_list.setdefault(i, [])
        friend_list.setdefault(csp_sol(i), []).append(i)


    for j in range(len(friend_list)):
        list = friend_list[j]


        for k in range(len(list)):

            for l in range(len(list)):

                if list[i] in graph[list[i]]:
                    return False

    return True
