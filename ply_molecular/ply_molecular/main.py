# A grammar for chemical equations like "H2O", "CH3COOH" and "H2SO4"
# Uses David Beazley's PLY parser.
# Implements two functions: count the total number of atoms in the equation and
#   count the number of times each element occurs in the equation.

import ply.lex as lex
import ply.yacc as yacc

tokens = (
    "SYMBOL",
    "COUNT"
)

t_SYMBOL = (
    r"C[laroudsemf]?|Os?|N[eaibdpos]?|S[icernbmg]?|P[drmtboau]?|"
    r"H[eofgas]?|A[lrsgutcm]|B[eraik]?|Dy|E[urs]|F[erm]?|G[aed]|"
    r"I[nr]?|Kr?|L[iaur]|M[gnodt]|R[buhenaf]|T[icebmalh]|"
    r"U|V|W|Xe|Yb?|Z[nr]")


def t_COUNT(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))


lex.lex()


class Atom(object):
    def __init__(self, symbol, count):
        self.symbol = symbol
        self.count = count

    def __repr__(self):
        return "Atom(%r, %r)" % (self.symbol, self.count)


# When parsing starts, try to make a "chemical_equation" because it's
# the name on left-hand side of the first p_* function definition.
# The first rule is empty because I let the empty string be valid
def p_chemical_equation(p):
    """
    chemical_equation :
    chemical_equation : species_list
    """
    if len(p) == 1:
        # the empty string means there are no atomic symbols
        p[0] = []
    else:
        p[0] = p[1]


def p_species_list(p):
    "species_list :  species_list species"
    p[0] = p[1] + [p[2]]


def p_species(p):
    "species_list : species"
    p[0] = [p[1]]


def p_single_species(p):
    """
    species : SYMBOL
    species : SYMBOL COUNT
    """
    if len(p) == 2:
        p[0] = Atom(p[1], 1)
    elif len(p) == 3:
        p[0] = Atom(p[1], p[2])


def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))


yacc.yacc()


def atom_count(s):
    count = 0
    for atom in yacc.parse(s):
        count += atom.count
    return count


def test():
    assert atom_count("He") == 1
    assert atom_count("H2") == 2
    assert atom_count("H2SO4") == 7
    assert atom_count("CH3COOH") == 8
    assert atom_count("NaCl") == 2
    assert atom_count("C60H60") == 120


if __name__ == "__main__":
    test()
    print("All tests passed.")
