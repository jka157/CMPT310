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
import random
import numpy

"""variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
"""

# One CSP variable for each of the n people
# Domain for these variables are team names (integers 0, 1, 2, .. etc.)
# Constraint: Can't have two friends on the same team
# Goal: Find smallest domain size for variables that satisfies all the constraints


# Randomly generated n and p values for testing
# n = random.randint(1, 10)
# p = random.uniform(0, 1)

# print("N is equal to = ", n)


# creates a new random graph with n nodes numbered 0 to n-1 such that every different pair of nodes is connected with probability p:
# assume n>1, and 0<= p <= 1
def rand_graph(p,n):
    var_graph={}

    if n == 0:
        print("No friends?")
        var_graph[0] = []

    for i in range(0,n):
        value_list = []

        for j in range(i,n):

            if i == j:
                pass
            else:
                r = random.uniform(0, 1)
                if p > r:
                    value_list.append(j)
                    #print(value_list)

        var_graph[i] = value_list

    # print(var_graph)

    for k in range(0,n):
        comp_list = var_graph.get(k)

        for l in range(0,len(comp_list)):
            index = comp_list[l]
            exist_list = var_graph.get(index)
            # print(index)
            # print(exist_list)

            if k not in exist_list:
                exist_list.append(k)
                exist_list.sort()
                var_graph[index] = exist_list

    # print(var_graph)
    return(var_graph)

# rand_graph(0.2, 10)