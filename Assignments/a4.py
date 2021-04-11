# John (Junseong) Kim
# 301262540
# jka157@sfu.ca

# References:

# TA - Mohammad's Tutorials
# https://www.tutorialspoint.com/python/python_dictionary.htm
# https://pyformat.info/
# https://www.geeksforgeeks.org/reading-writing-text-files-python/
# https://www.programiz.com/python-programming/methods
# https://www.guru99.com/reading-and-writing-files-in-python.html#3
# Stackoverflow
# https://www.faceprep.in/python/how-to-take-multiple-inputs-in-python/#:~:text=a)%20split%20(),it%20for%20taking%20multiple%20inputs.
# https://www.geeksforgeeks.org/python-difference-two-lists/

import random
import copy
import os


# returns True if, and only if, string s is a valid variable name
def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])


def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"

# Gets the user input and the user command
def getInput():
    user_input = list(map(str, input("kb> ").split()))
    command = user_input[0]
    action = []

    for i in range(1, len(user_input)):
        action.append(user_input[i])

    return command, action

# From the given input from the user, opens the txt file and organize head and atoms into dictionary
def loadKB(file_name):
    try:
        load_file = open(file_name, "r+")
    except FileNotFoundError:
        print("Error:", file_name, "is not a valid knowledge base\n")
        return None, None, None, None
    else:
        if load_file.mode == 'r+':
            # knowledge_base = kb.read()

            var_list = []
            head_list = []
            atom_list = []

            kb_dict = {}
            index = 0

            for line in load_file:

                atom_list.append(line.strip(os.linesep))
                word_list = line.split()
                head_list.append(word_list[0])
                temp_list = []

                for j in range(0, len(word_list)):

                    if word_list[j] == "<--" or word_list[j] == "&":
                        pass
                    elif j > 1:
                        var_list.append(word_list[j])
                        temp_list.append(word_list[j])

                # print(head_list[index])
                # print(temp_list)
                kb_dict[head_list[index]] = [temp_list]
                index += 1

            # print(kb_dict)

            num_lines = len(atom_list)
            for k in range(num_lines):
                print(atom_list[k])

            print()
            print(num_lines, "new rule(s) added \n")

            # print(kb_dict)

    return load_file, var_list, head_list, kb_dict

# Execute tell command and append them to list
def tellKB(new_atoms, old_atoms):
    for k in range(len(new_atoms)):
        correct_atom = is_atom(new_atoms[k])

        if not correct_atom:
            print('Error: "' + new_atoms[k] + '" is not a valid atom \n')
            return
        if new_atoms[k] in old_atoms:
            print('atom "' + new_atoms[k] + '" already known to be true \n')
            return old_atoms
        else:
            old_atoms.append(new_atoms[k])

    for n in range(len(new_atoms)):
        print('"' + new_atoms[n] + '" added to the KB')

    print()

    return old_atoms

# Compute infer command
# Compare atoms to tell list and see if they are equal
def infer_all(tell_kb, dict_kb, inferred_list, new_added):
    if not tell_kb:
        print('You must add atoms using "tell" before any atoms can be inferred\n')
        return

    kb_items = list(dict_kb.items())
    new_infer = []

    for i in range(len(kb_items)):
        kb_head = kb_items[i]
        kb_atoms = kb_items[i][1]

        kb_key = kb_head[0]
        kb_values = list(kb_atoms[0])

        # print(kb_key)
        # print(kb_values)

        # Only prints out the values that are the same in the two lists
        same_atoms = [j for j in kb_values if j in tell_kb]

        if same_atoms == kb_values:
            if kb_key not in inferred_list:
                new_infer.append(kb_key)
                # print('"'+kb_key+'" added to new inferred list')

        for t in range(len(tell_kb)):

            if tell_kb[t] in kb_values:
                # print(kb_key)
                # print("Comparing this KB:" + tell_kb[t])
                comp_temp = tell_kb[t]
                if comp_temp not in new_added:
                    new_added.append(comp_temp)

    # print("Testing:")
    # print(new_infer)
    # print(new_added)

    print("Newly inferred atoms:")
    if not new_infer:
        print("<none>\n")
    else:
        print(', '.join(new_infer), "\n")

    print("Atoms already known to be true:")
    print(', '.join(str(v) for v in new_added), "\n")

    if new_infer:
        for i in range(len(new_infer)):
            new_added.append(new_infer[i])
            inferred_list.append(new_infer[i])

    # print(new_added)

    return inferred_list, new_added

def clear_all(infer, known, atom_list):

    infer = []
    known = []
    atom_list = []

    return infer, known, atom_list


# ___________________________________________________________________________________________
infer_new = []
atoms_known = []
atom_list = []
loaded = False
told = False

# Continue to get user input
while True:

    user_command, comp_action = getInput()

    if user_command == "load":

        if loaded:
            infer_new, atoms_known, atom_list = clear_all(infer_new, atoms_known, atom_list)

        txt_file = comp_action[0]
        kb_file, num_atoms, head, kb = loadKB(txt_file)
        loaded = True

    elif user_command == "tell":
        told = True
        if not comp_action:
            print("Error: tell needs at least one atom")

        atom_list = tellKB(comp_action, atom_list)

    elif user_command == "infer_all":
        if not loaded:
            print("Error: You must load the KB file first\n")
        elif not told:
            print("You must tell at least one command before inferring \n")
        else:
            infer_new, atoms_known = infer_all(atom_list, kb, infer_new, atoms_known)

    elif user_command == "clear_atoms":
        print("Previous tell commands have been forgotten \n")
        told = False
        infer_new, atoms_known, atom_list = clear_all(infer_new, atoms_known, atom_list)
        # infer_new = []
        # atoms_known = []
        # atom_list = []

    else:
        print('Error: unknown command "' + user_command + '"\n')
