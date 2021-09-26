# Finite State Processing with `pywrapfst`
This repo demonstrates the use of the python wrapper around `openfst`, namely `pywrapfst`. 

For now, there's a single script `edit_distance.py` under `./code` that can be run.

This script computes the edit distance between a user specified (input, target) pair.
It can be run under `./code` as

    ./edit_distance.py actag ctagc

The script computes the edit distance between the input `actag` and the target `ctagc`, and shows the edit distance along with an explanation of the transitions one needs to make to achieve that score.

    Transition : 

    a	->	<eps>,	cost : 1
    c	->	c,	cost : 0
    t	->	t,	cost : 0
    a	->	a,	cost : 0
    g	->	g,	cost : 0
    <eps>	->	c,	cost : 1

    Total Edit Distance : 2

