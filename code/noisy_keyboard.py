#!/usr/bin/env python
"""
computes the edit distance between
a user provided (input, target) pair,
where the penalty between nearby letters
is smaller than other letter replacements.

Ilker Bayram, ibayram@ieee.org, 2021
"""

from os.path import exists, join
import argparse
import pywrapfst as fst

from fst_utils import (
    keyboard_layout,
    replacement_cost,
    noisy_left_factor,
    right_factor,
    create_alphabet,
    print_result,
    create_word_fst,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="computes the edit distance between"
        " an input and a target using a noisy keyboard model"
    )
    parser.add_argument("input", help="input")
    parser.add_argument("target", help="target")
    return parser.parse_args()


def main():
    args = parse_args()

    # set path, filename for the symboltable
    folder = join("..", "symbols")
    fname = "alphabet.sym"
    fname = join(folder, fname)

    # create symbols for the alphabet,
    # if it doesn't exist
    if not exists(fname):
        print(f"{fname} does not exist, creating...")
        create_alphabet(fname=fname)

    # create a SymbolTable object
    isym = fst.SymbolTable.read_text(fname)

    # create the right and left word FST's
    word_right = create_word_fst(word=args.target, symbols=isym)
    word_left = create_word_fst(word=args.input, symbols=isym)

    # create the right and left factor FSTs
    right = right_factor(isym)

    # create the special left factor, adapted to the keyboard
    layout = keyboard_layout()
    cost = replacement_cost(layout=layout, threshold=1.9)
    left = noisy_left_factor(symbols=isym, cost=cost)

    # compose the right FSTs and the left FSTs
    right_full = fst.compose(right, word_right)
    left_full = fst.compose(word_left, left)

    # compose the right and left pieces to obtain the search FST
    full = fst.compose(left_full.arcsort(), right_full.arcsort())
    path = fst.shortestpath(full)
    path.rmepsilon()
    path.topsort()

    print("\nTransition : \n")
    print_result(path, isymbols=isym, osymbols=isym)

    dist = fst.shortestdistance(path)
    print(f"\nTotal Edit Distance : {float(dist[-1].__float__())}\n")

    return None


if __name__ == "__main__":
    main()
