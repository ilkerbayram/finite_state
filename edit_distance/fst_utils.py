import pywrapfst as fst
import string
import numpy as np


def print_result(path, isymbols, osymbols):
    """
    prints arc weights for the shortest path
    """
    for st in path.states():
        for arc in path.arcs(st):
            print(
                f"{isymbols.find(arc.ilabel)}\t->\t{osymbols.find(arc.olabel)},\tcost : {arc.weight.__float__():.3f}"
            )

    return None


def keyboard_layout():
    """
    returns a dictionary holding the coordintes of each key
    """
    keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    offset = [0, 1 / 3, 2 / 3]
    layout = {}
    for row, (keys, offset) in enumerate(zip(keyboard, offset)):
        for col, k in enumerate(keys):
            layout[k] = (row, col + offset)
    return layout


def replacement_cost_numerical(input, target, threshold):
    """
    returns a dictionary where each key is an element from the input,
    each value is a dictionary.
    For instance for the key '1.0' from input, the dictionary consists of
    the distance of '1.0' to the elements in the target if they do not exceed 
    the threshold
    """
    cost = {
        str(x): {
            str(y): np.abs(x - y) for y in set(target) if np.abs(x - y) < threshold
        }
        for x in set(input)
    }
    return cost


def replacement_cost(layout: dict, threshold: float):
    """
    returns a dictionary where each key is a letter.
    each value is a dictionary.
    For instance for the key 'q', the dictionary consists of
    nearby keys on the keyboard, along with the cost of replacing 'q'
    with those keys.
    """
    cost = {}

    # if the distance to a key is less than the threshold,
    # include it in the list
    for key, pos_key in layout.items():
        pos_key = np.array(pos_key)
        cost[key] = {}
        for candidate, pos_cand in layout.items():
            pos_cand = np.array(pos_cand)
            dist = np.sqrt(((pos_key - pos_cand) ** 2).sum())
            if dist < threshold:
                cost[key][candidate] = dist / (2 * threshold)

    return cost


def create_alphabet(fname="alphabet.sym"):
    with open(fname, "w") as f:
        f.write("<eps>\t0")
        f.write("\n<del>\t1")
        f.write("\n<ins>\t2")
        f.write("\n<sub>\t3")
        for ind, letter in enumerate(string.ascii_lowercase):
            f.write(f"\n{letter}\t{ind+4}")
    return None


def create_numerical_alphabet(sequences, fname="numerical.sym"):
    with open(fname, "w") as f:
        f.write("<eps>\t0")
        f.write("\n<del>\t1")
        f.write("\n<ins>\t2")
        f.write("\n<sub>\t3")
        for ind, num in enumerate(sequences):
            f.write(f"\n{num}\t{ind+4}")
    return None


def create_word_fst(word, symbols):

    comp = fst.Compiler(
        isymbols=symbols, osymbols=symbols, keep_isymbols=True, keep_osymbols=True
    )
    for cnt, letter in enumerate(word):
        comp.write(f"{cnt} {cnt+1} {letter} {letter} 0")
    comp.write(f"{cnt+1}")
    wfst = comp.compile()

    return wfst


def print_fst(fst_in, isymbols, osymbols):
    """
    prints the states and the arcs of the input fst
    using the provided symbols
    """
    for st in fst_in.states():
        print(st)
        for arc in fst_in.arcs(st):
            print(
                f"{arc.nextstate}, {isymbols.find(arc.ilabel)}, {osymbols.find(arc.olabel)}, {arc.weight}"
            )

    return None


def right_factor(symbols):
    """
    create a right factor fst for edit distance computation
    """
    comp = fst.Compiler(
        isymbols=symbols, osymbols=symbols, keep_isymbols=True, keep_osymbols=True
    )
    for letter in string.ascii_lowercase:
        for inp, val in [(letter, 0), ("<sub>", 0.5), ("<ins>", 0.5)]:
            comp.write(f"0 0 {inp} {letter} {val}")
    comp.write("0 0 <del> <eps> 0.5")
    comp.write("0")
    return comp.compile()


def right_factor_numerical(symbols, target):
    """
    create a right factor for edit distance computation on numerical sequences
    """
    comp = fst.Compiler(
        isymbols=symbols, osymbols=symbols, keep_isymbols=True, keep_osymbols=True
    )
    for num in set(target):
        for inp, val in [(num, 0), ("<sub>", 0.5), ("<ins>", 0.5)]:
            comp.write(f"0 0 {inp} {num} {val}")
    comp.write("0 0 <del> <eps> 0.5")
    comp.write("0")
    return comp.compile()


def left_factor(symbols):
    """
    create a right factor fst for edit distance computation
    """
    comp = fst.Compiler(
        isymbols=symbols, osymbols=symbols, keep_isymbols=True, keep_osymbols=True
    )
    for letter in string.ascii_lowercase:
        for inp, val in [(letter, 0), ("<sub>", 0.5), ("<del>", 0.5)]:
            comp.write(f"0 0 {letter} {inp} {val}")
    comp.write("0 0 <eps> <ins> 0.5")
    comp.write("0")
    return comp.compile()


def noisy_left_factor(symbols, cost: dict):
    """
    create left factor for a noisy keyboard,
    given a cost dictionary like one produced by the function
    replacement_cost
    """
    comp = fst.Compiler(
        isymbols=symbols, osymbols=symbols, keep_isymbols=True, keep_osymbols=True
    )
    for letter in string.ascii_lowercase:
        for transition, penalty in cost[letter].items():
            comp.write(f"0 0 {letter} {transition} {penalty}")
        # add 'sub' and 'del'
        for inp, val in [("<sub>", 0.5), ("<del>", 0.5)]:
            comp.write(f"0 0 {letter} {inp} {val}")
    comp.write("0 0 <eps> <ins> 0.5")
    comp.write("0")
    return comp.compile()


def noisy_left_factor_numerical(symbols, cost: dict):
    """
    create left factor
    given a cost dictionary like one produced by the function
    replacement_cost_numerical
    """
    comp = fst.Compiler(
        isymbols=symbols, osymbols=symbols, keep_isymbols=True, keep_osymbols=True
    )
    for key, distance_dict in cost.items():
        for transition, penalty in distance_dict.items():
            comp.write(f"0 0 {key} {transition} {penalty}")
        # add 'sub' and 'del'
        for inp, val in [("<sub>", 0.5), ("<del>", 0.5)]:
            comp.write(f"0 0 {key} {inp} {val}")
    comp.write("0 0 <eps> <ins> 0.5")
    comp.write("0")
    return comp.compile()
