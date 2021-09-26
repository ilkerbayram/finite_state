#!/usr/bin/env python

import argparse
import pywrapfst as fst
from fst_utils import (
    create_alphabet,
    create_word_fst,
    print_fst,
    right_factor,
    left_factor,
)

# (
#    create_alphabet,
#    print_fst,
#    create_word_fst,
#    left_factor,
#    right_factor,
# )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="target for computing edit distance")
    parser.add_argument("input", help="input for computing edit distance")
    # parser.add_argument(
    #    "-c",
    #    "--create",
    #    help="create symbol file for the alphabet",
    #    type=bool,
    #    default=False,
    # )
    return parser.parse_args()


def main():
    args = parse_args()

    # create a
    create_alphabet()
    isym = fst.SymbolTable.read_text("alphabet.sym")
    osym = fst.SymbolTable.read_text("symbols.sym")
    word_right = create_word_fst(word=args.target, symbols=isym)
    word_left = create_word_fst(word=args.input, symbols=isym)
    print_fst(word_right, isymbols=isym, osymbols=isym)

    right = right_factor(isym)
    left = left_factor(isym)
    right_full = fst.compose(right, word_right)
    left_full = fst.compose(word_left, left)
    print("\nbefore projection : \n\n")
    print_fst(right_full, isymbols=isym, osymbols=isym)
    # right_full.project("input")
    print("\nafter projection : \n\n")
    print_fst(right_full, isymbols=isym, osymbols=isym)

    full = fst.compose(left_full.arcsort(), right_full.arcsort())
    # full.arcsort()
    # full.rmepsilon()
    path = fst.shortestpath(full)
    # path.rmepsilon()
    path.topsort()
    # path.minimize()
    print("\nresult : \n\n")
    print_fst(path, isymbols=isym, osymbols=isym)
    # comp = fst.Compiler(isymbols=isym, osymbols=osym)
    return None


if __name__ == "__main__":
    main()
