# Finite State Processing with `pywrapfst`
This repo demonstrates the use of the python wrapper around `openfst`, namely `pywrapfst`. 

For now, there are two scripts `edit_distance.py`, `noisy_keyboard.py` under `./code` that can be run.

## `edit_distance.py` 
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

## `noisy_keyboard.py`
This script is very similar to `edit_distance.py`, but uses a "noisy keyboard" model. The replacement of a key with a nearby key is penalized less than an arbitrary replacement. For instance, it costs less to replace **d** with **f**, than replacing it with  **h**.

Here's a sample run : 

    ./noisy_keyboard.py ieangr orange

    Transition : 

    i	->	o,	cost : 0.263157904
    e	->	r,	cost : 0.263157904
    a	->	a,	cost : 0
    n	->	n,	cost : 0
    g	->	g,	cost : 0
    r	->	e,	cost : 0.263157904

    Total Edit Distance : 0.789473712
