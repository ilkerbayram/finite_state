#!/usr/bin/env python
"""
this script computes the edit distance between 
a user provided (input,target) pair

Ilker Bayram, ibayram@ieee.org, 2021
"""

from os.path import exists, join
import argparse
import pywrapfst as fst

from fst_utils import (
    create_alphabet,
    create_word_fst,
    right_factor,
    left_factor,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="computes the edit distance between an input and a target"
    )
    parser.add_argument("input", help="input")
    parser.add_argument("target", help="target")
    parser.add_argument(
        "-c",
        "--create",
        help="create symbol file for the alphabet",
        action="store_true",
    )
    return parser.parse_args()


def print_result(path, isymbols, osymbols):
    """
    prints arc weights for the shortest path
    """
    for st in path.states():
        for arc in path.arcs(st):
            print(
                f"{isymbols.find(arc.ilabel)}\t->\t{osymbols.find(arc.olabel)},\tcost : {arc.weight}"
            )

    return None


def main():
    args = parse_args()
    folder = join("..", "symbols")
    fname = "alphabet.sym"
    fname = join(folder, fname)
    print(fname)
    # if the user asked for it, or if it does not already exist,
    # create symbols for the alphabet
    if args.create:
        create_alphabet(fname=fname)
    elif not exists(fname):
        print(f"{fname} does not exist, creating...")
        create_alphabet(fname=fname)

    # create a SymbolTable object
    isym = fst.SymbolTable.read_text(fname)

    # create the right and left word FST's
    word_right = create_word_fst(word=args.target, symbols=isym)
    word_left = create_word_fst(word=args.input, symbols=isym)

    # create the right and left factor FSTs
    right = right_factor(isym)
    left = left_factor(isym)

    # compose the FSTs right and left FSTs
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
    print(f"\nTotal Edit Distance : {int(dist[-1].__float__())}\n")

    return None


if __name__ == "__main__":
    main()
