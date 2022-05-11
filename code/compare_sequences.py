#!/usr/bin/env python
"""
computes a type of edit distance between
two numerical sequences

Ilker Bayram, ibayram@ieee.org, 2022
"""

from os.path import exists, join
import argparse
import pywrapfst as fst

from fst_utils import (
    keyboard_layout,
    replacement_cost_numerical,
    noisy_left_factor_numerical,
    right_factor_numerical,
    create_numerical_alphabet,
    print_result,
    create_word_fst,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="computes the edit distance between" " two numerical sequences"
    )
    parser.add_argument("--input", help="input", nargs="+", type=float)
    parser.add_argument("--target", help="target", nargs="+", type=float)
    parser.add_argument(
        "--distance_thold",
        help="distance threshold between floats to decide if they are related or not",
        type=float,
        default=1.0,
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # set path, filename for the symboltable
    folder = join("..", "symbols")
    fname = "numbers.sym"
    fname = join(folder, fname)

    # create symbols for the numbers,
    create_numerical_alphabet(set(args.input + args.target), fname=fname)

    # create a SymbolTable object
    isym = fst.SymbolTable.read_text(fname)

    str_input = [str(x) for x in args.input]
    str_target = [str(x) for x in args.target]

    # create the right and left word FST's
    word_right = create_word_fst(word=str_target, symbols=isym)
    word_left = create_word_fst(word=str_input, symbols=isym)

    # create the right and left factor FSTs
    right = right_factor_numerical(isym, target=args.target)

    # create the special left factor, adapted to the keyboard
    cost = replacement_cost_numerical(
        input=args.input, target=args.target, threshold=args.distance_thold
    )

    left = noisy_left_factor_numerical(symbols=isym, cost=cost)

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
