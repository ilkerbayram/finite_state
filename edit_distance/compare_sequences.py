#!/usr/bin/env python
"""
computes a type of edit distance between
two numerical sequences

Ilker Bayram, ibayram@ieee.org, 2022
"""

from os.path import exists, join
import argparse
import pywrapfst as fst
from os import remove

from edit_distance.fst_utils import (
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


def transform_cost(input, target, distance_threshold=1):
    """
    computes the cost of transforming the input 
    sequence to the target sequence
    
    variables : 
    input - list of numbers
    target - list of numbers
    
    output :  
    total_distance - minimum distance between the input and the target
    path - the path achieving the minimum cost
    """

    # set path, filename for the symboltable
    fname = "temp.sym"
    # create symbols for the numbers,
    create_numerical_alphabet(set(input + target), fname=fname)

    # create a SymbolTable object
    isym = fst.SymbolTable.read_text(fname)

    # delete the symbol file, as it cannot be used again
    remove(fname)

    str_input = [str(x) for x in input]
    str_target = [str(x) for x in target]

    # create the right and left word FST's
    word_right = create_word_fst(word=str_target, symbols=isym)
    word_left = create_word_fst(word=str_input, symbols=isym)

    # create the right and left factor FSTs
    right = right_factor_numerical(isym, target=target)

    # create the special left factor, adapted to the keyboard
    cost = replacement_cost_numerical(
        input=input, target=target, threshold=distance_threshold
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

    best_path = {"path": path, "isymbols": isym, "osymbols": isym}

    dist = fst.shortestdistance(path)
    total_distance = float(dist[-1].__float__())

    return total_distance, best_path


def main():
    """
    computes the minimum distance between the input and target
    also prints the min distance achieving path
    """
    args = parse_args()
    distance, path = transform_cost(input=args.input, target=args.target)

    print("\nTransition : \n")
    print_result(**path)

    print(f"\nTotal Edit Distance : {distance:.3f}\n")

    return None


if __name__ == "__main__":
    main()
