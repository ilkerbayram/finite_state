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


def transform_cost(
    input,
    target,
    distance_threshold=1,
    miss_penalty=1,
    insertion_penalty=1,
    deletion_penalty=1,
):
    """
    computes the cost of transforming the input 
    sequence to the target sequence

    transforming is performed via three operations with different costs
    1. changing an element of the input, x, to an element of the target, y,
        with penalty P(x,y) given as
            abs(x-y), if abs(x-y) < distance_threshold,
            miss_penalty, otherwise
    2. inserting an arbitrary element into the input
        with a penalty of insertion_penalty
    3. deletion of an arbitrary element from the input
        with a penalty of deletion_penalty
    
    variables : 
    input - list of numbers
    target - list of numbers
    distance_threshold - determines if two numbers match
    miss_penalty - penalty for individual mismatch
    insertion_penalty - penalty for inserting an arbitrary number in input
    deletion_penalty - penalty for removing an arbitrary number from input
    
    output :  
    total_distance - minimum distance between the input and the target
    path - the path achieving the minimum cost, 
        can be printed using print_result
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
    right = right_factor_numerical(
        isym,
        target=target,
        miss_penalty=miss_penalty,
        insertion_penalty=insertion_penalty,
        deletion_penalty=deletion_penalty,
    )

    # create the special left factor, adapted to the keyboard
    cost = replacement_cost_numerical(
        input=input, target=target, distance_threshold=distance_threshold
    )

    left = noisy_left_factor_numerical(
        symbols=isym,
        cost=cost,
        miss_penalty=miss_penalty,
        insertion_penalty=insertion_penalty,
        deletion_penalty=deletion_penalty,
    )

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
