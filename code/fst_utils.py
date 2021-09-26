import pywrapfst as fst
import string


def create_alphabet(fname="alphabet.sym"):
    with open(fname, "w") as f:
        f.write("<eps>\t0")
        f.write("\n<del>\t1")
        f.write("\n<ins>\t2")
        f.write("\n<sub>\t3")
        for ind, letter in enumerate(string.ascii_lowercase):
            f.write(f"\n{letter}\t{ind+4}")
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
