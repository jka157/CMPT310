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
from a2_q2 import *
import random
import numpy
import time

# For each of these friendship graphs, calculate the exact minimum number of teams that the people can be put into
# such that no team has 2 (or more) people on it who are friends.

# CSP class

class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases (for example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(n^4) for the
    explicit representation). In terms of describing the CSP as a
    problem, that's all there is.
    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP. Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints, unassigns):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0
        self.unassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
            self.unassigns += 1

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print(assignment)

    # These methods are for the tree and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: non conflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    def unassigns_count(self):
        return self.unassigns
    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

# ______________________________________________________________________________

# Map Coloring CSP Problems
class UniversalDict:
    """A universal dict maps any key to the same value. We use it here
    as the domains dict for CSPs in which all variables have the same domain.
    >>> d = UniversalDict(42)
    >>> d['life']
    42
    """

    # For any key, the dictionary is always going to output the same variables initially inserted

    def __init__(self, value): self.value = value

    def __getitem__(self, key): return self.value

    def __repr__(self): return '{{Friends with: {0!r}}}'.format(self.value)

def different_values_constraint(A, a, B, b):
    """A constraint saying two neighboring variables must differ in value."""
    return a != b


def MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint, 0)


def parse_neighbors(neighbors):
    """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
    regions to neighbors. The syntax is a region name followed by a ':'
    followed by zero or more region names, followed by ';', repeated for
    each region name. If you say 'X: Y' you don't need 'Y: X'.
    >>> parse_neighbors('X: Y Z; Y: Z') == {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
    True
    """
    dic = defaultdict(list)
    specs = [spec.split(':') for spec in neighbors.split(';')]
    for (A, Aneighbors) in specs:
        A = A.strip()
        for B in Aneighbors.split():
            dic[A].append(B)
            dic[B].append(A)
    return dic


def min_conflicts(csp, max_steps=100000):
    """Solve a CSP by stochastic Hill Climbing on the number of conflicts."""
    # Generate a complete assignment for all variables (probably with conflicts)
    csp.current = current = {}
    for var in csp.variables:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
        # csp.unassign(var, assignment)
    return None

# ______________________________________________________________________________

# Create initial teams for MapColoringCSP
def create_Teams(x, y):
    teams = []

    for i in range(y):

        teams.append(i)

        if i + 1 == x:
            break

    return teams



def max_member(csp_sol):

    max_num = len(csp_sol)
    team_list = []

    for j in range(max_num):
        if csp_sol[j] not in team_list:
            team_list.append(csp_sol[j])

    max_team = len(team_list)

    max_people = sum(value == 0 for value in csp_sol.values())
    # team = 0
    counter = 0


    for z in range(1, max_team):
        temp1 = sum(value == z for value in csp_sol.values())

        if max_people < temp1:
            max_people = temp1
            counter = z
        # print(temp1)
        # print(counter)
        # print(max_people)
        # print("\n")

    return max_team, counter, max_people


def run_q4():

    # Create the initial graphs using q1
    graphs = [rand_graph(0.1, 105), rand_graph(0.2, 105), rand_graph(0.3, 105),
               rand_graph(0.4, 105), rand_graph(0.5, 105), rand_graph(0.6, 105)]

    start_time = time.time()

    for one in range(0, 105):
        # if stop == False:

        # Create teams
        team_colors = create_Teams(one+1, 105)

        # Colors = Domain, Neighbors = graph[0-6]
        ice_breaker = MapColoringCSP(team_colors, graphs[0])
        AC3(ice_breaker)

        csp_sol = (min_conflicts(ice_breaker, 10000))

        # If csp_sol is not None, then the result is returned
        if csp_sol != None:
            elapsed_time = time.time() - start_time

            team, team_number, members = max_member(csp_sol)
            print("For friendship graph for n = 105, p = 0.1: ")
            print("The number of teams that the people are divided into:", team)
            print(f'The running time of the solver (in seconds): {elapsed_time}s')
            print("The count of the number of CSP variables assigned:", ice_breaker.nassigns)
            print("The count of the number of CSP variables unassigned:", ice_breaker.unassigns_count())
            print("The team", team_number,  "has the greatest number of people:", members)
            print("The solution of teams that were assigned:", csp_sol)
            print("\n")

            break

    for two in range(0, 105):
        # if stop == False:

        # Create teams
        team_colors = create_Teams(two+1, 105)

        # Colors = Domain, Neighbors = graph[0-6]
        ice_breaker = MapColoringCSP(team_colors, graphs[1])
        AC3(ice_breaker)

        csp_sol = (min_conflicts(ice_breaker, 10000))

        # If csp_sol is not None, then the result is returned
        if csp_sol != None:
            elapsed_time = time.time() - start_time

            team, team_number, members = max_member(csp_sol)
            print("For friendship graph for n = 105, p = 0.2: ")
            print("The number of teams that the people are divided into:", team)
            print(f'The running time of the solver (in seconds): {elapsed_time}s')
            print("The count of the number of CSP variables assigned:", ice_breaker.nassigns)
            print("The count of the number of CSP variables unassigned:", ice_breaker.unassigns_count())
            print("The team", team_number,  "has the greatest number of people:", members)
            print("The solution of teams that were assigned:", csp_sol)
            print("\n")

            break

    for three in range(0, 105):
        # if stop == False:

        # Create teams
        team_colors = create_Teams(three+1, 105)

        # Colors = Domain, Neighbors = graph[0-6]
        ice_breaker = MapColoringCSP(team_colors, graphs[2])
        AC3(ice_breaker)

        csp_sol = (min_conflicts(ice_breaker, 10000))

        # If csp_sol is not None, then the result is returned
        if csp_sol != None:
            elapsed_time = time.time() - start_time

            team, team_number, members = max_member(csp_sol)
            print("For friendship graph for n = 105, p = 0.3: ")
            print("The number of teams that the people are divided into:", team)
            print(f'The running time of the solver (in seconds): {elapsed_time}s')
            print("The count of the number of CSP variables assigned:", ice_breaker.nassigns)
            print("The count of the number of CSP variables unassigned:", ice_breaker.unassigns_count())
            print("The team", team_number,  "has the greatest number of people:", members)
            print("The solution of teams that were assigned:", csp_sol)
            print("\n")

            break

    for four in range(0, 105):
        # if stop == False:

        # Create teams
        team_colors = create_Teams(four+1, 105)

        # Colors = Domain, Neighbors = graph[0-6]
        ice_breaker = MapColoringCSP(team_colors, graphs[3])
        AC3(ice_breaker)

        csp_sol = (min_conflicts(ice_breaker, 10000))

        # If csp_sol is not None, then the result is returned
        if csp_sol != None:
            elapsed_time = time.time() - start_time

            team, team_number, members = max_member(csp_sol)
            print("For friendship graph for n = 105, p = 0.4: ")
            print("The number of teams that the people are divided into:", team)
            print(f'The running time of the solver (in seconds): {elapsed_time}s')
            print("The count of the number of CSP variables assigned:", ice_breaker.nassigns)
            print("The count of the number of CSP variables unassigned:", ice_breaker.unassigns_count())
            print("The team", team_number,  "has the greatest number of people:", members)
            print("The solution of teams that were assigned:", csp_sol)
            print("\n")

            break

    for five in range(0, 105):
        # if stop == False:

        # Create teams
        team_colors = create_Teams(five+1, 105)

        # Colors = Domain, Neighbors = graph[0-6]
        ice_breaker = MapColoringCSP(team_colors, graphs[4])
        AC3(ice_breaker)

        csp_sol = (min_conflicts(ice_breaker, 10000))

        # If csp_sol is not None, then the result is returned
        if csp_sol != None:
            elapsed_time = time.time() - start_time

            team, team_number, members = max_member(csp_sol)
            print("For friendship graph for n = 105, p = 0.5: ")
            print("The number of teams that the people are divided into:", team)
            print(f'The running time of the solver (in seconds): {elapsed_time}s')
            print("The count of the number of CSP variables assigned:", ice_breaker.nassigns)
            print("The count of the number of CSP variables unassigned:", ice_breaker.unassigns_count())
            print("The team", team_number,  "has the greatest number of people:", members)
            print("The solution of teams that were assigned:", csp_sol)
            print("\n")

            break

    for six in range(0, 105):
        # if stop == False:

        # Create teams
        team_colors = create_Teams(six+1, 105)

        # Colors = Domain, Neighbors = graph[0-6]
        ice_breaker = MapColoringCSP(team_colors, graphs[5])
        AC3(ice_breaker)

        csp_sol = (min_conflicts(ice_breaker, 10000))

        # If csp_sol is not None, then the result is returned
        if csp_sol != None:
            elapsed_time = time.time() - start_time

            team, team_number, members = max_member(csp_sol)
            print("For friendship graph for n = 105, p = 0.6: ")
            print("The number of teams that the people are divided into:", team)
            print(f'The running time of the solver (in seconds): {elapsed_time}s')
            print("The count of the number of CSP variables assigned:", ice_breaker.nassigns)
            print("The count of the number of CSP variables unassigned:", ice_breaker.unassigns_count())
            print("The team", team_number,  "has the greatest number of people:", members)
            print("The solution of teams that were assigned:", csp_sol)
            print("\n")

            break

# runs the code

run_q4()